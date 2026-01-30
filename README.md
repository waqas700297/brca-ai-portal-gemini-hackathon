# BrCa AI Analysis Portal

An NLP-powered application designed for Breast Cancer doctors to visualize patient data, generate AI-driven clinical summaries, and interact with datasets through an intelligent Q&A interface.

## 🌟 Key Features

- **AI Case Summaries**: Automatic generation of clinical summaries for any selected patient using **Gemini 3.0 Models**.
- **Interactive Q&A**: A chat interface that allows doctors to ask specific questions about a patient's medical history, tumor details, or surgery highlights.
- **Full Database Search**: Backend-powered search allows doctors to find any patient instantly by Name or BCNo.
- **Automated Data Import**: CSV data is imported into a local SQLite database for high-performance querying and AI context retrieval.
- **Premium UI**: A sophisticated dark-mode, glassmorphism-based React interface with a **Collapsible Sidebar** to maximize workspace for analysis.
- **Professional Reporting**: Export AI-generated summaries and Q&A interactions to **MS Word** documents. These exports employ smart formatting to preserve headers, lists, and bold text, ensuring the output is ready for clinical reports.
- **Quick Actions**: One-click **Copy to Clipboard** for text re-use.

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python 3.9), SQLite, Google Generative AI API.
- **Frontend**: React (Vite), Framer Motion, Lucide Icons, React-Markdown.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ 
- Node.js 20+
- Google Gemini API Key

### 2. Running the Application

#### 🏠 Local Access (Localhost)

#### 1. Backend Setup (Termimal 1)

Navigate to the project root directory and follow these steps:

1. **Create and Activate Virtual Environment**:
   ```powershell
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend Server**:
   ```bash
   python main.py
   ```
   > The backend will start on `http://localhost:8000`.

#### 2. Frontend Setup (Terminal 2)

Open a new terminal window, navigate to the `frontend` folder, and follow these steps:

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   ```bash
   npm run dev
   ```
   > The frontend will usually start on `http://localhost:5173` (check the terminal output for the exact URL).



