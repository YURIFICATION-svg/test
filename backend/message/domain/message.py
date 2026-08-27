from dataclasses import dataclass

@dataclass
class Message:
    id: str
    sender_id: str
    receiver_id: str
    title: str
    content: str