# Federated Health Search Application

The Federated Health Search Application provides a secure and quick way for you to search for different conditions, medicines, symptoms and treatments. Users can search in the general web - Bing, and two specialised medical websites - Medline Plus and healthfinder.gov.

Registered users can create categories and save resources they find into them. Moreover, they can maintain their public profile and choose whether to share their categories with other users of the website. The application should help the users understand if the information is easy to read, is loaded with sentiment and subjectivity. Created by students at the University of Glasgow for a group student project. 

## Getting Started

To clone the repository, use:
```
https://github.com/vjvasilev95/fhs_project.git
```

### Prerequisities

For your Python environment,  use the ```requirements.txt``` file to install the needed packages.

List of application specific requirements:
```
beautifulsoup4
django-pagination-bootstrap
Pillow
textblob
textstat
```

## Running the population scripts

When initially populating the database, first run
```
population_script_users.py
```
What this will do is it will populate the database with three users:
jill
bob
jen

Afterwards run:
```
population_script_catpage.py
```
This will create some categories, put some random pages in them, and assign them randomly to the three users created above.

## Changes made after the presentation on Monday
After the feedback received from the presentation, the following changes were added to the project:
* The ability to change the category's shared state after its creation
* The need to add your age and gender when registering
* The option choose whether the engine will search using the user's data (gender and age), or another data, specified by the user
* Dynamically calculating all the pages' scores while fetching the results from the search.
* The ability to create categories with the same name (added after Dr. Azzopardi's feedback on the matter)

## Built With

The technologies used for this project are as follows:
* Python - The python programming language, which the Django web development framework uses.
* Django - The web development framework used. [Source](https://www.djangoproject.com/)
* HTML, CSS, jQuery - used to style and add functionality to front end of the website.
* Twitter Bootstrap 3 - used to enhance the style and the visual appeal of the website. [Source](http://getbootstrap.com/)
* Bootstrap Switch - used to style some of the HTML input tags on the website. [Source](http://www.bootstrap-switch.org/)
* Bootstrap Sticky Footer - used to style the footer of the website. [Source](http://getbootstrap.com/examples/sticky-footer/)
* Google Autocomplete "API" - undocumented API used to provide suggestions to the user while they are typing their search query. To implement it, [this](http://shreyaschand.com/blog/2013/01/03/google-autocomplete-api/) tutorial was followed.
* Textstat and textblob - the two Python packages used to calculate the readability, polarity (sentiment) and subjectivity of the page.


## Authors
* [vjvasilev95](https://github.com/vjvasilev95): Veselin Vasilev 2132561v
* [andrey1995](https://github.com/andrey1995): Andrey Georgiev 2133919g
* [georgikoyrushki95](https://github.com/georgikoyrushki95): Georgi Koyrushki 2114429k
* [katya1995](https://github.com/katya1995): Katya Bacheva 2145759b


## Acknowledgments

* [Tango With Django Book](http://www.tangowithdjango.com/) This was the most invaluable resource which helped the team learn about the Django web development framework. A lot of our work was based on the tutorial provided in this book.


