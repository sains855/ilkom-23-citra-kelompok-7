document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.querySelector('input[type="file"]');
  const previewImg = document.createElement('img');
  const sizeInfo = document.createElement('p');

  previewImg.style.maxWidth = '300px';
  previewImg.style.marginTop = '10px';
  sizeInfo.style.fontSize = '14px';

  if (fileInput) {
    fileInput.parentNode.insertBefore(previewImg, fileInput.nextSibling);
    fileInput.parentNode.insertBefore(sizeInfo, previewImg.nextSibling);

    fileInput.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        alert('Harap pilih file gambar (jpg, jpeg, png)');
        fileInput.value = '';
        previewImg.src = '';
        sizeInfo.textContent = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        previewImg.src = e.target.result;
        sizeInfo.textContent = `Ukuran File: ${(file.size / 1024).toFixed(2)} KB`;
      };
      reader.readAsDataURL(file);
    });
  }
});
