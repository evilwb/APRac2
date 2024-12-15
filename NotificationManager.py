import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class QueuedMessage:
    message: str
    duration: float


class NotificationManager:
    notification_queue: list[QueuedMessage] = []
    time_since_last_message: float = 0
    last_message_time: float = 0
    message_duration: float = None
    default_duration: float = None
    send_notification_func = None

    def __init__(self, message_duration, send_notification_func):
        self.message_duration = message_duration
        self.default_duration = message_duration
        self.send_notification_func = send_notification_func

    def queue_size(self) -> int:
        return len(self.notification_queue)

    def queue_notification(self, message, duration: Optional[float] = None):
        self.notification_queue.append(QueuedMessage(message, duration if duration else self.message_duration))

    def handle_notifications(self):
        self.time_since_last_message = time.time() - self.last_message_time
        if len(self.notification_queue) > 0 and self.time_since_last_message >= self.message_duration:
            notification = self.notification_queue[0]
            result = self.send_notification_func(notification.message)
            if result:
                self.message_duration = notification.duration
                self.notification_queue.pop(0)
                self.last_message_time = time.time()
                self.time_since_last_message = 0
