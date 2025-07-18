let cropper;
const inputImage = document.getElementById('inputImage');
const image = document.getElementById('image');
const cropButton = document.getElementById('cropButton');

inputImage.addEventListener('change', function (e) {
    const files = e.target.files;
    const done = (url) => {
        image.src = url;
        image.style.display = 'block';
        if (cropper) cropper.destroy();
        cropper = new Cropper(image, {
            aspectRatio: NaN,
            viewMode: 1
        });
        cropButton.style.display = 'inline-block';
    };

    if (files && files.length > 0) {
        const reader = new FileReader();
        reader.onload = () => {
            done(reader.result);
        };
        reader.readAsDataURL(files[0]);
    }
});

cropButton.addEventListener('click', function () {
    if (cropper) {
        const cropData = cropper.getData();   // ✅ Ambil koordinat crop
        console.log('Koordinat Crop:', cropData); 

        const canvas = cropper.getCroppedCanvas();
        canvas.toBlob(function (blob) {
            const formData = new FormData();
            formData.append('croppedImage', blob, 'cropped.png');

            // Kalau mau kirim koordinat ke backend:
            formData.append('x', cropData.x);
            formData.append('y', cropData.y);
            formData.append('width', cropData.width);
            formData.append('height', cropData.height);

            fetch('/process_crop', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    alert('Crop failed.');
                }
            })
            .catch(() => {
                alert('Crop upload error.');
            });
        }, 'image/png');
    }
});
