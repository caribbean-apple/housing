# housing
Runing list of things to work on 
    Delete listing available to all users - solved   
        Attempted to solve.
    No current way to favorite items
    No way to deactivate a listing if the user owns it.
    Create listing photos uploads neads work.  Need to figure out the multiple photo upload. - solved


Challenges Experienced:

    Clean_data: During the validation of our add listing form, we encountered an issue where the comparison between the start date and end date was returning a comparison error.  
        What we Learned: if you use clean_x_date, it will not let the user access other aspects of the form to evaluate.  Thses need to be combined into one clean function.

    File Pathing: Tadhg spent a couple hours trying to debug file pathing, just to relaize the static folder was "static/sublets" instead of "static/sublet"

    Django Versions: There was an observed issue with uploading multiple photos at once.  The selected model type was ClearableFileInput.  It turns out that this works in Django 4.1, which Felix was using, but does not in Django 5.0.7, which Tadhg was using.  This was causing a headache until identified.  

    Getting only two photos per image: The .filter(filter files).first or sliceing mechanism does not seem to provide a way to limit by id.  Tadhg was looking for a way to get the first two photos for each listing, but struggled to find them.  Settled on iterating through the relevant ids and only taking the first two and joining those to a another table to replace the append function.

    Working through the filterign took some time to identify how to reexecute the same search again.  Decided on an inefficient useage of the code by redoing all of the extraction in views.py.  This is likely a poor solution, but one that was intuitive and started working.

    Deleteing Listing available to all users - solved by comparing the current user to the user who created the listing.