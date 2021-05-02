from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task
# Celery-progress
from celery_progress.backend import ProgressRecorder
from recipes.services import *

# Task imports
import os, time, subprocess, re
from time import sleep
from recipes.models import *
from recipes.services import *
from contextlib import contextmanager
from celery_once import QueueOnce
import random

@shared_task(bind=True, base=QueueOnce, once={'graceful': True} )
def sync_recipes(self):
	sync = MealPlanning.sync_epicurious_from_file()
	return sync


@shared_task(bind=True, base=QueueOnce, once={'graceful': True} )
def create_meal_plan(self, startdate, enddate, user):
	# Announce new task (celery worker output)
	sleep(3)
	print('TASkCreate meal plan')
	print(startdate)
	print(enddate)
	dayIntensitys = DayIntensity.objects.filter(date__range=[startdate, enddate], user=user)
	print(dayIntensitys)
	progress_recorder = ProgressRecorder(self)
	dayCount = 0 
	intensityCount = dayIntensitys.count()
	dayList = []
	while dayCount < intensityCount:
		for day in reversed(dayIntensitys):
			print(day.id)
			dayList.append(day.id)
			response = MealPlanning.meal_planning(day, user)
			dayCount += 1
			#sleep(2)
			progress_recorder.set_progress(int(dayCount), 7, f'Another day of awesomeness planned...')
	
	return 'done'

@shared_task(bind=True, base=QueueOnce, once={'graceful': True})
def sync_recipes(self):
	SyncRecipes.sync_epicurious_from_file()
	return 'done'

#delete this one 
@shared_task(bind=True, base=QueueOnce, once={'graceful': True})
def sync_ingredients(self):
	print('sync ingredients')
	SyncRecipes.sync_recipes_with_files()
	return 'done'

@shared_task(bind=True, base=QueueOnce, once={'graceful': True})
def sync_ingredients_now(self):
	print('sync ingredients')
	SyncRecipes.sync_recipes_with_files()
	return 'done'

def update_progress(self, dayCount, instensityCount):
	# Create progress recorder instance
	progress_recorder = ProgressRecorder(self)

	if dayCount < instensityCount:
		progress_recorder.set_progress(int(dayCount), days)
		sleep(3)
	else:
		print('all done')

#delete this
@shared_task(bind=True, base=QueueOnce, once={'graceful': True})
def update_nutrients(self):
	recipes = RecipeOverview.objects.filter(percentCarbs__isnull=True)
	endInt = recipes.count()
	randomList = random.sample(range(0,endInt), 800)
	count = 0
	while count <= 800:
		for number in randomList:
			recipe = recipes[number]
			sleep(2)
			count = count + 1 
			print(count)
			nutrition = Spoonacular.getRecipeInfo(recipe.url)
			print(nutrition)
	
	return 'done'

@shared_task(bind=True, base=QueueOnce, once={'graceful': True})
def update_nutrients_now(self):
	recipes = RecipeOverview.objects.filter(percentCarbs__isnull=True)
	endInt = recipes.count()
	randomList = random.sample(range(0,endInt), 800)
	count = 0
	while count <= 800:
		for number in randomList:
			recipe = recipes[number]
			sleep(2)
			count = count + 1 
			print(count)
			nutrition = Spoonacular.getRecipeInfo(recipe.url)
			print(nutrition)
	
	return 'done'