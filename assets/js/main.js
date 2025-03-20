// Initialize UI elements 
function initializeUI() {
    console.log('Initializing UI elements');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name-display');
    const textbookName = document.getElementById('textbook-name');
    const lessonName = document.getElementById('lesson-name');
    
    // Clear deck information fields on page load
    textbookName.value = '';
    lessonName.value = '';
    
    // Check if elements exist
    if (!dropZone || !fileInput || !fileNameDisplay || !textbookName || !lessonName) {
        console.error('Required DOM elements not found');
        return;
    }
    
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
        console.log('File dropped');
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    // Handle choose file button click
    chooseFileBtn.addEventListener('click', () => {
        console.log('Choose file button clicked');
        fileInput.click();
    });

    // Display uploaded file name
    fileInput.addEventListener('change', async () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileName = file.name;
            fileNameDisplay.textContent = `Uploaded file: ${fileName}`;
            fileNameDisplay.classList.remove('hidden');
            console.log(`Uploaded file: ${fileName}`);
        } else {
            fileNameDisplay.textContent = '';
            fileNameDisplay.classList.add('hidden');
        }
    });

    textbookName.addEventListener('input', validateForm);
    lessonName.addEventListener('input', validateForm);
    fileInput.addEventListener('change', validateForm);

    console.log('UI initialization complete');
}

// Global function to be called from Python to scroll to the download section
function scrollToDownloadSection() {
    console.log('Scrolling to download section');
    const downloadSection = document.getElementById('download-section');
    if (downloadSection) {
        downloadSection.scrollIntoView({ behavior: 'smooth' });
    } else {
        console.error('Download section not found');
    }
}

// Add the function to the window object to make it accessible from Python
window.scrollToDownloadSection = scrollToDownloadSection;

function validateForm() {
    console.log('Validating form');
    const textbookName = document.getElementById('textbook-name');
    const lessonName = document.getElementById('lesson-name');
    const downloadBtn = document.getElementById('download-btn');
    const vocabularyTableBody = document.getElementById('vocabulary-table-body');
    const fileInput = document.getElementById('file-input');

    // Check if we have at least one vocabulary item
    const hasVocabularyData = vocabularyTableBody && vocabularyTableBody.children.length > 0;
    console.log('Vocabulary table rows:', vocabularyTableBody ? vocabularyTableBody.children.length : 0);

    const isValid = textbookName.value.trim() !== '' && 
                   lessonName.value.trim() !== '' && 
                   fileInput.files && fileInput.files.length > 0 &&
                   hasVocabularyData;

    if (downloadBtn) {
        downloadBtn.disabled = !isValid;
    }
}

// Set up event listeners when both DOM and PyScript are ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM content loaded');
    
    // Check if PyScript is already ready
    if (window.isPyScriptReady) {
        initializeUI();
    } else {
        // Add a listener for when PyScript becomes ready
        document.addEventListener('py:ready', () => {
            console.log('PyScript ready event received in main.js');
            window.isPyScriptReady = true;
            initializeUI();
        });
    }
});

// In case py:ready fires before our listener is attached
document.addEventListener('py:ready', () => {
    window.isPyScriptReady = true;
}); 