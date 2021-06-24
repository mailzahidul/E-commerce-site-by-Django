from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

DISTRICT_CHOICE = (
    ('dhaka', 'Dhaka'),
    ('borishal', 'Borishal'),
    ('jessor', 'Jessor'),
    ('khulna', 'Khulna'),
    ('rajshahi', 'Rajshahi'),
    ('sylet', 'Sylet'),
    ('rongpur', 'Rongpur'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(default='+8841524204242')
    email = models.EmailField(default='yourmailaddress@yourserver.com')
    address = models.CharField(max_length=200)
    district = models.CharField(choices=DISTRICT_CHOICE, max_length=30)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.name




CATEGORY_CHOICE = (
    ('mobile', 'Mobile'),
    ('laptop', 'Laptop'),
    ('top_wear', 'Top Wear'),
    ('bottom_wear', 'Bottom Wear'),
)

BRAND_CHOICE = (
    ('samsung', 'Samsung'),
    ('apple', 'Laptop'),
    ('redme', 'Redme'),
)


class Product(models.Model):
    title = models.CharField(max_length=200)
    product_code = models.CharField(max_length=200, blank=False, unique=True)
    quantity = models.PositiveIntegerField(default=10)
    selling_price = models.FloatField()
    discount_price = models.FloatField(default=0)
    description = models.TextField()
    brand = models.CharField(choices=BRAND_CHOICE,max_length=20)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=20)
    product_img = models.ImageField(upload_to='product_img/')

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


STATUS_CHOICE = (
    ('accepted', 'Accepted'),
    ('packed', 'Packed'),
    ('on the way', 'On the way'),
    ('delivered', 'Delivered'),
    ('cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_auto_now = models.DateTimeField(auto_now=True)
    date_auto_now_add = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default="Pending" )

    def __str__(self):
        return self.customer.name

    @property
    def total_cost(self):
        return self.product.selling_price * self.quantity

PAYMENT_CHOICE = (
    ('cash on deliver', 'Cash On Deliver'),
    ('bkash', 'Bkash'),
    ('visa', 'Visa Cart')
)

class Mulytic_labs_test(models.Model):
    customer_name = models.CharField(max_length=200)
    phone = PhoneNumberField()
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICE, default="bkash")
    order_time = models.DateTimeField(default=now)
    qr_code = models.ImageField(upload_to='media/qr_code/', blank=True)

    def __str__(self):
        return str(self.customer_name)

    # def save(self, *args, **kwargs):
    #     qrcode_img = qrcode.make(self.name+self.order_time)
    #     canvas = Image.new('RGB', (290, 290), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'qr_code-{self.name+self.order_time}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)
