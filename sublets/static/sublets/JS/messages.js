document.addEventListener('DOMContentLoaded', function() {

  // Show inbox view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';
  document.querySelector('#response_form').style.display = 'none';

  // Handle back button click and history storage for js-loaded pages
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
  // TODO: Change this to listen only for the container and then 
  // on click, select the nearest element.
  const message_button = document.querySelectorAll(".message_button");
  message_button.forEach(function(button) {
    button.addEventListener("click", function() {
      // do something when the button is clicked
      respond(button.id)
    });
  });
}

function respond(id) {
  document.querySelector('#respond').style.display = 'block';
  document.querySelector('#response_form').style.display = 'block';
  document.querySelector('#show-messages').style.display = 'none';

  history.pushState({page: 'reply', id: id}, "", `/message-reply/${id}`);

  fetch('/message_info/' + id)      
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
}