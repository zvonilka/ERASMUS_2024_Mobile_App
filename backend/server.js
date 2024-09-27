const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 8000 });

const clients = []; // list of connected users

wss.on('connection', (ws) => {
    console.log('New client connected');
    
    // hardcoded names for devices for information
    let clientName = '';
    if (clients.length === 0) {
        clientName = 'LUKAS'; // First user
    } else if (clients.length === 1) {
        clientName = 'TOMAS'; // Second user
    } else if (clients.length === 2) {
        clientName = 'SAHAND'; // Third user
    } else {
        clientName = 'None'; // More than three users
    }
    
    clients.push({ ws, name: clientName }); // save users in memorz
    ws.send(`Welcome ${clientName} to the WebSocket server!`);

    const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(''));
        }
    }, 30000);

    ws.on('message', (message) => {
        console.log(`Received from ${clientName}: ${message}`);
        // send the message to everzone
        clients.forEach((client) => {
            if (client.ws.readyState === WebSocket.OPEN) {
                client.ws.send(`${clientName} said: ${message}`);
            }
        });
    });

    ws.on('close', () => {
        clearInterval(interval);
        console.log(`${clientName} disconnected`);
        // upon disconnecting delete user from memorz
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
