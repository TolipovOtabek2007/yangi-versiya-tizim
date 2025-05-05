

from django.db.models.signals import post_save, post_delete

from .models import Cost_Model, Book_model

from django.dispatch import receiver
from .models import Cost_Model, income, Book_model

@receiver([post_delete, post_save], sender=Cost_Model)
@receiver([post_delete, post_save], sender=income)
def signal_cost_quantity(sender, instance, **kwargs):
    try:
        cost = Cost_Model.objects.filter(name__name=instance.name)
        book = Book_model.objects.get(name=instance.name)
        iincome = income.objects.filter(sold_book__name=instance.name)
    except:
        cost = Cost_Model.objects.filter(name__name=instance.sold_book)
        book = Book_model.objects.get(name=instance.sold_book)
        iincome = income.objects.filter(sold_book__name=instance.sold_book)

    cost_book_quantity = 0
    sold_book_quantity = 0

    for i in cost:
        cost_book_quantity += i.quantity

    for i in iincome:
        sold_book_quantity += i.quantity

    book.quantity = cost_book_quantity - sold_book_quantity
    book.save()
