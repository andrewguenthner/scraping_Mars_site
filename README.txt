Files for a Flask website / app that scrapes public domain Mars data and 
displays it on a web page, with storage via a Mongo DB. Intended for use
as a web scraping demo.  

Requirements:
-- Mongo DB server 
-- Flask server (development version)
-- flask and flask_pymongo libraries for server
-- requests, bs4 (Beautiful Soup), and splinter (0.1) for scraping
-- pandas (0.23) for table scraping and handling
The system is configured to use ChromeDriver on Windows 10 for scraping

Files:
-- app.py contains the Flask routines
-- scrape_mars.py is imported by app.py and contains the scraping routines
-- mission_to_mars.jpynb contains the code snippets and tests for scraping
-- chromedriver.exe is provided for scraping.  Scraping is not configured
in headless mode, so that the user can see what's happening.
The folder "templates" contains the default route page "index.html"
The folder "static" contains "style.css" for overriding the included
Bootstrap 4.0 styling in places
The folder "op_images" contains screenshots of the server and web site
in action for validation purposes

Notes:
The data is scraped from public domain sites of the United States government
with the exception of space-facts.com, which itself gets it data from 
the United States government.  The space-facts data table ("Mars facts")
is collected from https://space-facts.com/mars/, and was originally
put together by the site owner, Chris Jones.  

This is a deliberate choice as data from government agencies is cleared
for public release without copyright.  The images used in the site are
also United States government images cleared for public release. Because
most Executive Branch agencies of the United States government have been
directed to make their publicly releaseable data widely available, I see
no issue whatsoever with scraping their site contents via GET type
requests and aggregating it.  As an 18-year veteran of the Federal civil 
service and a Code for America volunteer, I can assure you that in the 
vast majority of cases, these agencies would like to do a better job of
getting their data widely used but are hindered by bureuacracy, poor
contracting practices (the lowest bidder probably didn't put too much
thought into making the data widely accessable), and other pressing
concerns (e.g. cyberattacks).  By learning to scrape their sites and
repackage their data in a nicer form, you are doing them a favor, so I
encourage you to learn from this example and give it a try!  Just please
be considerate and don't overload their servers or cause problems.
As for space-facts.com, if you're going to do anything other than occasionally
copy and re-use the government data on the site, then you should check
with the site owner.  

The site uses Bootstrap 4.0 for styling, and includes some scripts, so
you should be able to add any other Bootstrap classes without needing
to edit the header or footer.  

Both splinter and requests.get are used for scraping.  Splinter can
be made to run headless, but, as configured, you will see a new instance
of Chrome appear on your desktop, and Chrome should warn you that it is
being driven remotely.  Even if scraping is unsuccessful, the browser
should close itself after a minute.

The database dictionaries contain success flags and timestamps for
each scraping activity.  These are not displayed in the site but are
available as pagedata.mars_[x].success and pagedata.mars-[x].when_visited
attributes (where [x] denotes the scraped item (e.g. "featured_image",
"weather_tweet", and so on.  

The test items scraped are the latest Mars news blurb from JPL, the 
latest featured image from JPL, the latest weather tweet (these days
from Mars Insight), the Mars facts table (from space-facts.com), and 
enhanced Mars hemisphere images from the US Geological Service.  The
server code is designed to fail gracefully, so that if the scraping
fails then the site will still display, but you will see placeholder
content.  This makes it much easier to locate the problem.  Note that
some sites can have temporary downtime, so you may on occasion get
placeholder content even if the code is working perfectly.  Also note
that web sites change over time, so at some point this code will become
out-dated.  There are plenty of other scraping demos out there, so I
offer no long-term committment to maintain the functionality of the demo,
and I may archive or delete this repository at any time, so please 
clone it if you want it to remain available.  

The site is configured to run on localhost:5000.  It has been tested
with Chrome v74 on Windows 10 only. 


