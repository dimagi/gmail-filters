from eulxml.xmlmap import XmlObject, StringField, NodeListField

NS = {
    'apps': 'http://schemas.google.com/apps/2006',
    'atom': 'http://www.w3.org/2005/Atom'
}


class EntryProperty(XmlObject):

    ROOT_NAME = 'property'
    ROOT_NS = NS['apps']

    name = StringField('@name')
    value = StringField('@value')


class Entry(XmlObject):
    ROOT_NAME = 'entry'
    ROOT_NAMESPACES = NS
    ROOT_NS = NS['atom']

    category_term = StringField('atom:category/@term')
    title = StringField('atom:title')
    id = StringField('atom:id')
    updated = StringField('atom:updated')
    content = StringField('atom:content')
    properties = NodeListField('apps:property', EntryProperty)

    def __init__(self, node=None, context=None, id=None, updated=None,
                 properties=None):
        super(Entry, self).__init__(node, context)
        self.category_term = 'filter'
        self.title = 'Mail Filter'
        self.id = id
        self.updated = updated
        self.content = ''
        self.properties = properties


class Feed(XmlObject):

    ROOT_NAME = 'feed'
    ROOT_NS = NS['atom']
    ROOT_NAMESPACES = NS

    title = StringField('atom:title')
    id = StringField('atom:id')
    updated = StringField('atom:updated')
    author_name = StringField('atom:author/atom:name')
    author_email = StringField('atom:author/atom:email')
    entries = NodeListField('entry', Entry)

    def __init__(self, node=None, context=None, id=None, updated=None,
                 author_name=None, author_email=None, entries=None):
        super(Feed, self).__init__(node, context)
        self.title = 'Mail Filters'
        self.id = id
        self.updated = updated
        self.author_name = author_name
        self.author_email = author_email
        self.entries = entries
