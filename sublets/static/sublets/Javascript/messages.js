document.addEventListener('DOMContentLoaded', function() {

  // Show compose view and hide other views
  document.querySelector('#show-messages').style.display = 'block';
  document.querySelector('#respond').style.display = 'none';


  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Select the two buttons for both the archive and respond button
  message_button = document.querySelector(".archive_button");


  load_messages()


})

// Reworked the compose function to take in arguments, used for the respond function.
function load_messages() {

    // Show compose view and hide other views
    document.querySelector('#show-messages').style.display = 'block';
    document.querySelector('#respond').style.display = 'none';

}