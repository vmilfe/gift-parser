import os
import asyncio

from typing import AsyncGenerator, Dict, Any

from pyrogram import Client
from pyrogram.types import ChatMember
from pyrogram.enums import ChatMemberStatus

from config import API_HASH, API_ID, GIFT_IDS


async def get_client():
    session = [file for file in os.listdir('session') if file.split('.')[-1] == 'session']
    
    if not session:
        session = ['main']
    
    client = Client(
        name=f'session/{session[0].replace(".session", "")}',
        api_id=API_ID,
        api_hash=API_HASH,
        system_version="4.16.30-vxCUSTOM"
    )
    await client.start()
    return client

async def parse_members(chat: str) -> AsyncGenerator[Dict[str, Any], None]:
    client = await get_client()
    
    try:
        async for user in client.get_chat_members(chat):
            user: ChatMember
            if user.status == ChatMemberStatus.MEMBER:
                gifts = await get_user_gifts(client, user.user.id, user.user.username)

                if gifts:
                    yield gifts

                await asyncio.sleep(0.5)

    except Exception as e:
        print(e)
    
    if client:
        await client.stop()

async def get_user_gifts(client: Client, user_id: int, username: str):
    result = []
    try:
        async for gift in client.get_user_gifts(user_id):
            if gift.is_limited == True or gift.is_upgraded == None or gift.id in GIFT_IDS:
                result.append({"gift": gift.id, "user_id": user_id, "username": username})
        
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return []
    
    return result


async def main():
    client = await get_client()
    pass


if __name__ == '__main__':
    asyncio.run(main())
