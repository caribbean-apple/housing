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
