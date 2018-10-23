
## Using Person Search

This set of scripts and python packages meet the requirements of the following programming challenge:

```
Challenge Brief

In this role you’ll be building secure tools to identify the gender, educational background, university/schools attended, work experience, location, certifications/ courses, etc of a person, given their name and email address.

Given the full name and email address of a person, build a web scraping tool in Python that identifies the following information:
- gender
- degree(s) earned (MS/BS/ BA, etc)
- universities/ schools attended

The tool should be capable of reporting the number of people with a Master’s degree in the form of pie chart.

You may use existing open source or publicly available technologies/ APIs to build this tool.

To check if the tool is accurate use the attached csv file (in View Resources) of 50 names and emails for testing. Your tool should aim to accurately identify details for 7 out 10 profiles.

The profile values should be encrypted and stored in a postgres db.

Include a README.md and a design document for your prototype.
```

Helper scripts are provided to do integration testing, see instructions below.

Requirements to Run
===================

* Python >= 3.5
* ``pip``
* Internet access
* A working PostgreSQL installation and sudo access

Tested on

```
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.1 LTS
Release:	18.04
Codename:	bionic
```

and

```
OS-X
```

Quick Start
===========

The following assumes that the current working directory is the ``person_search`` package directory (the root of the tarball).

First install in "editable" mode

```bash
pip install -e .
```

This should download and install the required python packages (feel free to use a virtualenv).

Sqlite
------

To run a quick "integration" test using Sqlite3 (will write to ``/tmp``) first "make clean"...

```bash
export PERSON_SEARCH_RDBMS=SQLITE
./person_search/scripts/sqlite-from-zero.sh
```

Then run the web server...

```bash
python manage.py runserver
```

In another terminal...
```bash
export PERSON_SEARCH_RDBMS=SQLITE
DJANGO_SETTINGS_MODULE='person_search.settings' python person_search/scrape.py
```

This script takes an iterable of email addresses as input and uses the Django ORM (hence the environment variable) to scrape user profile web pages and writes results to the configured database. We assume a 1:1 mapping between "full name" and "email" and therefore the email address alone is sufficient for scraping.

Once complete, you can visit the pie chart to view the results of "persons with masters" at

* [http://127.0.0.1:8000/pie/](http://127.0.0.1:8000/pie/)

PostgreSQL
----------

The instructions for testing with PostgreSQL are identical, but you would insead set ``PERSON_SEARCH_RDBMS=POSTGRES`` and ``./person_search/scripts/mkdb.sh`` is used instead of ``./person_search/scripts/sqlite-from-zero.sh`` to prep the database. See ``person_search/scripts/*`` for details.


About The Design
================

With only five days I had to make some decisions and sacrifice some features and elegance for the sake of time. Here are some of the relevant decisions:

Scraping
--------

As far as I can tell https://rapportive.com/ was aquired by Linkedin and is no longer free to use. If this is a REST API that provides structued results, then the problem is easy. If it provides *part* of the answer and some scraping and crawling is required, that requires a bit of work. But gernalized scraping for this kind of information is hard. There is ongoing development in this domain and a truly *general* solution probaly would be a huge project requiring some "AI". I chose to focus on other aspects of the exercise and demonstrate some simple scraping in my solution. Everything eles is implemented per the specs.

This package scrapes and parses my own contrived "profile" web pages hosted by the built-in Django web server. These are intentionally designed to be easy to parse.

If a email from the sample data is queried, the correpsonding samlpe data is returned. If any other (random) email address is queried, random data is generated and returned.

Once the web server is running, you can check out both [random results](http://127.0.0.1:8000/person_profile/foo@bar.com) and [results from the supplied data](http://127.0.0.1:8000/person_profile/rini.joseph@colorado.edu/)                                               ).

If I were implementing a more complex scraper I would consider:

* Logic to narrow down the possiblities
* Per-domain scraping "drivers": Have a custom scraper for facebook and a custom scraper for linkedin with exactly the same interface (which would be documented).
* Logic flows like "if linkedin member check github" ...
* Trying to learn more about the state of the art with regard to scraping and google searching with a [home-grown API](https://pypi.org/project/google/).

ORM
---

Since we're talking about using the data "outside" of Django, I monkeypatched things so that I could use the ORM just using plain python (the scraping in other words). There are many, many possiblities here and they all depend on the requirements. Things that come to mind:

* Have the scraper write to a separate db and have things syncronized using Rabbitmq or something. The scrapers run in a "farm" collecting queryies and reply back to the queue with some structured result. The web UI and/or the database would be participating in that queue, inserting the queries and waiting for responses (asyncronously).
* Use a separate ORM for scraper I/O. Something like sqlalchemy is robust and well-tested and would have fewer risks, sinice it doesn't look like the Django ORM is often used thi way. The downside is maintaining two schemas (table classes), etc.

Scaling
-------

I have no idea how much scaling we'd be expected to do. Three per second or millions per second...? The answer varies. For a more robust PoC I would consider simple PostgreSQL clustering. That wold not improve write performance, but that would be slower so we might not care. Some kind of CDS for anything static or cachable. Django would be running in some "clustered" fashion. Minimally Django would be running behind a fast, secure web server like nginix (tbd). On the web side of things, db access would be read-only (so clustering improves performance there) so minimally we would have a separate Postgres user for that, but having something else running that has write access to the same database is sketchy. It needs to get updated *somehow* gut that is some security "surface area" to keep in mind.

Encryption
----------

Whether this is a good idea or not depends on the requirements. In most cases, I'd see it as pointless. Some process has clear read access to that database via some kind of encryption and that's where an attacker would attack. So encryption gets you nothing unless someone breaks in the hard way, but why do that?

That's not to say there are no use cases for it. It would be an interesting discussino and at worst it complicates and slows thigns down. I could be wrong afterall!!

I chose to use symmetric encryption since having the private key and having a secret are pretty much the same thing. There are use cases for asymmetric encryption. I just don't know if this is one of them. Also, the **the encryption should live in the database** most likely. I wrote it into the ORM, probably not best. Searching the data is greatly complicated, we can search by encrypted output and that's what I did, but 1) it must be encryption that results in the same output for any given input, otherwise searching and querying get **REALLY** complicated and 2) it should probably be done at the RDBMS level. I didn't investigate that for the sake of time.

And because my first implementation doesn't satisfy the first point above, I was unable to use it. Oops. So I created a trival rot13 based "encryption" as a standin so in some weak sense, the data is "encrypted". Since this was fast, I had no caching concerns (see below.)

Caching
-------

At a big enough scale I'm pretty sure we'd need to cache and if we did that, we're now sitting around with a whole bunch of unencrypted data, whether in memory or on disk. That has more security implications. So, again, I'd at least have another look at just building for security (as in preventing attacks) instead of encryption. Need more info to understand the requirements.

I did **no** caching at all because that's not hard to add, even a module-level ``dict`` would be a big improvement if we had real encryption with more data.

Testing
-------

I have done minimal testing due to time constraints. Some Django unit tests have been implemented and the different utility scripts provide a measure of "integration testing".

Misc
----

A list of smaller "todos" and remarks about the implementation:

* Imports should be done in a smart, consistent way. I import ``person_search`` by name everywhere for now. It might be cleaved off as a separate package anyhow. All things being equal, just "best practices" is a good idea.
* I assume that for a given email, the scraped data never chances. This both simplifies things and speeds things up. In production, we might want to periodically chedck for updates: if a records has "expired", add that email address to the queue of addresses to be scraped.
* I also chose to use some OTS libraries, which I think is bad practice. It's ok to use some libraries, but if they're not well maintained, be prepared to completely understand and *own* them on an ongoing basis.


 UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("html.parser"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

The code that caused this warning is on line 18 of the file person_search/scrape.py. To get rid of this warning, pass the additional argument 'features="html.parser"' to the BeautifulSoup constructor.

  soup = BeautifulSoup(content)



* Q: https://www.gapjumpers.me/questions/gapjumpers/qs-362/?utm_swu=8495
* 100 uses per
* Search google and use name from linked result
* https://aeroleads.com/blog/how-to-find-email-address-of-anyone-from-linkedin/

* data: https://docs.google.com/spreadsheets/d/12UrT3MddhdXuFbCLmZfz92W6PQCzeg1YQErdFeK_4UY/edit#gid=0

* https://docs.djangoproject.com/en/2.1/howto/custom-model-fields/

* https://www.smashingmagazine.com/2015/07/designing-simple-pie-charts-with-css/

Linkedin API
* https://stackoverflow.com/questions/31481272/python-linkedin-api-how-do-i-use-it?rq=1
* https://stackoverflow.com/questions/17600244/how-to-use-linkedin-api-with-python
* https://www.linkedin.com/developer/apps/7010964/auth
* https://developer.linkedin.com/docs/oauth2