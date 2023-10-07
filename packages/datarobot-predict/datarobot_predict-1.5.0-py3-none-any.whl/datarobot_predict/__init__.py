import enum


class TimeSeriesType(enum.Enum):
    FORECAST = 1
    """Forecast point predictions"""

    HISTORICAL = 2
    """Historical predictions"""
