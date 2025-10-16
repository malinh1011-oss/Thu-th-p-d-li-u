# GIS Data Viewer - Streamlit (Deploy Instructions)

This repository contains a simple Streamlit app to view and filter an Excel workbook.
Files included:
- GIS_collector_web.py         (Streamlit app)
- Biểu mẫu dữ liệu hạ thế GIS_TBA_ĐZ.xlsx   (example Excel file)
- GIS_collector_README.txt    (local usage instructions)

## Quick local test
1. Install dependencies:
   ```bash
   pip install streamlit pandas openpyxl
   ```
2. Run locally:
   ```bash
   streamlit run GIS_collector_web.py
   ```
3. Open the URL shown in your terminal (usually http://localhost:8501).

## Deploy to Streamlit Cloud (free)
1. Create a GitHub account if you don't have one.
2. Create a new GitHub repository (public or private).
3. Upload the files in this zip to the repository root:
   - GIS_collector_web.py
   - Biểu mẫu dữ liệu hạ thế GIS_TBA_ĐZ.xlsx (optional sample)
   - GIS_collector_README.txt
4. Go to https://share.streamlit.io/ and sign in with your GitHub account.
5. Click **New app** → choose your repository, branch (usually main), and the file path `GIS_collector_web.py` → **Deploy**.
6. After a short build, you will receive a public URL for your app. Open it and test uploading/selecting your workbook.

## Notes
- If your Excel file is large, consider removing the sample file from the repo and upload it via the app or use cloud storage.
- For private data, keep the repository private and restrict access on Streamlit Cloud accordingly.
- If you want automatic saving back to the server-side Excel file, you must host the app on a machine that has read/write access to that file path (not possible on Streamlit Cloud unless you use external storage).

If you want, I can prepare the GitHub repo structure for you (zipped here) so you can upload it directly to GitHub.
