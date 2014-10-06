import jsonobject
import gmailfilterxml


class Base(jsonobject.JsonObject):
    _allow_dynamic_properties = False


FILTER_KEY_TO_TYPE = {
    xml_name: py_type
    for xml_name, py_name, py_type in gmailfilterxml.PROPERTIES
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
