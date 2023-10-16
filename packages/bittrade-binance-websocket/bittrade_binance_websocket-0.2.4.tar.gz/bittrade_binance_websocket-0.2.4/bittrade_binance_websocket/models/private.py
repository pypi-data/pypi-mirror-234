import dataclasses


@dataclasses.dataclass
class APIKeyPrivateRequest:
  apiKey: str

@dataclasses.dataclass
class PrivateRequest(APIKeyPrivateRequest):
  timestamp: str