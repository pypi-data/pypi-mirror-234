from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Tuple

import numpy as np
import SimpleITK as sitk
from PIL import Image
from skimage.transform import resize

from ._slide import TiffWSI
from .vectors import FloatVector, IntVector

DEFAULT_SLICE_THICKNESS = 4.0e-3
SUPPORTED_WSI_EXTENSIONS = ["ndpi", "svs", "tiff"]


class Reader(Protocol):
    mag: float
    mpp_x: float
    mpp_y: float
    maxdimensions: Tuple[int]
    level_dimensions: List[Tuple[int, int]]
    level_downsamples: List[int]
    dimensions: Tuple[int]
    properties: Dict[str, Any]

    def read_region(self, loc: Tuple[int, int], level: int, dimensions: Tuple[int, int]) -> np.ndarray:
        ...

    def get_best_level_for_downsample(self, downsample: float) -> int:
        ...


class WholeSlide:
    """Implement a whole slide image class. This a lazy operation; the metadata are read and
    store, but the actual image data is not read until it is needed for processing.
    """

    def __init__(
        self, path: str, reader_cls: Reader = TiffWSI, additional_metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """WholeSlide constructor.

        :param path: The path to the WSI format.
        :type path: str
        :param reader_cls: The reader class that will fetch the metadata and read the image data
        when needed. This reader class should implement the same API as the Reader Protocol class.
        Two choices have been implemented: ImageWSi for non-pyramidal formats and TiffWSI for
        pyramidal ones, defaults to TiffWSI.
        :type reader_cls: Reader, optional
        :param additional_metadata: The additional metadata that should be passed to the reader,
        defaults to None.
        :type additional_metadata: Optional[Dict[str, Any]], optional
        """

        self.path = path

        if reader_cls is TiffWSI:
            self.slide = reader_cls(path)
        else:
            self.slide = reader_cls(path, additional_metadata)

        self.mag = self.slide.mag

        logging.info("Slide properties:")

        self.dimensions = self.slide.maxdimensions
        self.slice_thickness = DEFAULT_SLICE_THICKNESS
        self.zposition = 0

    @property
    def mpp(self):
        return self.slide.mpp

    def set_thickness(self, thickness: float):
        """Thickness in mm"""
        self.slice_thickness = thickness

    def set_zposition(self, z: float):
        """Offset in mm"""
        self.zposition = z

    def get_best_level_for_magnification(self, magnification: float):
        return self.slide.get_best_level_for_downsample(self.mag / magnification)

    def get_magnification_for_resolution(self, mpp: FloatVector) -> float:
        """
        Get the required target magnification if we want a particular resolution in mpp.

        If the target downsample is different in x and y dimensions, takes the smallest
        downsample to compute the target magnification.
        :param mpp:
        :return:
        """
        dsx = self.mpp.x / mpp.x
        dsy = self.mpp.y / mpp.y

        return self.mag * min(dsx, dsy)

    def get_absolute_position(self, location: FloatVector) -> FloatVector:
        """
        Returns location in µm from the top-left corner
        :param location: relative location in %
        :return:
        """
        return FloatVector(
            x=location.x * self.dimensions.x * self.mpp.x, y=location.y * self.dimensions.y * self.mpp.y
        )

    def read_full(self, magnification: Optional[float] = None, resolution: Optional[float] = None) -> SlideRegion:
        if magnification is None and resolution is None:
            raise ValueError(f"Either magnification or resolution argument must be set.")
        if magnification is not None:
            return SlideRegion(
                wsi=self, location=FloatVector(x=0, y=0), dimensions=FloatVector(x=1, y=1), magnification=magnification
            )
        magnification = self.get_magnification_for_resolution(FloatVector(resolution, resolution))
        return SlideRegion(
            wsi=self, location=FloatVector(x=0, y=0), dimensions=FloatVector(x=1, y=1), magnification=magnification
        )

    def read_region(self, location: FloatVector, magnification: float, dimensions: FloatVector) -> SlideRegion:
        """
        :param location: relative location in % of full image
        :param magnification: target magnification
        :param dimensions: relative dimensions in % of full image
        :return:
        """

        return SlideRegion(wsi=self, location=location, dimensions=dimensions, magnification=magnification)

    def read_region_absolute(self, location: IntVector, magnification: float, dimensions: IntVector):
        """
        :param location: location in px of full-size image
        :param magnification: target magnification
        :param dimensions: dimensions in px of full-size image
        :return:
        """
        rel_location = FloatVector(x=location.x / self.dimensions.x, y=location.y / self.dimensions.y)
        factor = magnification / self.mag
        rel_dimensions = FloatVector(
            x=dimensions.x / (self.dimensions.x * factor), y=dimensions.y / (self.dimensions.y * factor)
        )
        return SlideRegion(wsi=self, location=rel_location, dimensions=rel_dimensions, magnification=magnification)

    def mm_per_pixel_at_mag(self, magnification: float):
        """
        Pixel size in mm/px
        :param magnification:
        :return:
        """
        scale = self.mag / magnification
        return self.mpp.scale(scale * 1e-3)

    def um_per_pixel_at_mag(self, magnification: float):
        """
        Pixel size in µm/px
        :param magnification:
        :return:
        """
        scale = self.mag / magnification
        return self.mpp.scale(scale)


@dataclass
class PaddingParameters:
    pad_before: IntVector
    pad_after: IntVector
    pad_value: float

    @property
    def pad_width(self):
        return [(self.pad_before.y, self.pad_after.y), (self.pad_before.x, self.pad_after.x), (0, 0)]

    def scale(self, s: FloatVector):
        return [
            (int(self.pad_before.y * s.y), int(self.pad_after.y * s.y)),
            (int(self.pad_before.x * s.y), int(self.pad_after.x * s.x)),
            (0, 0),
        ]


class SlideRegion:
    def __init__(
        self,
        *,
        wsi: WholeSlide,
        location: FloatVector,
        dimensions: FloatVector,
        magnification: float,
        preload: bool = False,
    ):
        self.wsi = wsi
        self.location = location
        self.dimensions = dimensions
        self.magnification = magnification
        self.ndarray: Optional[np.ndarray] = None
        self.px_dimensions = IntVector(
            x=int(self.dimensions.x * self.wsi.dimensions.x * self.magnification / self.wsi.mag),
            y=int(self.dimensions.y * self.wsi.dimensions.y * self.magnification / self.wsi.mag),
        )
        self.padding: Optional[PaddingParameters] = None
        if preload:
            self._load()

    def _load(self):
        level = self.wsi.get_best_level_for_magnification(self.magnification)
        dimensions_at_level = IntVector(
            x=int(self.dimensions.x * self.wsi.slide.level_dimensions[level][0]),
            y=int(self.dimensions.y * self.wsi.slide.level_dimensions[level][1]),
        )

        location_abs = IntVector(
            x=int(self.location.x * self.wsi.dimensions.x), y=int(self.location.y * self.wsi.dimensions.y)
        )

        logging.info(
            f"Loading region @ {location_abs}, "
            + f"magnification={self.magnification}, "
            + f"dimensions={dimensions_at_level}."
        )

        # check if we need to further rescale to get to the target magnification or if we can use the level as is
        if self.wsi.slide.level_downsamples[level] == self.wsi.mag / self.magnification:
            self.ndarray = self.wsi.slide.read_region(location_abs.xy, level, dimensions_at_level.xy)
            if self.ndarray.shape[1] != self.px_dimensions.x or self.ndarray.shape[0] != self.px_dimensions.y:
                raise ValueError(
                    f"Expected target dimensions are {self.px_dimensions}, real dimensions are "
                    f"{IntVector(x=self.ndarray.shape[1], y=self.ndarray.shape[0])}"
                )
            return

        logging.info(f"Resizing from {self.wsi.mag / self.wsi.slide.level_downsamples[level]}x ({level=})")
        logging.debug(f"{location_abs.xy=}, {level=}, {dimensions_at_level.xy=}")
        region = self.wsi.slide.read_region(location_abs.xy, level, dimensions_at_level.xy)
        self.ndarray = resize(region, self.px_dimensions.yx)

    @property
    def as_pil(self):
        if self.ndarray is None:
            self._load()

        return Image.fromarray(self.ndarray.astype(np.uint8))   # PIL only accepts UINT8 for RGB images

    @property
    def as_ndarray(self):
        if self.ndarray is None:
            self._load()
        if self.padding is not None:
            return np.pad(self.ndarray[..., :3], self.padding.pad_width, constant_values=self.padding.pad_value)
        return self.ndarray[..., :3]

    def pad(self, dimensions: IntVector, center: bool = True, pad_value: float = 0.0) -> None:
        pad_dimensions = dimensions - self.px_dimensions
        if pad_dimensions.x < 0 or pad_dimensions.y < 0:
            msg = f"Target dimensions must be larger than initial dimensions! {dimensions=}, {self.px_dimensions=}"
            logging.error(msg)
            raise ValueError(msg)
        if center:
            pad_before = IntVector(x=pad_dimensions.x // 2, y=pad_dimensions.y // 2)
            self.padding = PaddingParameters(
                pad_before=pad_before,
                pad_after=IntVector(x=pad_dimensions.x - pad_before.x, y=pad_dimensions.y - pad_before.y),
                pad_value=pad_value,
            )
        else:
            self.padding = PaddingParameters(
                pad_before=IntVector(x=0, y=0), pad_after=pad_dimensions, pad_value=pad_value
            )

    @property
    def as_sitk(self):
        return self._as_sitk(floating=True)

    @property
    def as_anchored_sitk(self):
        return self._as_sitk(floating=False)

    def _as_sitk(self, *, floating: bool = True):
        """Floating parameters indicates if the spacing / directions / offset should be set (if floating is False)."""
        if self.ndarray is None:
            self._load()

        image = sitk.GetImageFromArray(self.as_ndarray[np.newaxis, :, :, :3], isVector=True)

        if not floating:
            spacing = self.mpp(factor=1e-3)  # default: mm/px
            origin = self.wsi.get_absolute_position(self.location)

            image.SetSpacing(spacing.xyz)
            image.SetOrigin((origin.x * 1e-3, origin.y * 1e-3, self.wsi.zposition * spacing.z))
            image.SetDirection((1, 0, 0, 0, 1, 0, 0, 0, 1))

        return image

    def mpp(self, factor: float = 1e-3) -> FloatVector:
        # mpp = µm / px -> x 1e-3 = mm / px
        downsample = self.wsi.mag / self.magnification
        spacing = FloatVector(
            x=float(self.wsi.mpp.x) * downsample * factor,
            y=float(self.wsi.mpp.y) * downsample * factor,
            z=self.wsi.slice_thickness * factor,
        )
        return spacing

    @property
    def absolute_position(self):
        return self.wsi.get_absolute_position(self.location)


@dataclass
class SlideStack:
    slides: List[WholeSlide] = field(default_factory=list)
    pointer: int = 0

    def append(self, slide: WholeSlide) -> None:
        self.slides.append(slide)

    def generator(self):
        for slide in self.slides:
            yield slide

    def current(self):
        return self.slides[self.pointer]

    def next(self) -> Optional[WholeSlide]:
        if self.pointer + 1 >= len(self.slides):
            return None

        self.pointer += 1
        return self.current()

    def prev(self) -> Optional[WholeSlide]:
        if self.pointer <= 0:
            return None

        self.pointer -= 1
        return self.current()

    @classmethod
    def from_directory(
        cls, directory: str, file_prefix: str = "", extensions: Optional[List[str]] = None
    ) -> SlideStack:
        if extensions is None:
            extensions = SUPPORTED_WSI_EXTENSIONS
        files = os.listdir(directory)
        files = [os.path.join(directory, f) for f in files if not os.path.isdir(os.path.join(directory, f))]
        files = [
            f
            for f in files
            if (file_prefix == "" or f.startswith(file_prefix)) and f.rsplit(".", maxsplit=1)[1].lower() in extensions
        ]

        stack = SlideStack()

        if len(files) == 0:
            logging.warning(f"No files with {file_prefix=} and {extensions=} were found in {directory}")
            return stack

        logging.info(f"Creating stack with {len(files)} WSIs.")
        for f in files:
            stack.append(WholeSlide(path=f))

        return stack
