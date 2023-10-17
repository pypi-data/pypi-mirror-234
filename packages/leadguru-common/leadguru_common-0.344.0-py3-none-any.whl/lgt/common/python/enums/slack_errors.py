from enum import Enum


class SlackErrors(str, Enum):
    INVALID_AUTH = 'invalid_auth'
    TWO_FACTOR_REQUIRED = 'two_factor_setup_required'
