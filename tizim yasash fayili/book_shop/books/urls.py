from django.urls import path
from . import views
from .views import (
    update_reference, delete_reference, 
    update_book, delete_book, 
    update_cost, delete_cost,
    update_output, delete_output,
    update_staff, delete_staff,
    #update_staff_work, delete_staff_work,
    #update_income, delete_income,
    #update_user, delete_user,
    update_purchase, delete_purchase,
    update_staff_payments, delete_staff_payments
)


urlpatterns = [
    path('shablon/', views.books, name='books'),
 
    path('references/', views.reference_list, name='reference_list'),
    path('references/add/', views.add_reference, name='add_reference'),
    #book
    path('', views.book_list, name='book_list'),
    
    path('book/add/', views.add_book, name='add_book'),
    #cost
    path('costs/', views.cost_list, name='cost_list'),
    path('cost/add/', views.add_cost, name='add_cost'),
    #seff
    path('add_job/', views.add_job, name='add_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('staffs/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
   
    path('staff_payment_create/', views.staff_payment_create, name='staff_payment_create'),
    #outputs
    path('outputs/', views.output_list, name='output_list'),
    path('outut/add/', views.output_create, name='add_output'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('purchase/', views.purchase_list, name='purchase_list'),
    
    #daromad
    path('incomes/', views.income_list, name='income_list'),
    #logn
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # taxrirlash va o'chirish

    path('reference/update/<int:pk>/', update_reference, name='update_reference'),
    path('reference/delete/<int:pk>/', delete_reference, name='delete_reference'),

    path('book/update/<int:pk>/', update_book, name='update_book'),
    path('book/delete/<int:pk>/', delete_book, name='delete_book'),

    path('cost/update/<int:pk>/', update_cost, name='update_cost'),
    path('cost/delete/<int:pk>/', delete_cost, name='delete_cost'),

    path('output/update/<int:pk>/', update_output, name='update_output'),
    path('output/delete/<int:pk>/', delete_output, name='delete_output'),

    path('staff/update/<int:pk>/', update_staff, name='update_staff'),
    path('staff/delete/<int:pk>/', delete_staff, name='delete_staff'),

    #path('staff_work/update/<int:pk>/', update_staff_work, name='update_staff_work'),
    #path('staff_work/delete/<int:pk>/', delete_staff_work, name='delete_staff_work'),

    #path('income/update/<int:pk>/', update_income, name='update_income'),
    #path('income/delete/<int:pk>/', delete_income, name='delete_income'),

    #path('user/update/<int:pk>/', update_user, name='update_user'),
    #path('user/delete/<int:pk>/', delete_user, name='delete_user'),

    path('purchase/update/<int:pk>/', update_purchase, name='update_purchase'),
    path('purchase/delete/<int:pk>/', delete_purchase, name='delete_purchase'),

    path('staff_payments/update/<int:pk>/', update_staff_payments, name='update_staff_payments'),
    path('staff_payments/delete/<int:pk>/', delete_staff_payments, name='delete_staff_payments'),
  
    
]

