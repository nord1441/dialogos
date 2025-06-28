from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Export yesterday's ChatHistory to Notion as a single note"

    def handle(self, *args, **options):
        from chat.notion import add_yesterday_chathistory_to_notion
        add_yesterday_chathistory_to_notion()
        self.stdout.write(self.style.SUCCESS("Exported yesterday's ChatHistory to Notion"))
