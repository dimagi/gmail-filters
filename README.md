# Gmail Filters


## Install

To install requirements:

```bash
pip install -r requirements.txt
```

## Usage

Create a simple gmail filter:

```python
>>> from gmailfilterxml import GmailFilterSet, GmailFilter
>>> import datetime
>>>
>>>
>>> filter_set = GmailFilterSet(
...     author_name='Danny Roberts',
...     author_email='droberts@dimagi.com',
...     updated_timestamp=datetime.datetime(2014, 9, 19, 17, 40, 28),
...     filters=[
...         GmailFilter(
...             id='1286460749536',
...             from_='noreply@github.com',
...             label='github',
...             shouldArchive=True,
...         )
...     ]
... )
>>> print filter_set.to_xml(pretty=True),
<?xml version='1.0' encoding='UTF-8'?>
<atom:feed xmlns:apps="http://schemas.google.com/apps/2006" xmlns:atom="http://www.w3.org/2005/Atom">
  <atom:title>Mail Filters</atom:title>
  <atom:id>tag:mail.google.com,2008:filters:1286460749536</atom:id>
  <atom:updated>2014-09-19T17:40:28Z</atom:updated>
  <atom:author>
    <atom:name>Danny Roberts</atom:name>
    <atom:email>droberts@dimagi.com</atom:email>
  </atom:author>
  <atom:entry>
    <atom:category term="filter"/>
    <atom:title>Mail Filter</atom:title>
    <atom:id>tag:mail.google.com,2008:filter:1286460749536</atom:id>
    <atom:updated>2014-09-19T17:40:28Z</atom:updated>
    <atom:content></atom:content>
    <apps:property name="from" value="noreply@github.com"/>
    <apps:property name="label" value="github"/>
    <apps:property name="shouldArchive" value="true"/>
  </atom:entry>
</atom:feed>
>>>
```
