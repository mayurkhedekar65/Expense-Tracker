from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import CurrentBalance, TrackingHistory
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required

def mysignup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CurrentBalance.objects.create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect(index)  # change to your home/index page name
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, "login_signup/signup.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "login_signup/signup.html", {"form": form})

def mylogin(request):
    if request.method =="POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect(index)
    else:
        form = AuthenticationForm()
        return render(request, "login_signup/login.html", {"form": form})

def mylogout(request):
    logout(request)
    return redirect(index)

@login_required
def index(request):
    if request.method == "POST":
        myamount = float(request.POST.get("amount"))
        mydescription = request.POST.get("description")

        mydata, _ = CurrentBalance.objects.get_or_create(user=request.user)

        if myamount == 0:
            messages.error(request, "Amount cannot be zero.")
            return redirect(index)
        
        if myamount < 0:
            expense_type = "DEBIT"
        else:
            expense_type = "CREDIT"

      
        TrackingHistory.objects.create(
            user = request.user,
            amount=myamount,
            description=mydescription,
            expense_type=expense_type,
            income=mydata
        )
        mytransaction = TrackingHistory.objects.filter(user=request.user)

        if expense_type == "CREDIT":
            mydata.income += myamount
        mydata.save()

        
        return redirect(index)

    total_income = TrackingHistory.objects.filter(user=request.user,
    expense_type="CREDIT").aggregate(total=Sum("amount"))["total"] or 0


    total_expense = TrackingHistory.objects.filter( user=request.user,
    expense_type="DEBIT").aggregate(total=Sum("amount"))["total"] or 0

    balance = TrackingHistory.objects.filter(user=request.user).aggregate(
    total=Sum("amount"))["total"] or 0

    

    context = {
        "transactions": TrackingHistory.objects.filter(user=request.user),
        "income": total_income,
        "myexpense": total_expense,
        "current_income": CurrentBalance.objects.first(),
        "current_balance": balance
    }
    


    
    return render(request, "index.html", context)

@login_required
def delete_transaction(request, id):
        transaction = get_object_or_404(TrackingHistory, id=id, user=request.user)
        transaction.delete()
        return redirect(index) 

