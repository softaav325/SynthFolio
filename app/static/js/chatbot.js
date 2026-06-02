document.addEventListener('DOMContentLoaded', function() {
    const chatWidget = document.getElementById('ai-chat-widget');
    const chatTrigger = document.getElementById('ai-chat-trigger');
    const closeBtn = document.getElementById('close-chat');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('chat-typing');
    const sendBtn = document.getElementById('send-btn');

    // Функция открытия чата
    if (chatTrigger && chatWidget) {
        chatTrigger.addEventListener('click', () => {
            chatWidget.classList.remove('d-none');
            chatTrigger.classList.add('d-none');
        });
    }

    // Функция закрытия чата
    if (closeBtn && chatWidget && chatTrigger) {
        closeBtn.addEventListener('click', () => {
            chatWidget.classList.add('d-none');
            chatTrigger.classList.remove('d-none');
        });
    }

    // Функция добавления сообщения в чат
    function addMessage(text, isBot = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        
        messageDiv.innerHTML = `
            <div class="bubble">${text}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        
        // Автоматическая прокрутка вниз
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Обработка отправки формы
    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const message = userInput.value.trim();
            if (!message) return;

            addMessage(message, false);
            userInput.value = '';

            userInput.disabled = true;
            if (sendBtn) sendBtn.disabled = true;

            typingIndicator.classList.remove('d-none');
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                typingIndicator.classList.add('d-none');

                if (response.ok) {
                    addMessage(data.answer, true);
                } else {
                    addMessage(`Ошибка: ${data.error || 'Что-то пошло не так'}`, true);
                }

            } catch (error) {
                typingIndicator.classList.add('d-none');
                addMessage('Произошла ошибка сети. Пожалуйста, проверьте соединение.', true);
                console.error('Chat Network Error:', error);
            } finally {
                userInput.disabled = false;
                if (sendBtn) sendBtn.disabled = false;
                userInput.focus();
            }
        });
    }
});
