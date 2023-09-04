from django.db import models
from userauths.models import User
from app.models import Product,Variation
from userauths.models import Address
from.constant import PaymentStatus
from django.db.models import CharField
from django.utils.translation import gettext as _

# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField()
    tax=models.FloatField(null=True)
    status=models.CharField(max_length=10, choices=STATUS, default=False)
    ip =  models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    selected_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    discount=models.FloatField(null=True)
    paymenttype=models.CharField(null=True)

 
    def __str__(self):
        return self.user.first_name
    
class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE)
    ramandsize=models.CharField(max_length=20)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.product.title
    

class Razorpay_Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def _str_(self):
        return f"{self.id}-{self.name}-{self.status}"
    


   



    
