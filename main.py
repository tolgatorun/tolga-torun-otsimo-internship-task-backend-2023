import json
from http.server import HTTPServer, BaseHTTPRequestHandler

f = open('dataset.json')

data = json.load(f)

meals = data['meals']
ingredients = data['ingredients']
meal_ingredient_dict = {}
ingredient_dict = {}
meal_vegan_vegetarian_dict = {}
meals_ingredients_wo = data['meals']  #init for meals_ingredients_without options
valid_ingredients = [x['name'] for x in data['ingredients']] #valid ingredient list for quality and price calculation
#valid_ingredients = [(x[0].lower() + x[1:]) for x in valid_ingredients]
def ingredient_dict_init():
    for i in ingredients:
        ingredient_dict[i['name']] = i['groups']

def meal_ingredient_dict_init():
    for i in meals:
        meal_ingredient_dict[i['name']] = [j['name'] for j in i['ingredients']]

def meal_vegan_vegetarian_dict_init():
    for i in meal_ingredient_dict.keys():
        ingredient_number = len(meal_ingredient_dict[i])
        a = []
        for x in meal_ingredient_dict[i]:
            if x == 'Pork chops':
                pass
            else:
                a.append(len(ingredient_dict[x]))
        if a.count(2) == len(a):
            meal_vegan_vegetarian_dict[i] = 'vegan'
        else:
            meal_vegan_vegetarian_dict[i] = 'vegetarian'
        if a.count(0) > 0:
            meal_vegan_vegetarian_dict[i] = ''
        

def vegan_list_view():
    vegan_list = []
    for meal in data['meals']:
        meal_name = meal['name']
        if meal_vegan_vegetarian_dict[meal_name] == 'vegan':
            vegan_list.append(meal)
    return vegan_list

def vegetarian_list_view():
    vegetarian_list = []
    for meal in data['meals']:
        meal_name = meal['name']
        if meal_vegan_vegetarian_dict[meal_name] != '':
            vegetarian_list.append(meal)
    return vegetarian_list

def meals_ingredients_wo_init():
    for meal in meals_ingredients_wo:
        ingredients = []
        for ingredient in meal['ingredients']:
            for ingredient_with_options in data['ingredients']:
                if ingredient_with_options['name'] == ingredient['name']:
                    ingredients.append(ingredient_with_options)
        meal['ingredients'] = ingredients

def mealWithID(id):
    for meal in meals_ingredients_wo:
        if meal['id'] == id:
            return meal


meal_ingredient_dict_init()
ingredient_dict_init()
meal_vegan_vegetarian_dict_init()
meals_ingredients_wo_init()

vegan_vegetarian_dict = { #for /listMeals endpoint
    'is_vegetarian': False,
    'is_vegan': False
}

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path, query_params = self.path.split('?')
        query_params = query_params.split('&')


        if self.path == '/listMeals':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json') 
            self.end_headers()
            vegan_vegetarian_dict = {
                'is_vegetarian': False,
                'is_vegan' : False,
            }
            vegan_vegetarian_list = []
            for param in query_params:
                if len(vegan_vegetarian_list) == 2:
                    break
                if 'is_vegetarian' in param:
                    vegan_vegetarian_list.append(param)
                if 'is_vegan' in param:
                    vegan_vegetarian_list.append(param)

            for i in range(len(query_params)):
                dietary_type , bool_value=query_params[i].split('=')
                if bool_value == 'true':
                    vegan_vegetarian_dict[dietary_type] = True
                else:
                    vegan_vegetarian_dict[dietary_type] = False
            print(vegan_vegetarian_dict)
            if vegan_vegetarian_dict['is_vegan'] == True:
                self.wfile.write(json.dumps(vegan_list_view()).encode())
            elif vegan_vegetarian_dict['is_vegetarian'] == True and vegan_vegetarian_dict['is_vegan'] == False:
                self.wfile.write(json.dumps(vegetarian_list_view()).encode())
            else:
                self.wfile.write(json.dumps(data['meals']).encode())
        

        if self.path == '/getMeal':
            for param in query_params:
                if 'id' in param:
                    _, id = param.split('=') 
                    id = int(id)
            if id > 0 and id < len(data['meals']):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json') 
                self.end_headers()
                self.wfile.write(json.dumps(mealWithID(id)).encode())
            else:
                self.send_error(400, 'inappropriate id')
                self.send_header('Content-Type', 'application/json') 
                self.end_headers()

    def do_POST(self):
        self.path, query_params = self.path.split('?')
        if self.path == '/quality':
            parameter_list = []
            parameter_dict = {}
            for param in query_params.split('&'):
                parameter_list.append(param)
            for param in parameter_list:
                key, value = param.split('=')
                key = key[0].capitalize() + key[1:]
                parameter_dict[key] = value
            if parameter_dict.get('MealID') == None:
                self.send_error(400, "mealID is a must")
            for key,value in parameter_dict.items():
                if key == 'MealID':
                    pass
                else:
                    if key not in valid_ingredients:
                        print(key)
                        self.send_error(400, "invalid ingredient")
                        return
                    if value != 'high' and value != 'medium' and value != 'low':
                        self.send_error(400, "inappropriate quality")    
                        return
            meal = mealWithID(int(parameter_dict['MealID']))
            meal_name = meal['name']
            for key in parameter_dict.keys():
                if key == 'MealID':
                    pass
                else:
                    if key not in meal_ingredient_dict[meal_name]:
                        self.send_error(400, 'inappropriate ingredient')
            quality = 0
            ingredient_parameter_count = 0
            for key,value in parameter_dict.items():
                if key == 'MealID':
                    pass
                else:
                    ingredient_parameter_count += 1
                    if value == 'high':
                        quality = quality + 30
                    if value == 'medium':
                        quality = quality + 20
                    if value == 'low':
                        quality = quality + 10 
            ingredient_count = len(meal_ingredient_dict[meal_name])
            ingredient_parameter_count = ingredient_count - ingredient_parameter_count
            quality = quality + ingredient_parameter_count * 30
            quality_score = round(quality / ingredient_count, 2)
            quality_dict = { 'quality': quality_score}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json') 
            self.end_headers()
            self.wfile.write(json.dumps(quality_dict).encode())



httpd = HTTPServer(('localhost', 8000), APIHandler)
httpd.serve_forever()



