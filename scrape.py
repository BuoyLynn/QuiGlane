from bs4 import BeautifulSoup
import requests

# Request HTML from URL & Return as HTML Text to parse
response = requests.get("https://freegan.info/freegan-directories/dumpster-directory/manhattan/")
soup = BeautifulSoup(response.text, "html.parser")

# Go to directory content under <div class="entry-content">
divtag = soup.find('div', attrs={"class": "entry-content"})

# Remove <em>, <strong>, <a> and <span> as they are not needed
find_tags = divtag.find_all(["em", "strong", "a", "span"])
for tag in find_tags:
    tag.extract() 

# Replace </br> with "| to ease parsing later
find_br = divtag.find_all("br")
for br in find_br:
    br.replace_with(" | ")

# Remove unncessary beginning and end <p> tags in the beginning
badptag = divtag.find_all("p")
for i, badtag in enumerate(badptag):
    if i < 4:
        badtag.extract()

# Create a list of strings containing directory info
list_directory = []
ptags = divtag.find_all("p")
for store in ptags:
    list_directory.append(str(store.get_text()))

unwanted = ['', ' | \n']
for string in list_directory:
    if string in unwanted:
        list_directory.remove()


"""
['Bravo Supermarket | \nBroadway near 181st | \nGood selection of produce, includes some Latin American specialty items', 'Mike’s Bagels | \n4033 Broadway at W 168th Street', 'Morton-Williams | \nBroadway and 115th Street. When I’ve gone the staff have been in the process of throwing stuff out, so 9 or 9:30, and they were friendly enough about letting us dive away. It’s a very busy corner, and well-lit, so its high-profile dumpster diving, not for the shy.', 'D’Agostino | \nBroadway and 110th Street. I’m not sure what the best time is, but I think 9-9:30 is when I’ve had good luck there.'
"""