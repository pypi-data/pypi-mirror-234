"""Support classes for manipulating wavelengths."""
import astropy.units as u
from pydantic import BaseModel
from pydantic import validator


class WavelengthRange(BaseModel):
    """Model for holding a range of wavelengths."""

    min: u.Quantity
    max: u.Quantity

    @validator("min", "max")
    def convert_to_nanometers(cls, v):
        """Validate wavelength unit is for distance and convert to nanometers."""
        return v.to(u.nm)

    @validator("max")
    def max_greater_than_min(cls, v, values):
        """Validate that the max wavelength is greater than the min wavelength."""
        max = v
        min = values["min"]
        if min > max:
            raise ValueError("min is greater than max.  Values may be reversed.")
        return v

    class Config:
        """pydantic.BaseModel configuration."""

        arbitrary_types_allowed = True
