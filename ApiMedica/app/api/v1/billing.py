from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.subscription import Subscription
from app.services.stripe_service import create_checkout_session, create_portal_session, construct_webhook_event
from app.config import settings

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/checkout")
async def checkout(
    plan: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if plan not in ("pro", "enterprise"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    result = await create_checkout_session(user.id, user.email, plan)
    return result


@router.post("/portal")
async def portal(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result_sub = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    sub = result_sub.scalar_one_or_none()

    if not sub or not sub.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No active subscription")

    result = create_portal_session(sub.stripe_customer_id)
    return result


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        event = construct_webhook_event(payload, sig_header)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])
        plan = session["metadata"]["plan"]
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
        sub = result.scalar_one_or_none()

        if sub:
            sub.stripe_customer_id = customer_id
            sub.stripe_subscription_id = subscription_id
            sub.plan = plan
            sub.status = "active"
        else:
            sub = Subscription(
                user_id=user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                plan=plan,
                status="active",
            )
            db.add(sub)

        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        if user:
            user.plan = plan

        await db.commit()

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        sub_id = subscription.get("id")
        status = subscription.get("status")

        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
        )
        sub = result.scalar_one_or_none()

        if sub:
            sub.status = status
            if status == "canceled" or status == "unpaid":
                sub.plan = "free"
                user_result = await db.execute(select(User).where(User.id == sub.user_id))
                user = user_result.scalar_one_or_none()
                if user:
                    user.plan = "free"
            await db.commit()

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        sub_id = subscription.get("id")

        result = await db.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
        )
        sub = result.scalar_one_or_none()

        if sub:
            sub.plan = "free"
            sub.status = "canceled"
            user_result = await db.execute(select(User).where(User.id == sub.user_id))
            user = user_result.scalar_one_or_none()
            if user:
                user.plan = "free"
            await db.commit()

    return {"status": "ok"}
