# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "03/02/2022"


import os
from functools import partial
from operator import is_not
from typing import Iterable, Optional, Union

import h5py
import numpy
from h5py import VirtualSource
from silx.io.url import DataUrl
from silx.utils.proxy import docstring

from nxtomomill.utils.frameappender import FrameAppender
from nxtomomill.utils.h5pyutils import from_virtual_source_to_data_url

try:
    from tomoscan.esrf.scan.hdf5scan import ImageKey
except ImportError:
    from tomoscan.esrf.hdf5scan import ImageKey

from h5py import h5s as h5py_h5s
from tomoscan.io import HDF5File
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_path
from tomoscan.scanbase import FOV as FieldOfView
from tomoscan.unitsystem import TimeSystem, Unit
from tomoscan.unitsystem.metricsystem import MetricSystem

from nxtomomill.nexus.utils import cast_and_check_array_1D, get_data, get_data_and_unit

from .nxobject import ElementWithUnit, NXobject

try:
    from h5py._hl.vds import VDSmap
except ImportError:
    has_VDSmap = False
else:
    has_VDSmap = True
import logging

import h5py._hl.selections as selection

_logger = logging.getLogger(__name__)


class NXdetector(NXobject):
    def __init__(
        self,
        node_name="detector",
        parent=None,
        field_of_view=None,
        expected_dim: Optional[tuple] = None,
    ) -> None:
        """
        :param Optional[tuple] expected_dim: user can provide expected dimesions as a tuple of int to be checked when data is set
        """
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)

        self._expected_dim = expected_dim

        self._data = None
        self.image_key_control = None
        self._x_pixel_size = ElementWithUnit(default_unit=MetricSystem.METER)
        # x 'sample' detector size
        self._y_pixel_size = ElementWithUnit(default_unit=MetricSystem.METER)
        # y 'sample' detector size
        self._x_flippped = None
        self._y_flippped = None
        self._distance = ElementWithUnit(
            default_unit=MetricSystem.METER
        )  # detector / sample distance
        self.field_of_view = field_of_view
        self._count_time = ElementWithUnit(default_unit=TimeSystem.SECOND)
        self.estimated_cor_from_motor = None
        self.tomo_n = None
        self.group_size = None
        self.__master_vds_file = None
        # used to record the virtual dataset set file origin in order to solve relative links
        self._set_freeze(True)

    @property
    def data(self) -> Optional[Union[numpy.ndarray, tuple]]:
        """data can be None, a numpy array or a list of DataUrl xor h5py Virtual Source"""
        return self._data

    @data.setter
    def data(self, data: Optional[Union[numpy.ndarray, tuple]]):
        if isinstance(data, (tuple, list)) or (
            isinstance(data, numpy.ndarray)
            and data.ndim == 1
            and (self._expected_dim is None or len(self._expected_dim) > 1)
        ):
            for elmt in data:
                if has_VDSmap:
                    if not isinstance(elmt, (DataUrl, VirtualSource, VDSmap)):
                        raise TypeError(
                            f"element of 'data' are expected to be a {len(self._expected_dim)}D numpy array, a list of silx DataUrl or a list of h5py virtualSource. Not {type(elmt)}"
                        )
            data = tuple(data)
        elif isinstance(data, numpy.ndarray):
            if (
                self._expected_dim is not None
                and data is not None
                and data.ndim not in self._expected_dim
            ):
                raise ValueError(
                    f"data is expected to be {len(self._expected_dim)}D not {data.ndim}D"
                )
        elif data is None:
            pass
        else:
            raise TypeError(
                f"data is expected to be an instance of {numpy.ndarray}, None or a list of silx DataUrl or h5py Virtual Source. Not {type(data)}"
            )
        self._data = data

    @property
    def x_pixel_size(self) -> Optional[float]:
        """x pixel size in meter (S.I.)"""
        return self._x_pixel_size

    @x_pixel_size.setter
    def x_pixel_size(self, x_pixel_size: Optional[float]) -> None:
        if not isinstance(x_pixel_size, (type(None), float)):
            raise TypeError(
                f"x_pixel_size is expected ot be an instance of {float} or None. Not {type(x_pixel_size)}"
            )
        self._x_pixel_size.value = x_pixel_size

    @property
    def y_pixel_size(self) -> Optional[float]:
        """y 'sample' pixel size in meter (S.I.)"""
        return self._y_pixel_size

    @y_pixel_size.setter
    def y_pixel_size(self, y_pixel_size: Optional[float]) -> None:
        if not isinstance(y_pixel_size, (type(None), float)):
            raise TypeError(
                f"y_pixel_size is expected ot be an instance of {float} or None. Not {type(y_pixel_size)}"
            )
        self._y_pixel_size.value = y_pixel_size

    @property
    def x_flipped(self):
        return self._x_flippped

    @x_flipped.setter
    def x_flipped(self, flipped: Optional[bool]):
        if flipped is None:
            self._x_flippped = None
        elif not isinstance(flipped, (bool, numpy.bool_)):
            raise TypeError(f"flipped is expected to be a bool. Not {type(flipped)}")
        else:
            self._x_flippped = bool(flipped)

    @property
    def y_flipped(self):
        return self._y_flippped

    @y_flipped.setter
    def y_flipped(self, flipped: bool):
        if flipped is None:
            self._y_flippped = None
        elif not isinstance(flipped, (bool, numpy.bool_)):
            raise TypeError(f"flipped is expected to be a bool. Not {type(flipped)}")
        else:
            self._y_flippped = bool(flipped)

    @property
    def distance(self) -> Optional[float]:
        """
        sample / detector distance in meter
        """
        return self._distance

    @distance.setter
    def distance(self, distance: Optional[float]) -> None:
        if not isinstance(distance, (type(None), float)):
            raise TypeError(
                f"distance is expected ot be an instance of {float} or None. Not {type(distance)}"
            )
        self._distance.value = distance

    @property
    def field_of_view(self) -> Optional[FieldOfView]:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(
        self, field_of_view: Optional[Union[FieldOfView, str, None]]
    ) -> None:
        if field_of_view is not None:
            field_of_view = FieldOfView.from_value(field_of_view)
        self._field_of_view = field_of_view

    @property
    def count_time(self) -> Optional[numpy.ndarray]:
        return self._count_time

    @count_time.setter
    def count_time(self, count_time: Optional[Iterable]):
        self._count_time.value = cast_and_check_array_1D(count_time, "count_time")

    @property
    def estimated_cor_from_motor(self) -> Optional[float]:
        return self._estimated_cor_from_motor

    @estimated_cor_from_motor.setter
    def estimated_cor_from_motor(self, estimated_cor_from_motor: Optional[float]):
        if not isinstance(estimated_cor_from_motor, (type(None), float)):
            raise TypeError(
                f"estimated_cor_from_motor is expected to be None, or an instance of float. Not {type(estimated_cor_from_motor)}"
            )
        self._estimated_cor_from_motor = estimated_cor_from_motor

    @property
    def image_key_control(self) -> Optional[numpy.ndarray]:
        """
        control image key are the same as image key except that they can contain negative values for return / alignment projection.
        """
        return self._image_key_control

    @image_key_control.setter
    def image_key_control(self, control_image_key: Optional[Iterable]):
        control_image_key = cast_and_check_array_1D(
            control_image_key, "control_image_key"
        )
        if control_image_key is None:
            self._image_key_control = None
        else:
            # cast all value to instances of ImageKey
            self._image_key_control = numpy.asarray(
                [ImageKey.from_value(key) for key in control_image_key]
            )

    @property
    def image_key(self) -> Optional[numpy.ndarray]:
        """
        control_image_key with ALIGNEMENT keys cast to PROJECTION
        """
        if self.image_key_control is None:
            return None
        else:
            control_image_key = self.image_key_control.copy()
            control_image_key[
                control_image_key == ImageKey.ALIGNMENT
            ] = ImageKey.PROJECTION
            return control_image_key

    @property
    def tomo_n(self) -> Optional[int]:
        return self._tomo_n

    @tomo_n.setter
    def tomo_n(self, tomo_n: Optional[int]):
        self._tomo_n = tomo_n

    @property
    def group_size(self) -> Optional[int]:
        return self._group_size

    @group_size.setter
    def group_size(self, group_size: Optional[int]):
        self._group_size = group_size

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}

        # image key control
        if self.image_key_control is not None:
            path_img_key = f"{self.path}/{nexus_detector_paths.IMAGE_KEY}"
            nx_dict[path_img_key] = [img_key.value for img_key in self.image_key]
            path_img_key_ctrl = f"{self.path}/{nexus_detector_paths.IMAGE_KEY_CONTROL}"
            nx_dict[path_img_key_ctrl] = [
                img_key.value for img_key in self.image_key_control
            ]
        # x 'sample' pixel
        if self.x_pixel_size.value is not None:
            path_x_pixel_size = f"{self.path}/{nexus_detector_paths.X_PIXEL_SIZE}"
            nx_dict[path_x_pixel_size] = self.x_pixel_size.value
            nx_dict["@".join([path_x_pixel_size, "units"])] = str(
                self.x_pixel_size.unit
            )
        # y 'sample' pixel
        if self.y_pixel_size.value is not None:
            path_y_pixel_size = f"{self.path}/{nexus_detector_paths.Y_PIXEL_SIZE}"
            nx_dict[path_y_pixel_size] = self.y_pixel_size.value
            nx_dict["@".join([path_y_pixel_size, "units"])] = str(
                self.y_pixel_size.unit
            )
        # x flipped
        if self.x_flipped is not None:
            path_x_flipped = f"{self.path}/{nexus_detector_paths.X_FLIPPED}"
            nx_dict[path_x_flipped] = self.x_flipped
        # y flipped
        if self.y_flipped is not None:
            path_y_flipped = f"{self.path}/{nexus_detector_paths.Y_FLIPPED}"
            nx_dict[path_y_flipped] = self.y_flipped
        # distance
        if self.distance.value is not None:
            path_distance = f"{self.path}/{nexus_detector_paths.DISTANCE}"
            nx_dict[path_distance] = self.distance.value
            nx_dict["@".join([path_distance, "units"])] = str(self.distance.unit)
        # FOV
        if self.field_of_view is not None:
            path_fov = f"{self.path}/{nexus_detector_paths.FOV}"
            nx_dict[path_fov] = self.field_of_view.value
        # count time
        if self.count_time.value is not None:
            path_count_time = f"{self.path}/{nexus_detector_paths.EXPOSURE_TIME}"
            nx_dict[path_count_time] = self.count_time.value
            nx_dict["@".join([path_count_time, "units"])] = str(self.count_time.unit)
        # tomo n
        if self.tomo_n is not None:
            tomo_n_fov_path = f"{nexus_paths.TOMO_N_SCAN}"
            nx_dict[tomo_n_fov_path] = self.tomo_n
        if self.group_size is not None:
            group_size_path = f"{self.path}/{nexus_paths.GRP_SIZE_ATTR}"
            nx_dict[group_size_path] = self.group_size
        if self.estimated_cor_from_motor is not None:
            path_estimated_cor = (
                f"{self.path}/{nexus_detector_paths.ESTIMATED_COR_FRM_MOTOR}"
            )
            nx_dict[path_estimated_cor] = self.estimated_cor_from_motor
            nx_dict["@".join([path_estimated_cor, "units"])] = "pixel"

        nx_dict.update(
            self._data_to_nx_dict(
                nexus_path_version=nexus_path_version,
                data_path=data_path,
            )
        )
        return nx_dict

    def _data_to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}
        if self.data is not None:
            # add data
            path_data = f"{self.path}/{nexus_detector_paths.DATA}"
            nx_dict[path_data] = self.data
            nx_dict["@".join([path_data, "interpretation"])] = "image"
            nx_dict["__vds_master_file__"] = self.__master_vds_file
            # add attributes to data
            nx_dict[f"{self.path}@NX_class"] = "NXdetector"
            nx_dict[f"{self.path}@signal"] = nexus_detector_paths.DATA
            nx_dict[f"{self.path}@SILX_style/axis_scale_types"] = [
                "linear",
                "linear",
            ]
        return nx_dict

    def _load(
        self, file_path: str, data_path: str, nexus_version: float, load_data_as: str
    ) -> None:
        possible_as_values = ("as_virtual_source", "as_data_url", "as_numpy_array")
        if load_data_as not in possible_as_values:
            raise ValueError(
                f"load_data_as is expected to be in {possible_as_values} and not {load_data_as}"
            )

        self.__master_vds_file = file_path
        # record the input file if we need to solve virtual dataset path from it

        nexus_paths = get_nexus_path(nexus_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        data_dataset_path = f"{data_path}/{nexus_detector_paths.DATA}"

        def vs_file_path_to_real_path(file_path, vs_file_path):
            # get file path as absolute for the NXtomo. Simplify management of the
            # directories
            if os.path.isabs(vs_file_path):
                return vs_file_path
            else:
                return os.path.join(os.path.dirname(file_path), vs_info.file_name)

        with HDF5File(file_path, mode="r") as h5f:
            if data_dataset_path in h5f:
                dataset = h5f[data_dataset_path]
            else:
                _logger.error(f"unable to find {data_dataset_path}")
                return
            if load_data_as == "as_numpy_array":
                self.data = dataset[()]
            elif load_data_as == "as_data_url":
                if dataset.is_virtual:
                    urls = []
                    for vs_info in dataset.virtual_sources():
                        select_bounds = vs_info.vspace.get_select_bounds()
                        left_bound = select_bounds[0]
                        right_bound = select_bounds[1]
                        # warning: for now step is not managed with virtual
                        # dataset

                        length = right_bound[0] - left_bound[0] + 1
                        # warning: for now step is not managed with virtual
                        # dataset
                        virtual_source = h5py.VirtualSource(
                            vs_file_path_to_real_path(
                                file_path=file_path, vs_file_path=vs_info.file_name
                            ),
                            vs_info.dset_name,
                            vs_info.vspace.shape,
                        )
                        # here we could provide dataset but we won't to
                        # insure file path will be relative.
                        type_code = vs_info.src_space.get_select_type()
                        # check for unlimited selections in case where selection is regular
                        # hyperslab, which is the only allowed case for h5s.UNLIMITED to be
                        # in the selection
                        if (
                            type_code == h5py_h5s.SEL_HYPERSLABS
                            and vs_info.src_space.is_regular_hyperslab()
                        ):
                            (
                                source_start,
                                stride,
                                count,
                                block,
                            ) = vs_info.src_space.get_regular_hyperslab()
                            source_end = source_start[0] + length

                            sel = selection.select(
                                dataset.shape,
                                slice(source_start[0], source_end),
                                dataset=dataset,
                            )
                            virtual_source.sel = sel

                        urls.append(from_virtual_source_to_data_url(virtual_source))
                else:
                    urls = [
                        DataUrl(
                            file_path=file_path,
                            data_path=data_dataset_path,
                            scheme="silx",
                        )
                    ]
                self.data = urls
            elif load_data_as == "as_virtual_source":
                if dataset.is_virtual:
                    virtual_sources = []
                    for vs_info in dataset.virtual_sources():
                        u_vs_info = VDSmap(
                            vspace=vs_info.vspace,
                            file_name=vs_file_path_to_real_path(
                                file_path=file_path, vs_file_path=vs_info.file_name
                            ),
                            dset_name=vs_info.dset_name,
                            src_space=vs_info.src_space,
                        )

                        _, vs = FrameAppender._recreate_vs(
                            vs_info=u_vs_info, vds_file=file_path
                        )
                        virtual_sources.append(vs)
                    self.data = virtual_sources
                else:
                    raise ValueError(f"{data_dataset_path} is not virtual")
        # load 'sample' pixel size
        try:
            self.x_pixel_size, self.x_pixel_size.unit = get_data_and_unit(
                file_path=file_path,
                data_path="/".join([data_path, nexus_detector_paths.X_PIXEL_SIZE]),
                default_unit=MetricSystem.METER,
            )
        except TypeError as e:
            # in case loaded pixel size doesn't fit the type (case Diamond dataset)
            _logger.warning(f"Fail to load x pixel size. Error is {e}")
        try:
            self.y_pixel_size, self.y_pixel_size.unit = get_data_and_unit(
                file_path=file_path,
                data_path="/".join([data_path, nexus_detector_paths.Y_PIXEL_SIZE]),
                default_unit=MetricSystem.METER,
            )
        except TypeError as e:
            # in case loaded pixel size doesn't fit the type (case Diamond dataset)
            _logger.warning(f"Fail to load y pixel size. Error is {e}")

        self.x_flipped = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.X_FLIPPED]),
        )
        self.y_flipped = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.Y_FLIPPED]),
        )
        try:
            self.distance, self.distance.unit = get_data_and_unit(
                file_path=file_path,
                data_path="/".join([data_path, nexus_detector_paths.DISTANCE]),
                default_unit=MetricSystem.METER,
            )
        except TypeError as e:
            # in case loaded pixel size doesn't fit the type (case Diamond dataset)
            _logger.warning(f"Fail to load distance. Error is {e}")

        self.field_of_view = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.FOV]),
        )
        self.count_time, self.count_time.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.EXPOSURE_TIME]),
            default_unit=TimeSystem.SECOND,
        )
        self.tomo_n = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.TOMO_N_SCAN]),
        )
        self.group_size = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.GRP_SIZE_ATTR]),
        )
        self.estimated_cor_from_motor = get_data(
            file_path=file_path,
            data_path="/".join(
                [data_path, nexus_detector_paths.ESTIMATED_COR_FRM_MOTOR]
            ),
        )
        self.image_key_control = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.IMAGE_KEY_CONTROL]),
        )
        if self.image_key_control is None:
            # in the case image_key_control doesn't exists (dimaond dataset use case)
            self.image_key_control = get_data(
                file_path=file_path,
                data_path="/".join([data_path, nexus_detector_paths.IMAGE_KEY]),
            )

    @staticmethod
    def _concatenate_except_data(nx_detector, nx_objects: tuple):
        image_key_ctrl = [
            nx_obj.image_key_control
            for nx_obj in nx_objects
            if nx_obj.image_key_control is not None
        ]
        if len(image_key_ctrl) > 0:
            nx_detector.image_key_control = numpy.concatenate(image_key_ctrl)

        # note: image_key is deduced from image_key_control
        nx_detector.x_pixel_size = nx_objects[0].x_pixel_size.value
        nx_detector.y_pixel_size = nx_objects[0].y_pixel_size.value
        nx_detector.distance = nx_objects[0].distance.value
        nx_detector.field_of_view = nx_objects[0].field_of_view
        nx_detector.x_flipped = nx_objects[0].x_flipped
        nx_detector.y_flipped = nx_objects[0].y_flipped
        nx_detector.estimated_cor_from_motor = nx_objects[0].estimated_cor_from_motor
        for nx_obj in nx_objects[1:]:
            if nx_detector.x_pixel_size.value and not numpy.isclose(
                nx_detector.x_pixel_size.value, nx_obj.x_pixel_size.value
            ):
                _logger.warning(
                    f"found different x pixel size value. ({nx_detector.x_pixel_size.value} vs {nx_obj.x_pixel_size.value}). Pick the first one"
                )
            if nx_detector.y_pixel_size.value and not numpy.isclose(
                nx_detector.y_pixel_size.value, nx_obj.y_pixel_size.value
            ):
                _logger.warning(
                    f"found different y pixel size value. ({nx_detector.y_pixel_size.value} vs {nx_obj.y_pixel_size.value}). Pick the first one"
                )

            if nx_detector.x_flipped and nx_detector.x_flipped != nx_obj.x_flipped:
                _logger.warning(
                    f"found different x_flipped value. ({nx_detector.x_flipped} vs {nx_obj.x_flipped}). Pick the first one"
                )
            if nx_detector.y_flipped and nx_detector.y_flipped != nx_obj.y_flipped:
                _logger.warning(
                    f"found different y_flipped value. ({nx_detector.y_flipped} vs {nx_obj.y_flipped}). Pick the first one"
                )
            if nx_detector.distance.value and not numpy.isclose(
                nx_detector.distance.value, nx_obj.distance.value
            ):
                _logger.warning(
                    f"found different distance value. ({nx_detector.distance.value} vs {nx_obj.distance.value}). Pick the first one"
                )
            if (
                nx_detector.field_of_view
                and nx_detector.field_of_view != nx_obj.field_of_view
            ):
                _logger.warning(
                    f"found different field_of_view value. ({nx_detector.field_of_view} vs {nx_obj.field_of_view}). Pick the first one"
                )
            if (
                (nx_obj.estimated_cor_from_motor is not None)
                and (nx_detector.estimated_cor_from_motor is not None)
                and not numpy.isclose(
                    nx_detector.estimated_cor_from_motor,
                    nx_obj.estimated_cor_from_motor,
                )
            ):
                _logger.warning(
                    f"found different estimated_cor_from_motor value. ({nx_detector.estimated_cor_from_motor} vs {nx_obj.estimated_cor_from_motor}). Pick the first one"
                )

    @staticmethod
    @docstring(NXobject)
    def concatenate(nx_objects: tuple, node_name="detector"):
        # filter None obj
        nx_objects = tuple(filter(partial(is_not, None), nx_objects))
        if len(nx_objects) == 0:
            return None
        # warning: later we make the assumption that nx_objects contains at least one element
        for nx_obj in nx_objects:
            if not isinstance(nx_obj, NXdetector):
                raise TypeError("Cannot concatenate non NXinstrument object")

        nx_detector = NXdetector(node_name=node_name)
        NXdetector._concatenate_except_data(
            nx_objects=nx_objects, nx_detector=nx_detector
        )

        # now handle data on it's own
        detector_data = [
            nx_obj.data for nx_obj in nx_objects if nx_obj.data is not None
        ]
        if len(detector_data) > 0:
            if isinstance(detector_data[0], numpy.ndarray):
                # store_as = "as_numpy_array"
                expected = numpy.ndarray
            elif isinstance(detector_data[0], Iterable):
                if isinstance(detector_data[0][0], h5py.VirtualSource):
                    # store_as = "as_virtual_source"
                    expected = h5py.VirtualSource
                elif isinstance(detector_data[0][0], DataUrl):
                    # store_as = "as_data_url"
                    expected = DataUrl
                else:
                    raise TypeError(
                        f"detector data is expected to be a numpy array or a h5py.VirtualSource or a numpy array. {type(detector_data[0][0])} is not handled."
                    )
            else:
                raise TypeError(
                    f"detector data is expected to be a numpy array or a h5py.VirtualSource or a numpy array. {type(detector_data[0])} is not handled."
                )

            for data in detector_data:
                if expected in (DataUrl, h5py.VirtualSource):
                    # for DataUrl and VirtualSource check type of the element
                    cond = isinstance(data[0], expected)
                else:
                    cond = isinstance(data, expected)
                if not cond:
                    raise TypeError(
                        f"Incoherent data type cross detector data ({type(data)} when {expected} expected)"
                    )

            if expected in (DataUrl, h5py.VirtualSource):
                new_data = []
                [new_data.extend(data) for data in detector_data]
            else:
                new_data = numpy.concatenate(detector_data)
            nx_detector.data = new_data

        return nx_detector


class NXdetectorWithUnit(NXdetector):
    def __init__(
        self,
        default_unit: Unit,
        node_name="detector",
        parent=None,
        field_of_view=None,
        expected_dim: Optional[tuple] = None,
    ) -> None:
        super().__init__(node_name, parent, field_of_view, expected_dim)
        self._data = ElementWithUnit(default_unit=default_unit)

    @property
    def data(self) -> Union[numpy.ndarray, tuple]:
        """data can be None, a numpy array or a list of DataUrl xor h5py Virtual Source"""
        return self._data

    @data.setter
    def data(self, data: Optional[Union[numpy.ndarray, tuple]]):
        if isinstance(data, numpy.ndarray):
            if (
                self._expected_dim is not None
                and data is not None
                and data.ndim not in self._expected_dim
            ):
                raise ValueError(
                    f"data is expected to be {self._expected_dim}d not {data.ndim}d"
                )
        elif isinstance(data, (tuple, list)):
            for elmt in data:
                if not isinstance(elmt, (DataUrl, VirtualSource)):
                    raise TypeError(
                        f"'data' is expected to be a numpy array or a list/tuple composed of DataUrl or h5py virtualSource. Not {type(elmt)}"
                    )
            data = tuple(data)
        elif data is None:
            pass
        else:
            raise TypeError(
                f"data is expected to be an instance of {numpy.ndarray}, None or a list of silx DataUrl or h5py Virtual Source. Not {type(data)}"
            )
        self._data.value = data

    def _data_to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}
        if self.data.value is not None:
            # add data
            path_data = f"{self.path}/{nexus_detector_paths.DATA}"
            nx_dict[path_data] = self.data.value
            nx_dict["@".join([path_data, "interpretation"])] = "image"
            # add attributes to data
            nx_dict[f"{self.path}@NX_class"] = "NXdetector"
            nx_dict[f"{self.path}@signal"] = nexus_detector_paths.DATA
            nx_dict[f"{self.path}@SILX_style/axis_scale_types"] = [
                "linear",
                "linear",
            ]
        return nx_dict

    @staticmethod
    @docstring(NXobject)
    def concatenate(
        nx_objects: tuple, default_unit, expected_dim, node_name="detector"
    ):
        # filter None obj
        nx_objects = tuple(filter(partial(is_not, None), nx_objects))
        if len(nx_objects) == 0:
            return None
        # warning: later we make the assumption that nx_objects contains at least one element
        for nx_obj in nx_objects:
            if not isinstance(nx_obj, NXdetector):
                raise TypeError("Cannot concatenate non NXinstrument object")

        nx_detector = NXdetectorWithUnit(
            node_name=node_name, default_unit=default_unit, expected_dim=expected_dim
        )
        NXdetector._concatenate_except_data(
            nx_objects=nx_objects, nx_detector=nx_detector
        )

        # now handle data on it's own
        detector_data = [
            nx_obj.data.value
            for nx_obj in nx_objects
            if (nx_obj.data is not None and nx_obj.data.value is not None)
        ]
        detector_units = set(
            [
                nx_obj.data.unit
                for nx_obj in nx_objects
                if (nx_obj.data is not None and nx_obj.data.value is not None)
            ]
        )
        if len(detector_units) > 1:
            # with DataUrl and Virtual Sources we are not able to do conversion
            raise ValueError("More than one units found. Unagle to build the detector")

        if len(detector_data) > 0:
            if isinstance(detector_data[0], numpy.ndarray):
                # store_as = "as_numpy_array"
                expected = numpy.array
            elif isinstance(detector_data[0], Iterable):
                if isinstance(detector_data[0][0], h5py.VirtualSource):
                    # store_as = "as_virtual_source"
                    expected = h5py.VirtualSource
                elif isinstance(detector_data[0][0], DataUrl):
                    # store_as = "as_data_url"
                    expected = DataUrl
                else:
                    raise TypeError(
                        f"detector data is expected to be a numpy array or a h5py.VirtualSource or a numpy array. {type(detector_data[0][0])} is not handled."
                    )
            else:
                raise TypeError(
                    f"detector data is expected to be a numpy array or a h5py.VirtualSource or a numpy array. {type(detector_data[0])} is not handled."
                )

            for data in detector_data:
                if expected in (DataUrl, h5py.VirtualSource):
                    # for DataUrl and VirtualSource check type of the element
                    cond = isinstance(data[0], expected)
                else:
                    cond = isinstance(data, expected)
                if not cond:
                    raise TypeError(
                        f"Incoherent data type cross detector data ({type(data)} when {expected} expected)"
                    )

            if expected in (DataUrl, h5py.VirtualSource):
                new_data = []
                [new_data.extend(data) for data in detector_data]
            else:
                new_data = numpy.concatenate(detector_data)
            nx_detector.data.value = new_data
            nx_detector.data.unit = list(detector_units)[0]

        return nx_detector
