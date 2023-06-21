import json
from collections import defaultdict

import requests

# Token for any telegram bot.
TOKEN = "<YOUR_TOKEN_HERE>"

# Packs that will be used.
PACKS = {
    "https://t.me/addemoji/roflmoji",
    "https://t.me/addemoji/bttvemojis",
    "https://t.me/addemoji/RV_emoji",
    "https://t.me/addemoji/dev_emojis_solid",
    "https://t.me/addemoji/emojipremiumcatjpg",
    "https://t.me/addemoji/UnigramIcons",
    "https://t.me/addemoji/RestrictedEmoji",
    "https://t.me/addemoji/the_pgs",
    "https://t.me/addemoji/JJBAEmojis",
    "https://t.me/addemoji/OdnoklassnikiEmoji",
    "https://t.me/addemoji/reactiontext",
    "https://t.me/addemoji/FaceEmoji",
    "https://t.me/addemoji/AlphabetEmoji"
}


def main() -> None:
    mapping: dict[str, set[int]] = defaultdict(set)

    for pack in PACKS:
        print(f"Parsing: {pack}")
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getStickerSet?name={pack[22:]}")

        for sticker in response.json()["result"]["stickers"]:
            mapping[sticker["emoji"]].add(int(sticker["custom_emoji_id"]))

        print(f"Mapping size: {len(mapping)} -> {sum(map(len, mapping.values()))}")

    with open("mapping.json", "w") as file:
        json.dump({emoji: list(ids) for emoji, ids in mapping.items()}, file)


if __name__ == '__main__':
    main()
