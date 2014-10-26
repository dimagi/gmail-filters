from . import jsonschemas
from collections import defaultdict
import jinja2
from gmailfilterrecipes.jsonschemas import FILTER_KEY_TO_TYPE
from gmailfilterxml import GmailFilter


def generate_gmail_filters(recipe, options, option_values, id_prefix):
    """
    Args:
        recipe (jsonschema.Recipe)
        options (list of jsonschema.RecipeOption)
        option_values (dict of string => string)
    """

    options_by_key = {option.key: option for option in options}
    all_options = ([options_by_key[option_key]
                    for option_key in recipe.options] + recipe.custom_options)
    match = recipe.match
    filters = list(recipe.filters)

    for option in all_options:
        if option.filters and option_values.get(option.key):
            filters.extend(option.filters)

    gmail_filters = []
    for i, filter in enumerate(filters):
        id = '{}{}{}'.format(id_prefix, recipe.id, i)
        kwargs = defaultdict(list)
        for key, value in filter.items() + match.items():
            if isinstance(value, basestring):
                # it's a jinja2 template
                value = jinja2.Template(value).render(**option_values)
            kwargs[key].append(value)
        for key, value in kwargs.items():
            if FILTER_KEY_TO_TYPE[key] == basestring:
                kwargs[key] = ' AND '.join(value)
            elif FILTER_KEY_TO_TYPE[key] == bool:
                assert len(kwargs[key]) == 1, kwargs[key]
                kwargs[key], = value
            else:
                assert False
        gmail_filters.append(GmailFilter(id=id, **kwargs))
    return gmail_filters
