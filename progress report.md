Everything marked with X has been done.
Those marked with O have not been started.
Those marked with ~ are in progress (with a comment below)


=== INCOMPLETE ONLY ===
Separated out the complete stuff to leave only the incomplete.


#### Additional Features / Tasks


O Make README file
In a README file (whose extension can be .txt, .md, .adoc, or .pdf) in your project’s main directory, include a full write-up describing your project, what’s contained in each file you created, why you made certain design decisions, and any other additional information the staff should know about your project. This document should be sufficiently thorough for your teaching fellow to run your project without any need to contact you further with questions. Take your time, and do not save this step for last. A well-written and complete README file will take longer than you think it will.

O rename search_results to search-results.html

O On Listing page, your own listing should not show in featured.

O On saved listings page, if first listing doesn't have photos and second does, there is a problem
No photos in listing only showed if no photos in any listing. need to address.

O Redo pictures to not be that small for mobile responsiveness

O Check everything for mobile responsiveness

O Clean everything up at the end for design and style

O check for too big filesize (or delete the code and util)

=======================================================





This is from before and includes what we already did & 
what was missing at the time:

Everything (both )
#### Landing Page
X Has a search bar allowing the user to specify location by choosing a city from a dropdown.

X Has login or register buttons on the top right nav

X Landing page has featured listing example. Clicking brings you to that listing page.

#### Register Page
X Here you register with a name, email, password.

#### Search Results Page
x Displays results, one for each listing matching your city. Each result shows up to two photos from the listing. Clicking sends to the listing page.
~ Add clickable username to search results

X More filters: The search results page has additional filters that you can specify on the left bar, including specifying 
	- sublet start date (earliest date and latest date), 
	- accommodation type: rent a room, rent an entire apartment

#### Listing Page
X Here you can see a listing's photos, as well as a description made by the user who listed it.

X There is a textarea that lets you send a message for that listing.

X If it is your listing, you can delete it.

#### Create Listing Page
X Here you can create a listing. You must upload a photo, specify an address, and write a description. Rent can be specified here.

#### Saved Listings Page
~ Accessible via the top nav menu if logged in. Shows saved listings, displayed the same way as in search results, with an option to delete the listing via clicking a trash can icon to the right of that listing.
Comment: Done. But they don't display the same way as in search results. 

O On the saved listings page, you can enter your email to be notified if any of your saved listings get edited or deleted. You will receive an actual email to that email address letting you know if so (assuming you put in a real email address)

#### Inbox Page
X Accessible from anywhere for logged in users on the top nav bar.

X Lists messages you got from any user. Clicking opens that message
Comment: No JS on this page yet, just a basic version.

#### Message Read and Reply Page
X This is just a JS reload of the inbox page that lets you view the content any message you clicked, with the option to reply. The reply appears in the other user's inbox.

#### User Profile Page
~ Throughout the site (including the search results page and listing pages), wherever you see a username you can click it, bringing you to that user's profile. If it is your own profile, an edit button appears that adds in the fields with JS for you to edit
Comment: All done, except for editing profile functionality. Maybe he will letus skip that so I'll do it last. Also need to add links to profiles in search results.

#### Additional Features / Tasks
O Incorporates at least one CSS animation

~ Incorporates a tests.py file with at least two tests. One must use selenium.
Comment: Non-selenium test is done. Waiting for us to have more interactivity/JS before making a selenium test.

O Any single-page app features (like in the inbox) still have browser history and back button support

X Use bootstrap for at least one item

O Clean everything up at the end for design and style

