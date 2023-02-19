# tolga-torun-otsimo-internship-task-backend-2023

Pure Python backend for a restaurant 

python 3.10.5

/listMeals endpoint lists meals and accepts two parameters 'is_vegan' and 'is_vegetarian'. Every value except 'true' evaulates to False. These parameters are optional 

/getMeal endpoint returns specified meal. id parameter is required.

/quality endpoint returns average quality score. id parameter is required and can specify qualities of ingredients, quality options:['high', 'medium', 'low']

/price endpoint takes a meal id with all of its ingredients' quality selections and returns the resulting price.
 
