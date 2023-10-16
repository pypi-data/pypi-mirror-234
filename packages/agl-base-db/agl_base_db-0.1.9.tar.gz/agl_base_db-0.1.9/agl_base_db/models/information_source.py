from django.db import models

class InformationSourceManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class InformationSource(models.Model):
    objects = InformationSourceManager()

    name = models.CharField(max_length=100)
    name_de = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
