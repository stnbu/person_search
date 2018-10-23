
## Using Person Search

This set of scripts and Python packages meet the requirements of the following programming challenge:

```
Challenge Brief

In this role you’ll be building secure tools to identify the gender,
educational background, university/schools attended, work experience,
location, certifications/ courses, etc of a person, given their name
and email address.

Given the full name and email address of a person, build a web
scraping tool in Python that identifies the following information: -
gender - degree(s) earned (MS/BS/ BA, etc) - universities/ schools
attended

The tool should be capable of reporting the number of people with a
Master’s degree in the form of pie chart.

You may use existing open source or publicly available technologies/
APIs to build this tool.

To check if the tool is accurate use the attached csv file (in View
Resources) of 50 names and emails for testing. Your tool should aim to
accurately identify details for 7 out 10 profiles.

The profile values should be encrypted and stored in a postgres db.

Include a README.md and a design document for your prototype.
```

Helper scripts are provided to do integration testing, see instructions and design document below.

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
System Version:	macOS 10.13.3
Kernel Version:	Darwin 17.4.0
Model Name:	MacBook Air
Model Identifier:	MacBookAir7,2
```

(In the case of OSX you will likely need to modify the ``psql`` command in ``person_search/scripts/mkdb.sh`` to something like ``psql template1``.)

Quick Start
===========

The following assumes that the current working directory is the ``person_search`` package directory (the root of the tarball).

First install in "editable" mode

```bash
pip install -e .
```

This should download and install the required Python packages (feel free to use a virtualenv).

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

The instructions for testing with PostgreSQL are identical, but you would instead set ``PERSON_SEARCH_RDBMS=POSTGRES`` and ``./person_search/scripts/mkdb.sh`` is used instead of ``./person_search/scripts/sqlite-from-zero.sh`` to prep the database. See ``person_search/scripts/*`` for details.


About The Design
================

With only five days I had to make some decisions and sacrifice some features and elegance for the sake of time. Here are some of the relevant decisions:

Scraping
--------

As far as I can tell https://rapportive.com/ was acquired by Linkedin and is no longer free to use. If this is a REST API that provides structured results, then the problem is easy. If it provides *part* of the answer and some scraping and crawling is required, that requires a bit of work. But generalized scraping for this kind of information is hard. There is ongoing development in this domain and a truly *general* solution probably would be a huge project requiring some "AI". I chose to focus on other aspects of the exercise and demonstrate some simple scraping in my solution. Everything else is implemented per the specs.

This package scrapes and parses my own contrived "profile" web pages hosted by the built-in Django web server. These are intentionally designed to be easy to parse.

If an email from the sample data is queried, the corresponding sample data is returned. If any other (random) email address is queried, random data is generated and returned.

Once the web server is running, you can check out both [random results](http://127.0.0.1:8000/person_profile/foo@bar.com) and [results from the supplied data](http://127.0.0.1:8000/person_profile/rini.joseph@colorado.edu/).

If I were implementing a more complex scraper I would consider:

* Logic to narrow down the possibilities
* Per-domain scraping "drivers": Have a custom scraper for Facebook and a custom scraper for Linkedin with exactly the same interface (which would be documented).
* Logic flows like "if Linkedin member check github" ...
* Trying to learn more about the state of the art with regard to scraping and google searching with a [home-grown API](https://pypi.org/project/google/).

ORM
---

Since we're talking about using the data "outside" of Django, I monkey-patched things so that I could re-use the *Django* ORM and configuration in plain Python (the scraping in other words). There are many possibilities here and they all depend on the requirements. Things that come to mind:

* Have the scraper write to a separate db and have things synchronized using an AMQP. The scrapers run in a "farm" collecting queries and reply back to the queue with some structured result. The web UI and/or the database would be participating in that queue, inserting the queries and waiting for responses (asynchronously).
* Use a separate ORM for scraper I/O. Something like sqlalchemy is robust and well-tested and would have fewer risks, since it doesn't look like the Django ORM is often used this way. The downside is maintaining two schema (table classes), etc.
* The pie chart should be implemented in the browser. We could just return a single number and let JavaScript do the rest. I chose to implement everything in Python.

Scaling
-------

I have no idea how much scaling we'd be expected to do. The design would vary depending on the answer. For a more robust PoC that scales reasonably I would consider simple PostgreSQL clustering. That wold not improve write performance, but that would be slower so we might not care. Some kind of CDN for anything static or cachable. Django would be running in some "clustered" fashion. Minimally Django would be running behind a fast, secure web server like NGINX. On the web side of things, db access would be read-only (so clustering improves performance there) so minimally we would have a separate PostgreSQL user for that, but having something else running that has write access to the same database is sketchy. It needs to get updated *somehow* and that is some security "surface area" to keep in mind.

Encryption
----------

Whether this is a good idea or not depends on the requirements. In most cases, I'd question the benefit. Some process has clear access to that database via some kind of encryption and that's where an attacker would attack. So encryption gets you nothing unless someone breaks in the hard way (but why do that)?

That's not to say there are no use cases for it. It would be an interesting discussion and at worst it complicates and slows things down. I could be wrong after all!!

I chose to use symmetric encryption since having the private key on the system (say in memory) and having a secret on the system are pretty much the same thing security-wise. There are use cases for asymmetric encryption. I just don't know if this is one of them. Also, the **the encryption should live in the database** most likely. I wrote it into the ORM, which for performance and design reasons is a poor choice, at least in my implementation. Searching the data is greatly complicated, we can search by encrypted output and that's what I did, but 1) it must be encryption that results in the same output for any given input, otherwise searching and querying get **REALLY** complicated and 2) it should probably be done at the RDBMS level. I didn't investigate that for the sake of time.

And because my first encryption implementation (``person_search.crypto.crypt()``) doesn't satisfy the first point above, I was unable to use it. So I created a trivial rot13 based "encryption" as a stand-in so in some weak sense, the data is "encrypted". Since this was fast, I had no caching concerns (see below.)

In production I would investigate PostgreSQL's encryption options, which are [well documented](https://www.postgresql.org/docs/current/static/encryption-options.html).

Caching
-------

At a big enough scale I'm pretty sure we'd need to cache and if we did that, we're now sitting around with unencrypted data, whether in memory or on disk. That has more security implications. So, again, I'd at least have another look at just building for security (as in preventing attacks) instead of encryption. Need more info to understand the requirements.

I did **no** caching at all because that's not hard to add, even a module-level ``dict`` would be a big improvement if we had real encryption with more data.

Testing
-------

I have done minimal testing due to time constraints. Some Django unit tests have been implemented and the different utility scripts provide a measure of "integration testing".

Misc
----

A list of smaller "todos" and remarks about the implementation:

* Imports should be done in a smart, consistent way. I import ``person_search`` by name everywhere for now. It might be cleaved off as a separate package anyhow. All things being equal, just "best practices" is a good idea.
* I assume that for a given email, the scraped data never changes. This both simplifies things and speeds things up. In production, we might want to periodically check for updates: if a record has "expired", add that email address to the queue of addresses to be scraped.
* I also chose to use some off-the-shelf 3rd party libraries, which I think should be avoided if possible. It's ok to use some 3rd party libraries, but if they're not well maintained, be prepared to completely understand and *own* them indefinitely.
* Encryption as it's implemented adds a large amount of overhead. This also fixed by encrypting at the RDBMS-level.

Resources
=========

* https://www.postgresql.org/docs/current/static/encryption-options.html
* https://aeroleads.com/blog/how-to-find-email-address-of-anyone-from-linkedin/
* https://docs.djangoproject.com/en/2.1/howto/custom-model-fields/
* https://www.smashingmagazine.com/2015/07/designing-simple-pie-charts-with-css/
* https://stackoverflow.com/questions/31481272/python-linkedin-api-how-do-i-use-it
* https://stackoverflow.com/questions/17600244/how-to-use-linkedin-api-with-python
* https://www.linkedin.com/developer/apps/7010964/auth
* https://developer.linkedin.com/docs/oauth2