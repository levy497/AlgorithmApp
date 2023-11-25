document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var password = document.getElementById('pwd').value;
    var regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,}$/;

    if (!regex.test(password)) {
        document.getElementById('passwordError').textContent = 'Hasło musi zawierać co najmniej 8 znaków, w tym jedną cyfrę, jedną małą literę, jedną dużą literę i jeden znak specjalny.';
        document.getElementById('passwordError').style.display = 'block';
    } else {
        document.getElementById('passwordError').style.display = 'none';

        // Wysyłanie danych formularza do serwera
        var email = document.getElementById('email').value;
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'email=' + encodeURIComponent(email) + '&password=' + encodeURIComponent(password)
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                // Pokazanie komunikatu o sukcesie
                var toastElement = document.getElementById('successToast');
                var toast = new bootstrap.Toast(toastElement);
                toast.show();

                // Przekierowanie po opóźnieniu
                setTimeout(function() {
                    window.location.href = '/login';
                }, 3000);
            } else if(data.error) {
                document.getElementById('passwordError').textContent = data.error;
                document.getElementById('passwordError').style.display = 'block';
            }
        });
    }
});
