# Gmail Filters

Python library and simple web app for creating GMail filters.

See [GMail help](https://support.google.com/mail/answer/6579) for info on importing filters into GMail.

## Install

To install requirements:

```bash
pip install -r requirements.txt
npm install -g coffee-script
```

## Compile Coffee

```bash
coffee --compile gmailfilterrecipes/client/static/coffee/*.coffee
```


## Run

Just run

```bash
python run_server.py
```

and the web frontend should be running at http://localhost:8080/.

## Configure your recipeset

Each organization or team within an organization will have a different set of filters that are relevant to them;
each member of that team may then want to further tweak the base set to conform to their particular needs. For example,
everyone may want a basic filter labeling emails that contain their name, but each person's name is different, so each person's
filter must be tweaked accordingly.

In this framework, the shared filter descriptions are codified as "recipe sets", which are then displayed to the individual through
a web interface, so that they may customize it to themself by simply filling out a web form.

An example recipe set (which is used by the dev team at Dimagi) is included in this repo at `recipesets/default.yml`.
To use your own instead, simply change the `gmailfilterrecipes.filters_yml` option in `settings.ini` to point to your own.

A recipeset yaml file has two toplevel components, `options` and `recipes`: `options` let you specify filter options that can be shared
across all your recipes, which are then defined under `recipes`. A recipe looks somethin like this:

```yaml
    -
        label: Mails directly to me
        custom_options:
            -
                key: names
                label: "List your email addresses"
                type: list
        match:
            to: "{{ names|join(' OR ') }}"
        filters:
            - label: =^.^=
              shouldNeverSpam: true
              shouldAlwaysMarkAsImportant: true
```

Each recipe specifies a row in the web form that will be shown to the individual. In this case, that row would be labelled
"Mails directly to me", they would require the individual to specify a list of email addresses (could also be just a single one),
and would create a filter that matches on those emails, applies a gmail label named "=^.^=", keeps it from going to spam,
and marks it as important.

## Library Usage

If you aren't interested in the front end, you can use `gmailfilterxml`
as a library for reading and writing gmail filter xml files.

To create a simple gmail filter:

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
