import os
from notion_client import Client
import datetime
import pytz
vars = {
  "notion_token": "",
  "notion_database_id": "",
}

def read_env(identifier):
  if(len(identifier)!=0):
    prefix = identifier + "_"
  else:
    prefix = ""
  vars["notion_token"] = os.getenv(prefix + "NOTION_TOKEN", default="")
  vars["notion_database_id"] = os.getenv(prefix + "NOTION_DATABASE_ID", default="")

read_env("DJANGO_AICHAT")
client = Client(auth=vars["notion_token"])

def add_row_to_notion_database(name, date, content_rows):
    # content_rows: List[Tuple[str, str]]  # [(role, content), ...]
    children = []
    for role, content in content_rows:
        # roleを見出し（heading_3）、contentをパラグラフ
        children.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {"type": "text", "text": {"content": str(role)}}
                ]
            }
        })
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": str(content) if content else ""}}
                ]
            }
        })
    response = client.pages.create(
        **{
            "parent": { "database_id": vars["notion_database_id"]},
            "properties": {
                "名前": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ],
                },
                "日付": {
                    "date": {
                        "start": date
                    }
                },
            },
            "children": children
        }
    )

def add_yesterday_chathistory_to_notion():
    from .models import ChatHistory
    from django.utils import timezone
    from django.db.models import Q

    # 昨日の日付を取得
    yesterday = timezone.localdate() - datetime.timedelta(days=1)
    # 昨日分の履歴を取得
    histories = ChatHistory.objects.filter(
        created_at__date=yesterday
    ).order_by('created_at')

    if not histories.exists():
        return

    content_rows = []
    for h in histories:
        # roleフィールドを利用
        role = getattr(h, "role", "unknown")
        content_value = getattr(h, "content", None)
        content_rows.append((role, content_value))

    # ノートのタイトル
    name = f"ChatHistory {yesterday.strftime('%Y-%m-%d')}"
    # Notionの日付プロパティ
    date = yesterday.strftime('%Y-%m-%d')
    add_row_to_notion_database(name, date, content_rows)
    name = f"ChatHistory {yesterday.strftime('%Y-%m-%d')}"
    # Notionの日付プロパティ
    date = yesterday.strftime('%Y-%m-%d')
    add_row_to_notion_database(name, date, content_rows)



