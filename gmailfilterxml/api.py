

class FilterSet(object):
    def __init__(self, author_name, author_email, updated_timestamp, filters=None):
        self.author_name = author_name
        self.author_email = author_email
        self.updated_timestamp = updated_timestamp
        self.filters = filters if filters is not None else []


class GmailFilter(object):
    def __init__(self, from_=None, label=None, should_archive=None):
        self.from_ = from_
        self.label = label
        self.should_archive = should_archive
