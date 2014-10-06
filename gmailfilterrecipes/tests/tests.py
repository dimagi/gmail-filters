import yaml
import os
from unittest import TestCase
from gmailfilterrecipes import jsonschemas


class TestJsonSchemas(TestCase):
    def test(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'available-filters.yml')) as f:
            recipe_set = yaml.load(f)
        self.assertIsInstance(recipe_set, dict)
        self.assertDictEqual(
            jsonschemas.RecipeSet.wrap(recipe_set).to_json(), recipe_set)
