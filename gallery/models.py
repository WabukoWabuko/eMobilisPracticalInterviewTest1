from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='original_photos/')
    # We will store the manipulated version here too
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Inside the Photo class:
    def save(self, *args, **kwargs):
        if self.image:
            # 1. Open the uploaded image
            img = Image.open(self.image)

            # 2. Perform manipulation (e.g., Grayscale + Resize)
            img = img.convert('L')  # Convert to Grayscale
            img.thumbnail((300, 300))  # Resize

            # 3. Save the manipulated image to a buffer
            temp_thumb = BytesIO()
            img.save(temp_thumb, format='JPEG')
            temp_thumb.seek(0)

            # 4. Save to the thumbnail field without calling save() recursively
            self.thumbnail.save(f"thumb_{self.image.name}", ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

        super().save(*args, **kwargs)