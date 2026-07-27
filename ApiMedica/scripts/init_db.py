import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, async_session
from app.models import *
from app.models.user import User, ApiKey
from app.core.deps import hash_password


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(select(User).limit(1))
        if not result.scalar_one_or_none():
            admin = User(
                email="admin@commoditydata.io",
                hashed_password=hash_password("admin123"),
                full_name="Admin",
                company="CommodityData.io",
                plan="enterprise",
            )
            db.add(admin)
            await db.commit()
            print("Admin user created (admin@commoditydata.io / admin123)")

    print("Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(init_db())
