import http.server
import socketserver
import threading
import webbrowser

def start_server(port=8000):
    # Create the HTML file
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>Chess Game</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #2f3542;
        }
        #chess-container {
            width: 95vh;
            height: 95vh;
        }
        #chess-container img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    </style>
    <script>
        function refreshBoard() {
            const img = document.getElementById('chess-board');
            const newImg = new Image();
            newImg.src = 'game.svg?' + new Date().getTime();
            newImg.onload = () => {
                img.src = newImg.src;
            };
        }
        setInterval(refreshBoard, 50);
    </script>
</head>
<body>
    <div id="chess-container">
        <img id="chess-board" src="game.svg" alt="Chess Board">
    </div>
</body>
</html>'''
    
    with open('chess.html', 'w') as f:
        f.write(html)
    
    # Start server in a separate thread
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}/chess.html')
    
    return httpd