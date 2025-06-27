function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatBox = document.getElementById('chat-box');

    if (userInput) {
        // Display user message
        chatBox.innerHTML += "<div class='user-message'>You: " + userInput + "</div>";

        // Send message to Flask API
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'message=' + userInput
        })
        .then(response => response.json())
        .then(data => {
            // Display bot response
            chatBox.innerHTML += "<div class='bot-message'>Bot: " + data.response + "</div>";
            document.getElementById('user-input').value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}
