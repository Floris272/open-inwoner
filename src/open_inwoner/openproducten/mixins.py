from django.db import models


class OpenProductenMixin(models.Model):
    open_producten_uuid = models.UUIDField(unique=True, editable=False, null=True)

    class Meta:
        abstract = True
