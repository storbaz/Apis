import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

PRICE_IDS = {
    "pro": settings.STRIPE_PRO_PRICE_ID,
    "enterprise": settings.STRIPE_ENTERPRISE_PRICE_ID,
}


def create_checkout_session(user_id: int, email: str, plan: str) -> dict:
    price_id = PRICE_IDS.get(plan)
    if not price_id:
        raise ValueError(f"Invalid plan: {plan}")

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=settings.FRONTEND_URL + "/dashboard?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.FRONTEND_URL + "/pricing",
        metadata={"user_id": str(user_id), "plan": plan},
    )
    return {"checkout_url": session.url, "session_id": session.id}


def create_portal_session(stripe_customer_id: str) -> dict:
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=settings.FRONTEND_URL + "/dashboard",
    )
    return {"portal_url": session.url}


def construct_webhook_event(payload: bytes, sig_header: str) -> stripe.Event:
    return stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
