import jsonobject
from jsonobject.base_properties import DefaultProperty
import gmailfilterxml


class Base(jsonobject.JsonObject):
    _allow_dynamic_properties = False


FILTER_KEY_TO_TYPE = {
    name: py_type
    for name, py_type in gmailfilterxml.PROPERTIES
}


def validate_filter(filter_dict):
    for key, value in filter_dict.items():
        assert key in FILTER_KEY_TO_TYPE, (key, FILTER_KEY_TO_TYPE.keys())
        assert isinstance(value, FILTER_KEY_TO_TYPE[key]), (
            value, FILTER_KEY_TO_TYPE[key]
        )


def validate_filters(filter_dict_list):
    for filter_dict in filter_dict_list:
        validate_filter(filter_dict)


def _id_prefix_valid(value):
    assert len(value) == 6
    assert all(c in '0123456789' for c in value)


class RecipeOption(Base):
    key = jsonobject.StringProperty(required=True)
    type = jsonobject.StringProperty(required=True,
                                     choices=['list', 'bool', 'inverted-bool'])
    label = jsonobject.StringProperty(required=True)
    filters = jsonobject.ListProperty(dict, validators=validate_filters)


class Recipe(Base):
    label = jsonobject.StringProperty(required=True)
    id = jsonobject.StringProperty(validators=_id_prefix_valid)
    options = jsonobject.ListProperty(unicode)
    custom_options = jsonobject.ListProperty(RecipeOption)
    match = jsonobject.DictProperty(validators=validate_filter)
    filters = jsonobject.ListProperty(dict, validators=validate_filters)


class RecipeSet(Base):
    id_prefix = jsonobject.StringProperty(validators=_id_prefix_valid)
    options = jsonobject.ListProperty(RecipeOption)
    recipes = jsonobject.ListProperty(Recipe)


# User* are the above classes with user's responses

class UserRecipeOption(RecipeOption):
    value = DefaultProperty()


class UserRecipe(Recipe):
    selected = jsonobject.BooleanProperty()
    options = jsonobject.ListProperty(UserRecipeOption)
    custom_options = None


class UserRecipeSet(RecipeSet):
    options = None
    recipes = jsonobject.ListProperty(UserRecipe)

    @classmethod
    def from_recipe_set(cls, recipe_set):
        options_by_key = {option.key: option for option in recipe_set.options}

        def get_default_value(type):
            return {'inverted-bool': lambda: True, 'list': list}[type]()
        return UserRecipeSet(
            id_prefix=recipe_set.id_prefix,
            recipes=[
                UserRecipe(
                    selected=True,
                    label=recipe.label,
                    id=recipe.id,
                    options=[
                        UserRecipeOption(value=get_default_value(option.type),
                                         **option.to_json())
                        for option in (
                            recipe.custom_options
                            + [options_by_key[key] for key in recipe.options]
                        )
                    ],
                    match=recipe.match,
                    filters=recipe.filters,
                ) for recipe in recipe_set.recipes
            ],
        )
