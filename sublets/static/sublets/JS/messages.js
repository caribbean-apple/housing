document.addEventListener('DOMContentLoaded', function() {

  // Show compose view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';
  document.querySelector('#response_form').style.display = 'none';

  window.addEventListener('popstate', e => {
    if (e.state.page === 'inbox') {
      load_messages();
    }
    if (e.state.page === 'reply') {
      respond(e.state.id);
    }
  })

  if (!history.state) {
    history.replaceState({page: 'inbox'}, "", '/message-inbox');
  }
  
  load_messages()

})

// Reworked the compose function to take in arguments, used for the respond function.
function load_messages() {

  // Show compose view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';
  document.querySelector('#response_form').style.display = 'none';

  if (!history.state || history.state.page !== 'inbox') {
    history.replaceState({page: 'inbox'}, "", '/message-inbox');
  }

  // Select the two buttons for both the archive and respond button
  const message_button = document.querySelectorAll(".message_button");
  const reply_button = document.querySelector(".send_button")

  // loop through each button and add a click event listener
  message_button.forEach(function(button) {
            button.addEventListener("click", function() {
              // do something when the button is clicked

              respond(button.id)

            });
          });

  // TODO Add a refresh page to get all the images again.
}

function respond(id){
  document.querySelector('#respond').style.display = 'block';
  document.querySelector('#response_form').style.display = 'block';
  document.querySelector('#show-messages').style.display = 'none';

  history.pushState({page: 'reply', id: id}, "", `/message-reply/${id}`);

  //TODO Get message information and populate the javascript

  individual_message_confirm=fetch('/message_info/'+id)      
    .then(response => response.json())
    .then(single_message => {

                document.querySelector('#respond_message').innerHTML = `
                <hr>
                  Sender: ${single_message.sender} <br>
                  Recipients: ${single_message.recipient} <br>
                  Listing: ${single_message.listing}<br>
                  Body: ${single_message.body} <br>
                  Timestap: ${single_message.timestamp} <br>
                  <br>
                <hr>

                `;

                 document.querySelector('.recipient_id').value = single_message.sender_id;
                 document.querySelector('.listing_id').value = single_message.listing_id;
          
              
              })



  //TODO Set up event listener for reply button that pushes message to an api that adds to the messages model.


}