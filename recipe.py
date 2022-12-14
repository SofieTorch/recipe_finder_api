import utils as ut
import pandas as pd

class Recipe:
    def __init__(self,id: int, name: str, tags: list, steps: list, ingredients: list):
        self.id = id
        self.name = name
        self.tags = tags
        self.steps = steps
        self.ingredients = ingredients


    @classmethod
    def from_series(cls, series: pd.Series):
        return cls(
            id=series[0],
            name=series[1],
            tags=ut.csv_str_to_list(series[2]),
            steps=ut.csv_str_to_list(series[3]),
            ingredients=ut.csv_str_to_list(series[4])
        )

    def to_carousel_item(self):
        return {
            'title': f'#{self.id} {self.name.capitalize()}',
            'description': f'Requires {len(self.ingredients)} ingredients',
            'footer': f'{len(self.steps)} steps',
            "openUrlAction": {
                "url": "https://example.com"
            }
        }


    def to_suggestion(self):
        return {
            'title': f'Recipe #{self.id}'
        }


    def __str__(self):
     return f'#{self.id} {self.name}'

