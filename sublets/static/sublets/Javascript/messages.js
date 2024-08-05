document.addEventListener('DOMContentLoaded', function() {

  // Show compose view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';

  load_messages()


})

// Reworked the compose function to take in arguments, used for the respond function.
function load_messages() {

  // Show compose view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';

  // Select the two buttons for both the archive and respond button
  message_button = document.querySelector(".archive_button");

  // loop through each button and add a click event listener
  message_button.forEach(function(button) {
            button.addEventListener("click", function() {
              // do something when the button is clicked
              alert(button.id)
            });
          });


}