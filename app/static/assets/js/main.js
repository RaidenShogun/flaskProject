/*=============== SHOW HIDDEN - PASSWORD ===============*/
const showHiddenPass = (loginPass, loginEye) =>{
   const input = document.getElementById(loginPass),
         iconEye = document.getElementById(loginEye)

   iconEye.addEventListener('click', () =>{
      // Change password to text
      if(input.type === 'password'){
         // Switch to text
         input.type = 'text'

         // Icon change
         iconEye.classList.add('ri-eye-line')
         iconEye.classList.remove('ri-eye-off-line')
      } else{
         // Change to password
         input.type = 'password'

         // Icon change
         iconEye.classList.remove('ri-eye-line')
         iconEye.classList.add('ri-eye-off-line')
      }
   })
}


showHiddenPass('login-pass','login-eye')
// node
document.getElementById('loginButton').addEventListener('click', function() {
   let overlay = document.getElementById('overlay');
   overlay.style.opacity = '0';
   setTimeout(function() {
       overlay.style.display = 'none';
   }, 1000);
});

document.getElementById('registerButton').addEventListener('click', function() {
   window.location.href = "register";
});

document.getElementById('login_Button').addEventListener('click', function() {
   event.preventDefault();
   // Assuming you have input fields with id 'username' and 'password'
let username = document.getElementById('username').value;
let password = document.getElementById('login-pass').value;
console.log(username);
console.log(password);


// Send the username and password to the backend
fetch('http://127.0.0.1:5000/index', {
   method: 'POST',
   headers: {
      'Content-Type': 'application/json'
   },
   body: JSON.stringify({
      username: username,
      password: password
   })
}).then(response => {
      if (response.status === 200) {
         // If the login was successful, redirect to '/chat'
         window.location.href = '/chat';
      } else if (response.status === 401) {
         // If the login was unsuccessful, show an error message
         alert('Login Unsuccessful. Please check username and password');
      } else {
         // For other status codes, throw an error to be caught in the catch block
         throw new Error('Unexpected status code: ' + response.status);
      }
   })
   .catch((error) => {
      // Handle any errors that aren't caught in the then block
      console.error('Error:', error);
      alert('An unexpected error occurred. Please try again later.');
   });

   
});