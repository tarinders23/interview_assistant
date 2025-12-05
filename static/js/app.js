// Enhanced JavaScript functionality for Interview Assistant

class InterviewAssistant {
    constructor() {
        this.init();
    }

    init() {
        this.setupFileUpload();
        this.setupFormValidation();
        this.setupQuestionGeneration();
        this.setupExportFunctionality();
        this.setupKeyboardShortcuts();
    }

    setupFileUpload() {
        const fileInput = document.getElementById('resume');
        const uploadArea = document.querySelector('.file-upload-area');
        
        if (!fileInput || !uploadArea) return;

        // Enhanced drag and drop
        uploadArea.addEventListener('dragenter', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            if (!uploadArea.contains(e.relatedTarget)) {
                uploadArea.classList.remove('drag-over');
            }
        });

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelection(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelection(e.target.files[0]);
            }
        });
    }

    handleFileSelection(file) {
        const fileInput = document.getElementById('resume');
        const uploadContent = document.getElementById('upload-content');
        const fileSelected = document.getElementById('file-selected');
        const fileName = document.getElementById('file-name');

        // Validate file type (PDF, DOCX, or TXT)
        const validMimeTypes = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        ];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        const validExtensions = ['.pdf', '.docx', '.txt'];
        
        const isValidType = validMimeTypes.includes(file.type) || validExtensions.includes(fileExtension);
        
        if (!isValidType) {
            this.showToast('Please select a PDF, DOCX, or TXT file', 'error');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showToast('File size must be less than 10MB', 'error');
            return;
        }

        // Update UI
        uploadContent.classList.add('hidden');
        fileSelected.classList.remove('hidden');
        fileName.textContent = `${file.name} (${this.formatFileSize(file.size)})`;
        
        // Create a new file list for the input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        this.showToast('Resume uploaded successfully', 'success');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    setupFormValidation() {
        const form = document.getElementById('questionForm');
        if (!form) return;

        // Real-time validation
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });

        // Character count for textarea
        const jobDescTextarea = document.getElementById('job_description');
        if (jobDescTextarea) {
            this.setupCharacterCounter(jobDescTextarea);
        }

        // API Key handling
        const apiKeyInput = document.getElementById('api_key');
        if (apiKeyInput) {
            // Try to load from localStorage
            const savedApiKey = localStorage.getItem('gemini_api_key');
            if (savedApiKey) {
                apiKeyInput.value = savedApiKey;
            }

            // Save API key when input changes
            apiKeyInput.addEventListener('change', () => {
                if (apiKeyInput.value) {
                    localStorage.setItem('gemini_api_key', apiKeyInput.value);
                } else {
                    localStorage.removeItem('gemini_api_key');
                }
            });
        }
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        } else if (field.type === 'number') {
            const num = parseInt(value);
            const min = parseInt(field.getAttribute('min'));
            const max = parseInt(field.getAttribute('max'));
            
            if (num < min || num > max) {
                isValid = false;
                errorMessage = `Value must be between ${min} and ${max}`;
            }
        } else if (field.id === 'job_description' && value.length < 50) {
            isValid = false;
            errorMessage = 'Job description should be at least 50 characters';
        } else if (field.id === 'api_key' && value.length < 20) {
            isValid = false;
            errorMessage = 'Please enter a valid Gemini API key';
        }

        this.showFieldError(field, isValid ? '' : errorMessage);
        return isValid;
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        if (message) {
            field.classList.add('border-red-500', 'bg-red-50');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error text-red-600 text-sm mt-1';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        }
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500', 'bg-red-50');
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    setupCharacterCounter(textarea) {
        const counterDiv = document.createElement('div');
        counterDiv.className = 'text-sm text-gray-500 mt-1 text-right';
        textarea.parentNode.appendChild(counterDiv);

        const updateCounter = () => {
            const count = textarea.value.length;
            const minLength = 50;
            
            counterDiv.textContent = `${count} characters`;
            
            if (count < minLength) {
                counterDiv.className = 'text-sm text-red-500 mt-1 text-right';
                counterDiv.textContent += ` (minimum ${minLength})`;
            } else {
                counterDiv.className = 'text-sm text-green-600 mt-1 text-right';
            }
        };

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    setupQuestionGeneration() {
        const form = document.getElementById('questionForm');
        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.generateQuestions(form);
        });
    }

    async generateQuestions(form) {
        // Validate form
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        
        for (const input of inputs) {
            if (!this.validateField(input)) {
                isValid = false;
            }
        }

        if (!isValid) {
            this.showToast('Please fix the errors in the form', 'error');
            return;
        }

        this.showLoading();
        
        try {
            const formData = new FormData(form);
            
            // Add progress indicator
            const progressSteps = [
                'Uploading resume...',
                'Parsing resume content...',
                'Analyzing job requirements...',
                'Generating questions with AI...',
                'Formatting results...'
            ];
            
            this.showProgressSteps(progressSteps);
            
            const response = await fetch('/api/v1/generate-questions', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate questions');
            }

            const result = await response.json();
            this.displayQuestions(result);
            this.showToast('Questions generated successfully!', 'success');
            
            // Smooth scroll to results
            setTimeout(() => {
                document.getElementById('results-section').scrollIntoView({ 
                    behavior: 'smooth' 
                });
            }, 300);
            
        } catch (error) {
            console.error('Generation error:', error);
            this.showToast(error.message || 'Failed to generate questions', 'error');
        } finally {
            this.hideLoading();
        }
    }

    showProgressSteps(steps) {
        const loadingOverlay = document.getElementById('loading-overlay');
        const content = loadingOverlay.querySelector('div');
        
        let currentStep = 0;
        const stepElement = document.createElement('p');
        stepElement.className = 'text-gray-600 text-sm mt-4';
        content.appendChild(stepElement);

        const updateStep = () => {
            if (currentStep < steps.length) {
                stepElement.textContent = steps[currentStep];
                currentStep++;
                setTimeout(updateStep, 1500);
            }
        };

        updateStep();
    }

    displayQuestions(data) {
        const resultsSection = document.getElementById('results-section');
        const questionsContainer = document.getElementById('questions-container');
        
        if (!resultsSection || !questionsContainer) return;

        resultsSection.classList.remove('hidden');
        questionsContainer.innerHTML = '';

        // Add summary card with animation
        this.createSummaryCard(data, questionsContainer);

        // Add questions with staggered animation
        data.questions.forEach((question, index) => {
            setTimeout(() => {
                this.createQuestionCard(question, index, questionsContainer);
            }, index * 100);
        });

        // Store data for export
        this.currentQuestions = data;
    }

    createSummaryCard(data, container) {
        const summaryCard = document.createElement('div');
        summaryCard.className = 'bg-gradient-to-r from-primary-500 to-purple-600 text-white rounded-xl p-6 mb-6 opacity-0 transform -translate-y-4';
        
        summaryCard.innerHTML = `
            <h3 class="text-xl font-bold mb-4">Generation Summary</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                    <div class="text-2xl font-bold">${data.total_questions}</div>
                    <div class="text-sm opacity-90">Questions</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                    <div class="text-lg font-bold capitalize">${data.round_type.replace('_', ' ')}</div>
                    <div class="text-sm opacity-90">Interview Type</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                    <div class="text-lg font-bold capitalize">${data.difficulty}</div>
                    <div class="text-sm opacity-90">Difficulty</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                    <div class="text-lg font-bold">${data.metadata?.model || 'Gemini'}</div>
                    <div class="text-sm opacity-90">AI Model</div>
                </div>
            </div>
        `;
        
        container.appendChild(summaryCard);
        
        // Animate in
        setTimeout(() => {
            summaryCard.classList.remove('opacity-0', '-translate-y-4');
            summaryCard.classList.add('transition-all', 'duration-500');
        }, 100);
    }

    createQuestionCard(question, index, container) {
        const questionCard = document.createElement('div');
        questionCard.className = 'question-card bg-white rounded-xl shadow-lg p-6 mb-6 border-l-4 border-primary-500 opacity-0 transform translate-x-8';
        
        questionCard.innerHTML = `
            <div class="flex justify-between items-start mb-4">
                <div class="flex items-center flex-wrap gap-2">
                    <span class="bg-primary-100 text-primary-800 text-sm font-semibold px-3 py-1 rounded-full">
                        Question ${index + 1}
                    </span>
                    <span class="bg-gray-100 text-gray-800 text-sm font-semibold px-3 py-1 rounded-full">
                        ${question.category}
                    </span>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-500 capitalize px-2 py-1 bg-gray-50 rounded">${question.difficulty}</span>
                    <button class="copy-question text-gray-400 hover:text-primary-600 transition-colors" title="Copy question">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                        </svg>
                    </button>
                </div>
            </div>
            
            <h3 class="text-lg font-semibold text-gray-900 mb-4 leading-relaxed">
                ${question.question}
            </h3>
            
            ${question.context ? `
                <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4 rounded-r">
                    <p class="text-sm text-blue-800"><strong>Context:</strong> ${question.context}</p>
                </div>
            ` : ''}
            
            ${question.follow_up_questions && question.follow_up_questions.length > 0 ? `
                <div class="mt-4">
                    <h4 class="font-medium text-gray-900 mb-2 flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Follow-up Questions:
                    </h4>
                    <ul class="list-disc list-inside text-sm text-gray-700 space-y-1 ml-4">
                        ${question.follow_up_questions.map(q => `<li>${q}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${question.expected_topics && question.expected_topics.length > 0 ? `
                <div class="mt-4">
                    <h4 class="font-medium text-gray-900 mb-2 flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                        </svg>
                        Expected Topics:
                    </h4>
                    <div class="flex flex-wrap gap-2">
                        ${question.expected_topics.map(topic => 
                            `<span class="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded-full">${topic}</span>`
                        ).join('')}
                    </div>
                </div>
            ` : ''}
        `;
        
        container.appendChild(questionCard);
        
        // Add copy functionality
        const copyBtn = questionCard.querySelector('.copy-question');
        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(question.question).then(() => {
                this.showToast('Question copied to clipboard', 'success');
            });
        });
        
        // Animate in
        setTimeout(() => {
            questionCard.classList.remove('opacity-0', 'translate-x-8');
            questionCard.classList.add('transition-all', 'duration-500');
        }, 100);
    }

    setupExportFunctionality() {
        const exportBtn = document.getElementById('export-questions');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportQuestions();
            });
        }
    }

    exportQuestions() {
        if (!this.currentQuestions) {
            this.showToast('No questions to export', 'warning');
            return;
        }

        // Generate text content
        let content = `Interview Questions - Generated by Interview Assistant\n`;
        content += `================================================\n\n`;
        content += `Summary:\n`;
        content += `- Total Questions: ${this.currentQuestions.total_questions}\n`;
        content += `- Interview Type: ${this.currentQuestions.round_type.replace('_', ' ')}\n`;
        content += `- Difficulty: ${this.currentQuestions.difficulty}\n`;
        content += `- Generated: ${new Date().toLocaleDateString()}\n\n`;

        this.currentQuestions.questions.forEach((question, index) => {
            content += `Question ${index + 1} (${question.category})\n`;
            content += `${'-'.repeat(50)}\n`;
            content += `${question.question}\n\n`;
            
            if (question.context) {
                content += `Context: ${question.context}\n\n`;
            }
            
            if (question.follow_up_questions && question.follow_up_questions.length > 0) {
                content += `Follow-up Questions:\n`;
                question.follow_up_questions.forEach(fq => {
                    content += `- ${fq}\n`;
                });
                content += `\n`;
            }
            
            if (question.expected_topics && question.expected_topics.length > 0) {
                content += `Expected Topics: ${question.expected_topics.join(', ')}\n`;
            }
            
            content += `\n\n`;
        });

        // Create and download file
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `interview-questions-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showToast('Questions exported successfully', 'success');
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Enter to submit form
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const form = document.getElementById('questionForm');
                if (form) {
                    e.preventDefault();
                    form.dispatchEvent(new Event('submit'));
                }
            }
            
            // Escape to close loading overlay
            if (e.key === 'Escape') {
                this.hideLoading();
            }
        });
    }

    showLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('hidden');
            overlay.classList.add('flex');
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.add('hidden');
            overlay.classList.remove('flex');
            
            // Clear progress steps
            const progressStep = overlay.querySelector('p.text-gray-600');
            if (progressStep) {
                progressStep.remove();
            }
        }
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : 
                       type === 'error' ? 'bg-red-500' : 
                       type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500';
        
        toast.className = `toast ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full opacity-0 flex items-center space-x-2`;
        
        const icon = this.getToastIcon(type);
        toast.innerHTML = `${icon}<span>${message}</span>`;
        
        container.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.classList.remove('translate-x-full', 'opacity-0');
        }, 100);
        
        // Remove after 5 seconds
        setTimeout(() => {
            toast.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    getToastIcon(type) {
        const icons = {
            success: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>',
            error: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>',
            warning: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path></svg>',
            info: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
        };
        return icons[type] || icons.info;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new InterviewAssistant();
});

// Utility functions for backward compatibility
function showLoading() {
    const instance = window.interviewAssistant || new InterviewAssistant();
    instance.showLoading();
}

function hideLoading() {
    const instance = window.interviewAssistant || new InterviewAssistant();
    instance.hideLoading();
}

function showToast(message, type = 'info') {
    const instance = window.interviewAssistant || new InterviewAssistant();
    instance.showToast(message, type);
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500');
            isValid = false;
        } else {
            input.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}
