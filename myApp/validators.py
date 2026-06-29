from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit = 1 * 1024 * 1024  # 1 MB
    if value.size > limit:
        raise ValidationError('File size must be under 1 MB.')
