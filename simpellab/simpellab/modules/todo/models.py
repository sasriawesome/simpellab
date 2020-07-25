from django.db import models
from simpellab.core.models import BaseModel
from .workers import send_email
from polymorphic.models import PolymorphicModel

class Work(BaseModel):

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'
    
    title = models.CharField(max_length=250)
    score = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @staticmethod
    def send_email(recipient, message):
        try:
            send_email(recipient, message)
            return True
        except Exception as err:
            print(err)
            return False


class Note(BaseModel):

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Note'
    
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.title



class Produk(PolymorphicModel):

    name = models.CharField(max_length=100)


class Persediaan(Produk):

    minimum_stock = models.IntegerField()


class Asset(Produk):

    minimum_stock = models.IntegerField()
    price = models.IntegerField()


class Jasa(Produk):

    vendor = models.CharField(max_length=100)


class JasaLaboratorium(Jasa):

    parameter = models.CharField(max_length=100)


class JasaIspeksi(Jasa):

    parameter = models.CharField(max_length=100)


class JasaPelatihan(Jasa):

    materi = models.CharField(max_length=100)


class Order(models.Model):

    order_name = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=False)

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item_name = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=False)

class OrderItemFee(models.Model):

    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    extra_fee = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=False)