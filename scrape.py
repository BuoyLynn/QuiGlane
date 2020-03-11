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
    br.replace_with(" . ")

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

list_directory = [string.replace('\n', '') for string in list_directory]

new_txt = open('freegan_dir_clean.txt','w')
for string in list_directory:
    new_txt.write(string)
    new_txt.write('\n')
new_txt.close()
