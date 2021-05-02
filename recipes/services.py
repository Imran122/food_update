import os
import re
from glob import glob
import json
from recipes.models import *
import requests
from random import randint
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models.functions import Length


class SyncRecipes:

	def sync_json_from_local():
		path = 'recipes/recipe.json'
		with open(path) as f:
			data = json.load(f)
			print(path)
			print(f)
			for recipe in data: 
				try:
					recipeExist = RecipeOverview.objects.get(url=recipe['fields']['url'])
				except: 
					recipeExist = None 
				if not recipeExist:
					newRecipe = RecipeOverview()
					newRecipe.source = recipe['fields']['source']
					newRecipe.language = recipe['fields']['language']
					newRecipe.tags = recipe['fields']['tags']
					newRecipe.title = recipe['fields']['title']
					newRecipe.url = recipe['fields']['url']
					newRecipe.image = recipe['fields']['image']
					newRecipe.ingredients = recipe['fields']['ingredients']
					newRecipe.directions = recipe['fields']['directions']
					newRecipe.highProtein = recipe['fields']['highProtein']
					newRecipe.highCarbs = recipe['fields']['highCarbs']
					newRecipe.highFat = recipe['fields']['highFat']
					newRecipe.highCalories = recipe['fields']['highCalories']
					newRecipe.lowCarbs = recipe['fields']['lowCarbs']
					newRecipe.percentCarbs = recipe['fields']['percentCarbs']
					newRecipe.percentProtein = recipe['fields']['percentProtein']
					newRecipe.percentFat = recipe['fields']['percentCalories']
					newRecipe.percentCalories = recipe['fields']['percentCalories']
					newRecipe.mealTypes = recipe['fields']['mealTypes']
					newRecipe.cookingMins = recipe['fields']['cookingMins']
					newRecipe.save()
				else: 
					print('exists')
			return f





	def sync_allrecipes():
		path = 'recipes/jsonRecipes/allrecipes/vegan'
		for filename in glob(os.path.join(path, '*.json')):
			with open(filename) as currentFile:
				try:
					data = json.load(currentFile)
					recipeExist = RecipeOverview.objects.get(url=data['url'])
					if recipeExist:
						ingredients = data['ingredients']
						ingredientList = []
						for ingredient in ingredients:
							ingredientList.append(ingredient)
						recipeExist.ingredients = ingredientList
						recipeExist.save()
						directions = data['directions']
						directionList = []
						for direction in directions:
							directionList.append(direction)
						recipeExist.directions = directionList
						recipeExist.save()
						
					else: 
						try:
							recipe = RecipeOverview(source=data['source'], language=data['language'], tags=data['tags'], 
							title=data['title'], url=data['url'], image=data['image'], ingredients=data['ingredients'], directions=data['directions'])
							recipe.save()
						except Exception as e:
							print(e)
						if recipe:
							ingredients = data['ingredients']
							for ingredient in ingredients: 
								newIngredient = Ingredient(recipe=recipe, description=ingredient)
								newIngredient.save()
							directions = data['directions']
							for direction in directions:
								newDirection = Direction(recipe=recipe, description=direction)
								newDirection.save()
							
				except Exception as e:
					print(e)

	def sync_epicurious_from_file():
		path = 'recipes/jsonRecipes/allrecipes/vegan'
		for filename in glob(os.path.join(path, '*.json')):
			with open(filename) as currentFile:
				data = json.load(currentFile)
				try:
					recipeExist = RecipeOverview.objects.get(url=data['url'])
				except:
					recipeExist = None
				if not recipeExist:
					try:
						
						recipe = RecipeOverview(source=data['source'], language=data['language'], tags=data['tags'], 
						title=data['title'], url=data['url'], image=data['image'], ingredients=data['ingredients'], directions=data['directions'])
						recipe.save()
						print('recipe saved' + data['title'] )
					except Exception as e:
						print(e)
					if recipe:
						ingredients = data['ingredients']
						for ingredient in ingredients: 
							newIngredient = Ingredient(recipe=recipe, description=ingredient)
							newIngredient.save()
						directions = data['directions']
						for direction in directions:
							newDirection = Direction(recipe=recipe, description=direction)
							newDirection.save()
					
		return 'done'



	def sync_recipes_with_files():
		path = 'recipes/jsonRecipes/allrecipes/vegan'
		for filename in glob(os.path.join(path, '*.json')):
			with open(filename) as currentFile:
				try:
					data = json.load(currentFile)
					print('loaded file')
					try:
						recipeExist = RecipeOverview.objects.get(url=data['url'])
						print(recipeExist)
					except:
						recipeExist = None
					if recipeExist:
						
						ingredients = data['ingredients']
						for ingredient in ingredients:
							try:
								ingredientExists = Ingredient.objects.get(recipe=recipeExist, description=ingredient)
							except: 
								ingredientExists = None
							if ingredientExists is None:
								newIngredient = Ingredient(recipe=recipeExist, description=ingredient)
								newIngredient.save()
							else: 
								print('ingredient already exists from recipe' + str(recipeExist.id))
					
						
						
						directions = data['directions']
						for direction in directions:
							try:
								directionExists = Direction.objects.get(recipe=recipeExist, description=direction)
							except:
								directionExists = None
							
						   
							if directionExists is None:    
								newDirection = Direction(recipe=recipeExist, description=direction)
								newDirection.save()
							else:
								print('direction exists from recipe' + str(recipeExist.id))
						
					
						"""
						directions = data['directions']
						for direction in directions:
							directionsExist = Direction.objects.filter(recipe=recipeExist, description=direction)
							if directionsExist.count() > 1:
								while directionsExist.count() > 1:
									for directionExist in directionsExist:
										directionExist.delete()
							else:
								print('count not greater than 1 ')
						"""
					print('all good')
						
							
				except Exception as e:
					print(e)


class Spoonacular:

	def getRecipeInfo(recipeUrl):
		apiKey = '04162bc40c7b427daaa43e35cb3fd42c'

		"""Get recipe from provided URL"""
				
		recipeUrl = recipeUrl

		url = f'https://api.spoonacular.com/recipes/extract?apiKey={apiKey}'
		recipeUrl = recipeUrl
		querystring = {"url":recipeUrl, "includeNutrition":'true'}
		r = requests.request("GET", url, params=querystring)

		data = r.json()
		print(data)
		try: 
			nutrition = data['nutrition']

		
			data = r.json()

			nutrients = data['nutrition']['nutrients']
			nutrition = []

			for nutrient in nutrients:
				if nutrient['title'] == 'Calories':
					calories = nutrient['amount']
					caloriesUnit = nutrient['unit']
					needsCalories = nutrient['percentOfDailyNeeds']
					caloriesArray = {
						'calories':{
							'amount': calories,
							'unit': caloriesUnit,
							'percent': needsCalories
						}
					}
					nutrition.append(caloriesArray)
				elif nutrient['title'] == 'Fat':
					fat = nutrient['amount']
					fatUnit = nutrient['unit']
					needsFat = nutrient['percentOfDailyNeeds']
					fatArray = {
						'fat':{
							'amount': fat,
							'unit': fatUnit,
							'percent': needsFat
						}
					}
					nutrition.append(fatArray)
				elif nutrient['title'] == 'Carbohydrates':
					carbohydrate = nutrient['amount']
					carbUnit = nutrient['unit']
					needsCarb = nutrient['percentOfDailyNeeds']
					carbsArray = {
						'carbohydrates':{
							'amount': carbohydrate,
							'unit': carbUnit,
							'percent': needsCarb
						}
					}
					nutrition.append(carbsArray)
				elif nutrient['title'] == 'Protein':
					protein = nutrient['amount']
					proteinUnit = nutrient['unit']
					needsProtein = nutrient['percentOfDailyNeeds']
					proteinArray = {
						'protein':{
							'amount': protein,
							'unit': proteinUnit,
							'percent': needsProtein
						}
					}
					nutrition.append(proteinArray)
			try:
				completeTime = data['cookingMinutes'] + data['preparationMinutes']
			except: 
				completeTime = ""

			try: 
				dishType = data['dishTypes']
			except: 
				dishType = "" 

			additionalInfo = {
				'additionalInfo':{
					'completeTime': completeTime,
					'dishType': dishType
				}
			}
			nutrition.append(additionalInfo)

			print('fuck you')
			return nutrition
		except:
			return 'Did not work'
		

class ShoppingListManage: 
	def generate_list(start, end, name):
		meals = Events.objects.filter(start__range=[start, end])
		shoppingList = ShoppingList(start=start, end=end, name=name)
		shoppingList.save()

		for meal in meals:
			ingredients = Ingredient.objects.filter(recipe=meal.mealChosen)
			for ingredient in ingredients:
				shoppingItem = ShoppingListItem(shoppingList=shoppingList, complete=False, ingredient=ingredient)
				shoppingItem.save()
		return shoppingList

		print('complete')

class NeedsSorting:
	def needs(recipeId):
		recipe = RecipeOverview.objects.get(pk=recipeId)
		
		if recipe.percentCalories >= 30.00:
			recipe.highCalories = True
			recipe.save()
		else: 
			print('not high calories')
		
		if recipe.percentCarbs >= 25.00:
			recipe.highCarbs = True
			recipe.save()
		elif recipe.percentCarbs <= 10.00:
			recipe.lowCarbs = True
			recipe.save()
		else:
			print('normal')
		
		if recipe.percentProtein >= 25.00:
			recipe.highProtein = True
			recipe.save()



class MealPlanning:
	
	def updateRecipes():
		a_set = set()
		while True:
			a_set.add(randint(1020, 4256))
			print()
			if len(a_set) == 500:
				break
		reciepIdList = list(a_set)
	   
		for recipeId in reciepIdList:
			recipe = RecipeOverview.objects.get(pk=recipeId)
			print(recipeId)
			if not recipe.percentCalories:
				recipeInfo = Spoonacular.getRecipeInfo(recipeUrl=recipe.url)
				print(recipe.id)
				print(recipeInfo)
				try:
					recipe.cookingMins = recipeInfo[4]['additionalInfo']['completeTime']
				except:
					print('no cooking time')
				try: 
					recipe.mealTypes = recipeInfo[4]['additionalInfo']['dishType']
					recipe.percentCalories = recipeInfo[0]['calories']['percent']
					recipe.percentFat = recipeInfo[1]['fat']['percent']
					recipe.percentCarbs = recipeInfo[2]['carbohydrates']['percent']
					recipe.percentProtein = recipeInfo[3]['protein']['percent']
					recipe.save()
				except:
					print('didnt work')
				try: 
					if recipe.percentCalories >= 30.00:
						recipe.highCalories = True
						recipe.save()
					else: 
						print('not high calories')
					
					if recipe.percentCarbs >= 30.00:
						recipe.highCarbs = True
						recipe.save()
					elif recipe.percentCarbs <= 10.00:
						recipe.lowCarbs = True
						recipe.save()
					else:
						print('normal')
					
					if recipe.percentProtein >= 15.00:
						recipe.highProtein = True
						recipe.save()
					else: 
						print('not high protein')
				except:
					print('something went wrong, moving on')
			else:
				print('already done it')

	def meal_planning(dayIntensity, userId):
		user = User.objects.get(pk=userId)

		dayIntensityId = dayIntensity.id
		

		if dayIntensity.intensity == dayIntensity.REST:
			print(dayIntensity.id)
			options = MealPlanning.rest_day(dayIntensity, dayIntensity.date, user)
			return options
		elif dayIntensity.intensity == dayIntensity.EASY:
			print(dayIntensity.id)
			options = MealPlanning.easy_day(dayIntensity, dayIntensity.date, user)
			
			return options
		elif dayIntensity.intensity == dayIntensity.WORKOUT:
			print(dayIntensity.id)
			options = MealPlanning.workout_day(dayIntensity, dayIntensity.date, user)
			
			return options
		elif dayIntensity.intensity == dayIntensity.ALL_OUT:
			print(dayIntensity.id)
			options = MealPlanning.all_out_day(dayIntensity, dayIntensity.date, user)
			
			return options
		else: 
			return 'nothing'
	
	def busy_day(dayIntensity):
		if dayIntensity.busyDay == True:
		
			times = {
				'breakfast': 10,
				'amSnack': 10,
				'lunch': 20,
				'pmSnack':10,
				'dinner': 15, 
				'direction': 800 
			}
			return times
		else: 
			times = {
				'breakfast': 15,
				'amSnack': 10,
				'lunch': 30,
				'pmSnack':10,
				'dinner': 30, 
				'direction': 1200 
			}
			return times


	def rest_day(dayIntensity, date, user):
		limits = MealPlanning.busy_day(dayIntensity)

		mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'Smoothie' ) & Q(cookingMins__lte=limits['breakfast'])) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsAmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['amSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsLunch = RecipeOverview.objects.filter(Q(cookingMins__lte=limits['lunch']) & (Q(percentCalories__gte=20.00) & (Q(highProtein=True) | Q(lowCarbs=True))))
		mealsPmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['pmSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsDinner = RecipeOverview.objects.annotate(text_len=Length('directions')).filter((Q(cookingMins__gte=limits['dinner']) & Q(percentCalories__gte=20.00) & Q(text_len__lt=limits['direction'])) & (Q(highProtein=True) | Q(lowCarbs=True)))

		meals = MealPlanning.pick_meals(user, date, mealsBreakfast, mealsAmSnack, mealsLunch, mealsPmSnack, mealsDinner, dayIntensity)

		return meals

	def easy_day(dayIntensity, date, user):
		limits = MealPlanning.busy_day(dayIntensity) 
		mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'smoothie' ) & Q(cookingMins__lte=limits['breakfast'])) & (Q(highCalories=False) | Q(highProtein=True) | Q(lowCarbs=True)))
		mealsAmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['amSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['lunch']) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsPmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['pmSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(lowCarbs=True)))
		mealsDinner = RecipeOverview.objects.annotate(text_len=Length('directions')).filter((Q(cookingMins__gte=limits['dinner']) & Q(percentCalories__gte=20.00) & Q(text_len__lt=limits['direction'])) & (Q(highProtein=True) | Q(lowCarbs=True)))

		meals = MealPlanning.pick_meals(user, date, mealsBreakfast, mealsAmSnack, mealsLunch, mealsPmSnack, mealsDinner, dayIntensity)

		return meals

	def workout_day(dayIntensity, date, user):
		limits = MealPlanning.busy_day(dayIntensity) 
		mealsBreakfast = RecipeOverview.objects.filter((Q(title__icontains= 'smoothie' ) & Q(cookingMins__lte=limits['breakfast'])) & (Q(highProtein=True) | Q(highCarbs=True)| Q(highCalories=True)))
		mealsAmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['amSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(highCarbs=True)))
		mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['lunch']) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)))
		mealsPmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['pmSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(highCarbs=True)))
		mealsDinner = RecipeOverview.objects.annotate(text_len=Length('directions')).filter((Q(cookingMins__gte=limits['dinner']) & Q(percentCalories__gte=20.00) & Q(text_len__lt=limits['direction'])) & (Q(highProtein=True) | Q(highCarbs=True)| Q(highCalories=True)))

		meals = MealPlanning.pick_meals(user, date, mealsBreakfast, mealsAmSnack, mealsLunch, mealsPmSnack, mealsDinner, dayIntensity)

		return meals

	def all_out_day(dayIntensity, date, user):
		limits = MealPlanning.busy_day(dayIntensity) 

		mealsBreakfast = RecipeOverview.objects.filter(Q(cookingMins__lte=limits['breakfast']) & (Q(highCarbs=True)))
		mealsAmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['amSnack']) & Q(percentCalories__lte=18)) & (Q(highProtein=True) | Q(highCarbs=True)))
		mealsLunch = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['lunch']) & Q(percentCalories__gte=20.00)) & (Q(highProtein=True) | Q(highCarbs=True)))
		mealsPmSnack = RecipeOverview.objects.filter((Q(cookingMins__lte=limits['pmSnack']) & (Q(percentCalories__gte=15.00)) & Q(highProtein=True) | Q(highCarbs=True)))
		mealsDinner = RecipeOverview.objects.annotate(text_len=Length('directions')).filter((Q(cookingMins__gte=limits['dinner']) & Q(percentCalories__gte=25.00)  & Q(text_len__lt=limits['direction'])) & (Q(highCarbs=True) | Q(highCalories=True)))

		meals = MealPlanning.pick_meals(user, date, mealsBreakfast, mealsAmSnack, mealsLunch, mealsPmSnack, mealsDinner, dayIntensity)

		return meals



	def pick_meals(user, date, mealsBreakfast, mealsAmSnack, mealsLunch, mealsPmSnack, mealsDinner, dayIntensity):
		def check_repeat(meal, date):
			
			twoWeeks = date - timedelta(14)
			events = Events.objects.filter(mealChosen=meal, start__range=[twoWeeks, date])
			if events.count() <= 4:
				print(events.count())
				return True 
			else:
				return False

		def repeat_meals(date, dayIntensity, mealPosition):
			
			yesterday = date - timedelta(1)
			secondDay = date - timedelta(7)

			def daterange(date1, date2):
			
				for n in range(int ((date2 - date1).days)+1):
					yield date1 + timedelta(n)
			needed = True
			daterange = list(daterange(secondDay, yesterday))
			while needed:
				for dt in reversed(daterange):
					try:
						pastDayIntensity = DayIntensity.objects.get(date=dt)
					except: 
						pastDayIntensity = None
					if pastDayIntensity:
						if pastDayIntensity.intensity == dayIntensity.intensity:
							try:
								event = Events.objects.get(start=dt, mealPosition=mealPosition)
								useRecipe = check_repeat(event.mealChosen, dt)
								if useRecipe:
									
									needed = False
									return event 
							except:
								print('no event')
						else: 
							print('no match')
					else:
						print('no intensity created for that day')
				needed = False
				
			return False
			

		
		def find_if_yuk(meal):
			try: 
				userInterest = UserInterest.objects.get(user=self.user, recipe=meal)
				if userInterest.interest == userInterest.NOT_INTERESTED:
					return False
				else:
					return True 
			except:
				return True


		
		def pick_meal(meals, dayIntensity, mealPosition):
			try:
				mealSaved = Events.objects.get(start=dayIntensity.date, mealPosition=mealPosition, saved=True)
			except:
				mealSaved = False

			if not mealSaved:
				if dayIntensity.repeatMeals:
					repeat = repeat_meals(dayIntensity.date, dayIntensity, mealPosition)
					#print('DEF PICK MEAL' + str(repeat))
					if repeat:
						
						notyuk = find_if_yuk(repeat)
						if notyuk: 
							mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=mealPosition, defaults ={'mealChosen': repeat.mealChosen, 'dayIntensity': dayIntensity})
							mealSave[0].save()
							return mealSave
						else: 
							print(' yuk')
					else: 
					
						length = meals.count()
						print(length)
						interest = False

						for meal in meals: 
							chooseInt = randint(0, (length-1))
							meal = meals[chooseInt]
							interest = find_if_yuk(meal)

							if interest is True:
								
								mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=mealPosition, defaults ={'mealChosen': meal, 'dayIntensity': dayIntensity })
								mealSave[0].save()
								print(mealSave)
								return mealSave
				else:
					
					length = meals.count()
					print(length)
					interest = False

					for meal in meals: 
						chooseInt = randint(0, (length-1))
						meal = meals[chooseInt]
						interest = find_if_yuk(meal)

						if interest is True:
							print('DEF PICK MEAL interest is true')
							mealSave = Events.objects.update_or_create(user=user, start=date, mealPosition=mealPosition, defaults ={'mealChosen': meal, 'dayIntensity': dayIntensity })
							mealSave[0].save()
							print(mealSave)
							return mealSave
					



		
		if dayIntensity.needBreakfast:
			print('STARTING' + str(date))
			breakfastMeal = pick_meal(mealsBreakfast, dayIntensity, Events.BREAKFAST)
			print('need breakfast')
		else:
			breakfastMeal = None
		
		if dayIntensity.needAmSnack:
			print('STARTING' + str(date))
			amSnackMeal = pick_meal(mealsAmSnack, dayIntensity, Events.MORNING_SNACK)
			print('need am snack')
		else:
			amSnackMeal = None

		if dayIntensity.needLunch:
			print('STARTING' + str(date))
			lunchMeal = pick_meal(mealsLunch, dayIntensity, Events.LUNCH)
			print('need lunch')
		else:
			lunchMeal = None

		if dayIntensity.needPmSnack:
			print('STARTING' + str(date))
			pmSnackMeal = pick_meal(mealsPmSnack, dayIntensity, Events.AFTERNOON_SNACK)
			print('need pm snack')
		else:
			pmSnackMeal = None
		
		if dayIntensity.needDinner:
			print('STARTING' + str(date))
			dinnerMeal = pick_meal(mealsDinner, dayIntensity, Events.DINNER)
			print('need diner')
		else:
			dinnerMeal = None


		
		options = {
			'breakfast': breakfastMeal,
			'amSnack': amSnackMeal,
			'lunch': lunchMeal,
			'pmSnack': pmSnackMeal,
			'dinner': dinnerMeal
		}


		return options

	def add_https():
		recipes = RecipeOverview.objects.all()
		for recipe in recipes:
			url = recipe.url
			hasHttp = url.startswith('www.epicurious.com')
			if not hasHttp:
				newUlr = 'https://' + url
				recipe.url = newUlr
				recipe.save()
				print('saved' + str(recipe.id))

	def remove_long_https():
		recipes = RecipeOverview.objects.all()
		for recipe in recipes:
			url = recipe.url

			httpIssue = url.startswith('https://https://')
			if httpIssue:
				removeHttp = url.replace('https://https://', '')
				newUrl = 'https://' + removeHttp 
				recipe.url = newUrl
				recipe.save()
				print(newUrl)
#MealPlanning.updateRecipes()
#SyncRecipes.sync_json()

