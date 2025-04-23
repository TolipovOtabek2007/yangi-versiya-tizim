from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Create your models here.


class Reference(models.Model):
    name = models.CharField(max_length=255, verbose_name="reference nomi")
    value = models.CharField(max_length=255, verbose_name="reference qiymati")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.value


class Book_model(models.Model):
    name = models.CharField(verbose_name="Kitob nomi", max_length=255)
    category = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="book_category_references")
    price = models.FloatField(verbose_name="Kitob narxi")
    quantity = models.IntegerField(verbose_name="Kitob soni", default=0)  # boshlang'ichda 0
    image = models.ImageField(upload_to="media/", verbose_name="Kitob rasmi")
    description = models.TextField(verbose_name="Kitob haqida")
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.price}"



class Cost_Model(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Reference, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name="Cost narxi")
    quantity = models.IntegerField(verbose_name="Cost soni")
    image = models.ImageField(upload_to="media/", verbose_name="Cost rasmi")
    description = models.TextField(verbose_name="Cost haqida")
    creat_at = models.DateField(verbose_name="Cost sanasi")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.price}"


class Output(models.Model):
    name = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="output_names", verbose_name="Output nomi")
    deckripton = models.TextField(verbose_name="Tavsif")
    price = models.IntegerField(verbose_name="Narxi")
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name.name


class Staff(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Ism va familiya")
    birthday = models.DateField(null=True, blank=True)
    gender = models.ForeignKey(Reference, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, verbose_name="Telefon raqami")
    experience = models.PositiveIntegerField(verbose_name="Tajriba (yil)")
    birth_date = models.DateField(null=True, blank=True, default=timezone.now)
    hired_date = models.DateField(null=True, blank=True) 
    added_at = models.DateField()
    hourly_rate = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Job(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    hired_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff.full_name} - {self.hourly_rate} so‘m"


class Staff_work(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="book_Staff_work", verbose_name="Xodim")
    time_work = models.FloatField(verbose_name="tavsif")
    price = models.FloatField(verbose_name="Ish narxi ")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.staff.full_name


class income(models.Model):
    sold_book = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name="book_income", verbose_name="Sotilgan kitob")
    price = models.IntegerField(verbose_name="Narxi")
    quantity = models.IntegerField()
    description = models.TextField(verbose_name="Haqida")
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.sold_book.name


class SomeModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Model nomi")
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    book = models.ForeignKey(Book_model, on_delete=models.CASCADE, verbose_name="Kitob")
    buyer_name = models.CharField(max_length=255, verbose_name="Xaridor nomi")
    quantity = models.PositiveIntegerField(verbose_name="Sotib olingan miqdor")
    total_price = models.FloatField(verbose_name="Umumiy narx", editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Xarid sanasi")
    is_deleted = models.BooleanField(default=False)

    

    def __str__(self):
        return f"{self.buyer_name} - {self.book.name} ({self.quantity} dona)"
    
class Staff_payments(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
