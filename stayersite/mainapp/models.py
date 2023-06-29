from django.db import models

class furniture_types(models.Model):
    type_name = models.CharField(max_length=64,
                            verbose_name='Типы мебели')

class furniture(models.Model):
    type = models.ForeignKey(furniture_types,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=255,
                            verbose_name='Название')
    height = models.PositiveIntegerField(verbose_name='Высота',
                                         blank=True,
                                         null=True)
    width = models.PositiveIntegerField(verbose_name='Ширина',
                                         blank=True,
                                         null=True)
    color = models.CharField(max_length=64,
                             verbose_name='Цвет',
                             blank=True)
    price = models.DecimalField(verbose_name='Цена',
                                max_digits=8,
                                decimal_places=2,
                                default=0)
    image = models.ImageField(upload_to='furniture_images', blank=True)
