from abc import ABCMeta
from collections import defaultdict
from typing import Union, List, Dict, Tuple, Any, Optional
import logging

import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

from pyobs.utils.time import Time
from pyobs.interfaces import IAutoGuiding, IFitsHeaderBefore, IFitsHeaderAfter
from pyobs.images import Image
from ._base import BasePointing
from ...images.meta import PixelOffsets
from ...interfaces import ITelescope

log = logging.getLogger(__name__)


class _GuidingStatistics:
    """Calculates statistics for guiding."""

    def __init__(self):
        self._sessions: Dict[str, List[Tuple[float, float]]] = defaultdict(list)

    def reset_stats(self, client: str) -> None:
        """
        Initializes a stat measurement session for a client.

        Args:
            client: name/id of the client
        """
        if client in self._sessions:
            del self._sessions[client]

    @staticmethod
    def _calc_rms(data: List[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """Calculates RMS on data.

        Args:
            data: Data to calculate RMS for.

        Returns:
            Tuple of RMS.
        """
        if len(data) < 3:
            return None

        flattened_data = np.array(list(map(list, zip(*data))))
        data_len = len(flattened_data[0])
        rms = np.sqrt(np.sum(np.power(flattened_data, 2), axis=1) / data_len)
        return tuple(rms)

    def add_to_header(self, client: str, header: Dict[str, Any]):
        """ "Add statistics to given header.

        Args:
            client: id/name of the client
            header: Header dict to add statistics to.
        """

        # get dataset
        if client not in self._sessions:
            return
        data = self._sessions.pop(client)

        # calculate rms
        rms = self._calc_rms(data)
        if rms is not None:
            header["GUIDING RMS1"] = (float(rms[0]), "RMS for guiding on axis 1")
            header["GUIDING RMS2"] = (float(rms[1]), "RMS for guiding on axis 2")

    def add_data(self, image: Image) -> None:
        """
        Adds metadata from an image to all client measurement sessions.
        Args:
            image: Image witch metadata
        """

        # what kind of offsets do we have?
        if image.has_meta(PixelOffsets):
            # get data
            meta = image.get_meta(PixelOffsets)

            # add to all
            for k in self._sessions.keys():
                self._sessions[k].append((meta.dx, meta.dy))

        else:
            # unsupported
            log.warning("Image is missing the necessary meta information!")
            raise KeyError("Unknown meta.")


class BaseGuiding(BasePointing, IAutoGuiding, IFitsHeaderBefore, IFitsHeaderAfter, metaclass=ABCMeta):
    """Base class for guiding modules."""

    __module__ = "pyobs.modules.pointing"

    def __init__(
        self,
        max_exposure_time: Optional[float] = None,
        min_interval: float = 0,
        max_interval: float = 600,
        separation_reset: Optional[float] = None,
        pid: bool = False,
        reset_at_focus: bool = True,
        reset_at_filter: bool = True,
        **kwargs: Any,
    ):
        """Initializes a new science frame auto guiding system.

        Args:
            max_exposure_time: Maximum exposure time in sec for images to analyse.
            min_interval: Minimum interval in sec between two images.
            max_interval: Maximum interval in sec between to consecutive images to guide.
            separation_reset: Min separation in arcsec between two consecutive images that triggers a reset.
            pid: Whether to use a PID for guiding.
            reset_at_focus: Reset guiding, if focus changes.
            reset_at_filter: Reset guiding, if filter changes.
        """
        BasePointing.__init__(self, **kwargs)

        # store
        self._enabled = False
        self._max_exposure_time = max_exposure_time
        self._min_interval = min_interval
        self._max_interval = max_interval
        self._separation_reset = separation_reset
        self._pid = pid
        self._reset_at_focus = reset_at_focus
        self._reset_at_filter = reset_at_filter
        self._loop_closed = False

        # headers of last and of reference image
        self._last_header = None
        self._ref_header = None

        # stats
        self._statistics = _GuidingStatistics()

    async def start(self, **kwargs: Any) -> None:
        """Starts/resets auto-guiding."""
        log.info("Start auto-guiding...")
        await self._reset_guiding(enabled=True)

    async def stop(self, **kwargs: Any) -> None:
        """Stops auto-guiding."""
        log.info("Stopping auto-guiding...")
        await self._reset_guiding(enabled=False)

    async def is_running(self, **kwargs: Any) -> bool:
        """Whether auto-guiding is running.

        Returns:
            Auto-guiding is running.
        """
        return self._enabled

    async def get_fits_header_before(
        self, namespaces: Optional[List[str]] = None, **kwargs: Any
    ) -> Dict[str, Tuple[Any, str]]:
        """Returns FITS header for the current status of this module.

        Args:
            namespaces: If given, only return FITS headers for the given namespaces.

        Returns:
            Dictionary containing FITS headers.
        """

        # reset statistics
        self._statistics.reset_stats(kwargs["sender"])

        # state
        state = "GUIDING_CLOSED_LOOP" if self._loop_closed else "GUIDING_OPEN_LOOP"

        # return header
        return {"AGSTATE": (state, "Autoguider state")}

    async def get_fits_header_after(
        self, namespaces: Optional[List[str]] = None, **kwargs: Any
    ) -> Dict[str, Tuple[Any, str]]:
        """Returns FITS header for the current status of this module.

        Args:
            namespaces: If given, only return FITS headers for the given namespaces.

        Returns:
            Dictionary containing FITS headers.
        """

        # state
        state = "GUIDING_CLOSED_LOOP" if self._loop_closed else "GUIDING_OPEN_LOOP"
        hdr = {"AGSTATE": (state, "Autoguider state")}

        # add statistics
        self._statistics.add_to_header(kwargs["sender"], hdr)

        # finished
        return hdr

    async def _reset_guiding(self, enabled: bool = True, image: Optional[Union[Image, None]] = None) -> None:
        """Reset guiding.

        Args:
            image: If given, new reference image.
        """
        self._enabled = enabled
        self._loop_closed = False
        self._ref_header = None if image is None else image.header
        self._last_header = None if image is None else image.header

        # reset offset
        await self.reset_pipeline()
        if image is not None:
            # if image is given, process it
            await self.run_pipeline(image)

    async def _process_image(self, image: Image) -> Optional[Image]:
        """Processes a single image and offsets telescope.

        Args:
            image: Image to process.
        """

        # not enabled?
        if not self._enabled:
            return None

        # we only accept OBJECT images
        if image.header["IMAGETYP"] not in ["object", "guiding"]:
            return None

        # reference header?
        if self._ref_header is None:
            log.info("Setting new reference image...")
            await self._reset_guiding(image=image)
            return None

        # check RA/Dec in header and separation
        c1 = SkyCoord(ra=image.header["TEL-RA"] * u.deg, dec=image.header["TEL-DEC"] * u.deg, frame="icrs")
        c2 = SkyCoord(ra=self._ref_header["TEL-RA"] * u.deg, dec=self._ref_header["TEL-DEC"] * u.deg, frame="icrs")
        separation = c1.separation(c2).deg
        if self._separation_reset is not None and separation * 3600.0 > self._separation_reset:
            log.warning(
                'Nominal position of reference and new image differ by %.2f", resetting reference...',
                separation * 3600.0,
            )
            await self._reset_guiding(image=image)
            return None

        # check filter
        if (
            self._reset_at_filter
            and "FILTER" in image.header
            and "FILTER" in self._ref_header
            and image.header["FILTER"] != self._ref_header["FILTER"]
        ):
            log.warning("The filter has been changed since the last exposure, resetting reference...")
            await self._reset_guiding(image=image)
            return None

        # get time
        date_obs = Time(image.header["DATE-OBS"])

        # check times and focus
        if self._last_header is not None:
            # check times
            t0 = Time(self._last_header["DATE-OBS"])
            if (date_obs - t0).sec > self._max_interval:
                log.warning("Time between current and last image is too large, resetting reference...")
                await self._reset_guiding(image=image)
                return None
            if (date_obs - t0).sec < self._min_interval:
                log.warning("Time between current and last image is too small, ignoring image...")
                return None

            # check focus
            if (
                "TEL-FOCU" in image.header
                and self._reset_at_focus
                and abs(image.header["TEL-FOCU"] - self._last_header["TEL-FOCU"]) > 0.05
            ):
                log.warning("Focus difference between current and last image is too large, resetting reference...")
                await self._reset_guiding(image=image)
                return None

        # exposure time too large?
        if self._max_exposure_time is not None and image.header["EXPTIME"] > self._max_exposure_time:
            log.warning("Exposure time too large, skipping auto-guiding for now...")
            self._loop_closed = False
            return None

        # remember header
        self._last_header = image.header

        # get offset
        image = await self.run_pipeline(image)

        # update guiding stat
        self._statistics.add_data(image)

        # get telescope
        try:
            telescope = await self.proxy(self._telescope, ITelescope)
        except ValueError:
            log.error("Given telescope does not exist or is not of correct type.")
            self._loop_closed = False
            return image

        # apply offsets
        try:
            if await self._apply(image, telescope, self.location):
                self._loop_closed = True
                log.info("Finished image.")
            else:
                log.info("Could not apply offsets.")
                self._loop_closed = False
        except ValueError as e:
            log.info("Could not apply offsets: %s", e)
            self._loop_closed = False

        # return image, in case we added important data
        return image


__all__ = ["BaseGuiding"]
