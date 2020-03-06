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

# get list of strings of text between <p>
# directory_list_raw = []
# splitp = divtag.find_all("p")
# for p in splitp:
#     split_dir = splitp.text
#     directory_list_raw.append(split_dir)

# divtag.p.next_sibling


# for sibling in divtag.find("p").next_siblings:
# ...     print(repr(sibling))
# ... 
# '\n'
# <p>Mike’s Bagels | 
# 4033 Broadway at W 168th Street</p>
# '\n'
# <p> | 
# </p>
# '\n'
# <p></p>
# '\n'
# <p>Morton-Williams | 
# Broadway and 115th Street. When I’ve gone the staff have been in the process of throwing stuff out, so 9 or 9:30, and they were friendly enough about letting us dive away. It’s a very busy corner, and well-lit, so its high-profile dumpster diving, not for the shy.</p>
# '\n'
# <p>D’Agostino | 
# Broadway and 110th Street. I’m not sure what the best time is, but I think 9-9:30 is when I’ve had good luck there.</p>
# '\n'
# <p>Absolute Bagel | 
# Broadway and 108th St. The usual bagel abundance, plenty fresh.</p>
# '\n'




# if <em> remove
# if <p><strong> remove


"""
<p>Morton Williams | 
58th Street just east of Broadway (store entrance is on 57th, but the trash is on 58th) | 
On the messy side, but on a pretty quiet street, so a good place for the shy. In October 2012 we found a bunch of produce and bread, some dairy products and a whole heap of cookies.</p>

<p>Dunkin Donuts | 
54th and 10th Avenue | 
May vary. In October 2012, no donuts were out, but there was a lot of pumpkin donut mix.</p>

<p>Gristedes | 
8th Avenue and 54th Street | 
Lots  of produce, bread, eggs, and packaged goods here. In the past employees got a bit angry with us, but didn’t try to stop us. (Updated October 2012)</p>

<p>Pick a Bagel | 
53 and 8th | 
croissants and bagels. Updated October 2012.</p>
<p>Duane Reade | 
53rd and 8th | 
This chain is becoming one of NYC’s bigger wasters. Here’s a report for this location from October 2012: | 
“One of the largest curbside piles of usable goods I have ever seen! You could have opened up a pop-up store with the finds here! (no exaggeration) bagful of gum!   bagful of cookies, snacks (Pirate’s booty stuff), cans of baked beans, mac and cheese, cologne, chocolate (Hersheys), soap, some pills (prenatal, still not expired!), hair care products, baby care products (soaps, lotions), scar-away (ideal for c-section), many other drugstore-type things… | 
I can’t imagine this was a typical night… I can’t even guess why so much was tossed that night… at least a couple of other passers-by took some.  wild!”</p>
<p>Food Emporium | 
Dumpsters are on 49th Street just east of 8th Avenue | 
Loads of stuff. We found veggies, tofu, bread, dairy, nuts and seeds. It’s a bit overwhelming here, as there is a lot of stuff. (updated Jan. 2010)</p>
<p>Dunkin Donuts | 
9th Avenue between 48th and 49th | 
Typical DD fare! (updated Jan. 2010)</p>

"""