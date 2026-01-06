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

### 2. Configuration
Create a `.env` file in the root directory and add your API key:
```env
GOOGLE_API_KEY=your_api_key_here
```

### 3. Running the Application

To run the full application, you need to start both the **Backend** and the **Frontend** servers in separate terminal windows.

#### ▶️ Start Backend (FastAPI)
```bash
# 1. Activate the environment
.\.venv\Scripts\activate

# 2. Run the server
python main.py
```
> The API will run at: **http://localhost:8000**

#### ▶️ Start Frontend (React)
```bash
# 1. Navigate to frontend folder
cd frontend

# 2. Install dependencies (first time only)
npm install

# 3. Start development server
npm run dev
```
> The Portal will be available at: **http://localhost:5173**

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
