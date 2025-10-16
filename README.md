## HeyDay API (FastAPI)

### Prerequisites
- Python 3.10+
- Windows PowerShell

### Setup (Windows)
1. Clone/open this folder in your IDE.
2. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
3. Install dependencies (without activating venv):
   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
4. Create your `.env` from the example:
   ```powershell
   Copy-Item .env.example .env
   ```
5. Run the API:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Open http://localhost:8000/docs to try the endpoints.

### Project Structure
```
app/
  api/
    routes/
  core/
  db/
    models/
    schemas/
    crud/
  services/
```

### Environment Variables
See `.env.example` for keys (DB, OpenAI, Twilio, SendGrid).

### Deploy: Neon + Railway + Vercel

1) Create Neon Postgres
- Create a Neon project and a database
- Get the connection string in the format:
  `postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require`

2) Deploy API on Railway
- Create a new Railway project and select "Deploy from GitHub" or upload
- Add environment variables:
  - `DATABASE_URL` = your Neon URL
  - `OPENAI_API_KEY` = (optional)
  - `ALLOWED_ORIGINS` = your Vercel domain (e.g. https://heyday-yourname.vercel.app)
- Ensure `Procfile` exists (web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000})
- Deploy; note your Railway domain, e.g. https://your-app.up.railway.app

3) Deploy frontend on Vercel
- In `frontend/vercel.json`, replace `YOUR-RAILWAY-APP` with your Railway subdomain
- Deploy the `frontend` directory as a Vercel project
- Vercel will serve `index.html` and proxy `/api/*` to Railway

4) Verify
- Open your Vercel URL and click "Check" under API Health
- Use the form to create a customer; confirm in Swagger at Railway `/docs`

