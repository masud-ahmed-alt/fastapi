const logsContainer = document.getElementById('logs');
const logsWrapper = document.getElementById('logs-container');

// const url = "localhost:8000"

var url = window.location.hostname;
var port = 8000

// Function to append logs to the DOM
function appendLog(log) {
    const p = document.createElement('p');
    p.textContent = log;
    logsContainer.appendChild(p);
    logsWrapper.scrollTop = logsWrapper.scrollHeight; // Scroll to bottom
}

// Function to handle WebSocket connection
function connectWebSocket() {
    const ws = new WebSocket(`ws://${url}:${port}/ws`);

    ws.onopen = function (event) {
        console.log('WebSocket connection established.');
    };

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        logsContainer.innerHTML = ''; // Clear previous logs
        data.logs.forEach(log => {
            appendLog(log);
        });
    };

    ws.onclose = function (event) {
        console.log('WebSocket connection closed.');
        setTimeout(connectWebSocket, 1000); // Attempt to reconnect after 1 second
    };

    ws.onerror = function (event) {
        console.error('WebSocket error:', event);
    };
}

// Connect to WebSocket on page load
document.addEventListener('DOMContentLoaded', function () {
    connectWebSocket();
});