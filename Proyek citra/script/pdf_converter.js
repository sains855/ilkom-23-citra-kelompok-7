document.addEventListener("DOMContentLoaded", function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const convertBtn = document.querySelector('.convert-btn');
    
    // Handle drag and drop
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        fileInput.files = e.dataTransfer.files;
        handleFiles(fileInput.files);
    });
    
    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });
    
    function handleFiles(files) {
        previewContainer.innerHTML = '';
        
        if (files.length > 0) {
            convertBtn.disabled = false;
            uploadArea.style.display = 'none';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const previewItem = document.createElement('div');
                    previewItem.className = 'preview-item';
                    
                    previewItem.innerHTML = `
                        <img src="${e.target.result}" alt="Preview">
                        <span>${file.name}</span>
                        <span class="file-size">${formatFileSize(file.size)}</span>
                    `;
                    
                    previewContainer.appendChild(previewItem);
                };
                
                reader.readAsDataURL(file);
            }
        } else {
            convertBtn.disabled = true;
            uploadArea.style.display = 'block';
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
});