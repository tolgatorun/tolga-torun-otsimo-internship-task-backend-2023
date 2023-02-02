import json
from http.server import HTTPServer, BaseHTTPRequestHandler

f = open('dataset.json')

data = json.load(f)

meals = data['meals']
ingredients = data['ingredients']
meal_ingredient_dict = {}
ingredient_dict = {}
meal_vegan_vegetarian_dict = {}
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


meal_ingredient_dict_init()
ingredient_dict_init()
meal_vegan_vegetarian_dict_init()




#print(meal_ingredient_dict)
#print(ingredient_dict)
#for i in meal_vegan_vegetarian_dict:
#    print(i,'------', meal_vegan_vegetarian_dict[i])

vegan_vegetarian_dict = {
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
            


httpd = HTTPServer(('localhost', 8000), APIHandler)
httpd.serve_forever()



