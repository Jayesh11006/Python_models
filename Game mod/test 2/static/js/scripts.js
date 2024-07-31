document.getElementById('specs-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const cpuScore = document.getElementById('cpu_score').value;
    const gpuScore = document.getElementById('gpu_score').value;
    const ramSize = document.getElementById('ram_size').value;
    const storageSize = document.getElementById('storage_size').value;

    const data = {
        cpu_score: parseInt(cpuScore),
        gpu_score: parseInt(gpuScore),
        ram_size: parseInt(ramSize),
        storage_size: parseInt(storageSize)
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('recommendation-result');
        if (data.recommendation) {
            resultDiv.innerHTML = `Recommended Game Performance: Your pc is <b> ${data.recommendation} </b>`;
        } else {
            resultDiv.innerHTML = `Error: ${data.error}`;
        }
    })
    .catch(error => console.error('Error:', error));
});
