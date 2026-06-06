from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

RESERVED_USERNAMES = {
    "admin",
    "api",
    "logged_user",
    "settings",
    "notifications",
}

username_validator = RegexValidator(
    regex=r'^[a-z0-9_]+$',
    message='Only lowercase letters, numbers and underscores allowed.'
)

def validate_reserved_username(value):
    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError("This username is reserved.")
