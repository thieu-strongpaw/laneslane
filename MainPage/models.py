from django.db import models


class ArtistProfile(models.Model):
    id = models.PositiveSmallIntegerField(
            primary_key=True,
            default=1,
            editable=False,
            )

    title = models.CharField(
            max_length=150
            )

    description = models.TextField()

    main_image = models.ImageField(
            upload_to="profiles/"
            )

    class Meta:
        verbose_name = "Artist Profile"
        constraints = [
                models.CheckConstraint(
                    condition=models.Q(id=1),
                    name="single_artist_profile"
                    )
                ]

    def __str_(self):
        return self.title

class Spotlight(models.Model):
    profile = models.ForeignKey(
            ArtistProfile,
            on_delete=models.CASCADE,
            related_name="spotlight"
            )

    title = models.CharField(
            max_length=150
            )

    image = models.ImageField(
            upload_to="spotlight/"
            )

    description = models.TextField(
            max_length=800,
            help_text="A short, one-ish-paragraph description.",
            )

    is_public = models.BooleanField(
            default=False,
            )

    display_order = models.PositiveSmallIntegerField(
            default=0,
            )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title
