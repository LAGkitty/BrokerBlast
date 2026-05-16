# BrokerBlast 🚀

### 🛑 Trust, Privacy & Transparency First
**If you do not trust this script, do not use it. Or better yet: look at the code yourself.** This tool requires your email credentials (via an App Password) to send emails on your behalf. Because your security matters, **BrokerBlast is 100% open-source, contains zero hidden tracking, uses absolutely zero third-party packages, and runs entirely on your local machine.** You can read every single line of Python code in `autoprivacy.py` in less than five minutes to verify exactly how your data is handled before entering a single character. If you are still uncomfortable, please do not download or use this software.

---

BrokerBlast is a lightweight, zero-dependency Python graphical user interface (GUI) application designed to automate personal data removal requests. It dispatches formal legal requests under the **GDPR Article 17 (Right to Be Forgotten)** framework directly to major corporate data broker networks, forcing them to scrub your phone number, name, and email from their systems.

## ✨ Features
* **Zero External Dependencies:** Built entirely on Python's native standard libraries (`tkinter`, `smtplib`, `threading`). You don't have to run any sketchy `pip install` commands.
* **Pre-Baked 2026 Database:** Contains active, verified privacy compliance email endpoints for major data compilers, with dead/retired corporate inboxes removed.
* **Multi-Threaded Execution:** The email handshake loop runs on a background thread. The user interface will never freeze or crash while sending messages.
* **Input Masking:** The Google App Password field automatically hides your input characters to ensure no accidental leaks occur during screen shares or video recordings.

## 📦 What the App Looks Like
The application is split into two clean tabs:
1. **Automation Tool:** Where you input your configuration details, target data to delete, and view a live-updating console log of your outbound requests.
2. **How to Use:** A complete, un-scrollable walkthrough guide embedded right into the software so users don't have to keep flipping back to GitHub.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/LAGkitty/BrokerBlast.git
cd BrokerBlast
