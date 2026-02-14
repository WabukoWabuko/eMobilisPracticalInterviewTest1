from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Only process if there's an image and no thumbnail yet
        if self.image and not self.thumbnail:
            img = Image.open(self.image)
            img = img.convert('L')
            img.thumbnail((300, 300))
            temp_thumb = BytesIO()
            img.save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)
            self.thumbnail.save(f"thumb_{self.image.name}", ContentFile(temp_thumb.read()), save=False)
        super().save(*args, **kwargs)