# 📞 ARB SoftTech AI Calling Agent — Step-by-Step Beginner Setup Guide

Yeh guide ekdum **basic aur step-wise** banayi gayi hai taaki koi bhi client ya naya user apne laptop/PC par is platform ko **Step 1 se Step 14 tak** aasaani se setup aur run kar sake.

---

## 📋 Quick Setup Roadmap (Overview)

1. **Phase 1**: Required Software Install Karna (Git, Python, Node.js, Ngrok, Docker)
2. **Phase 2**: GitHub se Project Download (Clone) Karna
3. **Phase 3**: API Keys aur `.env` File Setup Karna
4. **Phase 4**: Packages Install Karna (Backend & Frontend)
5. **Phase 5**: 1-Click Launch (`start_all.bat`)
6. **Phase 6**: Live Phone Call Test Karna

---

# 🟢 PHASE 1: Software Requirements (Pehle Yeh Install Karein)

Apne computer mein pehle yeh **4 zaroori software** install karein:

### Step 1: Git Install Karein
1. [Git for Windows Download Page](https://git-scm.com/download/win) par jayein.
2. **"Click here to download"** par click karein aur setup file download karein.
3. Setup open karein aur sabhi options par default **Next ➔ Next ➔ Install** click karein.

---

### Step 2: Python Install Karein (Important Step ⚠️)
1. [Python 3.12 Download Page](https://www.python.org/downloads/) par jayein aur **"Download Python 3.12.x"** par click karein.
2. Installer open karein.
3. > [!CRITICAL]
   > Installer ki **sabse pehli screen** par sabse niche ek checkbox hoga:  
   > ☑️ **"Add python.exe to PATH"**  
   > **Is box ko TICK karna zaroori hai!** Phir **Install Now** par click karein.

---

### Step 3: Node.js Install Karein
1. [Node.js Official Website](https://nodejs.org/) par jayein.
2. **"LTS (Recommended for Most Users)"** wale green button par click karke download karein.
3. Download hone ke baad setup file run karein aur **Next ➔ Next ➔ Install** karein.

---

### Step 4: Ngrok Install Karein (Telephony Webhooks ke liye)
VoBiz carrier se live phone call aane ke liye Ngrok public tunnel chahiye hota hai:
1. [ngrok.com](https://ngrok.com/download) par jayein aur Windows version download karein.
2. Zip file ko extract karke `ngrok.exe` ko kisi folder mein rakh dein (ya Windows PATH mein add karein).
3. [ngrok.com](https://dashboard.ngrok.com/signup) par free sign-up karein.
4. Dashboard se apna **AuthToken** copy karein aur Command Prompt (CMD) mein yeh command chalayein:
   ```bash
   ngrok config add-authtoken <AAPKA_NGROK_AUTHTOKEN>
   ```

---

### Step 5 (Optional): Docker Desktop Install Karein
*Note: Agar aap 1-Click Native Mode chala rahe hain toh Docker ki bilkul zaroorat nahi hai. Docker sirf tab chahiye jab aap MinIO S3 aur PostgreSQL container mein chalana chahein.*
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) se download karein.
2. Setup chalayein aur **"Use WSL 2 instead of Hyper-V"** par tick rehne dein.
3. Install hone ke baad **PC restart** karein.
4. Agar WSL error aaye toh PowerShell (Admin) mein chalayein:
   ```powershell
   wsl --update
   wsl --set-default-version 2
   ```

---

# 🔵 PHASE 2: GitHub Se Project Download Karna

### Step 6: Code Clone Karein
1. Apne laptop mein **Command Prompt (CMD)** ya **PowerShell** kholein.
2. Jahan project rakhna hai wahan jayein (jaise Desktop ya C:\Projects):
   ```bash
   cd C:\Projects
   ```
3. GitHub se repository clone karein:
   ```bash
   git clone https://github.com/Qaanit-Khan/calling-agent-platform.git
   ```
4. Project folder ke andar enter karein:
   ```bash
   cd calling-agent-platform
   ```

---

# 🟡 PHASE 3: Configuration & API Keys (`.env` Setup)

Project mein do `.env` files banani hoti hain: ek Backend ke liye aur ek Frontend ke liye.

### Step 7: Backend `.env` File Banayein
Terminal mein yeh command chalayein:
```bash
cd backend
copy .env.example .env
```

### Step 8: Backend `.env` File Mein Keys Dalein
`backend/.env` file ko Notepad ya VS Code mein open karein aur yeh main details fill karein:

```ini
# 1. Server aur Ngrok URL
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8001
ENVIRONMENT=development
# Ngrok start karne par jo https://xxxx.ngrok-free.dev milta hai, wo yahan dalein:
BACKEND_PUBLIC_URL=https://your-ngrok-subdomain.ngrok-free.dev

# 2. Database (Zero configuration SQLite — koi setup nahi chahiye)
DATABASE_URL=sqlite+aiosqlite:///./calling_agent.db

# 3. Sarvam AI Credentials (Voice STT / TTS)
VOICE_ENGINE=sarvam
ACTIVE_MODEL_MODE=sarvam
SARVAM_API_KEY=sk_your_sarvam_api_key_here
SARVAM_DEFAULT_VOICE=shubh
SARVAM_TTS_MODEL=bulbul:v3
SARVAM_STT_MODEL=saaras:v3
SARVAM_LLM_MODEL=sarvam-105b-conversations

# 4. Google Gemini API Key (Transcript Lead Intelligence)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# 5. VoBiz Carrier Telephony Credentials
VOBIZ_AUTH_ID=your_vobiz_auth_id
VOBIZ_AUTH_TOKEN=your_vobiz_auth_token
VOBIZ_FROM_NUMBER=+91XXXXXXXXXX
```

### Step 9: Frontend `.env` File Banayein
Terminal mein yeh command chalayein:
```bash
cd ../frontend_1
copy .env.example .env
```
*(Isme pehle se `VITE_API_BASE_URL=http://localhost:8001` likha hoga, isko waise hi rehne dein).*

---

# 🟣 PHASE 4: Packages & Dependencies Install Karna

### Step 10: Backend Python Environment & Packages Setup
Terminal mein Backend folder mein jayein:
```bash
cd ../backend

# 1. Virtual Environment banayein
python -m venv .venv

# 2. Virtual Environment activate karein (Windows CMD mein):
.\.venv\Scripts\activate.bat
# (Agar PowerShell use kar rahe hain toh: .\.venv\Scripts\Activate.ps1)

# 3. Python packages install karein (FastAPI, SQLAlchemy, Sarvam SDK, etc.)
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 11: Frontend Node Packages Setup
Ab Frontend folder mein jayein aur packages install karein:
```bash
cd ../frontend_1

# React aur UI dependencies install karein
npm install
```

---

# 🟠 PHASE 5: Project Start Karna (1-Click Run)

### Step 12: `start_all.bat` Run Karein (Sabse Aasan Tarika)

1. Project ke main root folder (`calling-agent-platform`) mein jayein.
2. Wahan **`start_all.bat`** file par double-click karein!
3. Yeh script automatically:
   - **Backend** start karega Port `8001` par.
   - **Frontend** start karega Port `5173` par.
   - **Ngrok Tunnel** launch karega Port `8001` ke liye.
4. Apne browser mein yeh link kholein:  
   👉 **`http://localhost:5173`**

---

### *Alternative: Agar Docker mein chalana ho (Docker Stack Mode)*
Agar aap containers use karna chahte hain:
1. Docker Desktop open karein.
2. Root directory mein command chalayein:
   ```bash
   docker compose up -d --build
   ```
3. Dashboard: `http://localhost:5174` | Backend: `http://localhost:8001`

---

# 🔴 PHASE 6: Testing & Live Calling (Aise Check Karein)

Sab kuch chalne ke baad yeh **3 checks** karein:

### Step 13: Settings Page Verify Karein
1. Browser mein jayein: `http://localhost:5173/settings`
2. **Sarvam AI Tab**: **"Test Connection"** par click karein ➔ **`CONNECTED`** (Green) aana chahiye.
3. **VoBiz Telephony Tab**: Check karein Auth ID aur Caller ID saved hain.
4. **Transcript API Tab**: **"Test Live Connection"** par click karein ➔ Google Gemini verified ho jayega (`CONNECTED (xx ms)`).

### Step 14: Live Outbound Call Lagayein
1. Dashboard ke left menu mein **"AI Agents"** par click karein.
2. Kisi bhi agent (e.g. *Customer Support Agent*) par click karein.
3. **"Call Now"** ya **Quick Dial** button dabayein aur apna 10-digit mobile number dalein (`+91XXXXXXXXXX`).
4. **"Call Now"** click karein.
5. **Aapke phone par call aayegi!** Phone uthaiye aur Hindi ya English mein baat karein.
6. Call disconnect hone ke baad **"Calls History"** mein jayein:
   - Wahan aapko **Customer aur AI Agent dono ka live transcript** dikhega.
   - Audio Player mein **100% original call recording** sun sakte hain.
   - AI interest analysis (Interested / Callback / Not Interested) check karein.

---

## 🛠️ Common Errors & Quick Fixes (FAQ)

### 1. `python` command recognize nahi ho rahi?
> **Karan**: Python install karte waqt "Add python.exe to PATH" tick nahi kiya gaya tha.  
> **Solution**: Python installer dobara run karein, **Modify** par click karein aur PATH checkbox tick karein.

### 2. `ExecutionPolicy` error in PowerShell when activating venv?
> **Solution**: PowerShell ko "Run as Administrator" kholein aur yeh command chalayein:
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Google Gemini API key quota khatam ho gaya?
> **Solution**: Server ya code chhedne ki zaroorat nahi hai!  
> 1. [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) se free mein nayi key generate karein.  
> 2. `http://localhost:5173/settings?tab=transcript` par paste karke **Save & Update Key** click karein. Yeh bina restart kiye turant live apply ho jayegi.

### 4. Phone par aawaz nahi aa rahi ya call drop ho gayi?
> **Solution**: Check karein ki Ngrok chal raha hai aur `backend/.env` mein `BACKEND_PUBLIC_URL` ka link wahi hai jo Ngrok terminal window mein dikh raha hai (e.g. `https://xxxx.ngrok-free.dev`).

---

## 📞 Support & Handover Note
Platform successfully verified and tested for enterprise production deployment. Sabhi source codes, models, aur real-time audio pipeline scripts configured hain.
