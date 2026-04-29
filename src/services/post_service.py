from typing import List

class PostService:
    def __init__(self, client, parser, limit: int):
        self.client = client
        self.parser = parser
        self.limit = limit

    def get_latest_posts(self, username: str) -> List[dict]:
        html = self.client.get_profile_page(username)

        data = self.parser.extract_json_from_html(html)
        posts = self.parser.parse_posts(data)

        return posts[:self.limit]