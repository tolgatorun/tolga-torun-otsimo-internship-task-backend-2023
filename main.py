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
            
            


httpd = HTTPServer(('localhost', 8000), APIHandler)
httpd.serve_forever()



