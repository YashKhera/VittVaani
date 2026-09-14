class NotificationService:
    def send(self, user_id: int, title: str, body: str) -> None:
        pass

    def notify_reminder(self, user_id: int, scheme_name: str) -> None:
        self.send(user_id, "Application Reminder", f"Don't forget to apply to {scheme_name}")


notification_service = NotificationService()