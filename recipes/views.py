from django.shortcuts import render, redirect, get_object_or_404
from recipes.services import SyncRecipes, Spoonacular, MealPlanning
from recipes.models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.views.decorators.cache import cache_page
from datetime import datetime, date, timedelta
from django.http import HttpResponse, JsonResponse
from app.tasks import my_first_task, data_extractor
from django.contrib.auth.decorators import login_required
from pages.tasks import sync_recipes, sync_ingredients, update_nutrients

# Create your views here.
@login_required()
@cache_page(60 * 15)
def recipe(request, recipe_id):
    
    shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
    if not shoppingListModal:
        shoppingListModal = None

    recipeShow = get_object_or_404(RecipeOverview, id=recipe_id)
    ingredients = Ingredient.objects.filter(recipe=recipeShow)
    directions = Direction.objects.filter(recipe=recipeShow).order_by('id')
    
    try:
        
        nutrition = Spoonacular.getRecipeInfo(recipeUrl=recipeShow.url)

        calories = nutrition[0]['calories']['amount']
        caloriesUnit = nutrition[0]['calories']['unit']
        caloriesNeeds = nutrition[0]['calories']['percent']
        fat = nutrition[1]['fat']['amount']
        fatUnit = nutrition[1]['fat']['unit']
        fatNeeds = nutrition[1]['fat']['percent']
        carbs = nutrition[2]['carbohydrates']['amount']
        carbsUnit = nutrition[2]['carbohydrates']['unit']
        carbNeeds = nutrition[2]['carbohydrates']['percent']
        protein = nutrition[3]['protein']['amount']
        proteinUnit = nutrition[3]['protein']['unit']
        proteinNeeds = nutrition[3]['protein']['percent']
    except:
        print(recipeShow.url)

    if request.method == 'POST':
        date = request.POST.get('date')
        
        meal = request.POST.get('meal')
        print(meal)
        mealId = request.POST.get('recipeId')
        mealChosen = RecipeOverview.objects.get(pk=recipe_id)
        if meal == 'BREAKFAST':
            mealPos = Events.BREAKFAST
        elif meal == 'MORNING_SNACK':
            mealPos = Events.MORNING_SNACK
        elif meal == 'LUNCH':
            mealPos = Events.LUNCH
        elif meal == 'AFTERNOON_SNACK':
            mealPos = Events.AFTERNOON_SNACK
        elif meal == 'DINNER':
            mealPos = Events.DINNER
        elif meal == 'EVENING_SNACK':
            mealPos = Events.EVENING_SNACK


        event = Events.objects.update_or_create(start=date, user=request.user, mealPosition=mealPos, defaults ={'mealChosen': mealChosen, })
        event[0].save()
    startdate = datetime.today()
    enddate = startdate + timedelta(14)
    pastdate = startdate - timedelta(14)
    futureMeals = Events.objects.filter(mealChosen=recipeShow, user=request.user, start__range=[startdate, enddate])
    pastMeals = Events.objects.filter(mealChosen=recipeShow, user=request.user, start__range=[pastdate, startdate])
    
    print(pastMeals)
    
    userInterest = UserInterest.objects.get_or_create(recipe=recipeShow, user=request.user)
    interest = userInterest[0]
    context = {
        'recipe': recipeShow,
        'ingredients': ingredients,
        'directions': directions,
        'calories': calories,
        'caloriesUnit': caloriesUnit,
        'fat': fat,
        'fatUnit': fatUnit,
        'carbs': carbs,
        'carbsUnit': carbsUnit,
        'protein': protein,
        'proteinUnit': proteinUnit,
        'calorieNeeds': caloriesNeeds,
        'fatNeeds': fatNeeds,
        'carbNeeds': carbNeeds,
        'proteinNeeds': proteinNeeds,
        'futureMeals' : futureMeals,
        'pastMeals': pastMeals,
        'userInterest': interest,
        'shoppingListModal': shoppingListModal
        
    }

    return render(request, 'recipes/recipe.html', context)
@login_required()
def recipe_search(request):
    
    shoppingListModal = ShoppingList.objects.filter(user=request.user, completed=False, delete=False)
    """
    The Sync Recipes script will sync all of the recipes in json files into the database
    """
    
    #sync_recipes.delay()
    #update = update_nutrients_now.delay()

    recipes = RecipeOverview.objects.all()
    paginator = Paginator(recipes, 24)
    page = request.GET.get('page')
    paged_recipes = paginator.get_page(page)
    

    if 'keywords' in request.GET: 
        keywords = request.GET['keywords']
        if keywords:
            recipes = RecipeOverview.objects.filter(Q (ingredients__icontains=keywords) | Q(directions__icontains=keywords) | Q(title__icontains=keywords))
            paginator = Paginator(recipes, 24)
            page = request.GET.get('page')
            paged_recipes = paginator.get_page(page)

    context = {
        'paged_recipes': paged_recipes, 
        'shoppingListModal': shoppingListModal
    }

    return render(request, 'recipes/recipe_search.html', context)
@login_required()
def faq(request):
    return render(request, 'faq/faq.html')

@login_required()
def user_favorite(request):
    recipeId = request.GET.get('recipe_id')
    interestId = request.GET.get('interest_id')
    interestObj = UserInterest.objects.get(id=interestId)
    interestObj.interest = interestObj.FAVORITE
    interestObj.save()
    print(interestObj.interest)
   
    
@login_required()
def user_yuk(request):
    recipeId = request.GET.get('recipe_id')
    interestId = request.GET.get('interest_id')
    interestObj = UserInterest.objects.get(id=interestId)
    interestObj.interest = interestObj.NOT_INTERESTED
    interestObj.save()
    print(interestObj.interest)


@login_required()
def progress_view(request):
    result = my_task.delay(10)
    return render(request, 'pages/display_progress.html', context={'task_id': result.task_id})

