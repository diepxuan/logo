from facebook_scraper import get_posts
from datetime import datetime
import mysql.connector
import __os as os

# Cấu hình
FB_PAGE = "Everonpage"  # Thay bằng page bạn cần lấy
NUM_PAGES = 1

# db = mysql.connector.connect(
#     host=os.environ.get("DB_HOST", "mysql.diepxuan.corp"),
#     user=os.environ.get("DB_USERNAME", "n8n"),
#     password=os.environ.get("DB_PASSWORD"),
#     database=os.environ.get("DB_DATABASE", "n8n"),
#     port=os.environ.get("DB_PORT", 3306)
# )

def crawl():
    # cursor = db.cursor()
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS fb_posts (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         post_id VARCHAR(50) UNIQUE,
    #         text TEXT,
    #         post_time DATETIME,
    #         link TEXT
    #     );
    # """)

    for post in get_posts(FB_PAGE, pages=NUM_PAGES):
        post_id = post.get("post_id")
        text = post.get("text", "")[:1000]
        time = post.get("time")
        link = post.get("post_url")

        # cursor.execute("""
        #     INSERT INTO fb_posts (post_id, text, post_time, link)
        #     VALUES (%s, %s, %s, %s)
        #     ON DUPLICATE KEY UPDATE text = VALUES(text), post_time = VALUES(post_time), link = VALUES(link)
        # """, (post_id, text, time, link))
        print("Đã lấy bài viết:", post_id)
        print("Nội dung:", text)
        print("Thời gian:", time)
        print("Link:", link)
        print("=====================================")
        # Lưu vào database

    # db.commit()
    # db.close()
    print("✅ Lưu thành công các bài viết!")