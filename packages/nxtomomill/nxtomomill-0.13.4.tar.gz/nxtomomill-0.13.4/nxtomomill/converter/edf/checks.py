import numpy
import logging
from silx.utils.enum import Enum as _Enum
from tomoscan.esrf.scan.hdf5scan import HDF5TomoScan
from tomoscan.io import HDF5File
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from silx.io.utils import get_data

_logger = logging.getLogger(__name__)


class OUPUT_CHECK(_Enum):
    COMPARE_VOLUME = "compare-output-volume"


def compare_volumes(edf_volume_as_urls: tuple, hdf5_scan: HDF5TomoScan) -> tuple:
    """
    :param tuple edf_volume_as_urls: ordered list of the expected volume.
                                     contains (DataUrl, bool). first element is the location of the orginal frame,
                                     second is a boolean notifying if the frame has been modified or not.
                                     If yes then we cannot do the comparaison.
    :param HDF5TomoScan hdf5_scan: NXtomo that we want to check the construction.

    On this function we compare a final volume and it's construction. The idea here is more to prevent from
    some 'external' issues such as a file behing not accessible or some 'rock in the shoe'
    """
    issues = set()
    with HDF5File(hdf5_scan.master_file, mode="r") as h5f:
        entry_node = h5f[hdf5_scan.entry]
        nexus_path_version = entry_node.attrs.get("version", None)
        nexus_paths = get_nexus_paths(nexus_path_version)
        detector_dataset = entry_node[nexus_paths.PROJ_PATH]

        for i_frame, ((url_original, modified), output_frame) in enumerate(
            zip(edf_volume_as_urls, detector_dataset)
        ):
            original_data = get_data(url_original)
            if modified:
                _logger.info(
                    f"skip comparaison of frame {i_frame}, expected to be different"
                )
            elif original_data.dtype != detector_dataset.dtype:
                # TODO: in this case maybe we want to be more 'accommodating'
                issues.add(
                    f"orignial data and new dataset have different data type ({original_data.dtype} vs {detector_dataset.dtype})"
                )
            elif not numpy.allclose(original_data, output_frame):
                issues.add(
                    f"difference found on frame  {i_frame}. Orignal url is {url_original.path()}"
                )
    return tuple(issues)
