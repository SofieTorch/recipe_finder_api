from flask import Response
from flask import Flask
from flask import request
from recipe import Recipe

import pandas as pd


app = Flask(__name__)
df = pd.read_csv('recipes_dataset.csv', delimiter=';')


INTENT_BY_ID = 'Obtener detalle de receta'
INTENT_BY_INGREDIENTS = 'Peticion de receta por ingredientes'


@app.route('/')
def index():
    return "Hello world!"


@app.route('/<id>')
def get_recipe(id):
    recipe = _get_recipe_by_id(int(id))
    return recipe.to_json()


@app.route('/webhook', methods=['POST'])
def process_webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']

    if intent == INTENT_BY_ID:
        id = req['queryResult']['parameters']['recipe_id']
        recipe = _get_recipe_by_id(int(id))
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [str(recipe)]
                    }
                }
            ],
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": str(recipe)
                                }
                            }
                        ],
                    }
                }
            }
        }
    elif intent == INTENT_BY_INGREDIENTS:
        ingredients = req['queryResult']['parameters']['ingredients']
        recipes = _get_recipes_by_ingredients(ingredients)
        recipes_str = list(map(lambda r: str(r), recipes))
        recipes_carousel = list(map(lambda r: r.to_carousel_item(), recipes))
        recipes_suggestions = list(map(lambda r: r.to_suggestion(), recipes))

        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": recipes_str
                    }
                }
            ],
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Estas son algunas recetas con los ingredientes que mencionaste:"
                                }
                            },
                            {
                                "carouselBrowse": {
                                    "items": recipes_carousel
                                }
                            },
                            {
                                "simpleResponse": {
                                    "textToSpeech": "¿De cual te gustaria ver detalles?"
                                }
                            }
                        ],
                        "suggestions": recipes_suggestions
                    }
                }
            }
        }
    else:
        recipes = _get_random_recipes()
        recipes_str = list(map(lambda r: str(r), recipes))
        recipes_carousel = list(map(lambda r: r.to_carousel_item(), recipes))
        recipes_suggestions = list(map(lambda r: r.to_suggestion(), recipes))

        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": recipes_str
                    }
                }
            ],
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Te recomiendo las siguientes recetas:"
                                }
                            },
                            {
                                "carouselBrowse": {
                                    "items": recipes_carousel
                                }
                            },
                            {
                                "simpleResponse": {
                                    "textToSpeech": "¿De cual te gustaria ver detalles?"
                                }
                            }
                        ],
                        "suggestions": recipes_suggestions
                    }
                }
            }
        }


def _get_random_recipes() -> list:
    recipes_df = df.sample(n=5)
    recipes = [(Recipe.from_series(row)) for _, row in recipes_df.iterrows()]
    return recipes


def _get_recipe_by_id(id) -> Recipe:
    recipe_series = df[df['id'] == id].iloc[0]
    return Recipe.from_series(recipe_series)


def _get_recipes_by_ingredients(ingredients: list) -> list:
    recipes_df = df[df['ingredients'].str.contains('|'.join(ingredients))].sample(n=5)
    recipes = [(Recipe.from_series(row)) for _, row in recipes_df.iterrows()]
    return recipes


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port='9000', debug=True)