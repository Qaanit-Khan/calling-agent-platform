# <div align="center">📞 ARB SoftTech — Autonomous AI Calling Agent Platform</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Sarvam AI](https://img.shields.io/badge/Sarvam_AI-Indic_Voice-FF6B00?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-Intelligence-4285F4?style=for-the-badge&logo=google&logoColor=white)
![VoBiz](https://img.shields.io/badge/VoBiz-PSTN_Telephony-FF4500?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Enterprise-Ready Autonomous Voice Calling & Lead Intelligence Platform**  
*Real-Time Natural Indic Voice AI • Sub-Second Latency • Authentic 2-Way Recording • Zero-Disk Buffer*

[⚡ Quick Start](#-quick-setup-roadmap) • [📥 Client Handover Guide](#-stage-1-repository-sharing--access) • [🐳 Docker Guide](#-stage-2-software-prerequisites-installation) • [🛠️ Troubleshooting](#-troubleshooting--common-errors)

</div>

---

## 🌟 Platform Highlights

> [!TIP]
> **What is ARB SoftTech Calling Agent?**  
> An autonomous outbound telephony agent that dials real phone numbers over PSTN networks, speaks fluent **Hindi, English & Indic dialects** with conversational barge-in interruption handling, records authentic 2-way audio, and extracts sales intelligence (Interested, Callback, Rejection) using Google Gemini.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   LIVE TELEPHONY ARCHITECTURE                                  │
│                                                                                                 │
│  📱 Customer Phone <───(PSTN)───> 📞 VoBiz Carrier <───(WebSocket 8kHz)───> ⚙️ FastAPI Engine  │
│                                                                                      │          │
│                                                                        ┌─────────────┴──────┐   │
│                                                                        │ In-Memory Buffer   │   │
│                                                                        │ (Zero Disk Lag)    │   │
│                                                                        └─────────────┬──────┘   │
│                                                                                      │          │
│          ┌──────────────────────┬──────────────────────┬─────────────────────────────┘          │
│          ▼                      ▼                      ▼                                        │
│  🎙️ Sarvam AI STT/TTS    🧠 Gemini Intelligence   🗄️ SQLite / PostgreSQL                        │
│   (Saaras v3 / Bulbul)     (Buyer Intent Scoring)   (calling_agent.db)                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Quick Setup Roadmap

```
Stage 1: Repository Access Share  ➔  Stage 2: Install 4 Tools (Git, Python, Node, Ngrok)
                 │                                        │
                 ▼                                        ▼
Stage 4: Backend Setup (.env)     ◀──  Stage 3: Git Clone to Client PC
                 │
                 ▼
Stage 5: Frontend Setup (npm)     ➔  Stage 6: Ngrok Tunnel (Port 8001)
                 │                                        │
                 ▼                                        ▼
Stage 7: 1-Click Launch (.bat)    ➔  Stage 8: Live Test Call & Dashboard Verification!
```

---

# 🚀 Complete Step-by-Step Client Handover Guide

Yeh guide ekdum **basic se (Step 1 se Step 14)** banayi gayi hai. Har step ke sath **Exact Folder**, **Terminal Command**, aur **Kya file kahan banegi** clearly likha hai.

---

## 🟢 STAGE 1: Repository Sharing & Access

Agar repository **Private** hai, toh pehle client ko GitHub repository ka access dena hoga:

1. Apne browser mein repository kholein:  
   👉 `https://github.com/Qaanit-Khan/calling-agent-platform`
2. Upar navigation tabs mein **Settings** par click karein.
3. Left-side menu mein **Collaborators** par click karein.
4. Green button **"Add people"** par click karein.
5. Client ka GitHub username ya email daal kar invite bhej dein.
6. Client apni email check karke **"Accept Invitation"** click karega.

---

## 💻 STAGE 2: Software Prerequisites Installation

Client ke PC par pehli baar setup karne ke liye yeh **4 core tools** install karne honge:

### Step 2.1: Git Install Karein
- **Download Link**: [git-scm.com/download/win](https://git-scm.com/download/win)
- **Kaise Install Karein**: Installer download karke double-click karein. Har screen par **Next ➔ Next ➔ Install** click karein.

---

### Step 2.2: Python 3.12 Install Karein (Critical Step ⚠️)
- **Download Link**: [python.org/downloads](https://www.python.org/downloads/)
- **Kaise Install Karein**:
  1. `python-3.12.x-amd64.exe` download karein aur launch karein.
  2. > [!CAUTION]
     > **MANDATORY CHECKBOX:** Installer ki **first screen par sabse niche**:  
     > ☑️ **"Add python.exe to PATH"**  
     > **Is box ko tick (check) ZAROOR karein!** Agar yeh tick nahi kiya toh terminal mein Python kaam nahi karega.
  3. **"Install Now"** par click karein aur wait karein.

---

### Step 2.3: Node.js (LTS Version) Install Karein
- **Download Link**: [nodejs.org](https://nodejs.org/)
- **Kaise Install Karein**: Green button **"LTS (Recommended)"** par click karein aur setup run karke **Next ➔ Next ➔ Install** karein.

---

### Step 2.4: Ngrok Install Karein (Carrier Webhooks ke liye)
- **Download Link**: [ngrok.com/download](https://ngrok.com/download)
- **Kaise Setup Karein**:
  1. Zip file download karke extract karein aur `ngrok.exe` ko `C:\Windows` folder mein daal dein.
  2. [ngrok.com/signup](https://dashboard.ngrok.com/signup) par free sign-up karein.
  3. Dashboard se apna AuthToken copy karein aur Command Prompt (CMD) mein chalayein:
     ```bash
     ngrok config add-authtoken <AAPKA_NGROK_AUTHTOKEN>
     ```

---

### Step 2.5 (Optional): Docker Desktop
> [!NOTE]
> Agar aap **1-Click Native Mode (`start_all.bat`)** chala rahe hain, toh **Docker ki zaroorat nahi hai**. Docker sirf tab chahiye jab aap MinIO S3 object storage ya PostgreSQL container mein run karna chahein.

1. Download from [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/).
2. Run installer, keep **"Use WSL 2 instead of Hyper-V"** checked.
3. Restart PC when prompted.
4. If WSL error occurs, open PowerShell as Administrator:
   ```powershell
   wsl --update
   wsl --set-default-version 2
   ```

---

## 📥 STAGE 3: Git Clone to Client PC

### Step 3.1: Command Prompt (CMD) Kholein
- Keyboard par `Win + R` dabayein, `cmd` likhein aur **Enter** dabayein.

### Step 3.2: Folder Banayein aur Clone Karein
```cmd
cd C:\
mkdir CallingAgent
cd CallingAgent
```
*(Ab aapka path hai: `C:\CallingAgent`)*

```cmd
git clone https://github.com/Qaanit-Khan/calling-agent-platform.git
cd calling-agent-platform
```
📍 **Location:** `C:\CallingAgent\calling-agent-platform`

---

## ⚙️ STAGE 4: Backend Setup (.env & Python Virtual Environment)

### Step 4.1: Backend Folder mein Jayein
```cmd
cd backend
```
📍 **Location:** `C:\CallingAgent\calling-agent-platform\backend`

### Step 4.2: Backend `.env` File Banayein
```cmd
copy .env.example .env
```
*(Screen par message aayega: `1 file(s) copied.`)*

### Step 4.3: `.env` File Configure Karein
```cmd
notepad .env
```
Notepad khulega. Yeh configuration check karein aur apni credentials dalein:

```ini
# ============================================================
# 1. Server aur Ngrok Webhook Settings
# ============================================================
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
ENVIRONMENT=development
# Ngrok start karne par jo https://xxxx.ngrok-free.dev milta hai, wo yahan dalein:
BACKEND_PUBLIC_URL=https://your-ngrok-subdomain.ngrok-free.dev

# ============================================================
# 2. Database (Zero-configuration SQLite — automatic banega)
# ============================================================
DATABASE_URL=sqlite+aiosqlite:///./calling_agent.db

# ============================================================
# 3. Sarvam AI Voice Engine Credentials
# ============================================================
VOICE_ENGINE=sarvam
ACTIVE_MODEL_MODE=sarvam
SARVAM_API_KEY=sk_your_sarvam_api_key_here
SARVAM_DEFAULT_VOICE=shubh
SARVAM_TTS_MODEL=bulbul:v3
SARVAM_STT_MODEL=saaras:v3
SARVAM_LLM_MODEL=sarvam-105b-conversations

# ============================================================
# 4. Google Gemini API Key (Transcript Intelligence)
# ============================================================
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# ============================================================
# 5. VoBiz Carrier Telephony Credentials
# ============================================================
VOBIZ_AUTH_ID=your_vobiz_auth_id
VOBIZ_AUTH_TOKEN=your_vobiz_auth_token
VOBIZ_FROM_NUMBER=+91XXXXXXXXXX
```
Keys daalne ke baad `Ctrl + S` dabakar save karein aur Notepad band kar dein.

### Step 4.4: Python Virtual Environment Banayein
```cmd
python -m venv .venv
```

### Step 4.5: Virtual Environment Activate Karein
```cmd
.\.venv\Scripts\activate.bat
```
*(Terminal prompt ke aage `(.venv)` likha hua dikhai dega).*

### Step 4.6: Python Dependencies Install Karein
```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🎨 STAGE 5: Frontend Setup (.env & npm packages)

### Step 5.1: Frontend Folder mein Jayein
```cmd
cd ..\frontend_1
```
📍 **Location:** `C:\CallingAgent\calling-agent-platform\frontend_1`

### Step 5.2: Frontend `.env` File Banayein
```cmd
copy .env.example .env
```
*(Is file mein pehle se `VITE_API_BASE_URL=http://localhost:8001` set hota hai).*

### Step 5.3: Node Modules Install Karein
```cmd
npm install
```

---

## 🌐 STAGE 6: Ngrok Tunnel Setup (Carrier Live Calling ke liye)

Carrier (VoBiz) ko live audio packets bhejne ke liye public HTTPS URL zaroori hota hai:

### Step 6.1: Nayi Terminal Window kholein aur Run Karein
```cmd
ngrok http 8001
```

### Step 6.2: Forwarding URL Copy Karein
Screen par aisi line dikhegi:
```text
Forwarding    https://xxxx-xxxx.ngrok-free.dev -> http://localhost:8001
```
Yeh `https://xxxx-xxxx.ngrok-free.dev` copy karein aur `backend/.env` file mein `BACKEND_PUBLIC_URL` ke aage paste kar dein.

---

## 🚀 STAGE 7: 1-Click Launch (Project Run Karna)

### Option A: 1-Click Native Mode (Recommended / Zero Docker)
1. File Explorer mein root folder kholein:  
   📍 `C:\CallingAgent\calling-agent-platform`
2. **`start_all.bat`** file par double-click karein!
3. Yeh automatically 3 windows launch karega:
   - 🟢 **FastAPI Backend**: `http://localhost:8001`
   - 🔵 **React Dashboard**: `http://localhost:5173`
   - 🟣 **Ngrok Tunnel**: Port 8001
4. Apne browser mein kholein: **`http://localhost:5173`**!

---

### Option B: Docker Stack Mode (Full Production)
Agar aap containerized services chalana chahte hain:
1. Docker Desktop launch karein.
2. Root directory mein chalayein:
   ```bash
   docker compose up -d --build
   ```
3. Dashboard: `http://localhost:5174` | Backend: `http://localhost:8001`

---

## 📱 STAGE 8: Live Testing & First Phone Call (Handover Verification)

### Step 8.1: Settings Verification
1. Dashboard mein left sidebar par **Settings** kholein (`http://localhost:5173/settings`).
2. **Sarvam AI Tab**: Click **"Test Connection"** ➔ Shows `CONNECTED` (Green).
3. **VoBiz Telephony Tab**: Verify Auth ID, Auth Token, and Caller ID.
4. **Transcript API Tab**: Click **"Test Live Connection"** ➔ Verifies Google Gemini connectivity (`CONNECTED (1200ms)`).

### Step 8.2: Outbound Call Lagayein
1. Sidebar mein **"AI Agents"** par click karein.
2. Kisi bhi Agent par click karke **"Quick Call / Dial"** dabayein.
3. Apna mobile number daalein (`+91XXXXXXXXXX`) aur **"Call Now"** dabayein.
4. **Aapka mobile phone ring hoga!**
5. Call answer karke Hindi/English mein baat karein.
6. Phone cut hone ke baad **"Calls History"** mein check karein:
   - 📝 **Live Multi-turn Transcript** (Caller & Agent dialogue).
   - 🔊 **Original 2-Way Audio Recording** (Embedded audio player).
   - 📊 **Lead Intelligence Qualification** (Interested / Callback / Rejected).

---

## 🛠️ Troubleshooting & Common Errors

| Issue | Cause | Quick 1-Click Solution |
| :--- | :--- | :--- |
| **`python` is not recognized** | Python was installed without checking "Add to PATH" | Re-run Python installer, choose **Modify**, and check **Add python.exe to PATH**. |
| **PowerShell script execution disabled** | Windows security policy blocks `activate.ps1` | Run PowerShell as Admin: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **Gemini API Key Quota Exhausted** | Free tier limit reached on Google AI Studio | Open `http://localhost:5173/settings?tab=transcript`, paste new key from [aistudio.google.com](https://aistudio.google.com/app/apikey), click **Save (Real-Time)**. |
| **Phone call drops / Silent call** | Ngrok URL in `backend/.env` is outdated | Re-copy current `https://xxxx.ngrok-free.dev` from ngrok window and update `BACKEND_PUBLIC_URL`. |
| **Port 8001 already in use** | A previous instance is still running | Run in CMD: `netstat -ano \| findstr :8001` then `taskkill /PID <PID> /F` |

---

## 📄 License & Intellectual Property
Developed and optimized for **ARB SoftTech AI Calling Agent System**. 100% proprietary code, models, and real-time audio pipeline scripts configured for direct enterprise deployment.
