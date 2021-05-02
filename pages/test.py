import requests 


querystring ={
    "date": 1611010057,
    "slot": 2,
    "position": 1,
    "type": 'RECIPE',
    "value": {
        "id": 296213,
        "servings": 2,
        }}


url = 'https://api.spoonacular.com/mealplanner/api-63887-lfutbol/items?hash=163ce77aa05ead0fac435b5d6c0ce7b8cab55ef0&apiKey=04162bc40c7b427daaa43e35cb3fd42c'
r = requests.request("POST", url, params=querystring)

print(r.content)