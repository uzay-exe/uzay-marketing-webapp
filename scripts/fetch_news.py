import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED_URL = "https://www.aa.com.tr/tr/rss/default?cat=spor"
OUT_PATH = "news.json"
MAX_ITEMS = 12


def main() -> None:
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = resp.read()

    root = ET.fromstring(data)
    items = []
    for item in root.findall("./channel/item")[:MAX_ITEMS]:
        items.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "link": (item.findtext("link") or "").strip(),
                "description": (item.findtext("description") or "").strip(),
                "pubDate": (item.findtext("pubDate") or "").strip(),
                "image": (item.findtext("image") or "").strip(),
            }
        )

    payload = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "source": "Anadolu Ajansı - Spor",
        "items": items,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
