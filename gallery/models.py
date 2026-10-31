from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    album = models.ForeignKey(
            Album,
            on_delete=models.CASCADE,
            related_name="images"
            )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    image = models.ImageField(
            upload_to="gallery/"
            )

    uploaded_at = models.DateTimeField(
            auto_now_add=True
            )

    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title
