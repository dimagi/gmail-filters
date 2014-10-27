from collections import defaultdict
import datetime
import jinja2
from gmailfilterrecipes.jsonschemas import FILTER_KEY_TO_TYPE
from gmailfilterxml import GmailFilter, GmailFilterSet


def generate_gmail_fitler_set(user_recipe_set, author_name=None,
                              author_email=None, updated_timestamp=None):
    gmail_filters = []
    for recipe in user_recipe_set.recipes:
        if recipe.selected:
            gmail_filters.extend(
                generate_gmail_filters(recipe, user_recipe_set.id_prefix))
    return GmailFilterSet(
        author_name=author_name,
        author_email=author_email,
        updated_timestamp=updated_timestamp or datetime.datetime.utcnow(),
        filters=gmail_filters,
    )


def generate_gmail_filters(user_recipe, id_prefix):
    """
    Args:
        recipe (jsonschema.Recipe)
        options (list of jsonschema.RecipeOption)
        option_values (dict of string => string)
    """

    match = user_recipe.match
    filters = list(user_recipe.filters)

    for option in user_recipe.options:
        if option.filters and option.value:
            filters.extend(option.filters)

    option_values = {option.key: option.value
                     for option in user_recipe.options}

    gmail_filters = []
    for i, filter in enumerate(filters):
        id = '{}{}{}'.format(id_prefix, user_recipe.id, i)
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
