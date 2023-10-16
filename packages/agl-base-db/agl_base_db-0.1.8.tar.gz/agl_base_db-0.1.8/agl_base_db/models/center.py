from django.db import models

class CenterManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Center(models.Model):
    import_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    name_de = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)