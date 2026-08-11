import os, http.server, socketserver, sys, traceback
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("_site")
PORT = 8899
try:
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), http.server.SimpleHTTPRequestHandler)
    print("Serving at port", PORT, flush=True)
    httpd.serve_forever()
except Exception:
    traceback.print_exc(file=sys.stderr)
