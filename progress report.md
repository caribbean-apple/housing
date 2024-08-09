Everything marked with X has been done.
Those marked with O have not been started.
Those marked with ~ are in progress (with a comment below)


=== INCOMPLETE ONLY ===
Separated out the complete stuff to leave only the incomplete.

#### Search Results Page
~ Add clickable username to search results

~ More filters: The search results page has additional filters that you can specify on the left bar, including specifying 
	- sublet start date (earliest date and latest date), 
	- accommodation type: rent a room, rent an entire apartment
Comment: Check on 2018 bug

#### Saved Listings Page

O On the saved listings page, you can enter your email to be notified if any of your saved listings get edited or deleted. You will receive an actual email to that email address letting you know if so (assuming you put in a real email address)

#### Message Read and Reply Page
~ Implement view message and reply for this page

#### Additional Features / Tasks
O Incorporate at least one CSS animation

~ Incorporates a tests.py file with at least two tests. One must use selenium.
Comment: Non-selenium test is done. Waiting for us to have more interactivity/JS before making a selenium test.

O Any single-page app features (like in the inbox) still have browser history and back button support

O Check everything for mobile responsiveness

O Clean everything up at the end for design and style

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

O More filters: The search results page has additional filters that you can specify on the left bar, including specifying 
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

~ Lists messages you got from any user. Clicking opens that message
Comment: No JS on this page yet, just a basic version.

#### Message Read and Reply Page
~ This is just a JS reload of the inbox page that lets you view the content any message you clicked, with the option to reply. The reply appears in the other user's inbox.

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

