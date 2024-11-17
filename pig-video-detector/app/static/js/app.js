/**
 * Video Upload and Processing Handler
 * Manages file uploads, progress tracking, and UI updates for video processing
 */
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const progressArea = document.getElementById('progress-area');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercentage = document.getElementById('progress-percentage');
    const progressStatus = document.getElementById('progress-status');
    const downloadArea = document.getElementById('download-area');
    const downloadLink = document.getElementById('download-link');
    const errorArea = document.getElementById('error-area');
    const errorMessage = document.getElementById('error-message');
    const uploadButton = document.getElementById('upload-button');
    const uploadText = document.getElementById('upload-text');

    // Configuration
    const config = {
        validTypes: ['video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-ms-wmv'],
        maxSize: 100 * 1024 * 1024, // 100MB
        progressInterval: 1000, // Check progress every second
        maxRetries: 3, // Maximum number of retries for progress checks
        errorDisplayTime: 5000 // How long to show error messages (ms)
    };

    // State
    let state = {
        isUploading: false,
        progressChecker: null,
        lastProgress: 0,
        retryCount: 0,
        startTime: null,
        fileSize: 0
    };

    function estimateRemainingTime(progress) {
        if (!state.startTime || progress <= 0) return null;
        
        const elapsedSeconds = (Date.now() - state.startTime) / 1000;
        const progressPercent = progress / 100;
        
        if (progressPercent === 0) return null;
        
        const estimatedTotalSeconds = elapsedSeconds / progressPercent;
        const remainingSeconds = estimatedTotalSeconds - elapsedSeconds;
        
        if (remainingSeconds > 0 && remainingSeconds < 7200) { // max 2 hours
            return Math.ceil(remainingSeconds / 60); // Convert to minutes
        }
        return null;
    }

    function disableUploadInterface() {
        uploadArea.classList.add('processing', 'pointer-events-none', 'opacity-50');
        uploadButton.disabled = true;
        uploadButton.classList.add('opacity-50', 'cursor-not-allowed');
        fileInput.disabled = true;
        if (uploadText) {
            uploadText.textContent = 'Processing video...';
        }
    }

    function enableUploadInterface() {
        uploadArea.classList.remove('processing', 'pointer-events-none', 'opacity-50');
        uploadButton.disabled = false;
        uploadButton.classList.remove('opacity-50', 'cursor-not-allowed');
        fileInput.disabled = false;
        if (uploadText) {
            uploadText.textContent = 'Upload video (max 100MB)';
        }
    }

    function initializeEventListeners() {
        // Prevent default drag and drop behavior
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        // Handle drag and drop visual feedback
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });

        // File handling events
        uploadArea.addEventListener('drop', handleDrop);
        uploadButton.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', handleChange);

        // Clean up on page unload
        window.addEventListener('beforeunload', cleanup);
    }

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        if (!state.isUploading) {
            uploadArea.classList.add('border-pink-300', 'bg-gray-100');
        }
    }

    function unhighlight() {
        uploadArea.classList.remove('border-pink-300', 'bg-gray-100');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleChange(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0 && !state.isUploading) {
            const file = files[0];
            if (validateFile(file)) {
                uploadFile(file);
            }
        }
    }

    function validateFile(file) {
        if (!config.validTypes.includes(file.type)) {
            showError('Please upload only MP4, AVI, MOV, or WMV files.');
            return false;
        }

        if (file.size > config.maxSize) {
            const sizeMB = Math.round(file.size / (1024 * 1024));
            showError(`File size (${sizeMB}MB) exceeds maximum limit of 100MB.`);
            return false;
        }

        return true;
    }

    function showError(message) {
        console.error('Error:', message);
        errorMessage.textContent = message;
        errorArea.classList.remove('hidden');
        
        setTimeout(() => {
            errorArea.classList.add('hidden');
        }, config.errorDisplayTime);
    }

    function updateProgress(progress) {
        const percentage = Math.min(Math.round(progress), 100);
        
        progressBar.style.width = `${percentage}%`;
        progressPercentage.textContent = `${percentage}%`;
        progressStatus.textContent = 'Processing...';
        
        if (percentage < 100) {
            const remainingMinutes = estimateRemainingTime(percentage);
            let statusText = '';
            
            if (remainingMinutes !== null) {
                statusText += ` (Aprox. ${remainingMinutes} min. left)`;
            }
            
            progressText.textContent = statusText;
        } else {
            progressText.textContent = 'Procesamiento completado!';
            progressStatus.textContent = 'Completado!';
            downloadArea.classList.remove('hidden');
            cleanup();
        }
    }

    async function checkProgress() {
        try {
            const response = await fetch('/progress');
            if (!response.ok) {
                throw new Error('Progress check failed');
            }

            const data = await response.json();
            console.log('Progress update:', data);

            if (data.progress != null) {
                const progress = Math.max(state.lastProgress, data.progress);
                state.lastProgress = progress;
                updateProgress(progress);

                if (progress >= 100) {
                    cleanup();
                    finishProcessing();
                }
            }

            state.retryCount = 0;

        } catch (error) {
            console.error('Error checking progress:', error);
            state.retryCount++;

            if (state.retryCount >= config.maxRetries) {
                showError('Lost connection to server. Please refresh the page.');
                cleanup();
                enableUploadInterface();
            }
        }
    }

    function startProgressMonitoring() {
        if (state.progressChecker) {
            clearInterval(state.progressChecker);
        }

        state.lastProgress = 0;
        state.retryCount = 0;
        state.progressChecker = setInterval(checkProgress, config.progressInterval);
    }

    function cleanup() {
        if (state.progressChecker) {
            clearInterval(state.progressChecker);
            state.progressChecker = null;
        }
        
        // Solo resetear si no se completó exitosamente
        if (state.lastProgress < 100) {
            resetUploadInterface();
        }
    }

    function resetUploadInterface() {
        // Rehabilitar la interfaz de carga
        uploadArea.classList.remove('processing', 'pointer-events-none', 'opacity-50');
        uploadButton.disabled = false;
        uploadButton.classList.remove('opacity-50', 'cursor-not-allowed');
        fileInput.disabled = false;
        
        // Restaurar el texto original
        const uploadText = document.getElementById('upload-text');
        if (uploadText) {
            uploadText.textContent = 'Upload video (max 100MB)';
        }
    
        // Reiniciar la barra de progreso
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
        progressStatus.textContent = '';
        progressText.textContent = '';
        
        // Ocultar áreas de progreso y descarga
        progressArea.classList.add('hidden');
        downloadArea.classList.add('hidden');
        
        // Limpiar el input de archivo
        fileInput.value = '';
        
        // Reiniciar el estado
        state.isUploading = false;
        state.lastProgress = 0;
        state.retryCount = 0;
        state.startTime = null;
        state.fileSize = 0;
    }

    function finishProcessing() {
    downloadArea.classList.remove('hidden');
    progressStatus.textContent = 'Complete!';
    progressText.textContent = 'Video processing completed successfully';
    uploadArea.classList.remove('processing');
    state.isUploading = false;
    
    // Agregar event listener al botón de descarga
    const downloadButton = downloadArea.querySelector('.download-button') || downloadLink;
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            // Esperar un momento breve para que comience la descarga antes de resetear
            setTimeout(resetUploadInterface, 1000);
        }, { once: true }); // El evento se elimina después de ejecutarse una vez
    }
}

    function resetUI() {
        progressArea.classList.remove('hidden');
        downloadArea.classList.add('hidden');
        errorArea.classList.add('hidden');
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
        progressStatus.textContent = 'Processing...';
        progressBar.classList.remove('progress-bar-animated');
    }

    async function uploadFile(file) {
        if (state.isUploading) return;

        state.isUploading = true;
        state.startTime = Date.now();
        state.fileSize = file.size;
        
        disableUploadInterface();
        resetUI();

        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            if (data.processed_video) {
                downloadLink.href = data.processed_video;
                downloadLink.download = `processed_${file.name}`;
                startProgressMonitoring();
            } else {
                throw new Error('No processed video URL received');
            }

        } catch (error) {
            console.error('Upload error:', error);
            showError(error.message || 'Error uploading file');
            cleanup();
            enableUploadInterface();
        }
    }

    // Initialize the application
    initializeEventListeners();
    console.log('Video upload handler initialized');
});