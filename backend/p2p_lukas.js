// p2p.js
const net = require('net');
const readline = require('readline');

// Create a readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Hardcoded peer configuration
const localHost = '172.20.10.3'; // Localhost for testing
const listeningPort = 8080; // Port for the server to listen
const sendingHost = '172.20.10.3'; // IP address to send messages to (can be changed to another peer's IP)
const sendingPort = 8080; // Port to send messages to (should match the listening port)

// Create a server to listen for incoming messages
const server = net.createServer((socket) => {
    console.log('Connected to peer');

    // Listen for incoming data from the peer
    socket.on('data', (data) => {
        // Print out the received message
        console.log(`Received: ${data.toString()}`); // Convert Buffer to string and print
    });

    // Handle socket end event
    socket.on('end', () => {
        console.log('Disconnected from peer');
    });
});

// Start the server
server.listen(listeningPort, () => {
    console.log(`Server listening on ${localHost}:${listeningPort}`);

    // Connect to the peer immediately after starting the server
    const client = net.createConnection({ host: sendingHost, port: sendingPort }, () => {
        console.log(`Connected to peer at ${sendingHost}:${sendingPort}. Type your messages:`);
    });

    // Handle input from the user
    rl.on('line', (input) => {
        client.write(input); // Send message to peer
    });

    // Handle client connection errors
    client.on('error', (err) => {
        console.error(`Connection error: ${err.message}`);
    });
});

// Handle server errors
server.on('error', (err) => {
    console.error(`Server error: ${err.message}`);
});

