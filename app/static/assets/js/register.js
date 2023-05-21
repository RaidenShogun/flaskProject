document.getElementById('login__form').addEventListener('submit', function(event) {
    // event.preventDefault();

    let username = document.getElementById('username').value;
      let password = document.getElementById('password').value;
      let confirmPassword =document.getElementById('confirm-pass').value;
    if (password !== confirmPassword) {
      event.preventDefault();
      alert('两次输入的密码不一致');
    } else {
      event.preventDefault();

      // var email = document.querySelector('.login__box input[type="email"]').value;
      // var gender = document.querySelector('.login__check input[name="gender"]:checked').value;
      // var password = document.querySelector('')

      
      
      console.log(username)
      console.log(password)



      // Send the form data to the backend
      fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password,
          // gender: gender
        })
      }).then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }









  });