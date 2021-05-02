from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import JsonResponse


from recipes.models import *
from .utils import Calendar
import calendar
from .forms import DayIntensityForm

# Create your views here.

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    
    model = DayIntensity
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoppingListModal = ShoppingList.objects.filter(user=self.request.user, completed=False, delete=False)
        context['shoppingListModal'] = shoppingListModal
        # use today's date for the calendar
        newd = get_date(self.request.GET.get('month', None))
        if newd:
            d = newd
        else: 
            d = get_date(self.request.GET.get('day'))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        newd = get_date(self.request.GET.get('month', None))
        print('newd' + str(newd))
        context['prev_month'] = prev_month(newd)
        context['next_month'] = next_month(newd)
        context['form'] = DayIntensityForm
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    print(month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def day_intensity(request, event_id=None):
    instance = DayIntensity()
    print(event_id)
    if event_id:
        instance = get_object_or_404(DayIntensity, pk=event_id)
    else:
        instance = DayIntensity()
    
    form = DayIntensityForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        day = form.save(commit=False)
        day.user = request.user
        day.save()
        
        

        return HttpResponseRedirect(reverse('cal:calendar'))
    return HttpResponse(form.as_p())