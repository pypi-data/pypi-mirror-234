"""Mixin for a WorkflowDataTaskBase subclass which implements fits data retrieval functionality."""
from pathlib import Path
from typing import Generator
from typing import Iterable
from typing import Type

from astropy.io import fits

from dkist_processing_common.codecs.fits import fits_access_decoder
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.models.fits_access import FitsAccessBase

tag_type_hint = Iterable[str] | str


class FitsDataMixin:
    """Mixin for the WorkflowDataTaskBase to support fits r/w operations."""

    def fits_data_read_hdu(
        self, tags: tag_type_hint
    ) -> Generator[fits.PrimaryHDU | fits.CompImageHDU, None, None]:
        """
        Return a generator of paths and hdu lists for the input data matching the given tags.

        This method is useful for reading files that lack the header information needed to ingest them as `FitsAccess`
        objects.
        """
        yield from self.read(tags=tags, decoder=fits_hdu_decoder)

    def fits_data_read_fits_access(
        self,
        tags: tag_type_hint,
        cls: Type[FitsAccessBase],
        auto_squeeze: bool = True,
    ) -> Generator[FitsAccessBase, None, None]:
        """Return a generator of fits access objects for the input data matching the given tags."""
        yield from self.read(
            tags=tags, decoder=fits_access_decoder, fits_access_class=cls, auto_squeeze=auto_squeeze
        )

    def fits_data_write(
        self,
        hdu_list: fits.HDUList,
        tags: tag_type_hint,
        relative_path: Path | str | None = None,
        overwrite: bool = False,
    ) -> Path:
        """Write the fits object to a file with the given path and tag with the given tags."""
        return self.write(
            data=hdu_list,
            tags=tags,
            relative_path=relative_path,
            encoder=fits_hdulist_encoder,
            overwrite=overwrite,
        )
