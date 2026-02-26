# Simple Python HIDS (Host-based Intrusion Detection System) 🛡️

A lightweight and efficient Host-based Intrusion Detection System built with Python. This tool monitors critical files in a specific directory and alerts the user in real-time if any file is modified, deleted, or created, helping to detect unauthorized access or malware activity (like Ransomware).

## 🚀 Features
* **SHA-256 Hashing:** Creates a secure cryptographic baseline of your files.
* **Real-time Monitoring:** Continuously scans the directory for changes.
* **Alert System:** Immediately detects and logs if a file's integrity is compromised.

## 🛠️ How it Works
1. **Baseline Creation:** The script reads all files in the target directory and calculates their SHA-256 hash, saving this "safe state" in a `baseline.json` file.
2. **Continuous Monitoring:** The script enters an infinite loop, constantly comparing the current hashes of the files against the saved baseline.
3. **Detection:** Any mismatch triggers an immediate alert.

## 💻 How to Run

1. Clone this repository or download the `monitor.py` file.
2. Ensure you have Python 3 installed.
3. Run the script in your terminal: 'python3 monitor.py'
4. Choose option A to create the initial baseline.
5. Choose option B to start the real-time monitoring.

## 🎓 About
Project developed as a practical exercise in cybersecurity, file integrity monitoring, and Python automation.
