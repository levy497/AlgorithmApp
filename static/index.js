document.getElementById('pso-form').addEventListener('submit', function(e) {
    e.preventDefault();

    var data = {
        num_particles: document.getElementById('num_particles').value,
        maxiter: document.getElementById('maxiter').value,
        function: document.getElementById('function').value // Dodane
    };

    fetch('/run_pso', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('pso-result').innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Wykres PSO">`;
    });
});




