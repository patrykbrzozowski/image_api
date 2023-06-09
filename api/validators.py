import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']

    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in valid_extensions:
        raise ValidationError({"message": "Unsupported file extension."})