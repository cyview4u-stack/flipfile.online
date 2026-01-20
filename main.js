// Enhanced Ripple Effect with Color Coding and Sound Effects
document.addEventListener('DOMContentLoaded', function() {
    
    // Create sound function for button clicks (optional)
    function createClickSound(type) {
        // In a real app, you would play actual sound files
        console.log(`${type} button clicked with enhanced ripple effect`);
    }
    
    // Enhanced ripple creation with color matching
    function createRipple(event) {
        const button = event.currentTarget;
        const rect = button.getBoundingClientRect();
        const circle = document.createElement('span');
        const diameter = Math.max(rect.width, rect.height);
        const radius = diameter / 2;
        
        // Set circle position and size
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - rect.left - radius}px`;
        circle.style.top = `${event.clientY - rect.top - radius}px`;
        circle.classList.add('ripple');
        
        // Determine button type and set appropriate ripple color
        if (button.classList.contains('btn-pdf')) {
            circle.style.backgroundColor = 'rgba(255, 35, 35, 0.7)';
            createClickSound('PDF');
        } else if (button.classList.contains('btn-language')) {
            circle.style.backgroundColor = 'rgba(76, 140, 245, 0.7)';
            createClickSound('Language');
        } else if (button.classList.contains('btn-login')) {
            circle.style.backgroundColor = 'rgba(255, 191, 0, 0.7)';
            createClickSound('Login');
        } else {
            circle.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        }
        
        // Remove any existing ripples
        const existingRipple = button.getElementsByClassName('ripple')[0];
        if (existingRipple) {
            existingRipple.remove();
        }
        
        // Add the new ripple
        button.appendChild(circle);
        
        // Remove ripple after animation completes
        setTimeout(() => {
            if (circle.parentNode === button) {
                circle.remove();
            }
        }, 800);
    }
    
    // Add enhanced ripple effect to all buttons
    document.querySelectorAll('.ripple-btn').forEach(button => {
        button.addEventListener('click', createRipple);
        
        // Enhanced hover effects with color transitions
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.15)';
            
            // Add color-specific glow effects
            if (this.classList.contains('btn-pdf')) {
                this.style.boxShadow = '0 6px 20px rgba(255, 35, 35, 0.3)';
            } else if (this.classList.contains('btn-language')) {
                this.style.boxShadow = '0 6px 20px rgba(76, 140, 245, 0.3)';
            } else if (this.classList.contains('btn-login')) {
                this.style.boxShadow = '0 6px 20px rgba(255, 191, 0, 0.3)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Mobile button functionality with enhanced feedback
    document.querySelectorAll('.mobile-button-group .btn').forEach(button => {
        button.addEventListener('click', function() {
            const text = this.querySelector('span').textContent;
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            if (text === 'PDF All Tools') {
                showMobileToolsModal();
            } else if (text === 'Lingo') {
                showLanguageModal();
            } else if (text === 'Login') {
                showLoginModal();
            }
        });
    });
    
    // File Upload Functionality
    const dropZone = document.getElementById('dropZone');
    const selectFileBtn = document.querySelector('.select-file-btn');
    
    if (dropZone) {
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.style.backgroundColor = '#e8e5db';
            dropZone.style.borderStyle = 'solid';
            dropZone.style.borderColor = '#1AA260';
            dropZone.style.boxShadow = '0 0 20px rgba(26, 162, 96, 0.3)';
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.style.backgroundColor = '';
            dropZone.style.borderStyle = 'dashed';
            dropZone.style.borderColor = '#1AA260';
            dropZone.style.boxShadow = 'none';
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.style.backgroundColor = '';
            dropZone.style.borderStyle = 'dashed';
            dropZone.style.boxShadow = 'none';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelection(files);
            }
        });
    }
    
    if (selectFileBtn) {
        selectFileBtn.addEventListener('click', () => {
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.multiple = true;
            fileInput.accept = '.pdf,.jpg,.jpeg,.svg,.png,.tiff,.doc,.docx,.xls,.xlsx,.ppt,.pptx';
            
            fileInput.addEventListener('change', (e) => {
                const files = e.target.files;
                if (files.length > 0) {
                    handleFileSelection(files);
                }
            });
            
            fileInput.click();
        });
    }
    
    function handleFileSelection(files) {
        const originalHTML = dropZone.innerHTML;
        
        // Show enhanced processing indicator with color animation
        dropZone.innerHTML = `
            <div style="text-align: center;">
                <i class="fas fa-spinner fa-spin" style="font-size: 48px; color: #1AA260; margin-bottom: 20px; animation: color-change 2s infinite;"></i>
                <div class="drag-drop-text">Processing ${files.length} file(s)...</div>
                <div class="drag-drop-subtext">Please wait while we securely process your files</div>
                <div style="margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #f5f5f5, #e8e5db); border-radius: 4px;">
                    <div class="ad-label">Advertisement</div>
                    <div style="height: 90px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #999;">
                        <i class="fas fa-ad"></i>
                        <span>Processing Ad - Files will be ready shortly</span>
                    </div>
                </div>
            </div>
        `;
        
        // Add CSS for color animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes color-change {
                0% { color: #1AA260; }
                50% { color: #4C8CF5; }
                100% { color: #1AA260; }
            }
        `;
        document.head.appendChild(style);
        
        // Simulate processing with enhanced delay
        setTimeout(() => {
            // Reset drop zone
            dropZone.innerHTML = originalHTML;
            
            // Re-attach event listeners
            document.querySelector('.select-file-btn').addEventListener('click', () => {
                selectFileBtn.click();
            });
            
            // Show enhanced success message
            showEnhancedNotification(`Successfully processed ${files.length} file(s)! Files are ready for download.`, 'success');
            
        }, 3000);
    }
    
    function showEnhancedNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const icon = type === 'success' ? 'fa-check-circle' : 
                    type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
        const color = type === 'success' ? '#1AA260' : 
                    type === 'error' ? '#FF2323' : '#4C8CF5';
        
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 15px 20px;
            background-color: ${color};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            font-size: 14px;
            max-width: 300px;
            display: flex;
            align-items: center;
            border-left: 4px solid white;
        `;
        notification.innerHTML = `
            <i class="fas ${icon}" style="margin-right: 10px; font-size: 16px;"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 500);
        }, 3000);
        
        // Add animation keyframes if not already present
        if (!document.querySelector('#notification-animations')) {
            const animStyle = document.createElement('style');
            animStyle.id = 'notification-animations';
            animStyle.textContent = `
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutRight {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(animStyle);
        }
    }
    
    // Add enhanced CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes highlight {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
            100% { transform: scale(1); }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(26, 162, 96, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(26, 162, 96, 0); }
            100% { box-shadow: 0 0 0 0 rgba(26, 162, 96, 0); }
        }
        
        @keyframes color-shift {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
        
        .tool-card:hover {
            animation: pulse 2s infinite;
        }
        
        /* Enhanced button animations */
        .btn-pdf, .btn-language, .btn-login {
            position: relative;
            z-index: 1;
        }
        
        .btn-pdf::before, .btn-language::before, .btn-login::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: inherit;
            border-radius: inherit;
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .btn-pdf:hover::before {
            opacity: 1;
            animation: color-shift 2s infinite;
        }
    `;
    document.head.appendChild(style);
});

// Modal Functions with enhanced styling
window.showMobileToolsModal = function() {
    const modalHTML = `
        <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
            <div style="background: white; padding: 25px; border-radius: 12px; width: 90%; max-width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">All PDF Tools</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                    <button onclick="selectTool('PDF Converter')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-exchange-alt"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Convert</span>
                    </button>
                    <button onclick="selectTool('PDF Compressor')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-compress-alt"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Compress</span>
                    </button>
                    <button onclick="selectTool('Color Extractor')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-palette"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Color</span>
                    </button>
                    <button onclick="selectTool('Protect PDF')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-lock"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Protect</span>
                    </button>
                    <button onclick="selectTool('Unlock PDF')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-unlock"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Unlock</span>
                    </button>
                    <button onclick="selectTool('Edit PDF')" style="background: #1AA260; color: white; border: none; padding: 12px; border-radius: 6px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s;">
                        <i class="fas fa-edit"></i>
                        <span style="margin-top: 5px; font-size: 12px;">Edit</span>
                    </button>
                </div>
                <button onclick="this.closest('.modal-overlay').remove()" style="margin-top: 20px; padding: 10px; background: #FF2323; color: white; border: none; border-radius: 6px; width: 100%; cursor: pointer; transition: all 0.3s;">Close</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add hover effects to modal buttons
    document.querySelectorAll('.modal-overlay button').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
};

window.showLanguageModal = function() {
    const modalHTML = `
        <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
            <div style="background: white; padding: 25px; border-radius: 12px; width: 90%; max-width: 300px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #4C8CF5;">
                <h3 style="color: #4C8CF5; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Select Language</h3>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <button onclick="setLanguage('en')" style="display: flex; align-items: center; gap: 10px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; text-align: left; transition: all 0.3s;">
                        <span style="font-size: 20px;">🇺🇸</span>
                        <span>English</span>
                    </button>
                    <button onclick="setLanguage('fr')" style="display: flex; align-items: center; gap: 10px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; text-align: left; transition: all 0.3s;">
                        <span style="font-size: 20px;">🇫🇷</span>
                        <span>Français</span>
                    </button>
                    <button onclick="setLanguage('es')" style="display: flex; align-items: center; gap: 10px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; text-align: left; transition: all 0.3s;">
                        <span style="font-size: 20px;">🇪🇸</span>
                        <span>Español</span>
                    </button>
                    <button onclick="setLanguage('de')" style="display: flex; align-items: center; gap: 10px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; text-align: left; transition: all 0.3s;">
                        <span style="font-size: 20px;">🇩🇪</span>
                        <span>Deutsch</span>
                    </button>
                </div>
                <button onclick="this.closest('.modal-overlay').remove()" style="margin-top: 20px; padding: 10px; background: #4C8CF5; color: white; border: none; border-radius: 6px; width: 100%; cursor: pointer; transition: all 0.3s;">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add hover effects to language buttons
    document.querySelectorAll('.modal-overlay button').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
            this.style.backgroundColor = this.textContent.includes('Cancel') ? '#3a7be0' : '#f8f9fa';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
            this.style.backgroundColor = this.textContent.includes('Cancel') ? '#4C8CF5' : 'white';
        });
    });
};

window.showLoginModal = function() {
    const modalHTML = `
        <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
            <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #FFBF00;">
                <h3 style="color: #FFBF00; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Login to FlipFile</h3>
                <form id="loginForm" style="display: flex; flex-direction: column; gap: 15px;">
                    <input type="email" placeholder="Email" required style="padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: all 0.3s;">
                    <input type="password" placeholder="Password" required style="padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: all 0.3s;">
                    <button type="submit" style="padding: 12px; background: #FFBF00; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Login</button>
                </form>
                <div style="margin-top: 20px; text-align: center;">
                    <p style="color: #666; font-size: 13px;">Don't have an account? <a href="#" style="color: #1AA260; text-decoration: none; font-weight: bold;" onclick="showSignupModal()">Sign up</a></p>
                </div>
                <button onclick="this.closest('.modal-overlay').remove()" style="margin-top: 20px; padding: 10px; background: #FF2323; color: white; border: none; border-radius: 6px; width: 100%; cursor: pointer; transition: all 0.3s;">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add focus effects to form inputs
    document.querySelectorAll('#loginForm input').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#FFBF00';
            this.style.boxShadow = '0 0 0 2px rgba(255, 191, 0, 0.2)';
        });
        input.addEventListener('blur', function() {
            this.style.borderColor = '#ddd';
            this.style.boxShadow = 'none';
        });
    });
    
    const form = document.getElementById('loginForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showEnhancedNotification('Login successful! Welcome back.', 'success');
            this.closest('.modal-overlay').remove();
        });
    }
};

window.setLanguage = function(lang) {
    const langText = {
        'en': 'Lingo',
        'fr': 'Lingo',
        'es': 'Lingo',
        'de': 'Lingo'
    };
    
    // Update all language buttons
    document.querySelectorAll('.btn-language span').forEach(span => {
        span.textContent = langText[lang] || 'Lingo';
    });
    
    // Close all modals
    document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
    
    // Show enhanced notification
    showEnhancedNotification(`Language changed to ${lang === 'en' ? 'English' : lang === 'fr' ? 'French' : lang === 'es' ? 'Spanish' : 'German'}`, 'success');
};

window.selectTool = function(toolName) {
    showEnhancedNotification(`Selected tool: ${toolName}`, 'success');
    document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
};

window.showSignupModal = function() {
    const modalHTML = `
        <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
            <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Create Free Account</h3>
                <form id="signupForm" style="display: flex; flex-direction: column; gap: 15px;">
                    <input type="text" placeholder="Full Name" required style="padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: all 0.3s;">
                    <input type="email" placeholder="Email" required style="padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: all 0.3s;">
                    <input type="password" placeholder="Password" required style="padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: all 0.3s;">
                    <button type="submit" style="padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Create Account</button>
                </form>
                <div style="margin-top: 20px; text-align: center;">
                    <p style="color: #666; font-size: 12px;">By signing up, you agree to our Terms of Service and Privacy Policy</p>
                </div>
                <button onclick="this.closest('.modal-overlay').remove()" style="margin-top: 20px; padding: 10px; background: #FF2323; color: white; border: none; border-radius: 6px; width: 100%; cursor: pointer; transition: all 0.3s;">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Add focus effects to form inputs
    document.querySelectorAll('#signupForm input').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#1AA260';
            this.style.boxShadow = '0 0 0 2px rgba(26, 162, 96, 0.2)';
        });
        input.addEventListener('blur', function() {
            this.style.borderColor = '#ddd';
            this.style.boxShadow = 'none';
        });
    });
    
    const form = document.getElementById('signupForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            showEnhancedNotification('Account created successfully! Check your email for verification.', 'success');
            this.closest('.modal-overlay').remove();
        });
    }
};

function showEnhancedNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const icon = type === 'success' ? 'fa-check-circle' : 
                type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    const color = type === 'success' ? '#1AA260' : 
                type === 'error' ? '#FF2323' : '#4C8CF5';
    
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${color};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideInRight 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
        font-size: 14px;
        max-width: 300px;
        display: flex;
        align-items: center;
        border-left: 4px solid white;
    `;
    notification.innerHTML = `
        <i class="fas ${icon}" style="margin-right: 10px; font-size: 16px;"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 500);
    }, 3000);
    
    // Add animation keyframes if not already present
    if (!document.querySelector('#notification-animations')) {
        const animStyle = document.createElement('style');
        animStyle.id = 'notification-animations';
        animStyle.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(animStyle);
    }
}
