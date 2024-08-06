from django.core.exceptions import ValidationError

def file_size_5mb(value):
    limit_mb = 5
    limit_bytes = limit_mb * 10**6
    if value.size > limit_bytes:
        raise ValidationError(
            f'File too large. Size should not exceed {limit_mb} MB.')
