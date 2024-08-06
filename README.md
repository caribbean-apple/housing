# housing
Runing list of things to work on 
    Delete listing available to all users   
        Attempted to solve.
    No current way to favorite items
    No way to deactivate a listing if the user owns it.
    Create listing photos uploads neads work.  Need to figure out the multiple photo upload.


Challenges Experienced:

    Clean_data: During the validation of our add listing form, we encountered an issue where the comparison between the start date and end date was returning a comparison error.  
        What we Learned: if you use clean_x_date, it will not let the user access other aspects of the form to evaluate.  Thses need to be combined into one clean function.

    File Pathing: Tadhg spent a couple hours trying to debug file pathing, just to relaize the static folder was "static/sublets" instead of "static/sublet"

    Django Versions: There was an observed issue with uploading multiple photos at once.  The selected model type was ClearableFileInput.  It turns out that this works in Django 4.1, which Felix was using, but does not in Django 5.0.7, which Tadhg was using.  This was causing a headache until identified.  