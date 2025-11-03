// Internationalization for Tigrinja-AI
const translations = {
    ti: {
        'main-title': 'ዝሓስብ ኮምፒተር ብ´ትግርኛ',
        'subtitle': 'Tigrinja AI',
        'reply-in-label': 'መልሲ ብ:',
        'auto-detect-info': 'ቋንቋ ኣውቶማቲክ ይሕወስ',
        'welcome-message': '👋 ሰላም! ኣነ <strong>Tigrinja AI</strong> እየ። ንምልሲኻ ዝመርጽ ቋንቋ ኣብ ላዕሊ ምረጽ፡ ድሕሪኡ ብእተኻእለካ ቋንቋ ሕቶ ሓቲንካ! መልእኽትኻ ብኣውቶማቲክ ክርድኦ እየ፡ ከምኡውን ብቕኑዕ ክመልስ እየ።',
        'input-placeholder': 'ብዝመርጽካዮ ቋንቋ ሕተት...',
        'translate-btn': 'ምትርጓም',
        'translate-tooltip': 'ኣብ Google Translate ክፍትን ንምትርጓም',
        'send-tooltip': 'መልእኽቲ ሰዲድ',
        'processing': 'ይሓስብ...',
        'english': 'English',
        'tigrinya': 'ትግርኛ',
        'norwegian': 'Norsk',
        'arabic': 'Arabic',
        'amharic': 'Amharic',
        'error-no-message': 'ብዛዕባ እዚ ኣይኮነን።',
        'error-processing': 'ይቕሬታ፡ መልእኽትኻ ክሰርሕ ኣይከኣለን።',
        'error-connection': 'ይቕሬታ፡ ምስ ሰርቨር ክትተሓሓዝ ኣይከኣለን።'
    },
    en: {
        'main-title': 'ዝሓስብ ኮምፒተር ብ´ትግርኛ',
        'subtitle': 'Tigrinja AI',
        'reply-in-label': 'Reply in:',
        'auto-detect-info': 'Input language is auto-detected',
        'welcome-message': '👋 Hello! I\'m <strong>Tigrinja AI</strong>, your intelligent multilingual assistant. Select your preferred reply language above, then ask me anything in any language! I\'ll automatically understand your message and respond fluently.',
        'input-placeholder': 'Ask me anything in any language...',
        'translate-btn': 'Translate',
        'translate-tooltip': 'Translate and open in Google Translate',
        'send-tooltip': 'Send message',
        'processing': 'Processing...',
        'english': 'English',
        'tigrinya': 'Tigrinya',
        'norwegian': 'Norwegian',
        'arabic': 'Arabic',
        'amharic': 'Amharic',
        'error-no-message': 'Please enter some text to translate.',
        'error-processing': 'Sorry, there was an error processing your message.',
        'error-connection': 'Sorry, there was an error connecting to the server.'
    },
    no: {
        'main-title': 'ዝሓስብ ኮምፒተር ብ´ትግርኛ',
        'subtitle': 'Tigrinja AI',
        'reply-in-label': 'Svar på:',
        'auto-detect-info': 'Inndata-språk oppdages automatisk',
        'welcome-message': '👋 Hei! Jeg er <strong>Tigrinja AI</strong>, din intelligente flerspråklige assistent. Velg ditt foretrukne svar på spørsmålet over, og still meg spørsmål på hvilket som helst språk! Jeg forstår meldingen din automatisk og svarer flytende.',
        'input-placeholder': 'Spør meg hva som helst på hvilket som helst språk...',
        'translate-btn': 'Oversett',
        'translate-tooltip': 'Oversett og åpne i Google Translate',
        'send-tooltip': 'Send melding',
        'processing': 'Behandler...',
        'english': 'Engelsk',
        'tigrinya': 'Tigrinja',
        'norwegian': 'Norsk',
        'arabic': 'Arabisk',
        'amharic': 'Amharisk',
        'error-no-message': 'Vennligst skriv inn tekst å oversette.',
        'error-processing': 'Beklager, det oppstod en feil ved behandling av meldingen din.',
        'error-connection': 'Beklager, det oppstod en feil ved tilkobling til serveren.'
    }
};

let currentUILang = 'ti'; // Default to Tigrinya

function setUILanguage(lang) {
    currentUILang = lang;
    localStorage.setItem('uiLang', lang);
    
    const t = translations[lang] || translations.ti;
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                // Don't change input values, only placeholders
                return;
            } else if (el.tagName === 'P' && key === 'welcome-message') {
                // Use innerHTML for welcome message to preserve HTML tags
                el.innerHTML = t[key];
            } else {
                el.textContent = t[key];
            }
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (t[key]) {
            el.placeholder = t[key];
        }
    });
    
    // Update titles/tooltips
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (t[key]) {
            el.title = t[key];
        }
    });
    
    // Update select options
    document.querySelectorAll('[data-i18n-option]').forEach(el => {
        const key = el.getAttribute('data-i18n-option');
        if (t[key]) {
            el.textContent = t[key];
        }
    });
}

function getTranslation(key) {
    return translations[currentUILang]?.[key] || translations.ti[key] || key;
}

