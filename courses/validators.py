from django.core.exceptions import ValidationError
import os

def validate_file_size(file):
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024

    if file.size > max_size_bytes:
        raise ValidationError(f'File size must be less than {max_size_mb}MB!')

def validate_image_file(file):
    ext = os.path.splitext(file.name)[1].lower()

    valid_extensions = ['.png', '.jpg', '.jpeg']

    if ext not in valid_extensions:
        raise ValidationError(f'Invalid file type. Allowed: {" ".join(valid_extensions)}')

def validate_video_url(value):
    allowed_url = False
    allowed_domains = ['youtube.com']

    for domain in allowed_domains:
        if domain in value.lower():
            allowed_url = True

    if not allowed_url:
        raise ValidationError('Only youtube urls are allowed!')
    
def validate_document_file(file):
    ext = os.path.splitext(file.name)[1].lower()

    valid_extensions = ['.pdf', '.doc', '.docx', '.txt']

    if ext not in valid_extensions:
        raise ValidationError(f'Invalid file type. Allowed: {" ".join(valid_extensions)}')