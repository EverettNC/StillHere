// Create Memorial Page JavaScript
let uploadedFiles = [];
let formData = {};

// Upload Zone
const uploadZone = document.getElementById('upload-zone');
const fileInput = document.getElementById('file-input');
const uploadedPhotos = document.getElementById('uploaded-photos');

uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            uploadedFiles.push(file);
            displayPhoto(file);
        }
    });
    
    document.getElementById('next-to-details').disabled = uploadedFiles.length === 0;
}

function displayPhoto(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const photoItem = document.createElement('div');
        photoItem.className = 'photo-item';
        photoItem.innerHTML = `
            <img src="${e.target.result}" alt="Uploaded photo">
            <button class="photo-remove" onclick="removePhoto(this)">×</button>
        `;
        uploadedPhotos.appendChild(photoItem);
    };
    reader.readAsDataURL(file);
}

function removePhoto(button) {
    const photoItem = button.parentElement;
    const index = Array.from(uploadedPhotos.children).indexOf(photoItem);
    uploadedFiles.splice(index, 1);
    photoItem.remove();
    
    document.getElementById('next-to-details').disabled = uploadedFiles.length === 0;
}

// Navigation between steps
document.getElementById('next-to-details')?.addEventListener('click', () => {
    showStep('step-details');
});

document.getElementById('back-to-upload')?.addEventListener('click', () => {
    showStep('step-upload');
});

document.getElementById('next-to-preview')?.addEventListener('click', () => {
    collectFormData();
    generatePreview();
    showStep('step-preview');
});

document.getElementById('back-to-details')?.addEventListener('click', () => {
    showStep('step-details');
});

function showStep(stepId) {
    document.querySelectorAll('.step-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(stepId).classList.add('active');
    window.scrollTo(0, 0);
}

function collectFormData() {
    const form = document.getElementById('details-form');
    const inputs = form.querySelectorAll('input, textarea, select');
    
    formData = {};
    inputs.forEach(input => {
        if (input.name) {
            formData[input.name] = input.value;
        }
    });
}

function generatePreview() {
    const summaryContent = document.getElementById('summary-content');
    summaryContent.innerHTML = `
        <div class="summary-item">
            <span class="summary-label">Name</span>
            <div class="summary-value">${formData.name || 'Not provided'}</div>
        </div>
        <div class="summary-item">
            <span class="summary-label">Photos</span>
            <div class="summary-value">${uploadedFiles.length} uploaded</div>
        </div>
        <div class="summary-item">
            <span class="summary-label">Music</span>
            <div class="summary-value">${formData.music || 'Gentle Piano'}</div>
        </div>
        ${formData.speech_text ? `
            <div class="summary-item">
                <span class="summary-label">Message</span>
                <div class="summary-value">${formData.speech_text}</div>
            </div>
        ` : ''}
    `;
}

// Checkout
document.getElementById('checkout-button')?.addEventListener('click', async () => {
    const tier = window.location.pathname.split('/').pop();
    
    try {
        const response = await fetch(`/api/checkout/${tier}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                formData: formData,
                photoCount: uploadedFiles.length
            })
        });
        
        const data = await response.json();
        
        if (data.checkout_url) {
            // Redirect to Stripe checkout
            window.location.href = data.checkout_url;
        } else {
            alert('Checkout coming soon! Your memorial will be created.');
        }
    } catch (error) {
        console.error('Checkout error:', error);
        alert('There was an error processing your request. Please try again.');
    }
});

document.getElementById('create-free')?.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/create-memorial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tier: 'free',
                formData: formData,
                photoCount: uploadedFiles.length
            })
        });
        
        const data = await response.json();
        
        if (data.video_url) {
            window.location.href = `/dashboard?memorial=${data.memorial_id}`;
        } else {
            alert('Your free memorial is being created! Check your dashboard in a few moments.');
        }
    } catch (error) {
        console.error('Creation error:', error);
        alert('There was an error creating your memorial. Please try again.');
    }
});
