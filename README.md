# RED-BITB
An educational Browser-in-the-Browser (BitB) simulation tool and modular factory. It features an interactive script to compile custom HTML templates and a built-in lightweight server to log simulated credential telemetry for security research.

<img width="1280" height="720" alt="RED-BITB" src="https://github.com/user-attachments/assets/4e1bf4aa-d538-4edc-94c3-3252792b6373" />

The primary objective is to demonstrate how modern phishing techniques exploit visual trust indicators in browser environments, allowing defenders and security students to build effective technical mitigations.

## ⚠️ Strict Legal Disclaimer

**This tool is created strictly for educational, academic, and authorized research purposes.** 
- **Malicious Use is Prohibited:** Do not use this tool to harm, defraud, or target individuals without explicit, prior written authorization. 
- **Legal Consequences:** Unauthorized use of this software against systems you do not own or do not have explicit permission to test is **illegal and punishable by law**.
- **User Responsibility:** You are **solely responsible for your own actions**. The developer assumes absolutely no liability for misuse, damage, or legal consequences caused by this software. By downloading or using this tool, you agree to use it responsibly and within legal boundaries.

## 🚀 Features & Capabilities

- **Interactive Factory Script:** Compiles a Browser-in-the-Browser simulation through a step-by-step command-line wizard.
- **Modular Component Design:** Dynamically reads available browser styles (`header_*.html`) and login interfaces (`login_*.html`) from a clean components folder.
- **Native Logging Server:** A lightweight Python web server that hosts files and exposes a `/log` endpoint to capture JSON telemetry.
- **Isolated Local Logs:** Automatically logs captured test credentials into local, timestamped text files.

## 📁 Repository Structure

```text
RED-BITB/
├── .gitignore
├── LICENSE
├── README.md
├── RED-BITB-Server.py
└── Generator/
    ├── RED-BITB-Generator.py
    └── componenten/
        ├── core_css.html
        ├── core_js.html
        ├── database_headers.html
        ├── detection_engine.html
        ├── header_chrome.html
        ├── header_firefox.html
        └── login_google.html (etc.)
```

## 🛠️ Step-by-Step Usage Guide

Follow these exact sequential steps to safely generate and run the educational simulation.

### Step 1: Clone the Repository
Open your terminal and clone the project files:
```bash
git clone https://github.com/eMVee-NL/RED-BITB.git
cd RED-BITB
```

### Step 2: Compile your Template
Navigate to the `Generator` directory and run the compiler script:
```bash
cd Generator
python3 RED-BITB-Generator.py
```
* Follow the on-screen prompts to choose your targeted browser headers and login interface.
* Enter your listening server's IP address or domain when prompted (or press **Enter** to keep it local).
* The script will generate a deployment file named `index.html` inside the `Generator` folder.

### Step 3: Move the Template Manually
The server hosts files from its own working directory. **You must manually move your newly generated template file to the server folder.**
```bash
# Move the compiled index.html up to the root folder where the server resides
mv index.html ../
```

### Step 4: Launch the Listening Server
Navigate back to the root directory and start the listener script. 
* *Note: Because the server binds to standard HTTP Port 80, administrative privileges are required.*

```bash
cd ..

# On Linux / Kali / macOS:
sudo python3 RED-BITB-Server.py

# On Windows:
# Open your Command Prompt or PowerShell as Administrator and run:
python RED-BITB-Server.py
```

### Step 5: Observe the Results
1. Open a browser and visit `http://localhost`.
2. Input test data into your compiled simulation.
3. Observe the captured credentials print live in your server terminal.
4. Check the root folder for a newly created `.txt` file containing the timestamped capture log.

## 🛡️ Defensive Mitigations
To defend against real-world BitB attacks, enforce **Password Managers** (which refuse to auto-fill inside unauthorized frames), deploy **FIDO2/WebAuthn Hardware Security Keys**, and train users to drag popup windows outside the main browser viewport to verify if they are simulated.

## 📄 License
This project is licensed under the GNU General Public License v3.0. Any modifications or derivative works must also be open-sourced under the same license terms.
