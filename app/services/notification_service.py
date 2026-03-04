import asyncio

async def send_notification(user_id: int, message: str):
    await asyncio.sleep(1)
    print(f"Notification to user {user_id}: {message}")