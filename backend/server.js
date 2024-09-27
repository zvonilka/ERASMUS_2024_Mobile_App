const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8000 });

const clients = []; // Array to store connected clients

wss.on('connection', (ws) => {
    console.log('New client connected');
    
    // Assign names to clients
    let clientName = '';
    if (clients.length === 0) {
        clientName = 'LUKAS'; // First client
    } else if (clients.length === 1) {
        clientName = 'TOMAS'; // Second client
    } else if (clients.length === 2) {
        clientName = 'SAHAND'; // Third client
    } else {
        clientName = 'None'; // More than three clients
    }
    
    clients.push({ ws, name: clientName }); // Store client with its name
    ws.send(`Welcome ${clientName} to the WebSocket server!`);

    const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(''));
        }
    }, 30000);

    ws.on('message', (message) => {
        console.log(`Received from ${clientName}: ${message}`);
        // Broadcast the message to all connected clients
        clients.forEach((client) => {
            if (client.ws.readyState === WebSocket.OPEN) {
                client.ws.send(`${clientName} said: ${message}`);
            }
        });
    });

    ws.on('close', () => {
        clearInterval(interval);
        console.log(`${clientName} disconnected`);
        // Remove the client from the list
        clients.splice(clients.indexOf({ ws }), 1);
    });
    
    ws.on('error', (error) => {
        console.error(`WebSocket error: ${error.message}`);
    });
});

wss.on('error', (error) => {
    console.error(`WebSocket server error: ${error.message}`);
});

console.log('WebSocket server is running on ws://localhost:8000');
