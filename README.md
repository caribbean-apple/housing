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

    Messaging: Figuring out how to do a response was a challenge.  This is where two different coders created a learning opportunity, as it is important to learn how the other individual has constructed their code such that you can integrate your sections with in it.  The messaging is an example, as Tadhg worked through the javascript, which then referenced a function that Felix had created.  Tadhg was unable to get this initially working, and only after multiple efforts running through brute force print debugging, was he able to understand and implement functioning code.

    Date Time:  Tadhg referenced a input from GeeksForGeeks to figure out the date for the input on the advanced search filter.  This caused some initial issues, as the code had an initial limit on the date time.  After debugging, this was a quick resolution.

    Version Control: Through multiple sessions of editing, a Fetch_Message function API that was built got deleted in version control.  This led to functional issues where one party was trying to run code but encountered errors with a url.py call to a none existent function.  This was a good exercise in iterating back through the past versions to find deleted code.