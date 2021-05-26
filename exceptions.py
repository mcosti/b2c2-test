class B2C2Exception(Exception):
    """Base class exception"""


class QuoteExpiredException(B2C2Exception):
    """The quote has expired"""


class OrderRejectedException(B2C2Exception):
    """The order has been rejected"""


class RiskExposureTooHighException(B2C2Exception):
    """Risk exposure too high"""


class MaximumQuantityExceededException(B2C2Exception):
    """Maximum quantity exceeded"""
