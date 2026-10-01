# Smart Retail

Full-stack prototype for counterparty checks and protected B2B escrow deals.

## Run the API

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
Set-Location backend
uvicorn main:app --reload --port 8000
```

Add a valid `DADATA_API_KEY` to `.env` to query DaData. Use `PARTY_PROVIDER=fns` or `PAYMENT_PROVIDER=yookassa` only after those integrations are implemented; the stubs deliberately return `501`.

## Run the web app

Requires Node.js 20+ (it was not installed in the supplied environment).

```powershell
Set-Location frontend
npm install
npm run dev
```

The browser app runs at `http://localhost:5173` and calls `http://localhost:8000` by default. To change this, set `VITE_API_URL` in `frontend/.env`.
