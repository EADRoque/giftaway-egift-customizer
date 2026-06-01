import logging
import uuid
from typing import Any

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from config import get_mail_settings, mail_is_configured
from email_service import send_gift_voucher_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if mail_is_configured():
    logger.info("SMTP configured for %s", get_mail_settings()["mail_from"])
else:
    logger.warning(
        "SMTP not configured. Add MAIL_USERNAME, MAIL_PASSWORD, and MAIL_FROM to backend/.env"
    )

app = FastAPI(title="Giftaway API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://giftaway-egift-customizer.vercel.app",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_BRANDS: list[dict[str, Any]] = [
    {
        "id": "nordstrom",
        "name": "Nordstrom",
        "logoUrl": "https://placehold.co/120x48/1a1a2e/ffffff?text=Nordstrom",
    },
    {
        "id": "apple",
        "name": "Apple",
        "logoUrl": "https://placehold.co/120x48/000000/ffffff?text=Apple",
    },
    {
        "id": "starbucks",
        "name": "Starbucks",
        "logoUrl": "https://placehold.co/120x48/00704a/ffffff?text=Starbucks",
    },
    {
        "id": "amazon",
        "name": "Amazon",
        "logoUrl": "https://placehold.co/120x48/ff9900/131921?text=Amazon",
    },
    {
        "id": "sephora",
        "name": "Sephora",
        "logoUrl": "https://placehold.co/120x48/000000/ffffff?text=Sephora",
    },
]


class BrandPayload(BaseModel):
    id: str
    name: str


class CheckoutRequest(BaseModel):
    brand: BrandPayload
    giftAmount: float = Field(..., gt=0, description="Gift card amount in USD")
    recipientName: str = Field(..., min_length=1, max_length=100)
    recipientEmail: EmailStr
    senderName: str = Field(..., min_length=1, max_length=100)
    personalMessage: str = Field(default="", max_length=500)
    themeColor: str = Field(
        ...,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Hex color used in the voucher email banner",
    )


class CheckoutResponse(BaseModel):
    success: bool
    orderId: str
    giftCode: str
    message: str
    emailQueued: bool


def generate_gift_code() -> str:
    return uuid.uuid4().hex[:8].upper()


async def _dispatch_gift_email(payload: CheckoutRequest, gift_code: str) -> None:
    try:
        await send_gift_voucher_email(
            recipient_email=str(payload.recipientEmail),
            recipient_name=payload.recipientName,
            sender_name=payload.senderName,
            brand_name=payload.brand.name,
            gift_amount=payload.giftAmount,
            gift_code=gift_code,
            personal_message=payload.personalMessage,
            theme_color=payload.themeColor,
        )
    except Exception:
        logger.exception("Failed to send gift email to %s", payload.recipientEmail)


@app.get("/api/brands")
def get_brands() -> list[dict[str, Any]]:
    return MOCK_BRANDS


@app.post("/api/checkout", response_model=CheckoutResponse)
async def checkout(
    payload: CheckoutRequest,
    background_tasks: BackgroundTasks,
) -> CheckoutResponse:
    order_id = f"ORD-{uuid.uuid4().hex[:12].upper()}"
    gift_code = generate_gift_code()
    email_queued = False

    if mail_is_configured():
        background_tasks.add_task(_dispatch_gift_email, payload, gift_code)
        email_queued = True
    else:
        logger.warning(
            "SMTP not configured (MAIL_USERNAME / MAIL_PASSWORD / MAIL_FROM). "
            "Skipping voucher email for order %s.",
            order_id,
        )

    return CheckoutResponse(
        success=True,
        orderId=order_id,
        giftCode=gift_code,
        emailQueued=email_queued,
        message=(
            f"Gift card for {payload.recipientName} "
            f"({payload.brand.name}, ${payload.giftAmount:.2f}) is confirmed."
        ),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
