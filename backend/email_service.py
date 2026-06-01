import html
import logging
import os
import resend

logger = logging.getLogger(__name__)

# Grab the API key from Render's environment variables
resend.api_key = os.environ.get("RESEND_API_KEY")

def build_voucher_html(
    *,
    recipient_name: str,
    sender_name: str,
    brand_name: str,
    gift_amount: float,
    gift_code: str,
    personal_message: str,
    theme_color: str,
) -> str:
    safe_message = html.escape(personal_message)
    safe_recipient = html.escape(recipient_name)
    safe_sender = html.escape(sender_name)
    safe_brand = html.escape(brand_name)

    message_block = (
        f'<p style="margin:0;font-size:16px;line-height:1.6;color:#374151;">{safe_message}</p>'
        if personal_message.strip()
        else '<p style="margin:0;font-size:15px;line-height:1.6;color:#9ca3af;font-style:italic;">'
        "No message was included — but the gift speaks for itself."
        "</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Your Giftaway</title>
</head>
<body style="margin:0;padding:0;background:#f4f3f0;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f4f3f0;padding:32px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0"
               style="max-width:520px;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(15,15,18,0.12);">
          <tr>
            <td style="height:8px;background:{theme_color};"></td>
          </tr>
          <tr>
            <td style="padding:32px 32px 24px;background:linear-gradient(135deg,{theme_color} 0%,color-mix(in srgb,{theme_color} 75%,#000) 100%);">
              <p style="margin:0 0 8px;font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:rgba(255,255,255,0.75);">
                Digital gift voucher
              </p>
              <h1 style="margin:0;font-size:28px;font-weight:700;color:#ffffff;">
                You&rsquo;ve received a gift!
              </h1>
              <p style="margin:12px 0 0;font-size:15px;color:rgba(255,255,255,0.9);">
                From <strong>{safe_sender}</strong> &middot; {safe_brand}
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:28px 32px;">
              <p style="margin:0 0 4px;font-size:13px;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;">
                Hello, {safe_recipient}
              </p>
              <p style="margin:0 0 24px;font-size:36px;font-weight:700;color:#0f0f12;">
                ${gift_amount:,.2f}
              </p>
              <div style="background:#f9fafb;border:1px dashed #e5e7eb;border-radius:14px;padding:20px;text-align:center;margin-bottom:24px;">
                <p style="margin:0 0 8px;font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:0.12em;">
                  Your gift code
                </p>
                <p style="margin:0;font-size:28px;font-weight:700;letter-spacing:0.15em;color:{theme_color};font-family:Consolas,Monaco,monospace;">
                  {gift_code}
                </p>
              </div>
              <div style="border-left:4px solid {theme_color};padding-left:16px;margin-bottom:24px;">
                {message_block}
              </div>
              <p style="margin:0;font-size:13px;line-height:1.5;color:#9ca3af;">
                Redeem this code at checkout on {safe_brand}. This voucher was sent via Giftaway.
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:20px 32px;background:#fafafa;border-top:1px solid #f3f4f6;text-align:center;">
              <p style="margin:0;font-size:12px;color:#9ca3af;">
                &copy; Giftaway &mdash; Premium digital gifting
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

async def send_gift_voucher_email(
    *,
    recipient_email: str,
    recipient_name: str,
    sender_name: str,
    brand_name: str,
    gift_amount: float,
    gift_code: str,
    personal_message: str,
    theme_color: str,
) -> None:
    html_content = build_voucher_html(
        recipient_name=recipient_name,
        sender_name=sender_name,
        brand_name=brand_name,
        gift_amount=gift_amount,
        gift_code=gift_code,
        personal_message=personal_message,
        theme_color=theme_color,
    )

    # Resend requires using their sandbox domain on the free tier
    sender = "onboarding@resend.dev"

    try:
        response = resend.Emails.send({
            "from": sender,
            "to": recipient_email, # Must be your verified GitHub/Resend email for this demo
            "subject": f"{sender_name} sent you a {brand_name} gift card",
            "html": html_content
        })
        logger.info("Gift voucher email sent via Resend for %s (code %s): %s", recipient_email, gift_code, response)
    except Exception as e:
        logger.error("Failed to send email via Resend: %s", e)