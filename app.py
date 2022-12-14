from flask import Response
from flask import Flask
from flask import request
from recipe import Recipe

import pandas as pd


app = Flask(__name__)
df = pd.read_csv('recipes_dataset.csv', delimiter=';')

@app.route('/')
def index():
    return "Hello world!"


@app.route('/')
def get_recipe():
    pass


@app.route('/webhook', methods=['POST'])
def process_webhook():
    req = request.get_json(force=True)
    intent = req['queryResult']['intent']['displayName']

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


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port='9000', debug=True)