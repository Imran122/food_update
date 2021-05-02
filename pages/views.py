from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from core.models import User
from django.http import HttpResponse, JsonResponse, HttpRequest
import requests
import re
from decimal import Decimal
from random import seed, randint
from recipes.models import *
from accounts.models import UserProfile
from recipes.services import *
from datetime import date, datetime, timedelta, time
from app.tasks import my_task
from .forms import MealPlanGenerate
from .tasks import create_meal_plan, sync_recipes
from django.template.loader import render_to_string
from datetime import date, datetime, timedelta 
from django.utils import timezone


def plan_create(request):

	my_task.delay(2)
	startdate = date(2021, 3, 29)
	enddate = date(2021, 4, 4)
	dayIntensitys = DayIntensity.objects.filter(date__range=[startdate, enddate], user=request.user)
	
	print(dayIntensitys)
	"""
	for day in dayIntensitys:
		print(day.id)
		response = MealPlanning.meal_planning(dayIntensityId=day.id, user=request.user)
		print(response)
	"""
	return render(request, 'pages/generate-meal-plan.html')

def shopping_list(request, list_id):
	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	url_parameter = request.GET.get("q")

	if url_parameter:
		print('in url param')
		shoppingList = ShoppingList.objects.get(pk=list_id)
		print(shoppingList)
		print(url_parameter)
		items = ShoppingListItem.objects.filter(shoppingList=shoppingList, dismissed=False, ingredient__description__icontains=url_parameter).order_by('ingredient__description')
		print('after iteams')
	else: 		
		shoppingList = ShoppingList.objects.get(pk=list_id)
		items = ShoppingListItem.objects.filter(shoppingList=shoppingList, dismissed=False).order_by('ingredient__description')

	context = {
		'items': items,
		'shoppingList': shoppingList
	}
	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	context['shoppingListModal'] = shoppingListModal
	if request.is_ajax():
		html = render_to_string(
			template_name="partials/_ingredient_results.html", 
			context={
				'items': items,
				'shoppingList': shoppingList
			}
		)

		data_dict = {"html_from_view": html}

		return JsonResponse(data=data_dict, safe=False)



	return render(request, 'pages/shoppinglist.html', context)

def mealplan_view(request):
	userId = request.user.id
	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	def daterange(date1, date2):
		for n in range(int ((date2 - date1).days)+1):
			yield date1 + timedelta(n)

	try: 
		mealsView = request.POST['date']
	except:
		mealsView = None
	
	try:
		generate = request.POST['startdate']
	except: 
		generate = None
	
	startdate = date.today()
	enddate = startdate + timedelta(days=7)

	if request.method == 'POST':
		if mealsView:
			start = request.POST['date']
			end = request.POST['enddate']
			startdatetime = datetime.strptime(start, '%Y-%m-%d')
			startdate = startdatetime.date()
			enddatetime = datetime.strptime(end, '%Y-%m-%d')
			enddate = enddatetime.date()
		elif generate:
			startDate = request.POST.get('startdate')
			#startDate = datetime.strptime(startDate, '%b %d, %Y')
			endDate = request.POST.get('enddate')
			#endDate = datetime.strptime(endDate, '%b %d, %Y')
			print(endDate)

			if startDate:
				# Retrieve URL from form data
				
				
				print(f'VIEW Starting meal plan: ')
				# Create Task
				print('View User ID' + str(userId))
				meal_plan_task = create_meal_plan.delay(startDate, endDate, userId)
				# Get ID
				task_id = meal_plan_task.task_id
				# Print Task ID
				print (f'VIEWCelery Task ID: {task_id}')
				
				

		


	mealPlans = Events.objects.filter(user=request.user, start__range=[startdate, enddate])
	datesList = []
	for dt in daterange(startdate, enddate):
		datesList.append(dt)

	

	print(datesList)
	context = {
		'dates': datesList,
		'mealPlans': mealPlans,
		'shoppingListModal': shoppingListModal,
		'startdate': startdate,
		'enddate': enddate,
	}
	try:
		context['task_id'] = task_id
	except:
		context['task_id'] = None

	return render(request, 'pages/mealPlanView.html', context)
def dashboard(request):
	
	try:
		notmember=1
		profile1 = UserProfile.objects.get(user=request.user)
		if profile1.expire_date < timezone.now():
			notmember=0


	except User.DoesNotExist:
		profile1 = None       
	#importRecipe = SyncRecipes.sync_json_from_local()
	#print(importRecipe)
	SyncRecipes.sync_recipes_with_files()


	if request.method == 'POST': 
		name = request.POST.get('name')
		print(name)
		startdate = request.POST.get('date')
		enddate = request.POST.get('enddate')
		shoppingList = ShoppingListManage.generate_list(start=startdate, end=enddate, name=name)
	else:
		shoppingList = ""

	shoppingLists = ShoppingList.objects.filter(user=request.user, delete=False, completed=False)

	today = datetime.today()
	breakfast = Events.objects.get_or_create(start=today, mealPosition=Events.BREAKFAST, user=request.user)
	breakfast = breakfast[0]
	breakfastIngredients = Ingredient.objects.filter(recipe=breakfast.mealChosen)
	breakfastDirections = Direction.objects.filter(recipe=breakfast.mealChosen).order_by('id')
	print('today')
	morningSnack = Events.objects.get_or_create(start=today, mealPosition=Events.MORNING_SNACK, user=request.user)
	morningSnack = morningSnack[0]
	morningSnackIngredients = Ingredient.objects.filter(recipe=morningSnack.mealChosen)
	morningSnackDirection = Direction.objects.filter(recipe=morningSnack.mealChosen).order_by('id')
	print('today')
	lunch = Events.objects.get_or_create(start=today, mealPosition=Events.LUNCH, user=request.user)
	lunch = lunch[0]
	lunchIngredients = Ingredient.objects.filter(recipe=lunch.mealChosen)
	lunchDirections = Direction.objects.filter(recipe=lunch.mealChosen).order_by('id')
	print('today')

	afternoonSnack = Events.objects.get_or_create(start=today, mealPosition=Events.AFTERNOON_SNACK, user=request.user)
	afternoonSnack = afternoonSnack[0]
	afternoonSnackIngredients = Ingredient.objects.filter(recipe=afternoonSnack.mealChosen)
	afternoonSnackDirections = Direction.objects.filter(recipe=afternoonSnack.mealChosen).order_by('id')
	print('today')
	dinner = Events.objects.get_or_create(start=today, mealPosition=Events.DINNER, user=request.user)
	dinner = dinner[0]
	dinnerIngredients = Ingredient.objects.filter(recipe=dinner.mealChosen)
	dinnerDirections = Direction.objects.filter(recipe=dinner.mealChosen).order_by('id')
	print('today')
	print(breakfast.mealPosition)
	pastdays = today - timedelta(14)
	yesterday = today - timedelta(1)
	print(yesterday)
	try:
		events = Events.objects.filter(user=request.user, start__range=[pastdays,yesterday])
		feedbacks = []
		print(events)
		for event in events:
			print(event.mealChosen)
			if event.mealChosen is not None:
				try:
					feedback = UserInterest.objects.get(recipe=event.mealChosen, user=request.user)
					print(feedback.interest)
					if feedback.interest is None:
						needFeedBack = True
						newFeedback = UserInterest.objects.update_or_create(user=request.user, recipe=event.mealChosen)
						print(newFeedback)
						feedbacks.append(newFeedback[0])
				except:
					needFeedBack = True 
					newFeedback = UserInterest.objects.update_or_create(user=request.user, recipe=event.mealChosen)
					print(newFeedback)
					feedbacks.append(newFeedback[0])
					
				
		print(feedbacks)		
		
		feedbackEventShow = feedbacks[0]
		print('has events')
	except Exception as e:
		print(e)
		feedbackEventShow = None
		print('has no events')
	

	favorites = UserInterest.objects.filter(user=request.user, interest=UserInterest.FAVORITE)[:10]
	
	context = {
		'profile1':profile1,
		'breakfast': breakfast,
		'morningSnack': morningSnack,
		'lunch': lunch,
		'afternoonSnack': afternoonSnack,
		'dinner': dinner,
		'breakfastIngredients': breakfastIngredients,
		'breakfastDirections': breakfastDirections,
		'morningSnackDirections': morningSnackDirection,
		'morningSnackIngredients': morningSnackIngredients,
		'lunchDirections': lunchDirections, 
		'lunchIngredients': lunchIngredients,
		'afternoonSnackIngredients': afternoonSnackIngredients,
		'afternoonSnackDirections': afternoonSnackDirections,
		'dinnerIngredients': dinnerIngredients,
		'dinnerDirections': dinnerDirections,
		'feedbackEvent': feedbackEventShow,
		'shoppingLists':shoppingLists,
		'usercheck':notmember,
		'favorites': favorites
	}

	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	context['shoppingListModal'] = shoppingListModal

	return render(request, 'pages/dashboard.html', context)

def index(request):
	week = WeekDays.objects.get(pk=4)
	dayNeed1 = week.day1.id
	print(dayNeed1)

	return render(request, 'pages/index.html')

def calendar(request):
	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	all_events = Events.objects.filter(user=request.user)
	meal_list =RecipeOverview.objects.all()
	context = {
		"events":all_events,
		'meal_list':meal_list,
		'shoppingListModal': shoppingListModal
	}   


	return render(request,'pages/calendar.html',context)




def plan_generate(request):
	shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
	userId = request.user.id
	# If method is POST, process form data and start task
	if request.method == 'POST':
		# Get form instance
		startDate = request.POST.get('startdate')
		endDate = request.POST.get('enddate')
		print(startDate)

		if startDate:
			# Retrieve URL from form data
			
			
			print(f'VIEW Starting meal plan: ')
			# Create Task
			meal_plan_task = create_meal_plan.delay(startDate, endDate, userId)
			# Get ID
			task_id = meal_plan_task.task_id
			# Print Task ID
			print (f'VIEWCelery Task ID: {task_id}')

			
			context = {
				'task_id': task_id, 
				'shoppingListModal': shoppingListModal,
				}



			# Return demo view with Task ID
			return render(request, 'generate/plan.html', context)
		else:
			# Return demo view
			return render(request, 'generate/plan.html', {'shoppingListModal': shoppingListModal})
	else:
		# Get form instance
		
		# Return demo view
		return render(request, 'generate/plan.html', {'shoppingListModal': shoppingListModal})


def dismiss_shopping_list_item(request):
	postIds = request.POST['post_id']
	data = json.loads(postIds)
	
	for x in data: 
		dismiss = ShoppingListItem.objects.get(pk=x) 
		dismiss.dismissed = True
		dismiss.save()
		print(dismiss.dismissed)
	return HttpResponse('success')

def meal_plan_lock_status(request):
	mealId = request.POST['mealId']
	status = request.POST['status']
	meal = Events.objects.get(pk=mealId)

	if status == 'LOCK':
		meal.saved = True
		
	elif status == 'UNLOCK':
		meal.saved = False
	
	else: 
		print('was neither')

	meal.save()

	return HttpResponse('success')


def remove_shopping_list(request):
	if request.method == 'POST':
		listId = request.POST.get('listId')
		shoppingList = ShoppingList.objects.get(pk=listId)
		shoppingList.delete = True
		shoppingList.save()
		print('removed' + listId)
	return HttpResponse('success')

def generate_shopping_list(request):
	if request.POST.get('name'): 
		name = request.POST.get('name')
		print(name)
		startdate = request.POST.get('date')
		enddate = request.POST.get('enddate')
		shoppingList = ShoppingListManage.generate_list(start=startdate, end=enddate, name=name)
		return HttpResponse(shoppingList.id)
	else:
		shoppingList = ""
	return 'done'


def feedback_meal(request):
	if request.method == 'POST': 
		interest = request.POST.get('interestId')
		feedback = request.POST.get('feedback')
		interest = UserInterest.objects.get(pk=interest)
		interest.interest = feedback
		interest.save()
		
		print(interest.interest)

		

		return HttpResponse('success')
