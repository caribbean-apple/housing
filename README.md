# housing
Title: Sublease Listing and Finding Website
Authors: Felix Feist and Tadhg Scannell
Semesster: Summer 2024

Project Description: This repo hosts all the code for a sublease housing application.  Users can create profiles, log-in, list and search for housing in different predetermined areas, and message the listing owner.  This project executes this functionality using a combination of Javascript, Python, SQL, and HTML, all managed via a Djagno App.

Requirements: See the requirements.txt file 

Youtube Video Link: https://www.youtube.com/watch?v=EB2120FxKmk

File Breakdown and Description

Housing:
    settings.py: Holds all relevant information.

Media:
    This is the folder where photos are stored to be used for listings and profiles.

In Sublets:

    Models: The file contains all the database models for usage.  This includes Users and their profiles, listings, photos for the listings, and messages between users.

    Forms: This file contains the forms used in the HTML and views.py funcitonality to pull requests from the webpages and store them in the models.

    Urls: This file contains the url pathing between the different available webpages for the application.

    Tests:This fil containst 

    Views: This file is where the majority of the backend code runs to display the webpage as different input are provided to the user.

    Static: This is the folder that contains all necessary static files, including the CSS and Javscript necessary to run the single page sub-applications.

    Templates: This is the folder holding all of the different templates available for viewing.  The Layout is the base template to provide consistency across the web app, which gets extended into the other options depending on the necessary view.


Major Design Decisions:

Runing list of things to work on 
    Delete listing available to all users - solved   
        Attempted to solve.
    No current way to favorite items
    No way to deactivate a listing if the user owns it.
    Create listing photos uploads neads work.  Need to figure out the multiple photo upload. - solved
    No photos in listing only showed if no photos in any listing. need to address.


Challenges Experienced and Design Decisions:

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

    Emails work: Attempted to get the emails working using the inhouse send_mail function in python.  This ended up cuasing the code disruption as mentioned by Glenn in his direction.  We then worked through the Celery documentation to try and get this running before realizing that we were not a server and as such the python function would not work.  So then we attempted to go through the Google API, including setting up an google cloud with a project email address that we built "housingCS33@gmail.com".  We worked through the documenation to build out the quick start guide to get it working.  The first problem was determining the webpage redirect that needed to be sent, which was http://localhost:44331/.  This ended up giving me an access blocked, so we added it to the google cloud.  I treid authorising the local host to be a valid origin, but that was not functioning for us.  Felix then found another API that ended up working better, Sendgrid.
        