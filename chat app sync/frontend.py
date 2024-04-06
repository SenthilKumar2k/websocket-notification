#frontend
const chatSocket = new WebSocket('ws://localhost:8000/ws/chat/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Received message:', data.message);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function sendMessage(message) {
    chatSocket.send(JSON.stringify({
        'message': message
    }));
}


"""
"""
#WebSocket Connection:

The frontend code establishes a WebSocket connection to the chat endpoint ws://localhost:8000/ws/chat/.
This connection enables bidirectional communication between the client and the WebSocket server.

#Event Handlers:

onmessage: This event handler is triggered when the client receives a message from the WebSocket server. 
It parses the JSON data received and logs the message to the console.

onclose: This event handler is triggered when the WebSocket connection is closed unexpectedly.
It logs an error message to the console.

#sendMessage Function:

This function is used to send messages to the WebSocket server.
It takes a message as input, converts it to a JSON string, and sends it to the WebSocket 
server using the send method.


Overall, this frontend code sets up a WebSocket client that listens for incoming messages 
from the server and sends messages to the server when invoked. However, it lacks the user 
interface elements required for a chat application, such as input fields for typing messages 
and displaying chat history. You would need to integrate this frontend code with HTML and 
JavaScript code to create a fully functional chat application UI.