from django.db import models

class ContactInfo(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    heading = models.CharField(max_length=150, default="Contact info")
    introduction = models.TextField(blank=True, help_text="Welcome visitors and describe the enquiries you accept, such as commissions or exhibitions.")
    email = models.EmailField(blank=True, help_text="Public email address for art enquiries.")
    phone = models.CharField(max_length=50, blank=True, help_text="Optional public phone number.")
    studio_details = models.TextField("Studio location and visiting information", blank=True, help_text="Only include an address or visiting hours you want to share publicly.")
    website_label = models.CharField("Link label", max_length=100, blank=True, help_text="For example: Instagram or Online shop.")
    website_url = models.URLField("Link address", blank=True)

    class Meta:
        verbose_name = "Contact information"
        verbose_name_plural = "Contact information"
        constraints = [models.CheckConstraint(condition=models.Q(id=1), name="single_contact_info")]

    def __str__(self):
        return self.heading
