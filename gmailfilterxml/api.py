from . import xmlschemas


class GmailFilterSet(object):
    def __init__(self, author_name, author_email, updated_timestamp,
                 filters=None):
        self.author_name = author_name
        self.author_email = author_email
        self.updated_timestamp = updated_timestamp
        self.filters = filters if filters is not None else []

    def to_xml(self):
        updated = self.updated_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

        def yield_properties():
            if gmail_filter.from_:
                yield 'from', gmail_filter.from_
            if gmail_filter.label:
                yield 'label', gmail_filter.label
            if gmail_filter.should_archive:
                yield 'shouldArchive', 'true'

        entries = [
            xmlschemas.Entry(
                id=('tag:mail.google.com,2008:filter:{}'
                    .format(gmail_filter.id)),
                updated=updated,
                properties=[xmlschemas.EntryProperty(name=name, value=value)
                            for name, value in yield_properties()]
            )
            for gmail_filter in self.filters
        ]

        feed = xmlschemas.Feed(
            author_name=self.author_name,
            author_email=self.author_email,
            updated=updated,
            id=('tag:mail.google.com,2008:filters:{}'
                .format(','.join(gmail_filter.id
                                 for gmail_filter in self.filters))),
            entries=entries
        )

        return feed.serializeDocument()


class GmailFilter(object):
    def __init__(self, id=None, from_=None, label=None, should_archive=False):
        assert isinstance(id, basestring)
        assert len(id) == 13
        assert all(c in '0123456789' for c in id)
        self.id = id
        self.from_ = from_
        self.label = label
        assert should_archive in (False, True)
        self.should_archive = should_archive
