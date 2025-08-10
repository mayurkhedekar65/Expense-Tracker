from django.shortcuts import render, redirect, get_object_or_404
from .models import CurrentBalance, TrackingHistory
from django.db.models import Sum

def index(request):
    if request.method == "POST":
        myamount = float(request.POST.get("amount"))
        mydescription = request.POST.get("description")

        mydata, _ = CurrentBalance.objects.get_or_create(id=1)

      
        if myamount < 0:
            expense_type = "DEBIT"
        else:
            expense_type = "CREDIT"

      
        TrackingHistory.objects.create(
            amount=myamount,
            description=mydescription,
            expense_type=expense_type,
            income=mydata
        )

        if expense_type == "CREDIT":
            mydata.income += myamount
        mydata.save()

        return redirect(index)

    total_income = TrackingHistory.objects.filter(
        expense_type="CREDIT"
    ).aggregate(total=Sum("amount"))["total"] or 0


    total_expense = TrackingHistory.objects.filter(
        expense_type="DEBIT"
    ).aggregate(total=Sum("amount"))["total"] or 0

    balance = TrackingHistory.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0
    

    context = {
        "transactions": TrackingHistory.objects.all(),
        "income": total_income,
        "myexpense": total_expense,
        "current_income": CurrentBalance.objects.first(),
        "current_balance": balance
    }
    


    
    return render(request, "index.html", context)
def delete_transaction(request, pk):
        transaction = get_object_or_404(TrackingHistory, id=pk)
        transaction.delete()
        return redirect(index) 

