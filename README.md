# Web Scraping about Mars
Using Beautiful Soup, Pandas &amp; Requests/Splinter to scrape web info, storing &amp; displaying with MongoDB &amp; Flask/HTML

Scraping the following websites for info:
- [NASA Mars News Site](https://mars.nasa.gov/news/)
- [JPL Mars Space Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
- [Mars Weather Twitter](https://twitter.com/marswxreport?lang=en)
- [Mars Facts Page](http://space-facts.com/mars/)
- [USGS Astrogeology](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

Also created a Flask app that would run the web scraping from above and pass the data into an HTML template to display the data
* Must run 'mongod' in command line for Flask app to work