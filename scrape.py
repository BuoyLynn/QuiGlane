from bs4 import BeautifulSoup
import requests

# Request HTML from URL & Return as HTML Text to parse
response = requests.get("https://freegan.info/freegan-directories/dumpster-directory/manhattan/")
soup = BeautifulSoup(response.text, "html.parser")

# Go to directory content under <div class="entry-content">
divtag = soup.find('div', attrs={"class": "entry-content"})

# Remove <em>, <strong>, <a> and <span> as they are not needed
find_ems = divtag.find_all("em")
for em in find_ems:
    em.extract()

find_strong = divtag.find_all("strong")
for strong in find_strong:
    strong.extract()

find_a = divtag.find_all("a")
for a in find_a:
    a.extract()

find_span = divtag.find_all("span")
for span in find_span:
    span.extract()

# Replace </br> with "| to ease parsing later

find_br = divtag.find_all("br")
for br in find_br:
    br.replace_with(" | ")


# get list of strings of text between <p>
directory_list_raw = []



# if <em> remove
# if <p><strong> remove


"""
<p>Bravo Supermarket<br/>
Broadway near 181st<br/>
Good selection of produce, includes some Latin American specialty items</p>, 

<p>Mike’s Bagels<br/>
4033 Broadway at W 168th Street</p>, 

<p><strong>Harlem and East Harlem</strong><br/>

<em> Know what’s happening here? Have ideas for a trailblaze? Send your ideas to <a href="mailto:ask@freegan.info">ask@freegan.info.</a></em></p>, 

<p><strong>Morningside Heights</strong></p>, 

<p>Morton-Williams<br/>
Broadway and 115th Street. When I’ve gone the staff have been in the process of throwing stuff out, so 9 or 9:30, and they were friendly enough about letting us dive away. It’s a very busy corner, and well-lit, so its high-profile dumpster diving, not for the shy.</p>, 

<p>D’Agostino<br/>
Broadway and 110th Street. I’m not sure what the best time is, but I think 9-9:30 is when I’ve had good luck there.</p>
"""