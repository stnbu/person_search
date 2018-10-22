
About The Design
================

With only five days I had to make some decisions and sacrifice some features and elegance for the sake of time. Here are some of the relevant decisions:

Scraping
--------

Simply scrapes google and "does its best" at collecting info by follwing links in the search results and using some tricks to narrow things down. This might be a lagitamete use case for an AI, and that would only make sense on a much bigger scale because it would be a big ivestment of time (not 5 days!) Scraping data off the web, as opposed to fetching it from an API is the basis for a whole industry. There may be tricks or insider info for where this data can be found, but that would be a lot of ratholing, time that would instead be spent gathering accurate requirements in production. I also chose to use some OTS libraries, which I think is bad practice. It's ok to use some libraries, but if they're not well maintained, be prepared to completely understand and *own* them on an ongoing basis.

I think with regardto scraping or data gathering, "I did my best" sums it up best. I did send a clarification request when quried for questions by email. I didn't get a respoinse, but it that's what I expected given the nature of the question so I carried on...

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

Misc
----

A list of smaller "todos" and remarks about the implementation:

* Imports should be done in a smart, consistent way. I import ``person_search`` by name everywhere for now. It might be cleaved off as a separate package anyhow. All things being equal, just "best practices" is a good idea.
* I assume that for a given email, the scraped data never chances. This both simplifies things and speeds things up. In production, we might want to periodically chedck for updates: if a records has "expired", add that email address to the queue of addresses to be scraped.


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