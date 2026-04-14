# AI Resume Analyzer / Job-Role Predictor(Flask)

A simple web app that analyzes resume text and suggests suitable job roles.

Uses NLP-based keyword extraction and intelligent rule-based scoring to analyze resumes.


## Features

- Paste resume text into a web form
- Extracts relevant technical skills from resume content
- Recommends best-fit roles:
  - Data Scientist
  - Web Developer
  - Data Analyst
- Calculates role-wise match score percentage
- Suggests missing skills to improve resume strength
- Shows all results on the same page

## Tech Stack

- Python
- Flask
- HTML + CSS (Jinja template)

## Project Structure

- app.py: Flask backend with skill extraction and scoring logic
- templates/index.html: Frontend form and result rendering


**Screenshots**

<img width="1200" height="813" alt="Screenshot 2026-04-14 213028" src="https://github.com/user-attachments/assets/878b4f96-2c89-4a53-a081-891a961514e1" />
<img width="1187" height="881" alt="Screenshot 2026-04-14 213058" src="https://github.com/user-attachments/assets/8b4172e7-0a45-4c28-ae25-67807c59551d" />

## Run Locally

1. Open terminal in the project folder.
2. Activate virtual environment (if not already active).
3. Run the app:

```powershell
python app.py
```

If `python` is not recognized, use:

```powershell
c:/Users/kanmani dhaya/OneDrive/Documents/AI Resume analyzer/.venv/Scripts/python.exe app.py
```

4. Open in browser:

- http://127.0.0.1:5000

## Notes

- This app uses lightweight logic (no heavy ML model), making it fast and easy to extend.
- You can add more skills and role profiles in app.py to improve recommendations.
