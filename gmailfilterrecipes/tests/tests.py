import datetime
import yaml
import os
from unittest import TestCase
from gmailfilterrecipes import jsonschemas
from gmailfilterrecipes.jsonschemas import (
    UserRecipe,
    UserRecipeOption,
    UserRecipeSet,
)
from gmailfilterrecipes.xmlgeneration import (
    generate_gmail_filters,
    generate_gmail_fitler_set,
)
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
        cls.archive_option = UserRecipeOption(yaml.load("""
            key: archive
            label: Do you want to see these in your inbox?
            type: inverted-bool
            filters:
              - to: -me
                shouldArchive: yes
            value: yes
        """))
        cls.id_prefix = '346244'

    def _test(self, recipe, expected_gmail_filters):
        recipe = UserRecipe.wrap(recipe)
        expected_gmail_filters = [GmailFilter(**kwargs)
                                  for kwargs in expected_gmail_filters]
        self.assertListEqual(
            generate_gmail_filters(recipe, id_prefix=self.id_prefix),
            expected_gmail_filters,
        )

    def test_label_and_archive(self):
        recipe = yaml.load("""
            label: Uservoice
            id: '000004'
            options: []
            match:
              to: dev+uservoice@dimagi.com
            filters:
              - label: UserVoice
        """)
        recipe['options'].append(self.archive_option.to_json())
        expected_gmail_filters = yaml.load("""
            - id: '3462440000040'
              to: dev+uservoice@dimagi.com
              label: UserVoice

            - id: '3462440000041'
              to: -me AND dev+uservoice@dimagi.com
              shouldArchive: yes
        """)
        self._test(recipe, expected_gmail_filters,)

    def test_timecards(self):
        recipe = yaml.load("""
            label: Timecards
            id: '000001'
            options:
              - key: names
                label: "Whose timecards do you want to see?"
                type: list
                value: ['sheffels', 'danny']
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
        self._test(recipe, expected_gmail_filters)

    def test_generate_gmail_filter_set(self):
        with open(os.path.join(os.path.dirname(__file__),
                               'data', 'user_recipe_set.yml')) as f:
            filter_set = generate_gmail_fitler_set(
                UserRecipeSet.wrap(yaml.load(f)),
                updated_timestamp=datetime.datetime(2014, 10, 27, 2, 20, 58)
            )
        with open(os.path.join(os.path.dirname(__file__),
                               'data', 'filters.xml')) as f:
            expected_xml = f.read()

        self.assertXmlEqual(filter_set.to_xml(pretty=True), expected_xml)
