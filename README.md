# Syllabi2Calendar

**Turn any syllabus PDF into Google Calendar events in seconds—no more manual copy-paste.**

A full-stack AI application that extracts assignments, quizzes, and exams from syllabus PDFs and pushes them to your Google Calendar. Built for students who want to spend less time data-entry and more time studying.

---

## Key Features

- **AI-powered extraction** — Gemini parses your syllabus and identifies assignments, quizzes, and exams with dates and descriptions.
- **Automatic timezone detection** — Infers the university’s IANA timezone (e.g. America/New_York) so events show at the right local time.
- **Review & Edit** — Inspect and edit extracted events in a table before pushing; fix mistakes or remove entries you don’t want.
- **Google OAuth2** — Native integration with Google Calendar API; one-time OAuth flow, then events go straight to your primary calendar.

---

## Architecture

Data flows through the stack as follows:

```
PDF upload → PyMuPDF4LLM (PDF → Markdown) → Gemini (Markdown → JSON) → Review UI → Google Calendar API
```

| Stage | What happens |
|-------|----------------------|
| **PDF** | User uploads a syllabus PDF in the frontend. |
| **Markdown** | Backend uses PyMuPDF4LLM to convert the PDF to structured markdown. |
| **Gemini** | AI extracts a JSON list of events (summary, start, end, description) and a timezone. |
| **Review** | Frontend shows a table; user can edit or delete rows. |
| **Calendar** | Backend calls Google Calendar API to create events (timed or all-day). |

---

## Tech Stack

| Layer | Stack |
|-------|--------|
| **Backend** | FastAPI (Python), Gemini (AI), Google Calendar API, PyMuPDF4LLM |
| **Frontend** | Next.js (React), Tailwind CSS, Framer Motion, Axios, Lucide React |

The UI is a dark-themed, responsive single-page flow: dropzone → processing steps → review table → success card with “Open Google Calendar” and “Clear & Start Over.”

---

## Installation

### Backend setup

1. **Clone and enter the repo**
   ```bash
   cd Syllabi2Calendar
   ```

2. **Create and activate a virtual environment (Windows PowerShell)**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   If execution policy blocks the script: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (once), then retry.

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**  
   In the repo root, create `.env` (and optionally `.env.local` for local overrides). See [Environment variables](#environment-variables) below.

### Frontend setup

1. **Enter the frontend directory and install**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the dev server**
   ```bash
   npm run dev
   ```
   Frontend runs at `http://localhost:3000` by default.

### Google Cloud setup

To use the “Push to Google Calendar” flow:

1. In [Google Cloud Console](https://console.cloud.google.com/), create or select a project and enable the **Google Calendar API**.
2. Create **OAuth 2.0 credentials** (Desktop app or Web application, depending on your setup).
3. Download the client secrets and save as `credentials.json` in the **backend repo root** (same folder as `main.py`).
4. On first run, the backend will open a browser for Google sign-in and then write `token.json` for reuse.

---

## Environment variables

Example structure for the backend (repo root):

```env
# Required for AI extraction (Gemini)
GEMINI_API_KEY=your_gemini_api_key_here
```

- Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
- `credentials.json` is not an env var—place the file in the backend root as described above.

---

## Running the app

1. **Start the backend** (from repo root with `venv` activated):
   ```bash
   uvicorn main:app --reload
   ```
   API: `http://localhost:8000` — docs at `http://localhost:8000/docs`.

2. **Start the frontend** (from `frontend/`):
   ```bash
   npm run dev
   ```

3. Open `http://localhost:3000`, upload a syllabus PDF, review the extracted events, then push to Google Calendar.

---

## Contribution & License

Contributions are welcome: open an issue or submit a PR. This project is licensed under the **MIT License**.

---

## Future roadmap

- **Canvas / Blackboard API** — Pull assignments and due dates directly from LMS APIs.
- **Multi-syllabus batch upload** — Process several PDFs in one run and merge into one calendar view.
- **SMS / Email reminders** — Optional notifications for upcoming deadlines.
