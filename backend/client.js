const WebSocket = require('ws');

const ws = new WebSocket('ws://192.168.214.11:8000');

ws.on('open', () => {
    console.log('Connected to the server');

    ws.send('Hello from the client!');
});

ws.on('message', (message) => {
    console.log(`Received from server: ${message}`);
});

ws.on('error', (error) => {
    console.error(`WebSocket error: ${error.message}`);
});

ws.on('close', () => {
    console.log('Disconnected from the server');
});
