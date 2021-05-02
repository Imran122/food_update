from django.forms import ModelForm, DateInput
from recipes.models import DayIntensity

class DayIntensityForm(ModelForm):
  class Meta:
    model = DayIntensity
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    }
    fields = ['date', 'intensity', 'busyDay', 'needBreakfast', 'needAmSnack', 'needLunch',
    'needPmSnack', 'needDinner', 'repeatMeals']


    labels = {
      'date': 'For Date',
      'intensity': 'Activity Level',
      'busyDay': 'Busy Day (Short on Time?)',
      'needBreakfast': 'Plan Breakfast',
      'needAmSnack': 'Plan Morning Snack',
      'needLunch': 'Plan Lunch',
      'needPmSnack': 'Plan Afternoon Snack',
      'needDinner': 'Plan Dinner',
      'repeatMeals': 'Repeat Meals?'
    }

  def __init__(self, *args, **kwargs):
    super(DayIntensityForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['date'].input_formats = ('%Y-%m-%d',)
    