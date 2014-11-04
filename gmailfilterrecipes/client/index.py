# coding: utf-8
import json
import bottle
import yaml
from gmailfilterrecipes.jsonschemas import UserRecipeSet, RecipeSet
from gmailfilterrecipes.xmlgeneration import generate_gmail_fitler_set


@bottle.route('/')
def index():
    return bottle.static_file('index.html',
                              root='gmailfilterrecipes/client/static/html/')


@bottle.route('/filters.json')
def filters_json():
    with open('recipesets/default.yml') as f:
        filters = yaml.load(f)
    user_recipe_set = UserRecipeSet.from_recipe_set(RecipeSet.wrap(filters))
    return json.dumps(user_recipe_set.to_json())


@bottle.post('/filters.xml')
def filters_xml():
    bottle.response.headers.update({
        'Content-Type': 'application/xml; charset="utf-8"',
        'Content-Disposition': 'attachment; filename="gmailFilters.xml"',
    })

    recipe_set_json = (
        bottle.request.json
        or json.loads(bottle.request.POST.get('recipeSet'))
    )
    user_recipe_set = UserRecipeSet.wrap(recipe_set_json)
    gmail_filter_set = generate_gmail_fitler_set(user_recipe_set)

    return gmail_filter_set.to_xml(pretty=True)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='gmailfilterrecipes/client/static')
