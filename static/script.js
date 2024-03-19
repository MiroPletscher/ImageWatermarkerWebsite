let watermarked_images = [];
const status_text = document.getElementById('status-text');
let download_allowed = false;

function uploadImages(){
    watermarked_images = [];
    const opacity = document.getElementById('opacity-input').value;
    const watermarkFile = document.getElementById('watermark-input').files[0];
    const files = document.getElementById('file-input').files;
    const formData = new FormData();
    // onst scale = document.getElementById('scale-input').value;

    status_text.innerHTML = "Processing images.";

    formData.append('watermark_image', watermarkFile);
    formData.append('opacity', opacity / 100)
    // formData.append('scale', scale)

    for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);
    }

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        for (i=0; i < data.watermarked_images.length; i++){
            // Create a new Image object
            let img = new Image();
            
            // Set the source of the Image object to the base64 string
            img.src = 'data:image/jpeg;base64,' + data.watermarked_images[i];
            
            // Add the image to the list
            watermarked_images.push(img);
        }
        download_allowed = true;
        console.log(watermarked_images);
        alert('Images processed successfully!');
        status_text.innerHTML = "Press the button below to download all of your images!";
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading images.');
        status_text.innerHTML = "Error uploading images, maybe try again.";
        download_allowed = false;
    });
}

function downloadImages() {
    watermarked_images.forEach((img, index) => {
        // Create a link element
        let link = document.createElement('a');
        
        // Set the href attribute to the image source
        link.href = img.src;
        
        // Set the download attribute to specify the filename
        link.download = 'image_' + index + '.jpg';
        
        // Append the link to the document body
        document.body.appendChild(link);
        
        // Simulate a click on the link to trigger the download
        link.click();
        
        // Remove the link from the document body
        document.body.removeChild(link);
    });
}