from django.shortcuts import render ,HttpResponse , redirect,get_object_or_404
from .models import Book_model
from .models import Reference  # Nomni aynan shunday yozing.
from .forms import StaffForm
from django.contrib.auth.decorators import login_required
from .forms import CostModelForm
from .forms import referenceForm 
from .forms import JobForm
from django.urls import reverse
from .forms import BookForm
from django.db.models import Q
from .forms import OutputForm
from .forms import PurchaseForm
from .forms import staff_paymentForm
from .models import Purchase
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from .models import  Staff_work
from .models import models
from .models import Reference, Book_model, Cost_Model, Output, Staff, income,Staff_payments,User,Job

@login_required
def books(request):
    return render(request, 'base.html')

def job_list(request):
    jobs = Job.objects.filter(is_deleted=False)
    return render(request, 'staff_list.html', {'jobs': jobs})


@login_required
def reference_list(request):
    reference_models = Reference.objects.filter(is_deleted=False)
    names = set()
    reference_values = dict()
    for item in reference_models:
        names.add(item.name)
        for name in names:
            if name == item.name:
                if name not in reference_values:
                    reference_values[name]= [{'id':item.id, 'value':item.value}]
                else:
                    reference_values[name].append({'id':item.id, 'value':item.value})    
    context ={
        'reference_values':reference_values
    }
    return render(request , "reference_list.html" , context=context)


@login_required
def book_list(request):
    books = Book_model.objects.filter(is_deleted=False)

    book_name = request.GET.get('book_name')
    author = request.GET.get('author')
    publish_date = request.GET.get('publish_date')

    if book_name:
        books = books.filter(name__icontains=book_name)
    if author:
        books = books.filter(author__icontains=author)
    if publish_date:
        books = books.filter(publish_date=publish_date)

    return render(request, 'book_list.html', {'books': books})

@login_required
def cost_list(request):
    costs = Cost_Model.objects.filter(is_deleted=False)

    # Filtr parametrlari
    name = request.GET.get('name', '').strip()
    category = request.GET.get('category', '').strip()
    date = request.GET.get('date', '').strip()

    # Filtr qo‘llash
    if name:
        costs = costs.filter(name__icontains=name)
    if category:
        costs = costs.filter(category__icontains=category)
    if date:
        costs = costs.filter(creat_at=date)

    return render(request, 'cost_list.html', {'costs': costs})

@login_required
def output_list(request):
    outputs = Output.objects.filter(is_deleted=False)

    # Filtr bo‘yicha qidirish
    name = request.GET.get('name')
    description = request.GET.get('description')
    date = request.GET.get('date')

    if name:
        outputs = outputs.filter(name__name__icontains=name)
    if description:
        outputs = outputs.filter(description__icontains=description)
    if date:
        outputs = outputs.filter(created_at__date=date)

    context = {
        'outputs': outputs
    }
    return render(request, 'output_list.html', context)


@login_required
def staff_list(request):
    """Hodimlar ro‘yxatini chiqarish va filtrlar bilan qidirish"""
    staff_list = Staff.objects.filter(is_deleted=False)
    # Filtrlash uchun GET parametrlarini olish
    name = request.GET.get('name', '').strip()
    gender_id = request.GET.get('gender', '').strip()  # Gender ID ni olish
    phone = request.GET.get('phone', '').strip()
    experience = request.GET.get('experience', '').strip()

    # Barcha hodimlarni olish
    staffs = Staff.objects.filter(is_deleted=False)
    
    total_balance = 0
    for staff in staff_list:
        total_balance += staff.hourly_rate

    # Filtrlash shartlari
    if name:
        staffs = staffs.filter(full_name__icontains=name)
    if gender_id:  # ForeignKey bo‘lgani uchun ID orqali filtrlash kerak
        staffs = staffs.filter(gender_id=gender_id)
    if phone:
        staffs = staffs.filter(phone_number__icontains=phone)
    if experience:
        try:
            experience = int(experience)
            staffs = staffs.filter(experience__gte=experience)
        except ValueError:
            pass  # Noto‘g‘ri qiymat kiritilsa, filtr qo‘llanmaydi

    # Hodimlarning to‘lovlari va ish ma’lumotlarini olish
    staff_payments = Staff_payments.objects.all()
    staff_jobs = Job.objects.all()
    
    
    
    
    context = {
        'staff_list': staffs,
        'staff_payment_list': staff_payments,
        'staff_jobs': staff_jobs,
        'genders': Reference.objects.all(),
        'total_balance': total_balance 
    }
    return render(request, 'staff_list.html', context)




@login_required
def add_reference(request):
    if request.method == "POST":
        forms = referenceForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(reference_list)
        
    forms = referenceForm()
    context = {
        "forms":forms
    }
    return render(request, "add_reference.html", context=context)

@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  # Hodimlar ro‘yxati sahifasiga qaytish
        else:
            print(form.errors)  # Xatolarni konsolga chiqarish
    else:
        form = StaffForm()

    return render(request, 'add_staff.html', {'form': form})

@login_required
def add_cost(request):
    if request.method == 'POST':
        form = CostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cost_list')  # Costlar ro‘yxati sahifasiga qaytaradi
    else:
        form = CostModelForm()
    return render(request, 'add_cost.html', {'form': form})


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Quantityni avtomatik 0 qilib o'rnatish
            form.cleaned_data['quantity'] = 0  # Bu yerda quantity qiymatini 0 qilib qo'yamiz
            form.save()
            return redirect('book_list')  # Kitoblar ro‘yxati sahifasiga yo‘naltirish
    else:
        form = BookForm()

    return render(request, "add_book.html", {"form": form})

@login_required
def output_create(request):
    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('output_list')
    else:
        form = OutputForm()
    return render(request, 'add_output.html', {'form': form})





@login_required
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')  # Yaratilgan sahifaga yo‘naltirish
    else:
        form = PurchaseForm()
    return render(request, 'add_purchase.html', {'form': form})



@login_required
def purchase_list(request):
    purchases = Purchase.objects.filter(is_deleted=False)

    # Filtr parametrlari
    buyer_name = request.GET.get('buyer_name', '').strip()
    book_name = request.GET.get('book_name', '').strip()
    date = request.GET.get('date', '').strip()

    # Filtrni qo‘llash
    if buyer_name:
        purchases = purchases.filter(buyer_name__icontains=buyer_name)  # buyer bo'lishi kerak
    if book_name:
        purchases = purchases.filter(book__name__icontains=book_name)  # book__name bo'lishi kerak
    if date:
        purchases = purchases.filter(purchase_date=date)

    return render(request, 'purchase_list.html', {'purchases': purchases})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')  # Login qilingandan so'ng login sahifasiga qaytadi
        else:
            messages.error(request, 'Username yoki parol noto‘g‘ri.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')










@login_required
def income_list(request):
    cost_list = Cost_Model.objects.all()
    output_list = Output.objects.all()
    payments = Staff_payments.objects.all()
    sold_books = income.objects.all()

    cost_total_sum = sum(i.price * i.quantity for i in cost_list)
    output_total_sum = sum(i.price for i in output_list)
    payment_total_sum = sum(i.price for i in payments)
    sold_book_total_sum = sum(i.price * i.quantity for i in sold_books)
    
    profit = sold_book_total_sum-(payment_total_sum+output_total_sum+cost_total_sum)

    context = {
        "cost_total_sum": cost_total_sum,
        "output_total_sum": output_total_sum,
        "payment_total_sum": payment_total_sum,
        "sold_book_total_sum": sold_book_total_sum,
        "profit":profit
    }

    return render(request, "income.html", context)
@login_required
def staff_payment_create(request):
    if request.method == "POST":
        forms = staff_paymentForm(request.POST)  # Forma `POST` ma'lumotlari bilan to‘ldiriladi
        if forms.is_valid():  # Forma yaroqli bo‘lsa, ma’lumotlar saqlanadi
            forms.save()
            return redirect("staff_list")
    else:
        forms = staff_paymentForm()  # `GET` so‘rov bo‘lsa, bo‘sh forma yaratish

    context = {
        "forms": forms  # `forms` har doim mavjud bo‘lishi kerak
    }
    return render(request, "staff_payment_create.html", context)

def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('job_list'))  # Ishlar ro‘yxatiga qaytish
    else:
        form = JobForm()

    return render(request, 'add_job.html', {'form': form})


    
    
    
    
    
    
    
    
@login_required
def update_object(request, model, model_form, pk, template_name, success_url):
    obj = get_object_or_404(model, pk=pk)
    
    if request.method == "POST":
        form = model_form(request.POST, request.FILES, instance=obj)  # ✅ request.FILES qo‘shilgan
        if form.is_valid():
            form.save()
            messages.success(request, "Ma'lumot muvaffaqiyatli yangilandi!")
            return redirect(success_url)
        else:
            print(form.errors)  # 📌 Xatolarni tekshirish uchun
    
    else:
        form = model_form(instance=obj)

    return render(request, template_name, {'form': form, 'object': obj})


# Universal Delete View (Mantiqiy o‘chirish uchun)
@login_required
def delete_object(request, model, pk, success_url):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.is_deleted = True  # Haqiqiy o‘chirish o‘rniga mantiqiy o‘chirish
        obj.save()
        messages.success(request, "Ma'lumot muvaffaqiyatli o‘chirildi!")
        return redirect(success_url)

    return render(request, "delete_confirm.html", {"object": obj})


# Har bir model uchun view funksiyalar
def update_reference(request, pk):
    return update_object(request, Reference, referenceForm, pk, "update_form.html", "reference_list")

def delete_reference(request, pk):
    return delete_object(request, Reference, pk, "reference_list")


def update_book(request, pk):
    return update_object(request, Book_model, BookForm, pk, "update_form.html", "book_list")

def delete_book(request, pk):
    return delete_object(request, Book_model, pk, "book_list")


def update_cost(request, pk):
    return update_object(request, Cost_Model, CostModelForm, pk, "update_form.html", "cost_list")

def delete_cost(request, pk):
    return delete_object(request, Cost_Model, pk, "cost_list")


def update_output(request, pk):
    return update_object(request, Output, OutputForm, pk, "update_form.html", "output_list")

def delete_output(request, pk):
    return delete_object(request, Output, pk, "output_list")


def update_staff(request, pk):
    return update_object(request, Staff, StaffForm, pk, "update_form.html", "staff_list")

def delete_staff(request, pk):
    return delete_object(request, Staff, pk, "staff_list")


#def update_staff_work(request, pk):
    return update_object(request, Staff_work, staff_paymentForm, pk, "update_form.html", "staff_work_list")

#def delete_staff_work(request, pk):
   # return delete_object(request, Staff_work, pk, "staff_work_list")


#def update_income(request, pk):
   # return update_object(request, income, Incomeform, pk, "update_form.html", "income_list")

def delete_income(request, pk):
    return delete_object(request, income, pk, "income_list")


#def update_user(request, pk):
    return update_object(request, User, UserForm, pk, "update_form.html", "user_list")

def delete_user(request, pk):
    return delete_object(request, User, pk, "user_list")


def update_purchase(request, pk):
    return update_object(request, Purchase, PurchaseForm, pk, "update_form.html", "purchase_list")

def delete_purchase(request, pk):
    return delete_object(request, Purchase, pk, "purchase_list")


def update_staff_payments(request, pk):
    return update_object(request, Staff_payments, staff_paymentForm, pk, "update_form.html", "staff_payments_list")

def delete_staff_payments(request, pk):
    return delete_object(request, Staff_payments, pk, "staff_payments_list")