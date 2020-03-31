# QuiGlane (pronounced: "Key-Glan")

> An application to help dumpster-divers find beneficial safe dives, and communicate as a community.


## Features

### User Login
  - User registration, login, logout. 
  - Current user identification and access management (login required).

### Dive site map:
  - Dumpster markers include a popup info with:
    * Name of business (dumpster owner)
    * Dumpster address
    * Category of business
    * Business closing hours
    * Optimal dive time
    * Dive rating (from review)
    * Dive safety (from review)
  - Marker data is populated through an API that pulls from the database.

### Add new dive review:
  - If the new review is under an existing location:
    * Autocomplete available - displays results from database.
    * New dive will be added to the database under the respective site.
  - If the location does not exist in the database:
    * A new site will be added to the database.
    * Then the dive will be added under the new site.

### User Profile "Dive Cards"
  - Displays each dive review as a card.
    * Each card unlocks other dive reviews with matching location via link.
    (Acts as a barrier to entry to safegaurd the community)
      - Unlocked reviews unveil reviewers' unique username.
    * Each review card can be updated or deleted upon verification of user.


## Database
![DB Model](/seed_data/db_glean_model.jpg)
