import os
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

def make_thumbnail(dst_image_field, src_image, size, name_suffix, sep='_'):
        image = Image.open(src_image)
        image.thumbnail(size, Image.ANTIALIAS)

        dst_path, dst_ext = os.path.splitext(src_image.name)
        dst_ext = dst_ext.lower()
        dst_fname = dst_path + sep + name_suffix + dst_ext

        if dst_ext in ['.jpg', '.jpeg']:
            filetype = 'JPEG'
        elif dst_ext == '.png':
            filetype = 'PNG'
        else:
            return False
        
        dst_bytes = BytesIO()
        image.save(dst_bytes, filetype)
        dst_bytes.seek(0)

        dst_image_field.save(dst_fname, ContentFile(dst_bytes.read()), save=False)
        dst_bytes.close()