const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8000 });

wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.send('Welcome to the WebSocket server!');

    const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
        }
    }, 30000);

    ws.on('message', (message) => {
        console.log(`Received: ${message}`);
        ws.send(`You said: ${message}`);
    });

    ws.on('close', () => {
        clearInterval(interval);
        console.log('Client disconnected');
    });
    
    ws.on('error', (error) => {
        console.error(`WebSocket error: ${error.message}`);
    });
});

wss.on('error', (error) => {
    console.error(`WebSocket server error: ${error.message}`);
});

console.log('WebSocket server is running on ws://localhost:8000');
