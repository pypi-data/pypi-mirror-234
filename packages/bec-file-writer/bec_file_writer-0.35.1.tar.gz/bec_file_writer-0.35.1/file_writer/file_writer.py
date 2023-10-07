from __future__ import annotations

import abc
import datetime
import json
import os
import traceback
import typing

import h5py
import xmltodict
from bec_lib.core import bec_logger

import file_writer_plugins as fwp

from .merged_dicts import merge_dicts

logger = bec_logger.logger


class NeXusLayoutError(Exception):
    pass


class FileWriter(abc.ABC):
    def __init__(self, file_writer_manager):
        self.file_writer_manager = file_writer_manager

    def configure(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def write(self, file_path: str, data):
        ...

    @staticmethod
    def _create_device_data_storage(data):
        device_storage = {}
        if data.baseline:
            device_storage.update(data.baseline)
        if data.async_data:
            device_storage.update(data.async_data)
        keys = list(data.scan_segments.keys())
        keys.sort()
        for point in keys:
            for dev in data.scan_segments[point]:
                if dev not in device_storage:
                    device_storage[dev] = [data.scan_segments[point][dev]]
                    continue
                device_storage[dev].append(data.scan_segments[point][dev])
        return device_storage


class XMLWriter:
    @staticmethod
    def get_type(type_string: str):
        if type_string == "float":
            return float
        if type_string == "string":
            return str
        if type_string == "int":
            return int
        raise NeXusLayoutError(f"Unsupported data type {type_string}.")

    def get_value(self, value, entry, source, data_type):
        if source == "constant":
            if data_type:
                return self.get_type(data_type)(value)
            return value
        return entry

    def add_group(self, container, val):
        name = val.pop("@name")
        group = container.create_group(name)
        self.add_content(group, val)

    def add_dataset(self, container, val):
        name = val.pop("@name")
        source = val.pop("@source")
        value = val.pop("@value", None)
        data_type = val.pop("@type", None)
        entry = val.pop("@entry", None)

        data = self.get_value(value=value, entry=entry, source=source, data_type=data_type)
        if data is None:
            return
        dataset = container.create_dataset(name, data=data)
        self.add_content(dataset, val)
        return

    def add_attribute(self, container, val):
        name = val.pop("@name")
        source = val.pop("@source")
        value = val.pop("@value", None)
        data_type = val.pop("@type", None)
        entry = val.pop("@entry", None)

        data = self.get_value(value=value, entry=entry, source=source, data_type=data_type)
        setattr(container.attrs, name, data)

    def add_hardlink(self, container, val):
        pass

    def add_softlink(self, container, val):
        pass

    def add_content(self, container, layout):
        for key, values in layout.items():
            if not isinstance(values, list):
                values = [values]
            for val in values:
                if key == "group":
                    self.add_group(container, val)
                elif key == "hdf5_layout":
                    self.add_base_entry(container, val)
                elif key == "attribute":
                    self.add_attribute(container, val)
                elif key == "dataset":
                    self.add_dataset(container, val)
                elif key == "hardlink":
                    self.add_hardlink(container, val)
                elif key == "softlink":
                    self.add_softlink(container, val)
                else:
                    pass
                    # raise NeXusLayoutError()

    def add_base_entry(self, container, val):
        self.add_group(container, val["group"])


class NeXusFileXMLWriter(FileWriter, XMLWriter):
    def configure(self, layout_file, **kwargs):
        self.layout_file = layout_file
        with open(self.layout_file, "br") as f:
            self.layout = xmltodict.parse(f)

    def get_value(self, value, entry, source, data_type):
        if source == "constant":
            if data_type:
                return self.get_type(data_type)(value)
            return value
        if source == "bec":
            return self.data.get(entry)
        return entry

    def write(self, file_path: str, data):
        print(f"writing file to {file_path}")
        self.data = self._create_device_data_storage(data)

        with h5py.File(file_path, "w") as file:
            self.add_content(file, self.layout)


class HDF5Storage:
    """
    The HDF5Storage class is a container used by the HDF5 writer plugins to store data in the correct NeXus format.
    """

    def __init__(self, storage_type: str = "group", data=None) -> None:
        self._storage = {}
        self._storage_type = storage_type
        self.attrs = {}
        self._data = data

    def create_group(self, name: str) -> HDF5Storage:
        """
        Create a group in the HDF5 storage.

        Args:
            name (str): Group name

        Returns:
            HDF5Storage: Group storage
        """
        self._storage[name] = HDF5Storage(storage_type="group")
        return self._storage[name]

    def create_dataset(self, name: str, data: typing.Any) -> HDF5Storage:
        """
        Create a dataset in the HDF5 storage.

        Args:
            name (str): Dataset name
            data (typing.Any): Dataset data

        Returns:
            HDF5Storage: Dataset storage
        """
        self._storage[name] = HDF5Storage(storage_type="dataset", data=data)
        return self._storage[name]

    def create_soft_link(self, name: str, target: str) -> HDF5Storage:
        """
        Create a soft link in the HDF5 storage.

        Args:
            name (str): Link name
            target (str): Link target

        Returns:
            HDF5Storage: Link storage
        """
        self._storage[name] = HDF5Storage(storage_type="softlink", data=target)
        return self._storage[name]

    def create_ext_link(self, name: str, target: str, entry: str) -> HDF5Storage:
        """
        Create an external link in the HDF5 storage.

        Args:
            name (str): Link name
            target (str): Name of the target file
            entry (str): Entry within the target file (e.g. entry/instrument/eiger_4)

        Returns:
            HDF5Storage: Link storage
        """
        data = {"file": target, "entry": entry}
        self._storage[name] = HDF5Storage(storage_type="ext_link", data=data)
        return self._storage[name]


class HDF5StorageWriter:
    device_storage = None

    def add_group(self, name: str, container: typing.Any, val: HDF5Storage):
        group = container.create_group(name)
        self.add_attribute(group, val.attrs)
        self.add_content(group, val._storage)

        if name == "bec" and container.attrs.get("NX_class") == "NXcollection":
            for key, value in self.device_storage.items():
                if value is None:
                    continue
                if isinstance(value, dict):
                    sub_storage = HDF5Storage(key)
                    dict_to_storage(sub_storage, value)
                    self.add_group(key, group, sub_storage)
                    # self.add_content(group, sub_storage._storage)
                    continue
                if isinstance(value, list) and isinstance(value[0], dict):
                    merged_dict = merge_dicts(value)
                    sub_storage = HDF5Storage(key)
                    dict_to_storage(sub_storage, merged_dict)
                    self.add_group(key, group, sub_storage)
                    continue

                group.create_dataset(name=key, data=value)

    def add_dataset(self, name: str, container: typing.Any, val: HDF5Storage):
        try:
            data = val._data
            if data is None:
                return
            if isinstance(data, list):
                if data and isinstance(data[0], dict):
                    data = json.dumps(data)
            dataset = container.create_dataset(name, data=data)
            self.add_attribute(dataset, val.attrs)
            self.add_content(dataset, val._storage)
        except Exception as exc:
            content = traceback.format_exc()
            logger.error(f"Failed to write dataset {name}: {content}")
        return

    def add_attribute(self, container: typing.Any, attributes: dict):
        for name, value in attributes.items():
            if value is not None:
                container.attrs[name] = value

    def add_hardlink(self, name, container, val):
        pass

    def add_softlink(self, name, container, val):
        container[name] = h5py.SoftLink(val._data)

    def add_external_link(self, name, container, val):
        container[name] = h5py.ExternalLink(val._data.get("file"), val._data.get("entry"))

    def add_content(self, container, storage):
        for name, val in storage.items():
            if val._storage_type == "group":
                self.add_group(name, container, val)
            elif val._storage_type == "dataset":
                self.add_dataset(name, container, val)
            elif val._storage_type == "hardlink":
                self.add_hardlink(name, container, val)
            elif val._storage_type == "softlink":
                self.add_softlink(name, container, val)
            elif val._storage_type == "ext_link":
                self.add_external_link(name, container, val)
            else:
                pass

    @classmethod
    def write_to_file(cls, writer_storage, device_storage, file):
        writer = cls()
        writer.device_storage = device_storage
        writer.add_content(file, writer_storage)


class NexusFileWriter(FileWriter):
    def write(self, file_path: str, data):
        device_storage = self._create_device_data_storage(data)
        device_storage["metadata"] = data.metadata

        # NeXus needs start_time and end_time in ISO8601 format, so we have to convert it
        if data.start_time is not None:
            device_storage["start_time"] = datetime.datetime.fromtimestamp(
                data.start_time
            ).isoformat()
        if data.end_time is not None:
            device_storage["end_time"] = datetime.datetime.fromtimestamp(data.end_time).isoformat()
        writer_format = getattr(fwp, self.file_writer_manager.file_writer_config.get("plugin"))
        for file_ref in data.file_references.values():
            rel_path = os.path.relpath(file_ref["path"], os.path.dirname(file_path))
            file_ref["path"] = rel_path

        writer_storage = writer_format(
            storage=HDF5Storage(),
            data=device_storage,
            file_references=data.file_references,
            device_manager=self.file_writer_manager.device_manager,
        )

        with h5py.File(file_path, "w") as file:
            HDF5StorageWriter.write_to_file(writer_storage._storage, device_storage, file)


def dict_to_storage(storage, data):
    for key, val in data.items():
        if isinstance(val, dict):
            sub = storage.create_group(key)
            dict_to_storage(sub, val)
            continue
        storage.create_dataset(key, val)
