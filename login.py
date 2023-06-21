import asyncio
from argparse import ArgumentParser

from telethon import TelegramClient


async def main() -> None:
    parser = ArgumentParser(
        prog='Session generator.',
        description='This command line tool will help you to generate a telegram session.',
        epilog='Cats are cool!'
    )

    parser.add_argument('api_id')
    parser.add_argument('api_hash')

    args = parser.parse_args()

    async with TelegramClient('./sessions/main', args.api_id, args.api_hash):
        pass

if __name__ == '__main__':
    asyncio.run(main())
