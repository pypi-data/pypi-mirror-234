"""JSON encoders to support quality reporting."""
import json
from datetime import datetime
from typing import Any

import numpy as np


class QualityReportEncoder(json.JSONEncoder):
    """A JSON encoder for the quality report create->format interface which encodes datetimes as iso formatted strings."""

    def default(self, obj):
        """Implement the default method required to subclass the encoder."""
        if isinstance(obj, datetime):
            return {"iso_date": obj.isoformat("T")}
        return super().default(obj)


class QualityValueEncoder(json.JSONEncoder):
    """
    A JSON encoder for the quality report distributed value storage -> report build interface.

    Currently, a placeholder for future serializations e.g. NaN,-Inf,+Inf
    """

    def default(self, obj: Any) -> Any:
        """Implement an encoder that correctly handles numpy float32 data."""
        # np.float32 is only for single values. Even an array of np.float32 objects is a np.ndarray
        if isinstance(obj, np.float32):
            return float(obj)
        return super().default(obj)
