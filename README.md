# Flask API for Electoral Divisions
Data taken directly from beta.data.gov.sg. Currently, this API has access only to what is on the site, aka: 2006, 2011, 2015 and 2020 electoral divisions.

## How to use
TLDR Here's a simple code snippet in Python that you can use.
```
import json
import requests
def get_grc(year,postal_code):
    url = f"https://eld-api.onrender.com/query?year={year}&postal_code={postal_code}"
    response = requests.get(url)
    return response
````

Shortcut: Run this URL in your browser, and replace the year and postal code with what you're interested in:
`https://eld-api.onrender.com/query?year=2020&postal_code=123456`

It works like any other HTTP GET request: send the year and postal code you're interested in to http://eld-api.onrender.com, and you'll get coordinates, ED (GRC/SMC) code and name, and the postal code and year that you sent in. (I might consider taking this back part off).

## What's going on 
The data from beta.data.gov.sg, in its raw form, gives coordinates as polygons (areas) that each GRC/SMC covers.
When you send in a postal code, it is converted into coordinates using the public OneMap API.
This is a single point. We figure out what polygon (area) this single point sits in.
We return the name of that polygon.

Will update with 2024 when it's out!
