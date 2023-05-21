document.getElementById('login__form').addEventListener('submit', function(event) {
    // event.preventDefault();

    let username = document.getElementById('username').value;
      let password = document.getElementById('password').value;
      let confirmPassword =document.getElementById('confirm-pass').value;
    if (password !== confirmPassword) {
      event.preventDefault();
      alert('not same password');
    } else {
      event.preventDefault();
// Send the form data to the backend
      fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password,
        })
      }).then(response => {
        response.json();
        window.location.href = '/index';  // Add this line
      }).then(data => {
        console.log('Success:', data);
      }).catch((error) => {
        console.error('Error:', error);
        window.location.href = '/index';  // Add this line
      });
    }



  });