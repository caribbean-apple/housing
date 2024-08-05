# housing
Runing list of things to work on 
    Delete listing available to all users
    No current way to favorite items
    No way to deactivate a listing if the user owns it.
    Create listing photos uploads neads work.  Need to figure out the multiple photo upload.


Challenges Experienced:

    Clean_data: During the validation of our add listing form, we encountered an issue where the comparison between the start date and end date was returning a comparison error.  
        What we Learned: if you use clean_x_date, it will not let the user access other aspects of the form to evaluate.  Thses need to be combined into one clean function.

    File Pathing: Tadhg spent a couple hours trying to debug file pathing, just to relaize the static folder was "static/sublets" instead of "static/sublet"