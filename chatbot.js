/**
 * Print Pro SG — AI Chat Bot Widget
 * Floating chat widget powered by GPT-4.1-mini
 */

(function () {
  'use strict';

  // ── CONFIG ──────────────────────────────────────────────────────
  const CHAT_API = 'https://8001-irj92ex2x0b9r8yzz0s0h-f37a8bc9.sg1.manus.computer/chat';
  const BOT_NAME = 'Print Boy';
  const BOT_AVATAR = '🤖';
  const WELCOME_MSG = "Hi! I'm **Print Boy**, your Print Pro SG assistant. 👋\n\nI can help you with:\n• Product recommendations & pricing\n• Paper stocks, sizes & finishes\n• Delivery & turnaround times\n• Design service queries\n\nWhat can I help you with today?";

  const QUICK_REPLIES = [
    { label: '💳 Name Card prices', msg: 'What are the prices for name cards?' },
    { label: '🚀 Same-day printing', msg: 'Do you offer same-day printing?' },
    { label: '🎨 Design services', msg: 'Tell me about your design services' },
    { label: '📦 Delivery info', msg: 'How long does delivery take?' },
  ];

  // ── STATE ────────────────────────────────────────────────────────
  let isOpen = false;
  let isTyping = false;
  let conversationHistory = [];
  let hasShownWelcome = false;
  let unreadCount = 0;

  // ── BUILD WIDGET HTML ────────────────────────────────────────────
  function buildWidget() {
    const widget = document.createElement('div');
    widget.id = 'printbot-widget';
    widget.innerHTML = `
      <!-- Toggle Button -->
      <button id="printbot-toggle" aria-label="Open chat with Print Boy">
        <span class="printbot-toggle-icon printbot-icon-chat">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </span>
        <span class="printbot-toggle-icon printbot-icon-close" style="display:none">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </span>
        <span id="printbot-badge" class="printbot-badge" style="display:none">1</span>
      </button>

      <!-- Chat Window -->
      <div id="printbot-window" class="printbot-window" aria-hidden="true">
        <!-- Header -->
        <div class="printbot-header">
          <div class="printbot-header-avatar">
            <span>🤖</span>
            <span class="printbot-online-dot"></span>
          </div>
          <div class="printbot-header-info">
            <div class="printbot-header-name">Print Boy</div>
            <div class="printbot-header-status">AI Assistant · Online</div>
          </div>
          <div class="printbot-header-actions">
            <button class="printbot-header-btn" id="printbot-clear" title="Clear chat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
                <path d="M10 11v6"></path><path d="M14 11v6"></path>
                <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path>
              </svg>
            </button>
            <button class="printbot-header-btn" id="printbot-close" title="Close chat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div id="printbot-messages" class="printbot-messages" role="log" aria-live="polite">
          <!-- Messages injected here -->
        </div>

        <!-- Quick Replies -->
        <div id="printbot-quick-replies" class="printbot-quick-replies">
          ${QUICK_REPLIES.map(q => `<button class="printbot-quick-btn" data-msg="${q.msg}">${q.label}</button>`).join('')}
        </div>

        <!-- Input Area -->
        <div class="printbot-input-area">
          <textarea
            id="printbot-input"
            class="printbot-input"
            placeholder="Ask me about printing..."
            rows="1"
            aria-label="Type your message"
          ></textarea>
          <button id="printbot-send" class="printbot-send-btn" aria-label="Send message" disabled>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
        <div class="printbot-footer-note">Powered by AI · Print Pro SG</div>
      </div>

      <!-- Greeting Bubble (shown after 5s) -->
      <div id="printbot-greeting" class="printbot-greeting" style="display:none">
        <span>👋 Hi! Need help with printing?</span>
        <button id="printbot-greeting-close">×</button>
      </div>
    `;
    document.body.appendChild(widget);
    injectStyles();
    bindEvents();

    // Show greeting bubble after 30 seconds
    setTimeout(() => {
      const greeting = document.getElementById('printbot-greeting');
      if (greeting && !isOpen) {
        greeting.style.display = 'flex';
        // Show unread badge
        showBadge(1);
        setTimeout(() => {
          greeting.style.display = 'none';
        }, 8000);
      }
    }, 30000);
  }

  // ── STYLES ───────────────────────────────────────────────────────
  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
      #printbot-widget {
        position: fixed;
        bottom: 28px;
        right: 28px;
        z-index: 99999;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      }

      /* Toggle Button */
      #printbot-toggle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #d62b2b 0%, #b01e1e 100%);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(214,43,43,0.45), 0 2px 8px rgba(0,0,0,0.15);
        transition: transform 280ms cubic-bezier(.34,1.56,.64,1), box-shadow 280ms ease;
        position: relative;
        color: #fff;
        margin-left: auto;
      }
      #printbot-toggle:hover {
        transform: scale(1.08);
        box-shadow: 0 8px 28px rgba(214,43,43,0.55), 0 4px 12px rgba(0,0,0,0.2);
      }
      #printbot-toggle:active { transform: scale(0.95); }
      .printbot-toggle-icon { display: flex; align-items: center; justify-content: center; }

      /* Badge */
      .printbot-badge {
        position: absolute;
        top: -4px;
        right: -4px;
        background: #ff3b30;
        color: #fff;
        font-size: 11px;
        font-weight: 700;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #fff;
        animation: printbot-bounce 0.4s ease;
      }
      @keyframes printbot-bounce {
        0% { transform: scale(0); }
        60% { transform: scale(1.2); }
        100% { transform: scale(1); }
      }

      /* Greeting Bubble */
      .printbot-greeting {
        position: absolute;
        bottom: 70px;
        right: 0;
        background: #fff;
        border-radius: 16px 16px 4px 16px;
        padding: 10px 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        font-size: 13px;
        font-weight: 500;
        color: #1d1d1f;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: printbot-slide-up 0.3s ease;
        border: 1px solid rgba(0,0,0,0.06);
      }
      #printbot-greeting-close {
        background: none;
        border: none;
        cursor: pointer;
        color: #999;
        font-size: 16px;
        padding: 0 2px;
        line-height: 1;
      }

      /* Chat Window */
      .printbot-window {
        position: absolute;
        bottom: 72px;
        right: 0;
        width: 380px;
        max-height: 580px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.18), 0 4px 20px rgba(0,0,0,0.08);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: scale(0.85) translateY(20px);
        opacity: 0;
        pointer-events: none;
        transition: transform 280ms cubic-bezier(.34,1.56,.64,1), opacity 220ms ease;
        transform-origin: bottom right;
        border: 1px solid rgba(0,0,0,0.06);
      }
      .printbot-window.open {
        transform: scale(1) translateY(0);
        opacity: 1;
        pointer-events: all;
      }

      /* Header */
      .printbot-header {
        background: linear-gradient(135deg, #d62b2b 0%, #b01e1e 100%);
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        flex-shrink: 0;
      }
      .printbot-header-avatar {
        width: 42px;
        height: 42px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        position: relative;
        flex-shrink: 0;
      }
      .printbot-online-dot {
        position: absolute;
        bottom: 1px;
        right: 1px;
        width: 10px;
        height: 10px;
        background: #34c759;
        border-radius: 50%;
        border: 2px solid #d62b2b;
      }
      .printbot-header-info { flex: 1; }
      .printbot-header-name { font-size: 15px; font-weight: 700; color: #fff; }
      .printbot-header-status { font-size: 11px; color: rgba(255,255,255,0.75); margin-top: 1px; }
      .printbot-header-actions { display: flex; gap: 4px; }
      .printbot-header-btn {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: rgba(255,255,255,0.15);
        border: none;
        cursor: pointer;
        color: rgba(255,255,255,0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 160ms ease;
      }
      .printbot-header-btn:hover { background: rgba(255,255,255,0.25); color: #fff; }

      /* Messages */
      .printbot-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        scroll-behavior: smooth;
        background: #f8f8fa;
      }
      .printbot-messages::-webkit-scrollbar { width: 4px; }
      .printbot-messages::-webkit-scrollbar-track { background: transparent; }
      .printbot-messages::-webkit-scrollbar-thumb { background: #ddd; border-radius: 4px; }

      /* Message Bubbles */
      .printbot-msg {
        display: flex;
        gap: 8px;
        animation: printbot-msg-in 0.25s ease;
        max-width: 100%;
      }
      @keyframes printbot-msg-in {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .printbot-msg.user { flex-direction: row-reverse; }
      .printbot-msg-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
        margin-top: 2px;
      }
      .printbot-msg.bot .printbot-msg-avatar { background: #fff0f0; }
      .printbot-msg.user .printbot-msg-avatar { background: #e8f4ff; }
      .printbot-msg-bubble {
        max-width: calc(100% - 46px);
        padding: 10px 14px;
        border-radius: 18px;
        font-size: 13.5px;
        line-height: 1.55;
        word-break: break-word;
      }
      .printbot-msg.bot .printbot-msg-bubble {
        background: #fff;
        color: #1d1d1f;
        border-bottom-left-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
      }
      .printbot-msg.user .printbot-msg-bubble {
        background: linear-gradient(135deg, #d62b2b, #b01e1e);
        color: #fff;
        border-bottom-right-radius: 6px;
      }
      .printbot-msg-bubble strong { font-weight: 700; }
      .printbot-msg-bubble a { color: inherit; text-decoration: underline; }
      .printbot-msg-time {
        font-size: 10px;
        color: #aaa;
        margin-top: 4px;
        text-align: right;
      }
      .printbot-msg.bot .printbot-msg-time { text-align: left; }

      /* Typing Indicator */
      .printbot-typing .printbot-msg-bubble {
        padding: 12px 16px;
        display: flex;
        gap: 4px;
        align-items: center;
      }
      .printbot-dot {
        width: 7px;
        height: 7px;
        background: #ccc;
        border-radius: 50%;
        animation: printbot-typing 1.2s infinite;
      }
      .printbot-dot:nth-child(2) { animation-delay: 0.2s; }
      .printbot-dot:nth-child(3) { animation-delay: 0.4s; }
      @keyframes printbot-typing {
        0%, 60%, 100% { transform: translateY(0); background: #ccc; }
        30% { transform: translateY(-5px); background: #d62b2b; }
      }

      /* Quick Replies */
      .printbot-quick-replies {
        padding: 8px 12px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        background: #f8f8fa;
        border-top: 1px solid #f0f0f0;
        flex-shrink: 0;
      }
      .printbot-quick-btn {
        background: #fff;
        border: 1.5px solid #e8e8ed;
        border-radius: 20px;
        padding: 10px 12px;
        min-height: 44px;
        font-size: 12px;
        font-weight: 500;
        color: #1d1d1f;
        cursor: pointer;
        transition: all 160ms ease;
        white-space: nowrap;
      }
      .printbot-quick-btn:hover {
        border-color: #d62b2b;
        color: #d62b2b;
        background: #fff0f0;
      }

      /* Input Area */
      .printbot-input-area {
        padding: 12px 14px;
        display: flex;
        gap: 8px;
        align-items: flex-end;
        background: #fff;
        border-top: 1px solid #f0f0f0;
        flex-shrink: 0;
      }
      .printbot-input {
        flex: 1;
        border: 1.5px solid #e8e8ed;
        border-radius: 22px;
        padding: 10px 14px;
        font-size: 16px;
        color: #1d1d1f;
        background: #f8f8fa;
        resize: none;
        outline: none;
        min-height: 44px;
        max-height: 100px;
        overflow-y: auto;
        transition: border-color 160ms ease, background 160ms ease;
        line-height: 1.5;
        font-family: inherit;
        box-sizing: border-box;
      }
      .printbot-input:focus {
        border-color: #d62b2b;
        background: #fff;
      }
      .printbot-input::placeholder { color: #aaa; }
      .printbot-send-btn {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: #d62b2b;
        border: none;
        cursor: pointer;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        transition: background 160ms ease, transform 160ms ease;
      }
      .printbot-send-btn:hover:not(:disabled) {
        background: #b01e1e;
        transform: scale(1.05);
      }
      .printbot-send-btn:disabled {
        background: #e8e8ed;
        color: #aaa;
        cursor: not-allowed;
      }

      /* Footer Note */
      .printbot-footer-note {
        text-align: center;
        font-size: 10px;
        color: #bbb;
        padding: 4px 0 8px;
        background: #fff;
        flex-shrink: 0;
      }

      @keyframes printbot-slide-up {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }

      /* Mobile */
      @media (max-width: 480px) {
        #printbot-widget { bottom: 16px; right: 16px; }
        .printbot-window {
          width: calc(100vw - 32px);
          right: -16px;
          bottom: 68px;
          max-height: 70vh;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // ── EVENTS ───────────────────────────────────────────────────────
  function bindEvents() {
    const toggle = document.getElementById('printbot-toggle');
    const closeBtn = document.getElementById('printbot-close');
    const clearBtn = document.getElementById('printbot-clear');
    const sendBtn = document.getElementById('printbot-send');
    const input = document.getElementById('printbot-input');
    const greetingClose = document.getElementById('printbot-greeting-close');

    toggle.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', closeChat);
    clearBtn.addEventListener('click', clearChat);
    sendBtn.addEventListener('click', sendMessage);
    greetingClose.addEventListener('click', () => {
      document.getElementById('printbot-greeting').style.display = 'none';
    });

    input.addEventListener('input', () => {
      // Auto-resize textarea
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 100) + 'px';
      // Enable/disable send button
      document.getElementById('printbot-send').disabled = input.value.trim() === '';
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (input.value.trim()) sendMessage();
      }
    });

    // Quick reply buttons
    document.querySelectorAll('.printbot-quick-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const msg = btn.getAttribute('data-msg');
        document.getElementById('printbot-input').value = msg;
        document.getElementById('printbot-send').disabled = false;
        sendMessage();
      });
    });
  }

  function toggleChat() {
    if (isOpen) {
      closeChat();
    } else {
      openChat();
    }
  }

  function openChat() {
    isOpen = true;
    const win = document.getElementById('printbot-window');
    const iconChat = document.querySelector('.printbot-icon-chat');
    const iconClose = document.querySelector('.printbot-icon-close');
    const greeting = document.getElementById('printbot-greeting');

    win.classList.add('open');
    win.setAttribute('aria-hidden', 'false');
    iconChat.style.display = 'none';
    iconClose.style.display = 'flex';
    greeting.style.display = 'none';
    hideBadge();

    if (!hasShownWelcome) {
      hasShownWelcome = true;
      setTimeout(() => addBotMessage(WELCOME_MSG), 300);
    }

    setTimeout(() => {
      document.getElementById('printbot-input').focus();
    }, 350);
  }

  function closeChat() {
    isOpen = false;
    const win = document.getElementById('printbot-window');
    const iconChat = document.querySelector('.printbot-icon-chat');
    const iconClose = document.querySelector('.printbot-icon-close');

    win.classList.remove('open');
    win.setAttribute('aria-hidden', 'true');
    iconChat.style.display = 'flex';
    iconClose.style.display = 'none';
  }

  function clearChat() {
    conversationHistory = [];
    hasShownWelcome = false;
    document.getElementById('printbot-messages').innerHTML = '';
    setTimeout(() => addBotMessage(WELCOME_MSG), 200);
  }

  // ── MESSAGING ────────────────────────────────────────────────────
  function sendMessage() {
    const input = document.getElementById('printbot-input');
    const text = input.value.trim();
    if (!text || isTyping) return;

    // Add user message
    addUserMessage(text);
    conversationHistory.push({ role: 'user', content: text });

    // Clear input
    input.value = '';
    input.style.height = 'auto';
    document.getElementById('printbot-send').disabled = true;

    // Hide quick replies after first message
    document.getElementById('printbot-quick-replies').style.display = 'none';

    // Show typing indicator
    showTyping();

    // Call API
    fetchBotReply(conversationHistory);
  }

  async function fetchBotReply(messages) {
    try {
      const response = await fetch(CHAT_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages }),
      });

      const data = await response.json();
      hideTyping();

      const reply = data.reply || "I'm sorry, I couldn't get a response. Please try again or contact us via WhatsApp.";
      addBotMessage(reply);
      conversationHistory.push({ role: 'assistant', content: reply });

    } catch (err) {
      hideTyping();
      addBotMessage("I'm having trouble connecting right now. Please contact us via WhatsApp at **+65 9875 1606** for immediate assistance! 📱");
    }
  }

  function addUserMessage(text) {
    const msgs = document.getElementById('printbot-messages');
    const time = getCurrentTime();
    const div = document.createElement('div');
    div.className = 'printbot-msg user';
    div.innerHTML = `
      <div class="printbot-msg-avatar">👤</div>
      <div>
        <div class="printbot-msg-bubble">${escapeHtml(text)}</div>
        <div class="printbot-msg-time">${time}</div>
      </div>
    `;
    msgs.appendChild(div);
    scrollToBottom();
  }

  function addBotMessage(text) {
    const msgs = document.getElementById('printbot-messages');
    const time = getCurrentTime();
    const div = document.createElement('div');
    div.className = 'printbot-msg bot';
    div.innerHTML = `
      <div class="printbot-msg-avatar">🤖</div>
      <div>
        <div class="printbot-msg-bubble">${formatMarkdown(text)}</div>
        <div class="printbot-msg-time">${time}</div>
      </div>
    `;
    msgs.appendChild(div);
    scrollToBottom();
  }

  function showTyping() {
    isTyping = true;
    const msgs = document.getElementById('printbot-messages');
    const div = document.createElement('div');
    div.className = 'printbot-msg bot printbot-typing';
    div.id = 'printbot-typing-indicator';
    div.innerHTML = `
      <div class="printbot-msg-avatar">🤖</div>
      <div class="printbot-msg-bubble">
        <span class="printbot-dot"></span>
        <span class="printbot-dot"></span>
        <span class="printbot-dot"></span>
      </div>
    `;
    msgs.appendChild(div);
    scrollToBottom();
  }

  function hideTyping() {
    isTyping = false;
    const indicator = document.getElementById('printbot-typing-indicator');
    if (indicator) indicator.remove();
  }

  function scrollToBottom() {
    const msgs = document.getElementById('printbot-messages');
    setTimeout(() => {
      msgs.scrollTop = msgs.scrollHeight;
    }, 50);
  }

  function showBadge(count) {
    const badge = document.getElementById('printbot-badge');
    badge.textContent = count;
    badge.style.display = 'flex';
    unreadCount = count;
  }

  function hideBadge() {
    const badge = document.getElementById('printbot-badge');
    badge.style.display = 'none';
    unreadCount = 0;
  }

  // ── HELPERS ──────────────────────────────────────────────────────
  function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-SG', { hour: '2-digit', minute: '2-digit' });
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function formatMarkdown(text) {
    // Basic markdown: bold, links, line breaks, bullet points
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/^• /gm, '• ')
      .replace(/\n/g, '<br>');
  }

  // ── INIT ─────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }

})();
