# YMBC Smart Information Kiosk

A premium, responsive college information kiosk built with Python 3, Streamlit and custom CSS. It is frontend-only: there is no Flask, Django, PHP, SQL database or external backend.

## Run in PyCharm / PowerShell

1. Open this folder as a PyCharm project.
2. Create and activate a project-local virtual environment in PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run the remaining commands with the venv interpreter directly:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python -m streamlit run app.py
   ```

Using `python -m streamlit` makes sure Streamlit runs from the same Python environment where it was installed; it also avoids the common Windows error where `streamlit.exe` is not on PATH.

## Included interactions

- Sidebar navigation across all reference-inspired views.
- Global search hinting for major sections.
- Course filtering by level, department and keyword.
- Facility and programme detail selection.
- Admission tabs, FAQs and expandable answers.
- Visitor information tabs, hours and directions states.
- Contact form with inline validation and success feedback.
- Session-based assistant prompts and responses.
- Responsive layout and reduced-motion CSS support.

The visual language follows the supplied references: deep burgundy, warm gold accents, pale blue surfaces, rounded cards, soft shadows, hero banners, metric strips and a kiosk-style assistant.
