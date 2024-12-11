#!/usr/bin/python3

import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as connection:
        async with connection.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as connection:
        async with connection.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()
        
async def fetch_concurrently():
    users = async_fetch_users()
    older_users = async_fetch_older_users()
    user, older_user = await asyncio.gather(users, older_users)
    print(user)
    print(older_user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())