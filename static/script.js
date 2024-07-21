document.getElementById('prediction-form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Collect form data
    let formData = new FormData(this);
    let queryParams = new URLSearchParams(formData).toString();  // Convert FormData to URL query parameters

    fetch('/predict?' + queryParams, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById('result').textContent = 'Prediction Result: ' + data.result;
            document.getElementById('popup').classList.add('openPopup');  // Use classList to add class
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function closePopup() {
    document.getElementById('popup').classList.remove('openPopup');  // Use classList to remove class
}
