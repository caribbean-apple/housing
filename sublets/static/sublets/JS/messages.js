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
  alert(id)
  document.querySelector('#respond').style.display = 'block';

  //TODO Get message information and populate the javascript

  individual_message_confirm=fetch('/message_info/'+id)      
    .then(response => response.json())
    .then(single_message => {
                // Print emails
                console.log(single_message);
              
              
              })


  //TODO Set up event listener for reply button that pushes message to an api that adds to the messages model.


}