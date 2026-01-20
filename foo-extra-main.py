// Enhanced Ripple Effect with Color Coding
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
                showToolSelectionModal(files);
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
                    showToolSelectionModal(files);
                }
            });
            
            fileInput.click();
        });
    }
    
    // Tool Selection Modal
    window.showToolSelectionModal = function(files) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 600px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260; max-height: 80vh; overflow-y: auto;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Select Tool for ${files.length} File(s)</h3>
                    
                    <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <h4 style="color: #333; margin-bottom: 10px;">Selected Files:</h4>
                        <div style="max-height: 100px; overflow-y: auto;">
                            ${Array.from(files).map(file => `
                                <div style="display: flex; align-items: center; padding: 5px 0; border-bottom: 1px solid #eee;">
                                    <i class="fas fa-file" style="color: #666; margin-right: 10px;"></i>
                                    <span style="font-size: 12px;">${file.name} (${formatBytes(file.size)})</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin-bottom: 25px;">
                        <button onclick="selectToolForProcessing('convert', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-exchange-alt" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Convert PDF</span>
                        </button>
                        
                        <button onclick="selectToolForProcessing('compress', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-compress-alt" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Compress PDF</span>
                        </button>
                        
                        <button onclick="selectToolForProcessing('protect', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-lock" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Protect PDF</span>
                        </button>
                        
                        <button onclick="selectToolForProcessing('unlock', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-unlock" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Unlock PDF</span>
                        </button>
                        
                        <button onclick="selectToolForProcessing('edit', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-edit" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Edit PDF</span>
                        </button>
                        
                        <button onclick="selectToolForProcessing('extract-colors', ${JSON.stringify(Array.from(files).map(f => f.name))})" style="background: #1AA260; color: white; border: none; padding: 15px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: all 0.3s; min-height: 100px;">
                            <i class="fas fa-palette" style="font-size: 24px; margin-bottom: 10px;"></i>
                            <span style="font-size: 12px; font-weight: bold;">Extract Colors</span>
                        </button>
                    </div>
                    
                    <button onclick="this.closest('.modal-overlay').remove()" style="padding: 12px; background: #FF2323; color: white; border: none; border-radius: 8px; width: 100%; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add hover effects to tool buttons
        document.querySelectorAll('.modal-overlay button').forEach(btn => {
            if (btn.textContent !== 'Cancel') {
                btn.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-5px)';
                    this.style.boxShadow = '0 8px 20px rgba(0,0,0,0.2)';
                    this.style.backgroundColor = '#15894e';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                    this.style.backgroundColor = '#1AA260';
                });
            }
        });
    };
    
    // Format bytes to human readable format
    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }
    
    // Tool Processing Functions
    window.selectToolForProcessing = async function(tool, filenames) {
        // Close modal
        document.querySelectorAll('.modal-overlay').forEach(modal => modal.remove());
        
        // Show tool-specific modal
        switch(tool) {
            case 'convert':
                await showConvertModal(filenames);
                break;
            case 'compress':
                await showCompressModal(filenames);
                break;
            case 'protect':
                await showProtectModal(filenames);
                break;
            case 'unlock':
                await showUnlockModal(filenames);
                break;
            case 'edit':
                await showEditModal(filenames);
                break;
            case 'extract-colors':
                await showExtractColorsModal(filenames);
                break;
        }
    };
    
    // Convert Modal
    window.showConvertModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Convert PDF Files</h3>
                    
                    <form id="convertForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Output Format:</label>
                            <select name="format" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                <option value="docx">Word Document (.docx)</option>
                                <option value="xlsx">Excel Spreadsheet (.xlsx)</option>
                                <option value="pptx">PowerPoint (.pptx)</option>
                                <option value="jpg">JPEG Image (.jpg)</option>
                                <option value="png">PNG Image (.png)</option>
                                <option value="txt">Text File (.txt)</option>
                                <option value="html">HTML (.html)</option>
                            </select>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Quality:</label>
                            <select name="quality" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                <option value="high">High Quality</option>
                                <option value="medium" selected>Medium Quality</option>
                                <option value="low">Low Quality (Smaller File)</option>
                            </select>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Pages (optional):</label>
                            <input type="text" name="pages" placeholder="e.g., 1,3,5 or 1-10" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            <small style="color: #666; font-size: 12px;">Leave blank for all pages</small>
                        </div>
                        
                        <div id="convertFilesList" style="max-height: 150px; overflow-y: auto; padding: 10px; background: #f8f9fa; border-radius: 6px;">
                            <p style="margin: 0; font-size: 12px; color: #666;">${filenames.length} file(s) selected</p>
                        </div>
                        
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <button type="button" onclick="processConversion()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Convert Now</button>
                            <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Store filenames in the modal for later use
        const modal = document.querySelector('.modal-overlay:last-child');
        modal.dataset.filenames = JSON.stringify(filenames);
    };
    
    // Process Conversion
    window.processConversion = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const form = modal.querySelector('#convertForm');
        const formData = new FormData(form);
        
        // Get files from original selection
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        // Show processing indicator
        showProcessingIndicator('Converting files...');
        
        try {
            // Create FormData for upload
            const uploadData = new FormData();
            
            // Add files
            for (const file of files) {
                uploadData.append('files', file);
            }
            
            // Add conversion parameters
            uploadData.append('format', formData.get('format'));
            uploadData.append('quality', formData.get('quality'));
            uploadData.append('pages', formData.get('pages') || '');
            uploadData.append('operation', 'convert');
            
            // Send to API
            const response = await fetch('/api/batch-process', {
                method: 'POST',
                body: uploadData
            });
            
            const result = await response.json();
            
            if (result.success) {
                hideProcessingIndicator();
                modal.remove();
                
                // Show success and offer download
                showDownloadModal(result);
            } else {
                hideProcessingIndicator();
                showEnhancedNotification(result.message || 'Conversion failed', 'error');
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Conversion failed: ' + error.message, 'error');
        }
    };
    
    // Compress Modal
    window.showCompressModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Compress PDF Files</h3>
                    
                    <form id="compressForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Compression Level:</label>
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="quality" value="low" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Low</span>
                                    <small style="font-size: 10px; color: #666;">30% smaller</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #1AA260; border-radius: 6px; cursor: pointer; background: #f0f9f4; transition: all 0.3s;">
                                    <input type="radio" name="quality" value="medium" checked style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Medium</span>
                                    <small style="font-size: 10px; color: #666;">50% smaller</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="quality" value="high" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">High</span>
                                    <small style="font-size: 10px; color: #666;">70% smaller</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="quality" value="extreme" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Extreme</span>
                                    <small style="font-size: 10px; color: #666;">90% smaller</small>
                                </label>
                            </div>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">DPI (Image Resolution):</label>
                            <input type="range" name="dpi" min="72" max="300" value="150" style="width: 100%;" oninput="this.nextElementSibling.value = this.value + ' DPI'">
                            <output style="display: block; text-align: center; font-size: 12px; color: #666;">150 DPI</output>
                        </div>
                        
                        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                            <input type="checkbox" name="remove_metadata" checked>
                            <span style="font-size: 14px;">Remove metadata (author, creation date, etc.)</span>
                        </label>
                        
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <button type="button" onclick="processCompression()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Compress Now</button>
                            <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add interactivity to compression level buttons
        const labels = document.querySelectorAll('#compressForm label');
        labels.forEach(label => {
            label.addEventListener('click', function() {
                labels.forEach(l => {
                    l.style.borderColor = '#ddd';
                    l.style.background = 'white';
                });
                this.style.borderColor = '#1AA260';
                this.style.background = '#f0f9f4';
            });
        });
    };
    
    // Process Compression
    window.processCompression = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const form = modal.querySelector('#compressForm');
        const formData = new FormData(form);
        
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        showProcessingIndicator('Compressing files...');
        
        try {
            const uploadData = new FormData();
            
            for (const file of files) {
                uploadData.append('files', file);
            }
            
            uploadData.append('quality', formData.get('quality'));
            uploadData.append('dpi', formData.get('dpi'));
            uploadData.append('remove_metadata', formData.get('remove_metadata') ? 'true' : 'false');
            uploadData.append('operation', 'compress');
            
            const response = await fetch('/api/batch-process', {
                method: 'POST',
                body: uploadData
            });
            
            const result = await response.json();
            
            if (result.success) {
                hideProcessingIndicator();
                modal.remove();
                showDownloadModal(result);
            } else {
                hideProcessingIndicator();
                showEnhancedNotification(result.message || 'Compression failed', 'error');
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Compression failed: ' + error.message, 'error');
        }
    };
    
    // Protect Modal
    window.showProtectModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Protect PDF Files</h3>
                    
                    <form id="protectForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Password:</label>
                            <input type="password" name="password" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;" placeholder="Enter password">
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Confirm Password:</label>
                            <input type="password" name="confirm_password" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;" placeholder="Confirm password">
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Encryption Level:</label>
                            <select name="encryption_level" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                <option value="128bit">128-bit AES (Recommended)</option>
                                <option value="256bit">256-bit AES (Strongest)</option>
                                <option value="40bit">40-bit RC4 (Legacy)</option>
                            </select>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 10px; font-weight: bold;">Permissions:</label>
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" name="print" checked>
                                    <span style="font-size: 14px;">Allow Printing</span>
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" name="copy" checked>
                                    <span style="font-size: 14px;">Allow Copying</span>
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" name="modify">
                                    <span style="font-size: 14px;">Allow Modifications</span>
                                </label>
                                <label style="display: flex; align-items: center; gap: 8px;">
                                    <input type="checkbox" name="annotations" checked>
                                    <span style="font-size: 14px;">Allow Annotations</span>
                                </label>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <button type="button" onclick="processProtection()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Protect Now</button>
                            <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    };
    
    // Process Protection
    window.processProtection = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const form = modal.querySelector('#protectForm');
        const formData = new FormData(form);
        
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        if (password !== confirmPassword) {
            showEnhancedNotification('Passwords do not match', 'error');
            return;
        }
        
        if (password.length < 4) {
            showEnhancedNotification('Password must be at least 4 characters', 'error');
            return;
        }
        
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        showProcessingIndicator('Protecting files...');
        
        try {
            const uploadData = new FormData();
            
            for (const file of files) {
                uploadData.append('files', file);
            }
            
            // Build permissions object
            const permissions = {
                print: formData.get('print') === 'on',
                copy: formData.get('copy') === 'on',
                modify: formData.get('modify') === 'on',
                annotations: formData.get('annotations') === 'on'
            };
            
            uploadData.append('password', password);
            uploadData.append('encryption_level', formData.get('encryption_level'));
            uploadData.append('permissions', JSON.stringify(permissions));
            uploadData.append('operation', 'protect');
            
            const response = await fetch('/api/batch-process', {
                method: 'POST',
                body: uploadData
            });
            
            const result = await response.json();
            
            if (result.success) {
                hideProcessingIndicator();
                modal.remove();
                showDownloadModal(result);
            } else {
                hideProcessingIndicator();
                showEnhancedNotification(result.message || 'Protection failed', 'error');
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Protection failed: ' + error.message, 'error');
        }
    };
    
    // Unlock Modal
    window.showUnlockModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Unlock PDF Files</h3>
                    
                    <form id="unlockForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Password (if known):</label>
                            <input type="password" name="password" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;" placeholder="Leave blank for automatic unlock">
                            <small style="color: #666; font-size: 12px;">We'll try common passwords and automatic methods if left blank</small>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Unlock Method:</label>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #1AA260; border-radius: 6px; cursor: pointer; background: #f0f9f4; transition: all 0.3s;">
                                    <input type="radio" name="method" value="auto" checked style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Automatic</span>
                                    <small style="font-size: 10px; color: #666;">Recommended</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="method" value="dictionary" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Dictionary</span>
                                    <small style="font-size: 10px; color: #666;">1-5 min</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="method" value="bruteforce" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">Brute Force</span>
                                    <small style="font-size: 10px; color: #666;">5-30 min</small>
                                </label>
                            </div>
                        </div>
                        
                        <div style="padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px;">
                            <p style="margin: 0; font-size: 12px; color: #856404;">
                                <i class="fas fa-info-circle" style="margin-right: 5px;"></i>
                                <strong>Note:</strong> We respect document security. This tool is for unlocking your own documents when you've forgotten the password. We do not support unauthorized access.
                            </p>
                        </div>
                        
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <button type="button" onclick="processUnlock()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Unlock Now</button>
                            <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    };
    
    // Process Unlock
    window.processUnlock = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const form = modal.querySelector('#unlockForm');
        const formData = new FormData(form);
        
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        showProcessingIndicator('Unlocking files... This may take a moment.');
        
        try {
            // Since batch unlock isn't implemented in API, process individually
            const results = [];
            
            for (const file of files) {
                const uploadData = new FormData();
                uploadData.append('file', file);
                
                const password = formData.get('password');
                if (password) {
                    uploadData.append('password', password);
                }
                
                const response = await fetch('/api/unlock', {
                    method: 'POST',
                    body: uploadData
                });
                
                const result = await response.json();
                results.push(result);
            }
            
            hideProcessingIndicator();
            modal.remove();
            
            // Show results
            const successful = results.filter(r => r.success);
            const failed = results.filter(r => !r.success);
            
            if (successful.length > 0) {
                // Create a zip of all successful unlocks
                const zipData = new FormData();
                for (let i = 0; i < files.length; i++) {
                    if (results[i].success) {
                        zipData.append('files', files[i]);
                    }
                }
                
                zipData.append('operation', 'compress'); // Reuse compress for zip creation
                
                const zipResponse = await fetch('/api/batch-process', {
                    method: 'POST',
                    body: zipData
                });
                
                const zipResult = await zipResponse.json();
                
                if (zipResult.success) {
                    showDownloadModal(zipResult);
                }
            }
            
            if (failed.length > 0) {
                showEnhancedNotification(`${failed.length} file(s) could not be unlocked`, 'error');
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Unlock failed: ' + error.message, 'error');
        }
    };
    
    // Edit Modal
    window.showEditModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 600px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260; max-height: 80vh; overflow-y: auto;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Edit PDF Files</h3>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 10px; font-weight: bold;">Select Operation:</label>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px;">
                            <button type="button" onclick="showEditOperation('merge')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-copy" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Merge</span>
                            </button>
                            <button type="button" onclick="showEditOperation('split')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-cut" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Split</span>
                            </button>
                            <button type="button" onclick="showEditOperation('rotate')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-redo" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Rotate</span>
                            </button>
                            <button type="button" onclick="showEditOperation('reorder')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-sort" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Reorder</span>
                            </button>
                            <button type="button" onclick="showEditOperation('extract')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-external-link-alt" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Extract</span>
                            </button>
                            <button type="button" onclick="showEditOperation('delete')" style="padding: 15px; background: #f8f9fa; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; transition: all 0.3s; display: flex; flex-direction: column; align-items: center;">
                                <i class="fas fa-trash" style="font-size: 24px; color: #1AA260; margin-bottom: 8px;"></i>
                                <span style="font-size: 12px; font-weight: bold;">Delete Pages</span>
                            </button>
                        </div>
                    </div>
                    
                    <div id="editOperationForm" style="display: none;">
                        <!-- Operation-specific forms will be loaded here -->
                    </div>
                    
                    <div style="display: flex; gap: 10px; margin-top: 20px;">
                        <button type="button" onclick="processEdit()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s; display: none;" id="editSubmitBtn">Process Edit</button>
                        <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    };
    
    // Show specific edit operation form
    window.showEditOperation = function(operation) {
        const formContainer = document.getElementById('editOperationForm');
        const submitBtn = document.getElementById('editSubmitBtn');
        
        let formHTML = '';
        
        switch(operation) {
            case 'merge':
                formHTML = `
                    <h4 style="color: #333; margin-bottom: 15px;">Merge PDF Files</h4>
                    <div style="margin-bottom: 15px;">
                        <p style="margin: 0 0 10px 0; font-size: 14px; color: #666;">Selected files will be merged in the order shown below:</p>
                        <div id="mergeFileList" style="max-height: 150px; overflow-y: auto; padding: 10px; background: #f8f9fa; border-radius: 6px;">
                            <p style="margin: 0; font-size: 12px; color: #666;">Drag files to reorder</p>
                        </div>
                        <button type="button" onclick="reorderMergeFiles()" style="margin-top: 10px; padding: 8px 12px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">Manual Reorder</button>
                    </div>
                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                        <input type="checkbox" name="add_bookmarks" checked>
                        <span style="font-size: 14px;">Add bookmarks for each file</span>
                    </label>
                `;
                break;
                
            case 'split':
                formHTML = `
                    <h4 style="color: #333; margin-bottom: 15px;">Split PDF Files</h4>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Split Method:</label>
                        <select name="split_method" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;" onchange="updateSplitOptions(this.value)">
                            <option value="single">Split into single pages</option>
                            <option value="ranges">Split by page ranges</option>
                            <option value="every_n">Split every N pages</option>
                        </select>
                    </div>
                    <div id="splitOptions" style="margin-bottom: 15px;">
                        <!-- Options will be updated dynamically -->
                    </div>
                `;
                break;
                
            case 'rotate':
                formHTML = `
                    <h4 style="color: #333; margin-bottom: 15px;">Rotate PDF Pages</h4>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Rotation Angle:</label>
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                            <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                <input type="radio" name="angle" value="90" style="margin-bottom: 5px;">
                                <span style="font-size: 12px;">90° Clockwise</span>
                            </label>
                            <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #1AA260; border-radius: 6px; cursor: pointer; background: #f0f9f4; transition: all 0.3s;">
                                <input type="radio" name="angle" value="-90" checked style="margin-bottom: 5px;">
                                <span style="font-size: 12px;">90° Counter-Clockwise</span>
                            </label>
                            <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                <input type="radio" name="angle" value="180" style="margin-bottom: 5px;">
                                <span style="font-size: 12px;">180°</span>
                            </label>
                        </div>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Pages to Rotate:</label>
                        <input type="text" name="pages" placeholder="e.g., 1,3,5 or 1-10 or all" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                        <small style="color: #666; font-size: 12px;">Leave blank or type 'all' for all pages</small>
                    </div>
                `;
                break;
        }
        
        formContainer.innerHTML = formHTML;
        formContainer.style.display = 'block';
        submitBtn.style.display = 'block';
        submitBtn.dataset.operation = operation;
        
        // Store current operation
        window.currentEditOperation = operation;
        
        // Initialize form if needed
        if (operation === 'split') {
            updateSplitOptions('single');
        }
    };
    
    // Process Edit
    window.processEdit = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const submitBtn = document.getElementById('editSubmitBtn');
        const operation = submitBtn.dataset.operation;
        
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        showProcessingIndicator(`Processing ${operation} operation...`);
        
        try {
            // Build parameters based on operation
            let parameters = {};
            
            switch(operation) {
                case 'merge':
                    parameters = {
                        operation: 'merge',
                        add_bookmarks: document.querySelector('input[name="add_bookmarks"]').checked
                    };
                    break;
                    
                case 'split':
                    const method = document.querySelector('select[name="split_method"]').value;
                    parameters = {
                        operation: 'split',
                        type: method
                    };
                    
                    if (method === 'ranges') {
                        const ranges = document.querySelector('input[name="page_ranges"]').value;
                        parameters.ranges = ranges.split(',').map(r => r.trim());
                    } else if (method === 'every_n') {
                        parameters.n = parseInt(document.querySelector('input[name="every_n"]').value) || 1;
                    }
                    break;
                    
                case 'rotate':
                    const angle = parseInt(document.querySelector('input[name="angle"]:checked').value) || -90;
                    const pages = document.querySelector('input[name="pages"]').value;
                    parameters = {
                        operation: 'rotate',
                        angle: angle,
                        pages: pages === '' ? 'all' : pages
                    };
                    break;
            }
            
            // Process each file individually
            const results = [];
            
            for (const file of files) {
                const uploadData = new FormData();
                uploadData.append('file', file);
                uploadData.append('operation', parameters.operation);
                uploadData.append('parameters', JSON.stringify(parameters));
                
                const response = await fetch('/api/edit', {
                    method: 'POST',
                    body: uploadData
                });
                
                const result = await response.json();
                results.push(result);
            }
            
            hideProcessingIndicator();
            modal.remove();
            
            // Handle results
            const successful = results.filter(r => r.success);
            
            if (successful.length > 0) {
                // For single file operations, show download
                if (files.length === 1 && successful[0].download_url) {
                    showDownloadModal(successful[0]);
                } else {
                    // For multiple files, create a zip
                    showEnhancedNotification(`${successful.length} file(s) processed successfully`, 'success');
                }
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Edit operation failed: ' + error.message, 'error');
        }
    };
    
    // Extract Colors Modal
    window.showExtractColorsModal = async function(filenames) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Extract Colors</h3>
                    
                    <form id="extractColorsForm" style="display: flex; flex-direction: column; gap: 15px;">
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Number of Colors:</label>
                            <input type="range" name="color_count" min="3" max="20" value="5" style="width: 100%;" oninput="this.nextElementSibling.value = this.value + ' colors'">
                            <output style="display: block; text-align: center; font-size: 12px; color: #666;">5 colors</output>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Color Format:</label>
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #1AA260; border-radius: 6px; cursor: pointer; background: #f0f9f4; transition: all 0.3s;">
                                    <input type="radio" name="format" value="hex" checked style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">HEX</span>
                                    <small style="font-size: 10px; color: #666;">#FF5733</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="format" value="rgb" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">RGB</span>
                                    <small style="font-size: 10px; color: #666;">255,87,51</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="format" value="hsl" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">HSL</span>
                                    <small style="font-size: 10px; color: #666;">11°,100%,60%</small>
                                </label>
                                <label style="display: flex; flex-direction: column; align-items: center; padding: 10px; border: 2px solid #ddd; border-radius: 6px; cursor: pointer; transition: all 0.3s;">
                                    <input type="radio" name="format" value="cmyk" style="margin-bottom: 5px;">
                                    <span style="font-size: 12px; font-weight: bold;">CMYK</span>
                                    <small style="font-size: 10px; color: #666;">0,66,80,0</small>
                                </label>
                            </div>
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Generate Color Palette:</label>
                            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                                <input type="checkbox" name="generate_palette" checked>
                                <span style="font-size: 14px;">Create palette image with extracted colors</span>
                            </label>
                        </div>
                        
                        <div style="display: flex; gap: 10px; margin-top: 10px;">
                            <button type="button" onclick="processColorExtraction()" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Extract Colors</button>
                            <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    };
    
    // Process Color Extraction
    window.processColorExtraction = async function() {
        const modal = document.querySelector('.modal-overlay:last-child');
        const form = modal.querySelector('#extractColorsForm');
        const formData = new FormData(form);
        
        const files = await getSelectedFiles();
        
        if (!files || files.length === 0) {
            showEnhancedNotification('Please select files first', 'error');
            return;
        }
        
        // Only process first file for color extraction (usually one image/PDF)
        const file = files[0];
        
        showProcessingIndicator('Extracting colors...');
        
        try {
            const uploadData = new FormData();
            uploadData.append('file', file);
            uploadData.append('color_count', formData.get('color_count'));
            uploadData.append('format', formData.get('format'));
            
            const response = await fetch('/api/extract-colors', {
                method: 'POST',
                body: uploadData
            });
            
            const result = await response.json();
            
            if (result.success) {
                hideProcessingIndicator();
                modal.remove();
                
                // Show color palette
                showColorPaletteModal(result);
            } else {
                hideProcessingIndicator();
                showEnhancedNotification(result.message || 'Color extraction failed', 'error');
            }
            
        } catch (error) {
            hideProcessingIndicator();
            showEnhancedNotification('Color extraction failed: ' + error.message, 'error');
        }
    };
    
    // Show Color Palette
    window.showColorPaletteModal = function(result) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 700px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260; max-height: 80vh; overflow-y: auto;">
                    <h3 style="color: #1AA260; margin-bottom: 20px; text-align: center; font-family: 'Saira Stencil One', cursive;">Color Palette</h3>
                    
                    <div style="text-align: center; margin-bottom: 20px;">
                        <p style="margin: 0; font-size: 14px; color: #666;">Extracted ${result.colors.length} colors from your file</p>
                    </div>
                    
                    <div style="margin-bottom: 30px;">
                        <h4 style="color: #333; margin-bottom: 15px;">Color Palette:</h4>
                        <div id="colorPalette" style="display: flex; height: 80px; border-radius: 8px; overflow: hidden; margin-bottom: 20px;">
                            ${result.colors.map(color => `
                                <div style="flex: 1; background-color: ${color.hex}; position: relative;" title="${color.hex}">
                                    <div style="position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; color: ${getContrastColor(color.hex)}; font-size: 11px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                                        ${color.hex}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div id="colorDetails" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                            ${result.colors.map((color, index) => `
                                <div style="padding: 15px; border: 1px solid #eee; border-radius: 8px; background: #f8f9fa;">
                                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                        <div style="width: 40px; height: 40px; background-color: ${color.hex}; border-radius: 6px; margin-right: 10px;"></div>
                                        <div>
                                            <div style="font-weight: bold; font-size: 14px;">Color ${index + 1}</div>
                                            <div style="font-size: 12px; color: #666;">${color.hex}</div>
                                        </div>
                                    </div>
                                    <div style="font-size: 12px;">
                                        ${color.rgb ? `<div>RGB: ${color.rgb.r}, ${color.rgb.g}, ${color.rgb.b}</div>` : ''}
                                        ${color.hsl ? `<div>HSL: ${color.hsl.h}°, ${color.hsl.s}%, ${color.hsl.l}%</div>` : ''}
                                        ${color.cmyk ? `<div>CMYK: ${color.cmyk.c}%, ${color.cmyk.m}%, ${color.cmyk.y}%, ${color.cmyk.k}%</div>` : ''}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-bottom: 20px;">
                        <img src="${result.palette_url}" alt="Color Palette" style="max-width: 100%; border-radius: 8px; border: 1px solid #eee;">
                        <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">Color palette image generated</p>
                    </div>
                    
                    <div style="display: flex; gap: 10px;">
                        <button type="button" onclick="downloadFile('${result.download_url}', '${result.filename}')" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">
                            <i class="fas fa-download" style="margin-right: 8px;"></i>Download Palette
                        </button>
                        <button type="button" onclick="copyColorPalette()" style="flex: 1; padding: 12px; background: #4C8CF5; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">
                            <i class="fas fa-copy" style="margin-right: 8px;"></i>Copy Colors
                        </button>
                        <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Store colors for copying
        window.currentColorPalette = result.colors;
    };
    
    // Copy Color Palette
    window.copyColorPalette = function() {
        if (!window.currentColorPalette) return;
        
        const colorText = window.currentColorPalette.map(color => color.hex).join('\n');
        
        navigator.clipboard.writeText(colorText).then(() => {
            showEnhancedNotification('Color palette copied to clipboard!', 'success');
        }).catch(err => {
            showEnhancedNotification('Failed to copy: ' + err, 'error');
        });
    };
    
    // Helper function to get contrast color
    function getContrastColor(hexcolor) {
        // Remove # if present
        hexcolor = hexcolor.replace('#', '');
        
        // Convert to RGB
        const r = parseInt(hexcolor.substr(0, 2), 16);
        const g = parseInt(hexcolor.substr(2, 2), 16);
        const b = parseInt(hexcolor.substr(4, 2), 16);
        
        // Calculate luminance
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        
        return luminance > 0.5 ? '#000000' : '#FFFFFF';
    };
    
    // Download File
    window.downloadFile = function(url, filename) {
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };
    
    // Show Download Modal
    window.showDownloadModal = function(result) {
        const modalHTML = `
            <div class="modal-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 500px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260; text-align: center;">
                    <div style="margin-bottom: 20px;">
                        <i class="fas fa-check-circle" style="font-size: 48px; color: #1AA260; margin-bottom: 15px;"></i>
                        <h3 style="color: #1AA260; margin-bottom: 10px; font-family: 'Saira Stencil One', cursive;">Processing Complete!</h3>
                        <p style="color: #666; font-size: 14px;">${result.message}</p>
                        
                        ${result.compression_ratio ? `
                            <div style="margin: 20px 0; padding: 15px; background: #f0f9f4; border-radius: 8px;">
                                <h4 style="color: #333; margin-bottom: 10px;">Compression Results:</h4>
                                <div style="display: flex; justify-content: space-around;">
                                    <div>
                                        <div style="font-size: 12px; color: #666;">Original</div>
                                        <div style="font-weight: bold;">${formatBytes(result.original_size)}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 12px; color: #666;">Compressed</div>
                                        <div style="font-weight: bold;">${formatBytes(result.compressed_size)}</div>
                                    </div>
                                    <div>
                                        <div style="font-size: 12px; color: #666;">Reduction</div>
                                        <div style="font-weight: bold; color: #1AA260;">${result.compression_ratio.toFixed(1)}%</div>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                    
                    <div style="display: flex; gap: 10px;">
                        <button type="button" onclick="downloadFile('${result.download_url}', '${result.filename}')" style="flex: 1; padding: 12px; background: #1AA260; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">
                            <i class="fas fa-download" style="margin-right: 8px;"></i>Download File
                        </button>
                        <button type="button" onclick="this.closest('.modal-overlay').remove()" style="flex: 1; padding: 12px; background: #FF2323; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s;">Close</button>
                    </div>
                    
                    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
                        <p style="font-size: 12px; color: #666; margin: 0;">
                            <i class="fas fa-shield-alt" style="margin-right: 5px;"></i>
                            Your file will be automatically deleted in 1 hour for security.
                        </p>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    };
    
    // Get selected files from global state
    async function getSelectedFiles() {
        // This function should retrieve files from wherever they're stored
        // For now, we'll use a global variable
        return window.selectedFiles || [];
    };
    
    // Store files when selected
    window.storeSelectedFiles = function(files) {
        window.selectedFiles = Array.from(files);
    };
    
    // Show processing indicator
    function showProcessingIndicator(message) {
        const indicatorHTML = `
            <div class="processing-indicator" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 3000; display: flex; flex-direction: column; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
                <div style="text-align: center; padding: 40px; background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); border-top: 4px solid #1AA260;">
                    <i class="fas fa-spinner fa-spin" style="font-size: 48px; color: #1AA260; margin-bottom: 20px; animation: color-change 2s infinite;"></i>
                    <h3 style="color: #333; margin-bottom: 10px;">Processing...</h3>
                    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">${message}</p>
                    <div style="width: 200px; height: 4px; background: #eee; border-radius: 2px; overflow: hidden;">
                        <div class="progress-bar" style="width: 30%; height: 100%; background: #1AA260; animation: progress 2s infinite ease-in-out;"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing indicator
        hideProcessingIndicator();
        
        document.body.insertAdjacentHTML('beforeend', indicatorHTML);
        
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes color-change {
                0% { color: #1AA260; }
                50% { color: #4C8CF5; }
                100% { color: #1AA260; }
            }
            @keyframes progress {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(400%); }
            }
        `;
        document.head.appendChild(style);
    };
    
    // Hide processing indicator
    function hideProcessingIndicator() {
        const indicator = document.querySelector('.processing-indicator');
        if (indicator) {
            indicator.remove();
        }
    };
    
    // Enhanced notification function
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
    };
    
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

// Keep existing modal functions
window.showMobileToolsModal = function() {
    // Same as before...
};

window.showLanguageModal = function() {
    // Same as before...
};

window.showLoginModal = function() {
    // Same as before...
};

window.setLanguage = function(lang) {
    // Same as before...
};

window.selectTool = function(toolName) {
    // Same as before...
};

window.showSignupModal = function() {
    // Same as before...
};
