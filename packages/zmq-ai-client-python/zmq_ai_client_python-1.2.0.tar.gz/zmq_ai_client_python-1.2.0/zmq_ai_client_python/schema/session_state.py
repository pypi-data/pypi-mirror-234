from dataclasses import dataclass


@dataclass
class SessionStateResponse:
    """
    Dataclass representing a session cache response.
    """
    session_id: str
    user_id: str
    exists: bool
