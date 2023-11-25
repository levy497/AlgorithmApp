document.addEventListener('DOMContentLoaded', function() {
        var loginForm = document.querySelector('.login-form');

        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            var formData = new FormData(loginForm);
            fetch('/login', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    window.location.href = '/'; // Przekierowanie na stronę główną
                } else {
                    // Wyświetlenie komunikatu o błędzie
                    document.getElementById('login-error').textContent = data.error;
                    document.getElementById('login-error').style.display = 'block';
                }
            });
        });
    });
