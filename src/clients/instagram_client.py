from typing import List, Dict
from playwright.sync_api import sync_playwright
from utils.downloader import Downloader
import json


class InstagramClient:

    def get_posts(self, username: str, limit: int = 10) -> List[Dict]:
        url = f"https://www.instagram.com/{username}/"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            main_page = browser.new_page()

            print("🌐 Loading profile...")
            main_page.goto(url, timeout=30000)

            try:
                main_page.wait_for_selector("article a", timeout=5000)
            except:
                print("⚠️ Grid not detected, continuing...")

            links = main_page.query_selector_all("article a")

            print(f"🔗 Links found: {len(links)}")

            post_urls = []

            for link in links[:limit]:
                href = link.get_attribute("href")
                if href:
                    post_urls.append(f"https://www.instagram.com{href}")

            posts = []

            for i, post_url in enumerate(post_urls):
                print(f"📄 Scraping post {i+1}/{len(post_urls)}")

                post_page = browser.new_page()

                try:
                    post_page.goto(post_url, timeout=30000)
                    post_page.wait_for_timeout(1500)

                    # 🔥 CAPTION
                    try:
                        caption = post_page.locator("article span").first.inner_text(timeout=2000)
                    except:
                        caption = ""

                    # 🔥 MEDIA
                    try:
                        media = post_page.locator("img").first.get_attribute("src", timeout=2000)
                    except:
                        media = ""

                    # 🔥 JSON INTERNO (MEJOR PARA DATE + LIKES)
                    date = ""
                    likes = ""

                    try:
                        json_text = post_page.locator("script[type='application/ld+json']").inner_text(timeout=2000)
                        parsed = json.loads(json_text)

                        date = parsed.get("uploadDate", "")
                        likes = parsed.get("interactionStatistic", {}).get("userInteractionCount", "")

                    except:
                        pass

                    # 🔥 DESCARGAR IMAGEN
                    image_path = ""

                    if media:
                        image_path = Downloader.download_image(media, f"post_{i}")

                    # 🔥 GUARDAR DATA
                    posts.append({
                        "post_url": post_url,
                        "caption": caption,
                        "media_url": media,
                        "image_path": image_path,
                        "date": date,
                        "likes": likes
                    })

                except Exception as e:
                    print(f"❌ Error scraping post: {e}")

                finally:
                    post_page.close()

            browser.close()

        return posts