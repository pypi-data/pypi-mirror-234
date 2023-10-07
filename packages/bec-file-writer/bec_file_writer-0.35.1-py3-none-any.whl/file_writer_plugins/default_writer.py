from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bec_lib.core import DeviceManagerBase

    from file_writer.file_writer import HDF5Storage


def NeXus_format(
    storage: HDF5Storage,
    data: dict,
    file_references: dict,
    device_manager: DeviceManagerBase,
) -> HDF5Storage:
    """
    Prepare the NeXus file format.

    Args:
        storage (HDF5Storage): HDF5 storage. Pseudo hdf5 file container that will be written to disk later.
        data (dict): scan data
        file_references (dict): File references. Can be used to add external files to the HDF5 file.
        device_manager (DeviceManagerBase): Device manager. Can be used to check if devices are available.

    Returns:
        HDF5Storage: Updated HDF5 storage
    """
    # /entry
    entry = storage.create_group("entry")
    entry.attrs["NX_class"] = "NXentry"
    entry.attrs["version"] = 1.0

    # entry.attrs["definition"] = "NXsas"
    entry.attrs["start_time"] = data.get("start_time")
    entry.attrs["end_time"] = data.get("end_time")

    # /entry/collection
    collection = entry.create_group("collection")
    collection.attrs["NX_class"] = "NXcollection"
    bec_collection = collection.create_group("bec")

    # /entry/control
    control = entry.create_group("control")
    control.attrs["NX_class"] = "NXmonitor"
    control.create_dataset(name="mode", data="monitor")

    # /entry/data
    if "eiger_4" in device_manager.devices:
        entry.create_soft_link(name="data", target="/entry/instrument/eiger_4")

    # /entry/sample
    control = entry.create_group("sample")
    control.attrs["NX_class"] = "NXsample"
    control.create_dataset(name="name", data=data.get("samplename"))
    control.create_dataset(name="description", data=data.get("sample_description"))

    # /entry/instrument
    instrument = entry.create_group("instrument")
    instrument.attrs["NX_class"] = "NXinstrument"
    # instrument.create_dataset(name="name", data="cSAXS beamline")

    source = instrument.create_group("source")
    source.attrs["NX_class"] = "NXsource"
    source.create_dataset(name="type", data="Synchrotron X-ray Source")
    source.create_dataset(name="name", data="Swiss Light Source")
    source.create_dataset(name="probe", data="x-ray")
    # distance = source.create_dataset(name="distance", data=-33800 - np.asarray(data.get("samz", 0)))
    # distance.attrs["units"] = "mm"
    # sigma_x = source.create_dataset(name="sigma_x", data=0.202)
    # sigma_x.attrs["units"] = "mm"
    # sigma_y = source.create_dataset(name="sigma_y", data=0.018)
    # sigma_y.attrs["units"] = "mm"
    # divergence_x = source.create_dataset(name="divergence_x", data=0.000135)
    # divergence_x.attrs["units"] = "radians"
    # divergence_y = source.create_dataset(name="divergence_y", data=0.000025)
    # divergence_y.attrs["units"] = "radians"
    # current = source.create_dataset(name="current", data=data.get("curr"))
    # current.attrs["units"] = "mA"

    return storage
