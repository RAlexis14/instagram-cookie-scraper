import re
import json

class InstagramParser:

    @staticmethod
    def extract_json_from_html(html: str) -> dict:
        """
        Extracts JSON from script tag (modern Instagram)
        """
        match = re.search(r'<script type="application/json">(.+?)</script>', html)

        if not match:
            raise ValueError("No JSON script found")

        return json.loads(match.group(1))

    @staticmethod
    def parse_posts(data: dict) -> list:
        """
        Extract posts safely
        """
        try:
            media = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        except KeyError:
            raise ValueError("Structure changed or invalid")

        posts = []

        for post in media:
            node = post["node"]

            posts.append({
                "id": node.get("id"),
                "shortcode": node.get("shortcode"),
                "caption": (
                    node.get("edge_media_to_caption", {})
                    .get("edges", [{}])[0]
                    .get("node", {})
                    .get("text", "")
                ),
                "post_url": f"https://www.instagram.com/p/{node.get('shortcode')}/",
                "timestamp": node.get("taken_at_timestamp"),
                "media_type": node.get("__typename"),
                "media_url": node.get("display_url")
            })

        return posts