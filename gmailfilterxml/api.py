from . import xmlschemas

PROPERTIES = (
    ('from', basestring),
    ('subject', basestring),
    ('hasTheWord', basestring),
    ('to', basestring),
    ('doesNotHaveTheWord', basestring),
    ('label', basestring),
    ('shouldArchive', bool),
    ('shouldMarkAsRead', bool),
    ('shouldNeverSpam', bool),
    ('shouldAlwaysMarkAsImportant', bool),
)


class GmailFilterSet(object):
    def __init__(self, author_name, author_email, updated_timestamp,
                 filters=None):
        self.author_name = author_name
        self.author_email = author_email
        self.updated_timestamp = updated_timestamp
        self.filters = filters if filters is not None else []

    def to_xml(self, **kwargs):

        def yield_properties(g):
            for name, py_type in PROPERTIES:
                value = getattr(g, name)
                if value:
                    if py_type is bool:
                        yield name, 'true'
                    else:
                        yield name, value

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

        return feed.serializeDocument(**kwargs)


class GmailFilter(object):
    def __init__(self, id=None, **kwargs):
        # deal with from_ => from
        kwargs = {key.rstrip('_'): value for key, value in kwargs.items()}
        unknown_kwargs = (
            set(kwargs.keys())
            - {name for name, _ in PROPERTIES}
        )
        if unknown_kwargs:
            raise TypeError(
                "__init__() got an unexpected keyword argument '{}'"
                .format(list(unknown_kwargs)[0])
            )
        xmlschemas.validate_entry_id(id)
        self.id = id

        for name, py_type in PROPERTIES:
            if py_type is bool:
                kwargs[name] = kwargs.get(name) or False
                assert isinstance(kwargs[name], bool)
            setattr(self, name, kwargs.pop(name, None))
