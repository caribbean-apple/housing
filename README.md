# housing
Title: Sublease Listing and Finding Website
Project Name: housing
App Name: sublets
Authors: Felix Feist and Tadhg Scannell
Semester: Summer 2024


### Summary & YouTube
This is an app that lets users 
1. Find a sublet posted by someone else 
2. Find a subletter, by posting their sublet offering.
Features include posting and searching for sublet listings, creating a public user profile with pictures, saving sublet listings, messaging other users about their sublets and replying, and receiving email notifications if a sublet you saved was removed from the site. 

Please enjoy this YouTube summary of most of the features. Some minor features were not included, as there were too many features for less than 3 minutes. 
Youtube video Link: https://www.youtube.com/watch?v=EB2120FxKmk

A partial list of features not visible in the video:
 - We include a robots.txt file, along with corresponding code in urls.py, that discourages scrapers from scraping our website. It is accessible once server is running at /robots.txt and is written according to standard.
 - We did not show our personal email inbox upon deletion of a saved listing. However, we tested this feature and it was functional.
 - Users can delete a listing by going to their own listing's page, findable through the search engine.
 - When visiting a user's profile that doesn't exist, there is a Poke button. This is just a teaser: it  was not part of the specs and will be implemented later.
 - We included a favicon, it's an image of a cat in a house.


### How to run this project
To guarantee functionality, ensure you have all requirements in requirements.txt. In particular, the Django version is important: Our multiple picture uploads don't work in every Django version.

The app uses a sendgrid API key. For grading we offer our version of the key in the /housing/local_settings.py file (adjacent to the regular settings.py file). This file is exempt in gitignore to ensure API key privacy. We will upload it for convenience.

Consider running the following commands (depending if you make a new db)
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

And for testing run
python manage.py test

Admin console is configured, feel free to use.

### Key design decisions & big picture of file structure
- Our navbar is mobile responsive: for small screens it displays as a hamburger menu.

- Most pages load with a GET request. However, message inbox and reply page are both on messages.html and are loaded with JS. Back button and history works for these JS-generated pages.

- Users can upload pictures directly, rather than through URL. These are saved in ./media. Listing pictures are organized in respective listing ID folders. Profile pictures are listed loose, for now, as they are a "BEST" feature and thus some features are not yet implemented.

- Two basic tests are included in the /tests/ folder:  testing pageloads for basic pages, and testing button click functionality with selenium. 

- Email notifications can be sent to your personal email when a listing you have already saved is deleted by the person who listed it (NOT if it is deleted in the admin console). This works through an @gmail address we created, and email sending works through the sendgrid API. We ended up not using celery, as the app was smoothly functional without it at our small scale. However, in general but especially if this website is scaled, it would be important to make the email sending asynchronous so that the user doesn't experience any delay.

- .gitignore ensures that unnecessary or private files don't get pushed to github. This includes our database, compiled or cache files, the local_settings file with API key, and for good measure all .env files to future proof (despite not using any so far). Our virtual environment /django-updated/ is in .gitignore but we do not include the folder itself as it can depend on the user's system.

- This entire site was designed from scratch. We did not start with a previous project as a template and almost no code was reused. This includes the implementation of user authentication, nav, and even the creation of the project with the django-admin command, and then app creation with startapp command.

- For details on files in the sublets app, see the next section:

### File Breakdown and Description

In the sublets directory, the following files are not included by default with python manage.py startapp.

- forms.py: We have separated the forms for readability. This file contains the forms used to allow user submission and input throughout the app.

- util.py: This file is for basic functions used in other files, separated out for readability. For now it is small, but if the project scales it is good practice.

The remaining files and directories in /sublets/ include: 
- models.py: The file contains all the database models for usage. This includes Users and their profiles, listings, photos for the listings, and messages between users.

- urls.py: This file contains the url pathing between the different available webpages for the application.

- views.py: This file is where the majority of the backend code runs to display the webpage as different input are provided to the user.

- static directory: This is the folder that contains all necessary static files, including the CSS and Javscript necessary to run the single page sub-applications. Since these files have unchanging content, they can be cached.

- templates directory: This file has all of our html templates (in the sublets folder) as well as the aforementioned robots.txt file. All templates extend the layout with navbar defined in layout.html.

### Future features (these were decidedly out of scope for the class project)
- We would like to make our email call asynchronous for better error management and less delay.

- Implement the ability to "poke" a user to create a custom profile. Right now it's an intentionally-nonworking button.

- Add the ability to unsubscribe from a listing and no longer get emails. Right now the only way is to enter a fake email.

### Challenges Experienced and Design Decisions

    Clean_data: During the validation of our add listing form, we encountered an issue where the comparison between the start date and end date was returning a comparison error.  
        What we Learned: if you use clean_x_date, it will not let the user access other aspects of the form to evaluate.  Thses need to be combined into one clean function.

    File Pathing: Tadhg spent a couple hours trying to debug file pathing, just to relaize the static folder was "static/sublets" instead of "static/sublet"

    Django Versions: There was an observed issue with uploading multiple photos at once.  The selected model type was ClearableFileInput.  It turns out that this works in Django 4.1, which Felix was using, but does not in Django 5.0.7, which Tadhg was using.  This was causing a headache until identified.  

    Getting only two photos per image: The .filter(filter files).first or sliceing mechanism does not seem to provide a way to limit by id.  Tadhg was looking for a way to get the first two photos for each listing, but struggled to find them.  Settled on iterating through the relevant ids and only taking the first two and joining those to a another table to replace the append function.

    Working through the filterign took some time to identify how to reexecute the same search again.  Decided on an inefficient useage of the code by redoing all of the extraction in views.py.  This is likely a poor solution, but one that was intuitive and started working.

    Deleteing Listing available to all users - solved by comparing the current user to the user who created the listing.

    Messaging: Figuring out how to do a response was a challenge.  This is where two different coders created a learning opportunity, as it is important to learn how the other individual has constructed their code such that you can integrate your sections with in it.  The messaging is an example, as Tadhg worked through the javascript, which then referenced a function that Felix had created.  Tadhg was unable to get this initially working, and only after multiple efforts running through brute force print debugging, was he able to understand and implement functioning code.

    Date Time:  Tadhg referenced a input from GeeksForGeeks to figure out the date for the input on the advanced search filter.  This caused some initial issues, as the code had an initial limit on the date time.  After debugging, this was a quick resolution.

    Version Control: Through multiple sessions of editing, a Fetch_Message function API that was built got deleted in version control.  This led to functional issues where one party was trying to run code but encountered errors with a url.py call to a none existent function.  This was a good exercise in iterating back through the past versions to find deleted code.

    Emails work: Attempted to get the emails working using the inhouse send_mail function in python.  This ended up causing the code disruption as mentioned by Glenn in his direction.  We then worked through the Celery documentation to try and get this running before realizing that we were not a server and as such the python function would not work.  So then we attempted to go through the Google API, including setting up an google cloud with a project email address that we built "housingCS33@gmail.com".  We worked through the documenation to build out the quick start guide to get it working.  The first problem was determining the webpage redirect that needed to be sent, which was http://localhost:44331/.  This ended up giving me an access blocked, so we added it to the google cloud.  I treid authorising the local host to be a valid origin, but that was not functioning for us.
