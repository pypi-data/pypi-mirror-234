from django.db import models
from django.utils.text import slugify

class GenericSimpleModel(models.Model):
    nome = models.CharField(
        max_length=200
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
        ordering = ['slug']

    def __str__(self):
        return f"{self.nome}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(f"{self.nome}")
        super().save(*args, **kwargs)

