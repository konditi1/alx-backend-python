#!/usr/bin/python3

import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as connection:
        async with connection.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(age = 40):
    async with aiosqlite.connect("users.db") as connection:
        async with connection.execute("SELECT * FROM users WHERE age > ?", (age,)) as cursor:
            return await cursor.fetchall()

async def main():
    users = async_fetch_users()
    older_users = async_fetch_older_users()
    user, older_user = await asyncio.gather(users, older_users)
    print(user)
    print(older_user)
asyncio.run(main())