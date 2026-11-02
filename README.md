# EduGenie

EduGenie is a desktop study assistant built with Python and Tkinter. It uses the Google Gemini API to create notes, summarize academic material, explain concepts, and generate study material.

## Features

- Generate structured academic notes
- Summarize academic content
- Explain concepts with simple examples
- Create definitions, key concepts, and revision points
- Run Gemini requests in a background thread so the interface remains responsive
- Display clear messages for quota, server, timeout, and configuration errors

## Requirements

- Windows
- Python 3.10 or newer
- A Google Gemini API key
- Internet access

## Installation

1. Clone or download this project.

2. Open a terminal in the project directory:

   ```powershell
   cd C:\Users\User\Downloads\EduGenie
   ```

3. Create and activate a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Gemini API Configuration

Create a `.env` file in the project directory if it does not already exist.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` or share your API key publicly. If a key has been exposed, revoke it in Google AI Studio and create a new key.

## Run the Application

```powershell
python app.py
```

If the virtual environment is already active, `python app.py` is sufficient. Alternatively, run it directly with the virtual environment interpreter:

```powershell
.\venv\Scripts\python.exe app.py
```

## How to Use

1. Choose one of the available tasks:
   - Generate Notes
   - Summarize Content
   - Explain a Concept
   - Generate Study Material
2. Enter your academic source material or topic in the input box.
3. Select **Generate Content**.
4. Review the generated content in the output box.
5. Select **Clear** to empty both text areas.

## API Limits and Errors

The Gemini free tier can impose daily and rate limits. If generation returns `429 RESOURCE_EXHAUSTED`, the daily quota may be exhausted or billing may need to be configured for the Google AI project.

Temporary `503` and `504` responses indicate high provider demand or a timeout. The application retries eligible transient failures, but requests may still fail when the provider or quota is unavailable.
