from abc import ABC
from dotenv import load_dotenv
import os


class RetrieveSecrets(ABC):
    def __init__(self) -> None:
        load_dotenv()
        self.EMAIL_SEND_ADDRESS = os.environ.get("EMAIL_SEND_ADDRESS")
        self.EMAIL_SEND_PASSWORD = os.environ.get("EMAIL_SEND_PASSWORD")
        self.EMAIL_RECEIVE_A = os.environ.get("EMAIL_RECEIVE_A")
        self.EMAIL_RECEIVE_N = os.environ.get("EMAIL_RECEIVE_N")
        
