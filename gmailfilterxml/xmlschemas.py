import functools
from eulxml.xmlmap import (
    XmlObject,
    OrderedXmlObject,
    StringField,
    NodeListField,
)
from eulxml.xmlmap.fields import SingleNodeManager, Field


NS = {
    'apps': 'http://schemas.google.com/apps/2006',
    'atom': 'http://www.w3.org/2005/Atom'
}


def validate_entry_id(id):
    assert isinstance(id, basestring)
    assert len(id) == 13
    assert all(c in '0123456789' for c in id)
    return id


class EntryIdMapper(object):
    PREFIX = 'tag:mail.google.com,2008:filter:'

    def to_xml(self, value):
        if value is None:
            return None
        id = validate_entry_id(value)
        return '{}{}'.format(self.PREFIX, id)

    def to_python(self, value):
        assert value.startswith(self.PREFIX)
        id = value[len(self.PREFIX):]
        return validate_entry_id(id)


class EntryIdListMapper(object):
    PREFIX = 'tag:mail.google.com,2008:filters:'

    def to_xml(self, value):
        if value is None:
            return None
        ids = [validate_entry_id(id) for id in value]
        return '{}{}'.format(self.PREFIX, ','.join(ids))

    def to_python(self, value):
        assert value.startswith(self.PREFIX)
        ids = value[len(self.PREFIX):].split(',')
        return [validate_entry_id(id) for id in ids]


class UTCDateTimeMapper(object):
    def to_xml(self, value):
        if value is None:
            return None
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_python(self, value):
        import datetime
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


SingleNodeField = functools.partial(Field, manager=SingleNodeManager())
EntryIdField = functools.partial(SingleNodeField, mapper=EntryIdMapper())
EntryIdListField = functools.partial(SingleNodeField,
                                     mapper=EntryIdListMapper())
UTCDateTimeField = functools.partial(SingleNodeField,
                                     mapper=UTCDateTimeMapper())

class EntryProperty(XmlObject):

    ROOT_NAME = 'property'
    ROOT_NS = NS['apps']

    name = StringField('@name')
    value = StringField('@value')


class Entry(OrderedXmlObject):
    ROOT_NAME = 'entry'
    ROOT_NAMESPACES = NS
    ROOT_NS = NS['atom']
    ORDER = ('category_term', 'title', 'id', 'updated', 'content',
             'properties')

    category_term = StringField('atom:category/@term')
    title = StringField('atom:title')
    id = EntryIdField('atom:id')
    updated = UTCDateTimeField('atom:updated')
    content = StringField('atom:content')
    properties = NodeListField('apps:property', EntryProperty)

    def __init__(self, node=None, context=None, **kwargs):
        if node is None:
            if 'category_term' not in kwargs:
                kwargs['category_term'] = 'filter'
            if 'title' not in kwargs:
                kwargs['title'] = 'Mail Filter'
            if 'content' not in kwargs:
                kwargs['content'] = ''
        super(Entry, self).__init__(node, context, **kwargs)


class Feed(OrderedXmlObject):

    ROOT_NAME = 'feed'
    ROOT_NS = NS['atom']
    ROOT_NAMESPACES = NS
    ORDER = ('title', 'ids', 'updated', 'author_name', 'author_email',
             'entries')

    title = StringField('atom:title')
    ids = EntryIdListField('atom:id')
    updated = UTCDateTimeField('atom:updated')
    author_name = StringField('atom:author/atom:name')
    author_email = StringField('atom:author/atom:email')
    entries = NodeListField('entry', Entry)

    def __init__(self, node=None, context=None, **kwargs):
        if node is None and 'title' not in kwargs:
            kwargs['title'] = 'Mail Filters'
        super(Feed, self).__init__(node, context, **kwargs)
