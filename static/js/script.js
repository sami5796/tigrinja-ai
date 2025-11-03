const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const translateBtn = document.getElementById('translateBtn');
const chatMessages = document.getElementById('chatMessages');
const replyLang = document.getElementById('replyLang');
const uiLang = document.getElementById('uiLang');

let thinkingMessageElement = null;

// Initialize UI language
window.addEventListener('load', () => {
    // Load saved language preference or default to Tigrinya
    const savedLang = localStorage.getItem('uiLang') || 'ti';
    if (uiLang) {
        uiLang.value = savedLang;
        setUILanguage(savedLang);
    } else {
        setUILanguage('ti');
    }
    messageInput.focus();
});

// Handle UI language change
if (uiLang) {
    uiLang.addEventListener('change', () => {
        setUILanguage(uiLang.value);
    });
}

// Format text for better display
function formatText(text) {
    if (!text) return '';
    
    // First, normalize the text
    let formatted = text
        // Replace multiple spaces with single space
        .replace(/\s{2,}/g, ' ')
        // Replace multiple asterisks (3+) with just double
        .replace(/\*{3,}/g, '**')
        // Normalize line breaks
        .replace(/\r\n/g, '\n')
        .replace(/\r/g, '\n');
    
    // Split into lines first to better handle formatting
    const lines = formatted.split('\n');
    const processedLines = [];
    let inList = false;
    let listItems = [];
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();
        if (!line) {
            // Empty line - close list if open
            if (inList && listItems.length > 0) {
                processedLines.push(`<ul>${listItems.join('')}</ul>`);
                listItems = [];
                inList = false;
            }
            continue;
        }
        
        // Check for headings (lines that start and end with **)
        const headingMatch = line.match(/^\*\*([^*]+)\*\*\s*:?\s*(.*)$/);
        if (headingMatch) {
            if (inList && listItems.length > 0) {
                processedLines.push(`<ul>${listItems.join('')}</ul>`);
                listItems = [];
                inList = false;
            }
            const headingText = headingMatch[1];
            const headingContent = headingMatch[2];
            if (headingContent) {
                processedLines.push(`<h3>${headingText}</h3><p>${headingContent}</p>`);
            } else {
                processedLines.push(`<h3>${headingText}</h3>`);
            }
            continue;
        }
        
        // Check for list items (starts with *, -, or number)
        const listMatch = line.match(/^([\*\-\•]|\d+[\.\)])\s+(.+)$/);
        if (listMatch) {
            if (!inList) {
                inList = true;
            }
            listItems.push(`<li>${listMatch[2]}</li>`);
            continue;
        } else {
            // Not a list item - close list if open
            if (inList && listItems.length > 0) {
                processedLines.push(`<ul>${listItems.join('')}</ul>`);
                listItems = [];
                inList = false;
            }
        }
        
        // Regular paragraph - convert ** to <strong>
        line = line.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        line = line.replace(/\*([^*\s][^*]*[^*\s])\*/g, '<strong>$1</strong>');
        processedLines.push(`<p>${line}</p>`);
    }
    
    // Close any remaining list
    if (inList && listItems.length > 0) {
        processedLines.push(`<ul>${listItems.join('')}</ul>`);
    }
    
    return processedLines.join('');
}

// Add message to chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (isUser) {
        // Simple text for user messages
        const p = document.createElement('p');
        p.textContent = text;
        contentDiv.appendChild(p);
    } else {
        // Formatted HTML for bot messages
        contentDiv.innerHTML = formatText(text);
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Show inline thinking message
function showThinking() {
    if (thinkingMessageElement) {
        return; // Already showing
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content thinking-message';
    
    const spinner = document.createElement('div');
    spinner.className = 'thinking-spinner';
    
    const text = document.createElement('span');
    text.textContent = getTranslation('processing');
    
    contentDiv.appendChild(spinner);
    contentDiv.appendChild(text);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    thinkingMessageElement = messageDiv;
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hide inline thinking message
function hideThinking() {
    if (thinkingMessageElement) {
        thinkingMessageElement.remove();
        thinkingMessageElement = null;
    }
}

// Handle send button click
sendBtn.addEventListener('click', async () => {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    messageInput.value = '';
    
    showThinking();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message,
                reply_lang: replyLang.value
            })
        });
        
        const data = await response.json();
        hideThinking();
        
        if (data.success) {
            // Display the AI response (already translated to reply language)
            if (data.response) {
                addMessage(data.response, false);
            } else {
                addMessage(getTranslation('error-processing'), false);
            }
        } else {
            addMessage(data.error || getTranslation('error-processing'), false);
        }
    } catch (error) {
        hideThinking();
        addMessage(getTranslation('error-connection'), false);
        console.error('Error:', error);
    }
});

// Handle translate button click
translateBtn.addEventListener('click', async () => {
    const message = messageInput.value.trim();
    if (!message) {
        addMessage(getTranslation('error-no-message'), false);
        return;
    }
    
    // Add user message
    addMessage(message, true);
    
    showThinking();
    
    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                text: message,
                reply_lang: replyLang.value
            })
        });
        
        const data = await response.json();
        hideThinking();
        
        if (data.success) {
            if (data.translation) {
                // Get language name for display
                const langNames = {
                    'en': 'English',
                    'ti': 'Tigrinya',
                    'no': 'Norwegian',
                    'ar': 'Arabic',
                    'am': 'Amharic'
                };
                const replyName = langNames[data.reply_lang] || data.reply_lang;
                addMessage(`Translation (${replyName}): ${data.translation}`, false);
            } else {
                addMessage(`${getTranslation('translate-tooltip')}: "${message}"`, false);
            }
            // Open Google Translate URL in new tab (cloud-compatible)
            if (data.translate_url) {
                window.open(data.translate_url, '_blank');
            }
        } else {
            addMessage(getTranslation('error-processing'), false);
        }
    } catch (error) {
        hideThinking();
        addMessage(getTranslation('error-connection'), false);
        console.error('Error:', error);
    }
});

// Handle Enter key press
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendBtn.click();
    }
});

// Handle Ctrl/Cmd + Enter for translate
messageInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        translateBtn.click();
    }
});


