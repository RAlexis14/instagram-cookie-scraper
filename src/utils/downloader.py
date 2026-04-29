import requests
import os


class Downloader:

    @staticmethod
    def download_image(url: str, filename: str):
        try:
            os.makedirs("data/images", exist_ok=True)

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                path = f"data/images/{filename}.jpg"
                with open(path, "wb") as f:
                    f.write(response.content)

                return path

        except Exception as e:
            print(f"Error downloading image: {e}")

        return ""