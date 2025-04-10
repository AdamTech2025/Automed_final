// Dental Code Extractor Pro - Main JS

document.addEventListener('DOMContentLoaded', function() {
    // Initialize process steps
    const processSteps = {
        'starting': { id: 'step-start', title: 'Starting Analysis', icon: 'fa-play-circle' },
        'cleaning': { id: 'step-clean', title: 'Cleaning Data', icon: 'fa-broom' },
        'storing': { id: 'step-store', title: 'Storing Data', icon: 'fa-database' },
        'analyzing_cdt': { id: 'step-cdt', title: 'Analyzing CDT', icon: 'fa-search' },
        'activating_cdt': { id: 'step-activate-cdt', title: 'Activating Topics', icon: 'fa-code-branch' },
        'analyzing_icd': { id: 'step-icd', title: 'Analyzing ICD', icon: 'fa-heartbeat' },
        'validating': { id: 'step-validate', title: 'Validating', icon: 'fa-check-double' },
        'complete': { id: 'step-complete', title: 'Complete', icon: 'fa-flag-checkered' },
    };
    
    // Track analysis state
    let isAnalyzing = false;
    
    // Handle form submission
    const form = document.getElementById('dental-form');
    const loadingContainer = document.getElementById('loading-container');
    const processTimeline = document.getElementById('process-timeline');
    const resultsContainer = document.querySelector('.results-container');
    
    // If we already have results, hide loading (this is for page refreshes)
    if (resultsContainer || document.querySelector('.alert-danger')) {
        if (loadingContainer) loadingContainer.style.display = 'none';
        if (processTimeline) processTimeline.style.display = 'none';
    }
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Get the scenario text
            const scenarioText = document.getElementById('scenario').value;
            if (!scenarioText.trim()) {
                e.preventDefault(); // Prevent empty submissions
                showStatusNotification('error', 'Empty Input', 'Please enter a dental scenario');
                return;
            }
            
            // Show the loading UI - will remain visible until page refreshes with results
            if (loadingContainer) loadingContainer.style.display = 'flex';
            
            // Show process timeline
            if (processTimeline) {
                processTimeline.style.display = 'flex';
                initializeTimeline();
            }
            
            // Set analyzing state to true
            isAnalyzing = true;
            
            // Let form submission proceed normally
            // The server will process the request and return the results
            // Loading will remain visible until the page refreshes with new content
        });
    }
    
    // Initialize process timeline
    function initializeTimeline() {
        // Clear existing steps
        if (processTimeline) {
            processTimeline.innerHTML = '';
            
            // Add process line
            const processLine = document.createElement('div');
            processLine.className = 'process-line';
            processTimeline.appendChild(processLine);
            
            // Add all steps as "waiting"
            Object.entries(processSteps).forEach(([key, step], index) => {
                const stepElement = document.createElement('div');
                stepElement.className = 'process-step';
                stepElement.id = step.id;
                
                const iconElement = document.createElement('div');
                iconElement.className = 'step-icon';
                iconElement.innerHTML = `<i class="fas ${step.icon}"></i>`;
                
                const contentElement = document.createElement('div');
                contentElement.className = 'step-content';
                
                const titleElement = document.createElement('div');
                titleElement.className = 'step-title';
                titleElement.textContent = step.title;
                
                const descriptionElement = document.createElement('div');
                descriptionElement.className = 'step-description';
                
                // Just show all steps as "Processing..."
                stepElement.className = 'process-step active';
                descriptionElement.textContent = 'Processing...';
                
                contentElement.appendChild(titleElement);
                contentElement.appendChild(descriptionElement);
                
                stepElement.appendChild(iconElement);
                stepElement.appendChild(contentElement);
                
                processTimeline.appendChild(stepElement);
                
                // Add pulse animation to each step
                iconElement.style.animation = 'pulse 1.5s infinite';
            });
        }
    }
    
    // Show status notification
    function showStatusNotification(type, title, message) {
        // Create notification if it doesn't exist
        let statusBox = document.getElementById('status-notification');
        if (!statusBox) {
            statusBox = document.createElement('div');
            statusBox.id = 'status-notification';
            statusBox.className = 'status-box';
            document.body.appendChild(statusBox);
        }
        
        // Update content and show
        statusBox.className = `status-box ${type}`;
        statusBox.innerHTML = `
            <div class="status-title">${title}</div>
            <div class="status-message">${message}</div>
        `;
        
        statusBox.classList.add('show');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusBox.classList.remove('show');
        }, 5000);
    }
    
    // Handle question form submission
    const submitQuestionsBtn = document.getElementById('submitQuestionsBtn');
    if (submitQuestionsBtn) {
        submitQuestionsBtn.addEventListener('click', function() {
            const form = document.getElementById('questionsForm');
            if (form && form.checkValidity()) {
                // Show loading while processing answers
                if (loadingContainer) loadingContainer.style.display = 'flex';
                if (processTimeline) {
                    processTimeline.style.display = 'flex';
                    initializeTimeline();
                }
            }
        });
    }
}); 