from . import xmlschemas

PROPERTIES = (
    ('from', 'from_', basestring),
    ('subject', 'subject', basestring),
    ('hasTheWord', 'has_the_word', basestring),
    ('to', 'to', basestring),
    ('doesNotHaveTheWord', 'does_not_have_the_word', basestring),
    ('label', 'label', basestring),
    ('shouldArchive', 'should_archive', bool),
    ('shouldMarkAsRead', 'should_mark_as_read', bool),
    ('shouldNeverSpam', 'should_never_spam', bool),
    ('shouldAlwaysMarkAsImportant', 'should_always_mark_as_important', bool),
)


class GmailFilterSet(object):
    def __init__(self, author_name, author_email, updated_timestamp,
                 filters=None):
        self.author_name = author_name
        self.author_email = author_email
        self.updated_timestamp = updated_timestamp
        self.filters = filters if filters is not None else []

    def to_xml(self):

        def yield_properties(g):
            for xml_name, py_name, py_type in PROPERTIES:
                value = getattr(g, py_name)
                if value:
                    if py_type is bool:
                        yield xml_name, 'true'
                    else:
                        yield xml_name, value

        entries = [
            xmlschemas.Entry(
                id=gmail_filter.id,
                updated=self.updated_timestamp,
                properties=[xmlschemas.EntryProperty(name=name, value=value)
                            for name, value in yield_properties(gmail_filter)]
            )
            for gmail_filter in self.filters
        ]

        feed = xmlschemas.Feed(
            author_name=self.author_name,
            author_email=self.author_email,
            updated=self.updated_timestamp,
            ids=[gmail_filter.id for gmail_filter in self.filters],
            entries=entries,
        )

        return feed.serializeDocument()


class GmailFilter(object):
    def __init__(self, id=None, **kwargs):
        unknown_kwargs = (
            set(kwargs.keys())
            - {py_name for _, py_name, _ in PROPERTIES}
        )
        if unknown_kwargs:
            raise TypeError(
                "__init__() got an unexpected keyword argument '{}'"
                .format(list(unknown_kwargs)[0])
            )
        xmlschemas.validate_entry_id(id)
        self.id = id

        for xml_name, py_name, py_type in PROPERTIES:
            if py_type is bool:
                kwargs[py_name] = kwargs.get(py_name) or False
                assert isinstance(kwargs[py_name], bool)
            setattr(self, py_name, kwargs.pop(py_name, None))
