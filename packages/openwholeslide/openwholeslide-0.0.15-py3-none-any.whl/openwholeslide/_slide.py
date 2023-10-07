import logging
import math
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import tifffile
from PIL import Image
from skimage.transform import resize
from tifffile.tifffile import svs_description_metadata

from .vectors import FloatVector, IntVector

Image.MAX_IMAGE_PIXELS = None


class Property:
    NDPI_MAGNIFICATION: str = "Magnification"
    SVS_MAGNIFICATION: str = "AppMag"
    RESOLUTION_UNIT: str = "ResolutionUnit"
    IMAGE_WIDTH: str = "ImageWidth"
    IMAGE_LENGTH: str = "ImageLength"
    X_RESOLUTION: str = "XResolution"
    Y_RESOLUTION: str = "YResolution"
    MPP: str = "MPP"


class ResolutionUnit:
    CENTIMETER: str = "CENTIMETER"
    MILLIMETER: str = "MILLIMETER"
    MICROMETER: str = "MICROMETER"


class AssociatedImages:
    THUMBNAIL: str = "Thumbnail"
    MACRO: str = "Macro"
    LABEL: str = "Label"

    @classmethod
    def as_list(cls):
        return [cls.THUMBNAIL, cls.MACRO, cls.LABEL]


class TiffWSI:
    """Reader class to handle pyramidal WSI format."""

    def __init__(self, path: str):
        """TiffWSI constructor.

        :param path: The path to the WSI image.
        :type path: str
        """

        self.path = path
        self.tiff_file = tifffile.TiffFile(path)
        self.description = self.tiff_file.pages[0].description

        self._properties = {}
        if self.tiff_file.is_ndpi:
            self.mag = self.tiff_file.pages[0].ndpi_tags.get(Property.NDPI_MAGNIFICATION, 1.0)
            for key, val in self.tiff_file.pages[0].ndpi_tags.items():
                self._properties[key] = val
        elif self.tiff_file.is_svs or self.description.startswith("Aperio"):
            _metadata = svs_description_metadata(self.tiff_file.pages[0].description)
            self.mag = _metadata.get(Property.SVS_MAGNIFICATION, 1.0)
            for key, val in _metadata.items():
                self._properties[key] = val
        else:
            self.mag = 1.0

        unit_: tifffile.TiffTag = self.tiff_file.pages[0].tags.get(Property.RESOLUTION_UNIT, None)
        if unit_ is not None:
            unit = unit_.value.name
        else:
            unit = ResolutionUnit.CENTIMETER

        for key, val in self.tiff_file.pages[0].tags.items():
            self._properties[key] = val.value

        self.resolution_scale = 1e4  # default = CENTIMETER
        if unit.upper() == ResolutionUnit.MILLIMETER:
            self.resolution_scale = 1e3
        elif unit.upper() == ResolutionUnit.MICROMETER:
            self.resolution_scale = 1

        self.mpp = FloatVector(x=1.0, y=1.0)
        if Property.X_RESOLUTION in self.tiff_file.pages[0].tags:
            d, n = self.tiff_file.pages[0].tags[Property.X_RESOLUTION].value
            self.mpp.x = self.resolution_scale * n / d
        elif Property.MPP in self._properties:
            self.mpp.x = self._properties[Property.MPP]

        if Property.Y_RESOLUTION in self.tiff_file.pages[0].tags:
            d, n = self.tiff_file.pages[0].tags[Property.Y_RESOLUTION].value
            self.mpp.y = self.resolution_scale * n / d
        elif Property.MPP in self._properties:
            self.mpp.y = self._properties[Property.MPP]

        self.maxdimensions = IntVector.from_yx(self.tiff_file.series[0].levels[0].shape[:2])

    @property
    def mpp_x(self) -> float:
        return self.mpp.x

    @property
    def mpp_y(self) -> float:
        return self.mpp.y

    @property
    def level_count(self):
        return len(self.tiff_file.series[0].levels)

    @property
    def dimensions(self):
        return self.maxdimensions.xy

    @property
    def level_downsamples(self) -> List[int]:
        level_downsamples = []
        for level in range(len(self.tiff_file.series[0].levels)):
            y = self.tiff_file.series[0].levels[level].shape[0]
            x = self.tiff_file.series[0].levels[level].shape[1]
            dsx = self.maxdimensions.x / x
            dsy = self.maxdimensions.y / y
            # if dsx & dsy are different, it means we are not just at a downsample but at another acquisition
            # (e.g. the macro image)
            if not math.isclose(dsx, dsy, rel_tol=1e-2):
                break
            level_downsamples.append(dsy)
        return list(np.round(level_downsamples).astype("int"))

    @property
    def level_dimensions(self) -> List[Tuple[int, int]]:
        level_dimensions = []
        for level in range(len(self.tiff_file.series[0].levels)):
            y = self.tiff_file.series[0].levels[level].shape[0]
            x = self.tiff_file.series[0].levels[level].shape[1]
            dsx = self.maxdimensions.x / x
            dsy = self.maxdimensions.y / y
            if not math.isclose(dsx, dsy, rel_tol=1e-2):
                break
            level_dimensions.append((x, y))
        return level_dimensions

    def read_region(self, loc: Tuple[int, int], level: int, dimensions: Tuple[int, int]) -> np.ndarray:
        """
        Based on https://gist.github.com/rfezzani/b4b8852c5a48a901c1e94e09feb34743 by Riadh Fezzani.

        Openslide-like interface to read a region from a large TIFF without loading the
        whole image in-memory.
        :param loc: Top-left of region in level-O px coordinates (x, y)
        :param level: Level of the pyramid to use
        :param dimensions: Size in level-coordinates (width, height)
        :return: numpy array with the image
        """
        if level >= len(self.level_dimensions):
            raise ValueError(f"Level not in pyramid. Maximum level = {len(self.level_dimensions)-1}")

        page = self.tiff_file.series[0].levels[level].pages[0]
        if not page.is_tiled:
            # if not tiled: try to read everything at once...
            return self._read_region_untiled(loc, level, dimensions)

        im_width = page.imagewidth
        im_height = page.imagelength

        startx = int(loc[0] * im_width / self.maxdimensions.x)
        starty = int(loc[1] * im_height / self.maxdimensions.y)
        w, h = dimensions
        endx = startx + w
        endy = starty + h

        if h < 1 or w < 1:
            raise ValueError("h and w must be strictly positive.")

        if startx < 0 or starty < 0 or endx > im_width or endy > im_height:
            raise ValueError(
                f"Requested crop area (({startx},{starty}), ({startx+w}, {starty+h})) is out of image bounds."
            )

        tile_width, tile_height = page.tilewidth, page.tilelength

        start_tile_x = startx // tile_width
        start_tile_y = starty // tile_height
        end_tile_x = int(math.ceil(endx / tile_width))
        end_tile_y = int(math.ceil(endy / tile_height))

        tile_per_line = int(np.ceil(im_width / tile_width))

        out = np.empty(
            (
                page.imagedepth,
                (end_tile_y - start_tile_y) * tile_height,
                (end_tile_x - start_tile_x) * tile_width,
                page.samplesperpixel,
            ),
            dtype=page.dtype,
        )

        fh = page.parent.filehandle

        jpegtables = page.tags.get("JPEGTables", None)
        if jpegtables is not None:
            jpegtables = jpegtables.value

        for tile_y in range(start_tile_y, end_tile_y):
            for tile_x in range(start_tile_x, end_tile_x):
                index = int(tile_y * tile_per_line + tile_x)

                offset = page.dataoffsets[index]
                bytecount = page.databytecounts[index]

                fh.seek(offset)
                data = fh.read(bytecount)
                jpegheader = getattr(page, "jpegheader", None)
                if jpegheader is not None:
                    data = page.jpegheader + data
                tile, indices, shape = page.decode(data, index, jpegtables=jpegtables)

                im_x = (tile_x - start_tile_x) * tile_width
                im_y = (tile_y - start_tile_y) * tile_height
                out[:, im_y : im_y + tile_height, im_x : im_x + tile_width, :] = tile

        im_x0 = startx - start_tile_x * tile_width
        im_y0 = starty - start_tile_y * tile_height

        if page.imagedepth == 1:
            return out[0, im_y0 : im_y0 + h, im_x0 : im_x0 + w, :]
        return out[:, im_y0 : im_y0 + h, im_x0 : im_x0 + w, :]

    def _read_region_untiled(self, loc: Tuple[int, int], level: int, dimensions: Tuple[int, int]) -> np.ndarray:
        logging.debug("Untiled image - requires loading whole image")
        page = self.tiff_file.series[0].levels[level].pages[0]

        im_width = page.imagewidth
        im_height = page.imagelength

        startx = int(loc[0] * im_width / self.maxdimensions.x)
        starty = int(loc[1] * im_height / self.maxdimensions.y)
        w, h = dimensions
        endx = startx + w
        endy = starty + h

        if h < 1 or w < 1:
            raise ValueError("h and w must be strictly positive.")

        if startx < 0 or starty < 0 or endx > im_width or endy > im_height:
            raise ValueError(
                f"Requested crop area is out of image bounds.{startx}_{endx}_{im_height}, {starty}_{endy}_{im_width}"
            )

        return page.asarray()[0, starty:endy, startx:endx, :]

    def get_best_level_for_downsample(self, downsample: float):
        for level, ds in enumerate(self.level_downsamples):
            if ds > downsample:
                return max(0, level - 1)
        return len(self.level_downsamples) - 1

    @property
    def properties(self) -> Dict:
        return self._properties

    @property
    def associated_images(self) -> Dict[str, np.ndarray]:
        _images = {}
        for serie in self.tiff_file.series:
            if serie.name in AssociatedImages.as_list():
                _images[serie.name] = serie.pages[0].asarray()
        return _images

    def get_thumbnail(self, size: Tuple[int, int]) -> Optional[np.ndarray]:
        _images = self.associated_images
        if AssociatedImages.THUMBNAIL in _images:
            im = _images[AssociatedImages.THUMBNAIL]
            ratio = 1
            if im.shape[0] > size[1]:
                ratio = size[1] / im.shape[0]
            if im.shape[1] > size[0]:
                ratio = min(ratio, size[0] / im.shape[1])
            if ratio != 1:
                newsize = (im.shape[0] * ratio, im.shape[1] * ratio)
                im = resize(im, newsize)
            return im

        # use lowest available resolution if no thumbnail found
        im = self.tiff_file.series[0].levels[self.level_count - 1].pages[0].asarray()
        ratio = min(size[1] / im.shape[0], size[0] / im.shape[1])
        newsize = (im.shape[0] * ratio, im.shape[1] * ratio)
        return resize(im, newsize)

    def close(self):
        self.tiff_file.close()


class ImageWSI:
    """Reader class to handle non-pyramidal WSI format."""

    def __init__(self, path: str, metadata: Dict[str, Any]) -> None:
        """ImageWSI constructor.

        :param path: The path to the WSI image.
        :type path: str
        :param metadata: The metadata that complement this image. Should be provided: (i) the magnification
        level of the image (float) with the key ``mag`` and (ii) the pixel size in x and y directions (float)
        with the respective keys ``mpp_x`` and ``mpp_y``. The properties of the slide (Dict, optional) can
        also be provided with the key ``properties``, but it is not required.
        :type metadata: Dict[str, Any]
        """

        self.path = path

        self.maxdimensions = IntVector.from_xy(Image.open(path).size)

        self.mag = metadata.get("mag", 1)
        self.mpp_x = metadata.get("mpp_x", 9)
        self.mpp_y = metadata.get("mpp_y", 9)
        self.mpp = FloatVector(x=self.mpp_x, y=self.mpp_y)
        self._properties = metadata.get("properties", {})
        self.level_count = 1

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self.maxdimensions.xy

    @property
    def level_downsamples(self) -> List[int]:
        return [1]

    @property
    def level_dimensions(self) -> List[Tuple[int, int]]:
        return [self.maxdimensions.xy]

    @property
    def properties(self) -> Dict[str, Any]:
        return self._properties

    def read_region(self, loc: Tuple[int, int], level: int, dimensions: Tuple[int, int]) -> np.ndarray:
        """Openslide-like interface to read a region from a large image.

        :param loc: Top-left of region in level-O px coordinates (x, y).
        :type loc: Tuple[int, int]
        :param level: Level of the pyramid to use.
        :type level: int
        :param dimensions: Size in level-coordinates (width, height).
        :type dimensions: Tuple[int, int]
        :raises ValueError: When level required is not in the available levels.
        :return: The desired image.
        :rtype: np.ndarray
        """

        if level >= len(self.level_dimensions):
            raise ValueError(f"Level not in pyramid. Maximum level = {len(self.level_dimensions)-1}")

        out = np.array(Image.open(self.path))

        w, h = dimensions

        return out[loc[1] : loc[1] + h, loc[0] : loc[0] + w, :]

    def get_best_level_for_downsample(self, downsample: float) -> int:
        for level, ds in enumerate(self.level_downsamples):
            if ds > downsample:
                return max(0, level - 1)
        return len(self.level_downsamples) - 1

    def close(self):
        pass
