# Giftaway API

FastAPI backend for the E-Gift prototype.

## Setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your SMTP credentials
```

### Install mail dependencies (if adding to an existing venv)

```powershell
pip install fastapi-mail pydantic-settings
```

## Run (port 8000)

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/brands` | List premium brands |
| POST | `/api/checkout` | Checkout + queue voucher email |

Interactive docs: http://localhost:8000/docs

### Checkout request body

```json
{
  "brand": { "id": "apple", "name": "Apple" },
  "giftAmount": 50,
  "recipientName": "Alex",
  "recipientEmail": "alex@example.com",
  "senderName": "Jordan",
  "personalMessage": "Happy birthday!",
  "themeColor": "#6d28d9"
}
```

### Checkout response

```json
{
  "success": true,
  "orderId": "ORD-ABC123",
  "giftCode": "A1B2C3D4",
  "message": "Gift card for Alex (Apple, $50.00) is confirmed.",
  "emailQueued": true
}
```

Emails are sent in the background via `BackgroundTasks` so the API responds immediately.
