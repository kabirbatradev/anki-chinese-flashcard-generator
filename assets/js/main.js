document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const chooseFileBtn = dropZone.querySelector('button');

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        });
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    // Handle choose file button click
    chooseFileBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Form validation
    const textbookName = document.getElementById('textbook-name');
    const lessonName = document.getElementById('lesson-name');
    const downloadBtn = document.getElementById('download-btn');

    function validateForm() {
        const isValid = textbookName.value.trim() !== '' && 
                       lessonName.value.trim() !== '' && 
                       fileInput.files.length > 0;
        downloadBtn.disabled = !isValid;
    }

    textbookName.addEventListener('input', validateForm);
    lessonName.addEventListener('input', validateForm);
    fileInput.addEventListener('change', validateForm);
}); 