import yaml
import os
from unittest import TestCase
from gmailfilterrecipes import jsonschemas
from gmailfilterrecipes.jsonschemas import Recipe, RecipeOption
from gmailfilterrecipes.xmlgeneration import generate_gmail_filters
from gmailfilterxml import GmailFilter
from utils.unittest import XmlTest


class TestJsonSchemasTest(TestCase):
    def test(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'available-filters.yml')) as f:
            recipe_set = yaml.load(f)
        self.assertIsInstance(recipe_set, dict)
        self.assertDictEqual(
            jsonschemas.RecipeSet.wrap(recipe_set).to_json(), recipe_set)


class XmlGenerationTest(XmlTest):

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        cls.archive_option = RecipeOption({
            'key': 'archive',
            'label': 'Do you want to see these in your inbox?',
            'type': 'inverted-bool',
            'filters': [
                {
                    'to': '-me',
                    'shouldArchive': True
                }
            ],
        })
        cls.id_prefix = '346244'

    def _test(self, recipe, expected_gmail_filters, option_values):
        recipe = Recipe.wrap(recipe)
        expected_gmail_filters = [GmailFilter(**kwargs)
                                  for kwargs in expected_gmail_filters]
        self.assertListEqual(
            generate_gmail_filters(recipe, [self.archive_option],
                                   option_values, id_prefix=self.id_prefix),
            expected_gmail_filters,
        )

    def test_label_and_archive(self):
        recipe = yaml.load("""
            label: Uservoice
            id: '000004'
            options:
              - archive
            match:
              to: dev+uservoice@dimagi.com
            filters:
              - label: UserVoice
        """)
        expected_gmail_filters = yaml.load("""
            - id: '3462440000040'
              to: dev+uservoice@dimagi.com
              label: UserVoice

            - id: '3462440000041'
              to: -me AND dev+uservoice@dimagi.com
              shouldArchive: yes
        """)
        self._test(recipe, expected_gmail_filters, {'archive': True})

    def test_timecards(self):
        recipe = yaml.load("""
            label: Timecards
            id: '000001'
            custom_options:
              - key: names
                label: "Whose timecards do you want to see?"
                type: list
            match:
              from: reports@dimagi.com
            filters:
              - label: Timecard
              - subject: '{% for name in names %}-"{{ name }}" {% endfor %}'
                shouldArchive: true
        """)
        expected_gmail_filters = yaml.load("""
            - id: '3462440000010'
              from: reports@dimagi.com
              label: Timecard
            - id: '3462440000011'
              from: reports@dimagi.com
              subject: '-"sheffels" -"danny" '
              shouldArchive: yes
        """)
        self._test(recipe, expected_gmail_filters,
                   {'names': ['sheffels', 'danny']})
