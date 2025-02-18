document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('image-upload');
    const effectSelect = document.getElementById('effect');

    formData.append('file', fileInput.files[0]);
    formData.append('effect', effectSelect.value);

    fetch('/cartoonify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.processed_image) {
            displayImage(data.processed_image);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        alert('Something went wrong. Please try again.');
    });
});

function displayImage(base64Image) {
    const inputImage = document.getElementById('input-image');
    const outputImage = document.getElementById('output-image');

    inputImage.src = URL.createObjectURL(document.getElementById('image-upload').files[0]);
    outputImage.src = base64Image;
}
