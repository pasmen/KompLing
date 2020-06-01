import asyncio
import sys

from dbconfig import TABLE_NAME, DATABASE_NAME
from dbmodel import Connection, Mongo

sys.path.append("..")


async def queue_printer(mongo, queue):
    while True:
        val = await queue.get()
        mongo.insert(TABLE_NAME, val)
        queue.task_done()


async def main():
    conn = Connection().getConnection()
    mongo = Mongo(conn, DATABASE_NAME)

    queue = asyncio.Queue()


if __name__ == '__main__':
    asyncio.run(main())
