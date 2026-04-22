from config.settings import TARGET_USERNAME, POST_LIMIT
from clients.instagram_client import InstagramClient
from storage.file_storage import FileStorage


def main():
    print("Starting Instagram scraper...")
    print(f"Target profile: {TARGET_USERNAME}")

    try:
        client = InstagramClient()

        print("Fetching posts from Instagram...")
        posts = client.get_posts(TARGET_USERNAME, POST_LIMIT)

        if not posts:
            print("No posts found.")
            return

        FileStorage.save_json(posts, "data/latest_posts.json")
        FileStorage.save_csv(posts, "data/latest_posts.csv")

        print(f"Successfully scraped {len(posts)} posts.")
        print("Data saved in /data folder.")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()