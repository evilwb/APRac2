import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class QueuedMessage:
    message: str
    duration: float


class NotificationManager:
    notification_queue: list[QueuedMessage] = []
    last_message_time: float = 0
    message_duration: float = None
    default_duration: float = None

    def __init__(self, message_duration):
        self.message_duration = message_duration
        self.default_duration = message_duration

    def queue_size(self) -> int:
        return len(self.notification_queue)

    def queue_notification(self, message, duration: Optional[float] = None):
        self.notification_queue.append(QueuedMessage(message, duration if duration else self.message_duration))

    def has_message_to_display(self):
        if len(self.notification_queue) <= 0:
            return False
        return time.time() - self.last_message_time >= self.message_duration

    def pop_message_from_queue(self):
        notification = self.notification_queue.pop(0)
        self.message_duration = notification.duration
        self.last_message_time = time.time()
        return notification.message
