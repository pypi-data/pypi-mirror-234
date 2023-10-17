"""Task(s) for writing level 1 data as 214 compliant fits files."""
import importlib
import logging
import uuid
from abc import ABC
from abc import abstractmethod
from functools import cached_property
from pathlib import Path
from typing import Literal

import astropy.units as u
import numpy as np
from astropy.io import fits
from astropy.time import Time
from dkist_fits_specifications import __version__ as spec_version
from dkist_fits_specifications.utils.formatter import reformat_spec214_header
from dkist_header_validator import spec214_validator
from dkist_header_validator.translator import remove_extra_axis_keys
from dkist_header_validator.translator import sanitize_to_spec214_level1
from dkist_spectral_lines.search import get_closest_spectral_line
from dkist_spectral_lines.search import get_spectral_lines
from scipy.stats import kurtosis
from scipy.stats import skew
from sunpy.coordinates import HeliocentricInertial

from dkist_processing_common._util.dkist_location import location_of_dkist
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.models.wavelength import WavelengthRange
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.tasks import WorkflowTaskBase

logger = logging.getLogger(__name__)

__all__ = ["WriteL1Frame"]

from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.metadata_store import MetadataStoreMixin


class WriteL1Frame(WorkflowTaskBase, FitsDataMixin, MetadataStoreMixin, ABC):
    """
    Task to convert final calibrated science frames into spec 214 compliant level 1 frames.

    It is intended to be subclassed as the dataset header table is instrument specific.
    """

    def run(self) -> None:
        """Run method for this task."""
        for stokes_param in self.constants.stokes_params:
            with self.apm_task_step(f"Get calibrated frames for stokes param {stokes_param}"):
                tags = [Tag.frame(), Tag.calibrated(), Tag.stokes(stokes_param)]
                calibrated_fits_objects = self.fits_data_read_fits_access(
                    tags=tags,
                    cls=L0FitsAccess,
                    auto_squeeze=False,
                )
                num_files = self.scratch.count_all(tags)

            for file_num, calibrated_fits_object in enumerate(calibrated_fits_objects, start=1):
                # Convert the headers to L1
                l1_header = self.convert_l0_to_l1(
                    header=calibrated_fits_object.header,
                    data=calibrated_fits_object.data,
                    hdu_size=calibrated_fits_object.size,
                    stokes_param=stokes_param,
                )

                # Get the tile size to use for compression. None means use astropy defaults
                tile_size = self._get_tile_size(calibrated_fits_object.data)
                # Write frame to disk - compressed
                hdu = fits.CompImageHDU(
                    header=l1_header, data=calibrated_fits_object.data, tile_shape=tile_size
                )
                formatted_header = reformat_spec214_header(hdu.header)
                hdu = fits.CompImageHDU(
                    header=formatted_header, data=hdu.data, tile_shape=tile_size
                )
                all_tags = self.tags(calibrated_fits_object.name)
                all_tags.remove(Tag.calibrated())
                relative_path = self.l1_filename(header=l1_header, stokes=stokes_param)
                temp_file_name = Path(calibrated_fits_object.name).name
                logger.debug(
                    f"{file_num} of {num_files}: Translate and write frame {temp_file_name} to {relative_path}"
                )
                self.fits_data_write(
                    hdu_list=fits.HDUList([fits.PrimaryHDU(), hdu]),
                    tags=[Tag.output()] + all_tags,
                    relative_path=relative_path,
                )
                # Check that the written file passes spec 214 validation if requested
                if self.validate_l1_on_write:
                    spec214_validator.validate(self.scratch.absolute_path(relative_path))

    @cached_property
    def _tile_size_param(self) -> int:
        return self.metadata_store_recipe_run_configuration().get("tile_size", None)

    @cached_property
    def validate_l1_on_write(self) -> bool:
        """Check for validate on write."""
        return self.metadata_store_recipe_run_configuration().get("validate_l1_on_write", True)

    def _get_tile_size(self, data: np.ndarray) -> list | None:
        if self._tile_size_param is None:
            return None
        tile_size = []
        for dim_size in data.shape:
            if dim_size < self._tile_size_param:
                tile_size.append(dim_size)
            else:
                tile_size.append(self._tile_size_param)
        return tile_size

    def _replace_header_values(self, header: fits.Header, data: np.ndarray) -> fits.Header:
        """Replace header values that should already exist with new values."""
        header["FILE_ID"] = uuid.uuid4().hex
        header["DATE"] = Time.now().fits
        # Remove BZERO and BSCALE as their value should be recalculated by astropy upon fits write
        header.pop("BZERO", None)
        header.pop("BSCALE", None)
        # Make sure that NAXIS is set to the shape of the data in case of squeezing
        header["NAXIS"] = len(data.shape)
        # The HLSVERS keyword was added after data was ingested into the data stores. This means
        # it isn't guaranteed to exist in all L0 data to be copied to the L1 data. This next line
        # ensures a copy will be made
        header["HLSVERS"] = header["ID___014"]
        header["DATE-END"] = self._calculate_date_end(header=header)
        return header

    @staticmethod
    def _add_stats_headers(header: fits.Header, data: np.ndarray) -> fits.Header:
        """Fill out the spec 214 statistics header table."""
        data = data.flatten()
        percentiles = np.nanpercentile(data, [1, 10, 25, 75, 90, 95, 98, 99])
        header["DATAMIN"] = np.nanmin(data)
        header["DATAMAX"] = np.nanmax(data)
        header["DATAMEAN"] = np.nanmean(data)
        header["DATAMEDN"] = np.nanmedian(data)
        header["DATA01"] = percentiles[0]
        header["DATA10"] = percentiles[1]
        header["DATA25"] = percentiles[2]
        header["DATA75"] = percentiles[3]
        header["DATA90"] = percentiles[4]
        header["DATA95"] = percentiles[5]
        header["DATA98"] = percentiles[6]
        header["DATA99"] = percentiles[7]
        header["DATARMS"] = np.sqrt(np.nanmean(data**2))
        header["DATAKURT"] = kurtosis(data, nan_policy="omit")
        header["DATASKEW"] = skew(data, nan_policy="omit")
        return header

    def _add_datacenter_headers(
        self,
        header: fits.Header,
        hdu_size: float,
        stokes: Literal["I", "Q", "U", "V"],
    ) -> fits.Header:
        """Fill out the spec 214 datacenter header table."""
        header["DSETID"] = self.constants.dataset_id
        header["POINT_ID"] = self.constants.dataset_id
        header["FRAMEVOL"] = hdu_size / 1024 / 1024
        header["PROCTYPE"] = "L1"
        header["RRUNID"] = self.recipe_run_id
        header["RECIPEID"] = self.metadata_store_recipe_id
        header["RINSTID"] = self.metadata_store_recipe_instance_id
        header["EXTNAME"] = "observation"
        header["SOLARNET"] = 1
        header["OBS_HDU"] = 1
        header["FILENAME"] = self.l1_filename(header=header, stokes=stokes)
        # Cadence keywords
        header["CADENCE"] = self.constants.average_cadence
        header["CADMIN"] = self.constants.minimum_cadence
        header["CADMAX"] = self.constants.maximum_cadence
        header["CADVAR"] = self.constants.variance_cadence
        # Keywords to support reprocessing
        if ids_par_id := self.metadata_store_input_dataset_parameters_part_id:
            header["IDSPARID"] = ids_par_id
        if ids_obs_id := self.metadata_store_input_dataset_observe_frames_part_id:
            header["IDSOBSID"] = ids_obs_id
        if ids_cal_id := self.metadata_store_input_dataset_calibration_frames_part_id:
            header["IDSCALID"] = ids_cal_id
        header["WKFLNAME"] = self.workflow_name
        header["WKFLVERS"] = self.workflow_version
        header = self._add_contributing_id_headers(header=header)
        # Spectral line keywords
        wavelength_range = self.get_wavelength_range(header=header)
        spectral_lines = get_spectral_lines(
            wavelength_min=wavelength_range.min,
            wavelength_max=wavelength_range.max,
        )
        if spectral_lines:
            header["NSPECLNS"] = len(spectral_lines)
            for i, l in enumerate(spectral_lines):
                header[f"SPECLN{str(i + 1).zfill(2)}"] = l.name
        return header

    @abstractmethod
    def get_wavelength_range(self, header: fits.Header) -> WavelengthRange:
        """
        Determine the wavelength range covered by the data in this frame.

        For imagers, this is generally the wavelengths covered by the filter.
        For spectrographs, this is the wavelengths covered by the spectral axis of the data.
        """

    def _add_solarnet_headers(self, header: fits.Header) -> fits.Header:
        """Add headers recommended by solarnet that haven't already been added."""
        header["DATE-AVG"] = self._calculate_date_avg(header=header)
        header["TELAPSE"] = self._calculate_telapse(header=header)
        header["DATEREF"] = header["DATE-BEG"]
        itrs = location_of_dkist()
        header["OBSGEO-X"] = itrs.x.to_value(unit=u.m)
        header["OBSGEO-Y"] = itrs.y.to_value(unit=u.m)
        header["OBSGEO-Z"] = itrs.z.to_value(unit=u.m)
        header["OBS_VR"] = (
            itrs.get_gcrs(obstime=Time(header["DATE-AVG"]))
            .transform_to(HeliocentricInertial(obstime=Time(header["DATE-AVG"])))
            .d_distance.to_value(unit=u.m / u.s)
        )  # relative velocity of observer with respect to the sun in m/s
        header["SPECSYS"] = "TOPOCENT"  # no wavelength correction made due to doppler velocity
        header["VELOSYS"] = 0.0  # no wavelength correction made due to doppler velocity
        header["WAVEBAND"] = get_closest_spectral_line(wavelength=header["LINEWAV"] * u.nm).name
        wavelength_range = self.get_wavelength_range(header=header)
        header["WAVEMIN"] = wavelength_range.min.to_value(u.nm)
        header["WAVEMAX"] = wavelength_range.max.to_value(u.nm)
        return header

    def l1_filename(self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]):
        """
        Use a FITS header to derive its filename in the following format.

        instrument_datetime_wavelength__stokes_datasetid_L1.fits.

        Example
        -------
        "VISP_2020_03_13T00_00_00_000_01080000_Q_DATID_L1.fits"

        Parameters
        ----------
        header
            The input fits header
        stokes
            The stokes parameter

        Returns
        -------
        The L1 filename
        """
        instrument = header["INSTRUME"]
        wavelength = str(round(header["LINEWAV"] * 1000)).zfill(8)
        datetime = header["DATE-BEG"].replace("-", "_").replace(":", "_").replace(".", "_")
        return f"{instrument}_{datetime}_{wavelength}_{stokes}_{self.constants.dataset_id}_L1.fits"

    @staticmethod
    def _calculate_date_avg(header: fits.Header) -> str:
        """Given the start and end datetimes of observations, return the datetime exactly between them."""
        start_time = Time(header["DATE-BEG"], format="isot", precision=6)
        end_time = Time(header["DATE-END"], format="isot", precision=6)
        time_diff = end_time - start_time
        return (start_time + (time_diff / 2)).to_value("isot")

    @staticmethod
    def _calculate_telapse(header: fits.Header) -> float:
        """Given the start and end time of observation, calculate the time elapsed, in seconds."""
        start_time = Time(header["DATE-BEG"], format="isot", precision=6).to_value("mjd")
        end_time = Time(header["DATE-END"], format="isot", precision=6).to_value("mjd")
        return (end_time - start_time) * 86400  # seconds in a day

    def convert_l0_to_l1(
        self,
        header: fits.Header,
        data: np.ndarray,
        hdu_size: float,
        stokes_param: Literal["I", "Q", "U", "V"],
    ) -> fits.Header:
        """
        Run through the steps needed to convert a L0 header into a L1 header.

        Parameters
        ----------
        header
            The L0 header
        data
            The data array
        hdu_size
            The hdu size
        stokes_param
            The stokes parameter

        Returns
        -------
        A header translated to L1
        """
        # Replace header values in place
        header = self._replace_header_values(header=header, data=data)
        # Add the stats table
        header = self._add_stats_headers(header=header, data=data)
        # Add the datacenter table
        header = self._add_datacenter_headers(header=header, hdu_size=hdu_size, stokes=stokes_param)
        # Add extra headers recommended by solarnet (not all in a single table)
        header = self._add_solarnet_headers(header=header)
        # Add the documentation headers
        header = self._add_doc_headers(header=header)
        # Add the dataset headers (abstract - implement in instrument task)
        header = self.add_dataset_headers(header=header, stokes=stokes_param)
        # Remove any headers not contained in spec 214
        header = sanitize_to_spec214_level1(input_headers=header)
        # Remove any keys referring to axes that don't exist
        header = remove_extra_axis_keys(input_headers=header)
        return header

    def _add_doc_headers(self, header: fits.Header) -> fits.Header:
        """
        Add URLs to the headers that point to the correct versions of documents in our public documentation.

        Parameters
        ----------
        header
            The FITS header to which the doc headers is to be added
        Returns
        -------
        None

        Header values follow these rules:
            1. header['INFO_URL']:
                The main documentation site: docs.dkist.nso.edu
            2. header['HEADVERS']:
                The version of the DKIST FITS specs used for this calibration:
                dkist_fits_specifications.__version__
            3. header['HEAD_URL']:
                The URL for the documentation of this version of the DKIST fits specifications:
                docs.dkist.nso.edu/projects/data-products/en/v<version> where <version> is header['HEADVERS']
            4. header['CALVERS']:
                The version of the calibration codes used for this calibration
                dkist_processing_<instrument>.__version__
                <instrument> is available as self.constants.instrument
            5. header['CAL_URL']:
                The URL for the documentation of this version of the calibration codes for
                the current instrument and workflow being executed
                docs.dkist.nso.edu/projects/<instrument>/en/v<version>/<workflow_name>.html
        """
        header["INFO_URL"] = self.docs_base_url
        header["HEADVERS"] = spec_version
        header["HEAD_URL"] = f"{self.docs_base_url}/projects/data-products/en/v{spec_version}"
        inst_name = self.constants.instrument.lower()
        calvers = self._get_version_from_module_name()
        header["CALVERS"] = calvers
        header[
            "CAL_URL"
        ] = f"{self.docs_base_url}/projects/{inst_name}/en/v{calvers}/{self.workflow_name}.html"
        return header

    def _get_version_from_module_name(self) -> str:
        """
        Get the value of __version__ from a module given its name.

        Returns
        -------
        The value of __version__
        """
        package = self.__module__.split(".")[0]
        module = importlib.import_module(package)
        return module.__version__

    @abstractmethod
    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        """
        Abstract method to be implemented in the instrument repos.

        Construction of the dataset object is instrument, or possibly instrument mode specific.

        Parameters
        ----------
        header
            The input fits header
        stokes
            The stokes parameter

        Returns
        -------
        The input header updated with the addition of the data set headers
        """

    @abstractmethod
    def _calculate_date_end(self, header: fits.Header) -> str:
        """
        Calculate the instrument specific version of the "DATE-END" keyword.

        This abstract method forces each instrument pipeline to consider the implementation of the
        DATE-END calculation.

        Parameters
        ----------
        header
            The input fits header

        Returns
        -------
        The isot formatted string of the DATE-END keyword value
        """

    def _add_contributing_id_headers(self, header: fits.Header) -> fits.Header:
        """Add headers for contributing proposal and experiment IDs."""
        # contributing proposal ID headers
        for i, contributing_proposal_id in enumerate(
            self.constants.contributing_proposal_ids, start=1
        ):
            header[f"PROPID{str(i).zfill(2)}"] = contributing_proposal_id
        header["NPROPOS"] = len(self.constants.contributing_proposal_ids)
        # contributing experiment ID headers
        for i, contributing_experiment_id in enumerate(
            self.constants.contributing_experiment_ids, start=1
        ):
            header[f"EXPRID{str(i).zfill(2)}"] = contributing_experiment_id
        header["NEXPERS"] = len(self.constants.contributing_experiment_ids)
        return header
