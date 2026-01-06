# BrCa AI Analysis Portal

An NLP-powered application designed for Breast Cancer doctors to visualize patient data, generate AI-driven clinical summaries, and interact with datasets through an intelligent Q&A interface.

## 🌟 Key Features

- **AI Case Summaries**: Automatic generation of clinical summaries for any selected patient using **Gemini 2.5 Flash**.
- **Interactive Q&A**: A chat interface that allows doctors to ask specific questions about a patient's medical history, tumor details, or surgery highlights.
- **Full Database Search**: Backend-powered search allows doctors to find any patient among more than 34,000 records instantly by Name or BCNo.
- **Automated Data Import**: CSV data is imported into a local SQLite database for high-performance querying and AI context retrieval.
- **Premium UI**: A sophisticated dark-mode, glassmorphism-based React interface with a **Collapsible Sidebar** to maximize workspace for analysis.
- **Quick Export**: Built-in **Copy to Clipboard** functionality for AI summaries, optimized for pasting into clinical reports or MS Word.

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python 3.9), SQLite, Google Generative AI API.
- **Frontend**: React (Vite), Framer Motion, Lucide Icons, React-Markdown.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ 
- Node.js 20+
- Google Gemini API Key
- [ngrok account](https://ngrok.com/) (for remote access)

### 2. Configuration
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here
```

### 3. Running the Application

#### 🏠 Local Access (Localhost)
To run the full application locally, you need to start both the **Backend** and the **Frontend** servers in separate terminal windows.

**Start Backend (FastAPI):**
```bash
.\.venv\Scripts\activate
python main.py
```
> API: **http://localhost:8000**

**Start Frontend (React):**
```bash
cd frontend
npm install
npm run dev
```
> Portal: **http://localhost:5173**

#### 🌐 Remote Access (via ngrok)
To expose the application to the internet, use the automated startup script:

```bash
python run_app_with_ngrok.py
```
This script will:
- Establish secure tunnels for both frontend and backend.
- Automatically link the frontend to the backend's public URL.
- Provide you with a public URL (e.g., `https://xxxx.ngrok-free.app`) to share.

---

> [!TIP]
> **Database Initialization**: If you need to re-import the clinical CSV data into your database, run `python init_db.py` from the root folder.


Starting MCP server with: ...\.venv\Scripts\python.exe ...\mcp_server.py
Initializing session...
Session initialized.
Listing tools...
Successfully connected to MCP Server!
Available tools: ['list_patients', 'get_patient_details', 'generate_summary', 'ask_patient_question']

Testing 'list_patients' tool...
Result content: [
  {
    "BCNo": "Z-1774",
    "PatientName": "ZAHIDA PARVEEN",
    ...
  }
]
