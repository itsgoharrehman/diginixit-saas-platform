/**
 * DiginixIT Standalone AI Chatbot Widget (Powered by Grok AI)
 * 
 * Secure Architecture:
 * - API keys are stored strictly server-side in environment variables (GROK_API_KEY).
 * - All chat completions route through the server proxy (/api/chat).
 * - No secrets or API key inputs exposed to the frontend browser.
 * - Floating launcher button at bottom-right corner with a dedicated Bot icon.
 * - Complete DiginixIT Knowledge Base (Dr. Nadeem Nazir, Services, Tech, Legal, Finance, Contact, Blogs).
 */

(function () {
    'use strict';

    // Prevent duplicate initialization
    if (window.DiginixChatbotLoaded) return;
    window.DiginixChatbotLoaded = true;

    // --- KNOWLEDGE BASE (Client-side fallback & reference) ---
    const DIGINIX_KNOWLEDGE_BASE = {
        company: "DiginixIT",
        tagline: "Build, Protect & Scale Your Business",
        website: "https://diginixit.com",
        headquarters: {
            corporate: "Main Boulevard, Lahore, 54000, Punjab, Pakistan",
            engineeringStudio: "Global Engineering Studio, Faisalabad, Punjab, Pakistan"
        },
        contact: {
            phone: "+92 300 7960300",
            phoneRaw: "+923007960300",
            email: "contact@diginix.com",
            technicalLeadEmail: "goharrehmanfsd260@gmail.com",
            hours: "Monday to Friday: 09:00 AM – 06:00 PM (PKT)",
            responseTime: "Average response within 2 hours",
            status: "Currently accepting new projects"
        },
        leadership: {
            executiveAdvisor: {
                name: "Dr. Nadeem Nazir",
                title: "Chief Executive & Founding Strategic Advisor",
                role: "Strategic Technology Advisor, Enterprise Architecture, Corporate Governance & Venture Consultant",
                bio: "Dr. Nadeem Nazir leads DiginixIT's strategic direction, high-stakes client advisory, technology governance, and venture acceleration. With extensive academic and industrial pedigree in computer engineering and business systems, Dr. Nadeem Nazir oversees the firm's multidisciplinary practice spanning custom web software, technology law, and corporate finance. He consults international enterprises and fast-growing startups on digital transformation, regulatory compliance, and scalable product architecture.",
                expertise: [
                    "Enterprise Software Architecture & Scalability",
                    "Corporate Governance & Cross-Border Tech Law",
                    "Venture Strategy, Capital Allocation & Valuations",
                    "High-Impact Engineering Leadership & Mentorship"
                ],
                linkedIn: "https://www.linkedin.com/company/diginixit/"
            }
        },
        socials: {
            linkedin: "https://www.linkedin.com/company/diginixit/",
            twitter: "https://twitter.com/diginixit",
            instagram: "https://www.instagram.com/diginixit/",
            github: "https://github.com/diginixit"
        }
    };

    const STORAGE_KEY_HISTORY = 'diginix_chat_history';

    function getStoredHistory() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY_HISTORY) || '[]');
        } catch (e) {
            return [];
        }
    }

    function setStoredHistory(history) {
        try {
            localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(history.slice(-30)));
        } catch (e) {}
    }

    // --- SCOPED CSS INJECTION ---
    const cssStyles = `
    /* DiginixIT Standalone Chatbot Styles */
    .dnx-chat-widget-root {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #171717;
        box-sizing: border-box;
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
    }
    .dnx-chat-widget-root *, .dnx-chat-widget-root *::before, .dnx-chat-widget-root *::after {
        box-sizing: border-box;
    }

    /* Floating Launcher Button */
    .dnx-chat-launcher {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 999990;
        width: 62px;
        height: 62px;
        border-radius: 50%;
        background: #171717;
        color: #ffffff;
        border: 1.5px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, background-color 0.2s ease;
        outline: none;
        user-select: none;
    }
    .dnx-chat-launcher:hover {
        transform: scale(1.07);
        background: #1f1f1f;
        box-shadow: 0 16px 32px -4px rgba(0, 0, 0, 0.4), 0 0 0 3px rgba(62, 207, 142, 0.32);
    }
    .dnx-chat-launcher:active {
        transform: scale(0.95);
    }
    .dnx-chat-launcher-badge {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 14px;
        height: 14px;
        background: #3ecf8e;
        border: 2px solid #171717;
        border-radius: 50%;
    }
    .dnx-chat-launcher-pulse {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 14px;
        height: 14px;
        background: #3ecf8e;
        border-radius: 50%;
        animation: dnxPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        opacity: 0.75;
    }
    @keyframes dnxPulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.7); opacity: 0; }
    }

    /* Popup Chat Container */
    .dnx-chat-window {
        position: fixed;
        bottom: 98px;
        right: 24px;
        z-index: 999991;
        width: 400px;
        max-width: calc(100vw - 32px);
        height: 600px;
        max-height: calc(100vh - 120px);
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #dfdfdf;
        box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.2), 0 10px 20px -5px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        opacity: 0;
        visibility: hidden;
        transform: translateY(16px) scale(0.97);
        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.25s;
    }
    .dnx-chat-window.dnx-open {
        opacity: 1;
        visibility: visible;
        transform: translateY(0) scale(1);
    }

    /* Header */
    .dnx-chat-header {
        background: #171717;
        color: #ffffff;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        flex-shrink: 0;
    }
    .dnx-chat-header-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .dnx-chat-avatar {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #222222;
        border: 1px solid rgba(62, 207, 142, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .dnx-chat-header-titles {
        display: flex;
        flex-direction: column;
    }
    .dnx-chat-title {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .dnx-chat-subtitle {
        font-size: 11px;
        color: #9a9a9a;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .dnx-status-indicator {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #3ecf8e;
        display: inline-block;
    }
    .dnx-chat-header-actions {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .dnx-header-btn {
        background: transparent;
        border: none;
        color: #a0a0a0;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
    }
    .dnx-header-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }

    /* Messages Container */
    .dnx-chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 18px 16px;
        display: flex;
        flex-direction: column;
        gap: 14px;
        background: #ffffff;
        scroll-behavior: smooth;
    }

    /* Message Bubbles */
    .dnx-message-row {
        display: flex;
        gap: 10px;
        max-width: 88%;
        animation: dnxFadeSlide 0.22s ease-out;
    }
    @keyframes dnxFadeSlide {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .dnx-message-row.dnx-user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    .dnx-message-row.dnx-bot {
        align-self: flex-start;
    }
    .dnx-message-avatar {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: #171717;
        color: #3ecf8e;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .dnx-message-bubble {
        padding: 12px 14px;
        border-radius: 14px;
        font-size: 13.5px;
        line-height: 1.48;
        word-break: break-word;
    }
    .dnx-message-row.dnx-user .dnx-message-bubble {
        background: #171717;
        color: #ffffff;
        border-bottom-right-radius: 4px;
    }
    .dnx-message-row.dnx-bot .dnx-message-bubble {
        background: #fafafa;
        color: #171717;
        border: 1px solid #ededed;
        border-bottom-left-radius: 4px;
    }
    .dnx-message-bubble p {
        margin: 0 0 8px 0;
    }
    .dnx-message-bubble p:last-child {
        margin-bottom: 0;
    }
    .dnx-message-bubble strong {
        font-weight: 600;
        color: inherit;
    }
    .dnx-message-bubble ul, .dnx-message-bubble ol {
        margin: 6px 0 6px 18px;
        padding: 0;
    }
    .dnx-message-bubble li {
        margin-bottom: 4px;
    }
    .dnx-message-bubble a {
        color: #24b47e;
        text-decoration: underline;
        font-weight: 500;
    }
    .dnx-message-bubble a:hover {
        color: #1a8f62;
    }
    .dnx-message-time {
        font-size: 10px;
        color: #9a9a9a;
        margin-top: 4px;
        text-align: right;
    }
    .dnx-message-row.dnx-bot .dnx-message-time {
        text-align: left;
    }

    /* Typing Indicator */
    .dnx-typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 8px 12px;
        background: #fafafa;
        border: 1px solid #ededed;
        border-radius: 12px;
        align-self: flex-start;
    }
    .dnx-typing-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #3ecf8e;
        animation: dnxBounce 1.4s infinite ease-in-out both;
    }
    .dnx-typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .dnx-typing-dot:nth-child(2) { animation-delay: -0.16s; }
    @keyframes dnxBounce {
        0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* Quick Starter Chips */
    .dnx-chips-container {
        padding: 8px 16px 12px 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        background: #ffffff;
        border-top: 1px solid #f2f2f2;
        flex-shrink: 0;
    }
    .dnx-chip-btn {
        background: #fafafa;
        border: 1px solid #dfdfdf;
        color: #212121;
        font-size: 11.5px;
        padding: 5px 10px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.15s ease;
        white-space: nowrap;
    }
    .dnx-chip-btn:hover {
        background: #171717;
        color: #ffffff;
        border-color: #171717;
    }

    /* Footer / Input Area */
    .dnx-chat-footer {
        padding: 12px 16px 14px 16px;
        background: #ffffff;
        border-top: 1px solid #ededed;
        display: flex;
        gap: 8px;
        align-items: flex-end;
        flex-shrink: 0;
    }
    .dnx-input-wrapper {
        flex: 1;
        position: relative;
    }
    .dnx-chat-input {
        width: 100%;
        max-height: 100px;
        min-height: 40px;
        padding: 10px 14px;
        font-size: 13.5px;
        line-height: 1.4;
        border: 1px solid #dfdfdf;
        border-radius: 12px;
        outline: none;
        resize: none;
        font-family: inherit;
        background: #fafafa;
        color: #171717;
        transition: border-color 0.15s, background 0.15s;
    }
    .dnx-chat-input:focus {
        border-color: #3ecf8e;
        background: #ffffff;
        box-shadow: 0 0 0 3px rgba(62, 207, 142, 0.15);
    }
    .dnx-send-btn {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: #3ecf8e;
        color: #171717;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.15s ease;
        flex-shrink: 0;
    }
    .dnx-send-btn:hover {
        background: #24b47e;
        color: #ffffff;
        transform: translateY(-1px);
    }
    .dnx-send-btn:active {
        transform: translateY(1px);
    }
    .dnx-send-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    /* Mobile Responsive adjustments */
    @media (max-width: 480px) {
        .dnx-chat-launcher {
            bottom: 16px;
            right: 16px;
            width: 56px;
            height: 56px;
        }
        .dnx-chat-window {
            bottom: 84px;
            right: 12px;
            left: 12px;
            width: auto;
            max-width: none;
            height: calc(100vh - 100px);
        }
    }
    `;

    // --- DOM TEMPLATE GENERATION ---
    function injectChatbot() {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'dnx-chatbot-styles';
        styleSheet.textContent = cssStyles;
        document.head.appendChild(styleSheet);

        const root = document.createElement('div');
        root.className = 'dnx-chat-widget-root';
        root.id = 'dnx-chatbot-root';

        root.innerHTML = `
            <!-- Floating Launcher with Bot Sign -->
            <button class="dnx-chat-launcher" id="dnx-launcher-btn" aria-label="Open DiginixIT Bot" title="DiginixIT AI Bot">
                <span class="dnx-chat-launcher-pulse"></span>
                <span class="dnx-chat-launcher-badge"></span>
                <!-- Robot / Bot Sign -->
                <svg id="dnx-launcher-icon-chat" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#3ecf8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2v3"></path>
                    <rect x="4" y="6" width="16" height="13" rx="3"></rect>
                    <circle cx="9" cy="11.5" r="1.5" fill="#3ecf8e"></circle>
                    <circle cx="15" cy="11.5" r="1.5" fill="#3ecf8e"></circle>
                    <path d="M9 15.5h6"></path>
                    <path d="M2 12h2"></path>
                    <path d="M20 12h2"></path>
                </svg>
                <svg id="dnx-launcher-icon-close" style="display:none;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>

            <!-- Chat Window -->
            <div class="dnx-chat-window" id="dnx-chat-window">
                <!-- Header -->
                <div class="dnx-chat-header">
                    <div class="dnx-chat-header-brand">
                        <div class="dnx-chat-avatar" title="DiginixIT Bot">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3ecf8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 2v3"></path>
                                <rect x="4" y="6" width="16" height="13" rx="3"></rect>
                                <circle cx="9" cy="11.5" r="1.5" fill="#3ecf8e"></circle>
                                <circle cx="15" cy="11.5" r="1.5" fill="#3ecf8e"></circle>
                                <path d="M9 15.5h6"></path>
                            </svg>
                        </div>
                        <div class="dnx-chat-header-titles">
                            <span class="dnx-chat-title">
                                DIGINIXIT.
                                <span class="dnx-status-indicator" title="Online"></span>
                            </span>
                            <span class="dnx-chat-subtitle">
                                AI Assistant &amp; Strategic Advisory
                            </span>
                        </div>
                    </div>
                    <div class="dnx-chat-header-actions">
                        <button class="dnx-header-btn" id="dnx-btn-clear" title="Clear Chat History" aria-label="Clear Chat">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                        </button>
                        <button class="dnx-header-btn" id="dnx-btn-close" title="Minimize Chat" aria-label="Close Chat">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Chat Messages Scroll Area -->
                <div class="dnx-chat-messages" id="dnx-messages-container"></div>

                <!-- Quick Starter Chips -->
                <div class="dnx-chips-container" id="dnx-chips-container">
                    <button class="dnx-chip-btn" data-query="Who is Dr. Nadeem Nazir and what is his role?">Dr. Nadeem Nazir</button>
                    <button class="dnx-chip-btn" data-query="What web engineering services does DiginixIT offer?">Web Engineering</button>
                    <button class="dnx-chip-btn" data-query="How can DiginixIT optimize Core Web Vitals and SEO?">SEO & Vitals</button>
                    <button class="dnx-chip-btn" data-query="Tell me about tech law & compliance consulting.">Law & Compliance</button>
                    <button class="dnx-chip-btn" data-query="How to contact DiginixIT or book a consultation?">Contact & Quote</button>
                </div>

                <!-- Footer / Input -->
                <div class="dnx-chat-footer">
                    <div class="dnx-input-wrapper">
                        <textarea class="dnx-chat-input" id="dnx-chat-input" placeholder="Ask anything about DiginixIT & Dr. Nadeem Nazir..." rows="1"></textarea>
                    </div>
                    <button class="dnx-send-btn" id="dnx-send-btn" aria-label="Send Message">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(root);
        bindEvents();
        renderInitialMessages();
    }

    // --- FORMAT MARKDOWN-LIKE TEXT TO HTML ---
    function formatMessageText(text) {
        if (!text) return '';
        let escaped = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');
        escaped = escaped.replace(/\[(.*?)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        escaped = escaped.replace(/(https?:\/\/[^\s<]+)/g, function(url) {
            if (url.includes('</a>')) return url;
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });

        const paragraphs = escaped.split(/\n\n+/);
        return paragraphs.map(p => {
            const lines = p.split('\n');
            const hasList = lines.some(l => l.trim().startsWith('- ') || l.trim().startsWith('• '));
            if (hasList) {
                let html = '<ul>';
                lines.forEach(l => {
                    const clean = l.replace(/^[-•]\s*/, '').trim();
                    if (clean) html += `<li>${clean}</li>`;
                });
                html += '</ul>';
                return html;
            }
            return `<p>${lines.join('<br>')}</p>`;
        }).join('');
    }

    let isOpen = false;
    let isTyping = false;
    let conversationHistory = [];

    function renderInitialMessages() {
        const container = document.getElementById('dnx-messages-container');
        if (!container) return;

        const stored = getStoredHistory();
        if (stored.length > 0) {
            conversationHistory = stored;
            container.innerHTML = '';
            stored.forEach(msg => appendMessageDOM(msg.role, msg.content, msg.time, false));
        } else {
            conversationHistory = [
                {
                    role: 'assistant',
                    content: `Hello and welcome to **DiginixIT**! 🚀\n\nI am your strategic AI consultant. I can assist you with:\n- **Dr. Nadeem Nazir**: Executive credentials, advisory & consultations\n- **Web Engineering**: Custom SaaS, serverless web apps & 3D WebGL\n- **UI/UX Design**: Bespoke design systems & typography\n- **Technical SEO**: Core Web Vitals & organic growth\n- **Tech Law & Corporate Finance**: Compliance & valuation modeling\n\nHow can we help engineer or scale your business today?`,
                    time: getCurrentTime()
                }
            ];
            container.innerHTML = '';
            appendMessageDOM('assistant', conversationHistory[0].content, conversationHistory[0].time, false);
            setStoredHistory(conversationHistory);
        }
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function appendMessageDOM(role, content, time = getCurrentTime(), scroll = true) {
        const container = document.getElementById('dnx-messages-container');
        if (!container) return;

        const row = document.createElement('div');
        row.className = `dnx-message-row ${role === 'user' ? 'dnx-user' : 'dnx-bot'}`;

        if (role === 'assistant') {
            const avatar = document.createElement('div');
            avatar.className = 'dnx-message-avatar';
            avatar.title = 'DiginixIT Bot';
            avatar.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3ecf8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"></path><rect x="4" y="6" width="16" height="13" rx="3"></rect><circle cx="9" cy="11.5" r="1.5" fill="#3ecf8e"></circle><circle cx="15" cy="11.5" r="1.5" fill="#3ecf8e"></circle><path d="M9 15.5h6"></path></svg>`;
            row.appendChild(avatar);
        }

        const bubbleWrap = document.createElement('div');
        bubbleWrap.style.display = 'flex';
        bubbleWrap.style.flexDirection = 'column';

        const bubble = document.createElement('div');
        bubble.className = 'dnx-message-bubble';
        bubble.innerHTML = formatMessageText(content);
        bubbleWrap.appendChild(bubble);

        const timeSpan = document.createElement('div');
        timeSpan.className = 'dnx-message-time';
        timeSpan.textContent = time;
        bubbleWrap.appendChild(timeSpan);

        row.appendChild(bubbleWrap);
        container.appendChild(row);

        if (scroll) {
            container.scrollTop = container.scrollHeight;
        }
    }

    function showTypingIndicator() {
        const container = document.getElementById('dnx-messages-container');
        if (!container) return null;

        const row = document.createElement('div');
        row.id = 'dnx-typing-row';
        row.className = 'dnx-message-row dnx-bot';

        const avatar = document.createElement('div');
        avatar.className = 'dnx-message-avatar';
        avatar.title = 'DiginixIT Bot';
        avatar.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3ecf8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"></path><rect x="4" y="6" width="16" height="13" rx="3"></rect><circle cx="9" cy="11.5" r="1.5" fill="#3ecf8e"></circle><circle cx="15" cy="11.5" r="1.5" fill="#3ecf8e"></circle><path d="M9 15.5h6"></path></svg>`;
        row.appendChild(avatar);

        const indicator = document.createElement('div');
        indicator.className = 'dnx-typing-indicator';
        indicator.innerHTML = '<span class="dnx-typing-dot"></span><span class="dnx-typing-dot"></span><span class="dnx-typing-dot"></span>';

        row.appendChild(indicator);
        container.appendChild(row);
        container.scrollTop = container.scrollHeight;
        return row;
    }

    function removeTypingIndicator() {
        const row = document.getElementById('dnx-typing-row');
        if (row) row.remove();
    }

    // Client-side fallback knowledge retrieval
    function getFallbackResponse(query) {
        const q = (query || '').toLowerCase();
        if (q.includes('nadeem') || q.includes('nazir') || q.includes('doctor') || q.includes('ceo') || q.includes('advisor')) {
            const doc = DIGINIX_KNOWLEDGE_BASE.leadership.executiveAdvisor;
            return `**${doc.name}** is the **${doc.title}** at DiginixIT.\n\n` +
                `**About Dr. Nadeem Nazir:**\n${doc.bio}\n\n` +
                `**Core Advisory Domains:**\n` +
                doc.expertise.map(e => `• ${e}`).join('\n') + '\n\n' +
                `**Contact & Appointments:**\n` +
                `• Voice/WhatsApp: [${DIGINIX_KNOWLEDGE_BASE.contact.phone}](tel:${DIGINIX_KNOWLEDGE_BASE.contact.phoneRaw})\n` +
                `• Email: [${DIGINIX_KNOWLEDGE_BASE.contact.email}](mailto:${DIGINIX_KNOWLEDGE_BASE.contact.email})\n` +
                `• LinkedIn: [DiginixIT LinkedIn](${doc.linkedIn})`;
        }
        if (q.includes('contact') || q.includes('email') || q.includes('phone') || q.includes('address')) {
            const c = DIGINIX_KNOWLEDGE_BASE.contact;
            const h = DIGINIX_KNOWLEDGE_BASE.headquarters;
            return `**Contact DiginixIT:**\n\n` +
                `• **Phone / WhatsApp**: [${c.phone}](tel:${c.phoneRaw})\n` +
                `• **Email**: [${c.email}](mailto:${c.email})\n` +
                `• **Corporate Address**: ${h.corporate}\n` +
                `• **Global Studio**: ${h.engineeringStudio}\n` +
                `• **Hours**: ${c.hours}`;
        }
        return `**DiginixIT | Build, Protect & Scale Your Business**\n\n` +
            `We are a premier multidisciplinary technology agency specializing in Web Engineering, UI/UX Design, Technical SEO, Tech Law, and Corporate Finance.\n\n` +
            `Executive Leadership: **Dr. Nadeem Nazir**\n` +
            `Direct Inquiries: [${DIGINIX_KNOWLEDGE_BASE.contact.phone}](tel:${DIGINIX_KNOWLEDGE_BASE.contact.phoneRaw}) | [${DIGINIX_KNOWLEDGE_BASE.contact.email}](mailto:${DIGINIX_KNOWLEDGE_BASE.contact.email})`;
    }

    // --- SECURE SERVER CALL ---
    async function queryServerChat(userMessage) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: userMessage,
                    history: conversationHistory.slice(-8)
                })
            });

            if (!response.ok) {
                console.warn('Server /api/chat error:', response.status);
                return getFallbackResponse(userMessage);
            }

            const data = await response.json();
            return data.reply || getFallbackResponse(userMessage);
        } catch (err) {
            console.error('Fetch /api/chat network error:', err);
            return getFallbackResponse(userMessage);
        }
    }

    // --- SEND MESSAGE HANDLER ---
    async function handleSendMessage(customText) {
        const input = document.getElementById('dnx-chat-input');
        const text = (customText || (input ? input.value : '')).trim();
        if (!text || isTyping) return;

        if (input) {
            input.value = '';
            input.style.height = '40px';
        }

        isTyping = true;
        const sendBtn = document.getElementById('dnx-send-btn');
        if (sendBtn) sendBtn.disabled = true;

        const now = getCurrentTime();
        appendMessageDOM('user', text, now);
        conversationHistory.push({ role: 'user', content: text, time: now });
        setStoredHistory(conversationHistory);

        showTypingIndicator();

        try {
            const botReply = await queryServerChat(text);
            removeTypingIndicator();

            const replyTime = getCurrentTime();
            appendMessageDOM('assistant', botReply, replyTime);
            conversationHistory.push({ role: 'assistant', content: botReply, time: replyTime });
            setStoredHistory(conversationHistory);
        } catch (e) {
            removeTypingIndicator();
            const errReply = "An error occurred while communicating with the server. Please contact us directly at " + DIGINIX_KNOWLEDGE_BASE.contact.email;
            appendMessageDOM('assistant', errReply, getCurrentTime());
        } finally {
            isTyping = false;
            if (sendBtn) sendBtn.disabled = false;
        }
    }

    // --- EVENT LISTENERS ---
    function bindEvents() {
        const launcher = document.getElementById('dnx-launcher-btn');
        const chatWin = document.getElementById('dnx-chat-window');
        const iconChat = document.getElementById('dnx-launcher-icon-chat');
        const iconClose = document.getElementById('dnx-launcher-icon-close');
        const btnClose = document.getElementById('dnx-btn-close');
        const btnClear = document.getElementById('dnx-btn-clear');
        const input = document.getElementById('dnx-chat-input');
        const sendBtn = document.getElementById('dnx-send-btn');
        const chipsContainer = document.getElementById('dnx-chips-container');

        function toggleChat(forceState) {
            isOpen = typeof forceState === 'boolean' ? forceState : !isOpen;
            if (isOpen) {
                chatWin.classList.add('dnx-open');
                iconChat.style.display = 'none';
                iconClose.style.display = 'block';
                setTimeout(() => {
                    if (input) input.focus();
                }, 150);
            } else {
                chatWin.classList.remove('dnx-open');
                iconChat.style.display = 'block';
                iconClose.style.display = 'none';
            }
        }

        launcher.addEventListener('click', () => toggleChat());
        btnClose.addEventListener('click', () => toggleChat(false));

        btnClear.addEventListener('click', () => {
            if (confirm('Clear chat history?')) {
                localStorage.removeItem(STORAGE_KEY_HISTORY);
                conversationHistory = [];
                renderInitialMessages();
            }
        });

        sendBtn.addEventListener('click', () => handleSendMessage());

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });

        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 100) + 'px';
        });

        chipsContainer.addEventListener('click', (e) => {
            const btn = e.target.closest('.dnx-chip-btn');
            if (btn && btn.dataset.query) {
                handleSendMessage(btn.dataset.query);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectChatbot);
    } else {
        injectChatbot();
    }

    window.DiginixChatbot = {
        open: function() {
            const chatWin = document.getElementById('dnx-chat-window');
            if (chatWin) chatWin.classList.add('dnx-open');
        },
        close: function() {
            const chatWin = document.getElementById('dnx-chat-window');
            if (chatWin) chatWin.classList.remove('dnx-open');
        },
        sendMessage: handleSendMessage
    };

})();
