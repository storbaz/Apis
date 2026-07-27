import resend
from app.config import settings

resend.api_key = settings.RESEND_API_KEY


def send_welcome_email(to: str, name: str):
    if not settings.RESEND_API_KEY:
        return
    resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": [to],
        "subject": "Welcome to CommodityData.io",
        "html": f"""
        <h2>Welcome, {name}!</h2>
        <p>Your account is ready. Here's how to get started:</p>
        <ol>
            <li>Go to your <a href="{settings.FRONTEND_URL}/dashboard">dashboard</a></li>
            <li>Create an API key</li>
            <li>Make your first API call</li>
        </ol>
        <p>Free tier includes 100 requests/day. Upgrade anytime for more.</p>
        <p>— The CommodityData.io Team</p>
        """,
    })


def send_api_key_email(to: str, name: str, key_name: str, key_value: str):
    if not settings.RESEND_API_KEY:
        return
    resend.Emails.send({
        "from": settings.EMAIL_FROM,
        "to": [to],
        "subject": f"New API Key Created: {key_name}",
        "html": f"""
        <h2>New API Key</h2>
        <p>Hi {name},</p>
        <p>You created a new API key named <strong>{key_name}</strong>:</p>
        <pre style="background:#f5f5f5;padding:12px;border-radius:6px;font-size:14px;">{key_value}</pre>
        <p>⚠️ Store this key securely. It won't be shown again.</p>
        <p>— The CommodityData.io Team</p>
        """,
    })
