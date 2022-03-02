from tkinter.messagebox import YES
from django.shortcuts import redirect, render
import datetime
from recap.models import Recap
from django.contrib.auth.decorators import login_required
from recap.forms import RecapForm

@login_required
def recap_create(request):

    current_month = datetime.datetime.now().month

    current_year = datetime.datetime.now().year

    recaps = Recap.objects.all()

    months = [1,2,3,4,5,6,7,8,9,10,11,12]

    past_months = months[0:current_month]

    recap_forms = {}
    for month in past_months:
        if not recaps.filter(date__year=current_year,month = month):
            recap_form = RecapForm(initial={'month': month})
            recap_forms[recap_form] = month

    if request.method == 'POST':
        recap_form = RecapForm(data=request.POST)
        if recap_form.is_valid():
            month = recap_form.cleaned_data.get('month')
            dias_trabajados = recap_form.cleaned_data.get('dias_trabajados')

            attrs = {'dias_trabajados':dias_trabajados, 'month':month}

            new_recap = Recap(**attrs)
            new_recap.save()

            return redirect('recap:recap_list')

    return render(request, 'recap/recap_create.html',{'recap_forms':recap_forms,
                                                    'current_year':current_year,
                                                    'recaps':recaps})


@login_required
def recap_list(request):

    recaps = Recap.objects.all()

    return render(request,'recap/recap_list.html',{'recaps':recaps})