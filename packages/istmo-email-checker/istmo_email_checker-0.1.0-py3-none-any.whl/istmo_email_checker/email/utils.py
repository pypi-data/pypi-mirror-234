from __future__ import annotations
from istmo_email_checker.email import verify


class Email:
    email:str = ''

    def __init__(self, email:str) -> None:
        self.email = email

    def clear_email(self) -> Email:
        self.to_lower()
        self.clear_spaces()
        return self

    def clear_spaces(self) -> Email:
        self.email = self.email.replace(" ", "")
        return self

    def to_lower(self) -> Email:
        self.email = self.email.lower()
        return self
    
    def validate(self, dns_checker=False, recipient_checker=False) -> (bool, str):
        self.clear_email()
        status = verify.check_email(self.email, dns_checker=dns_checker, recipient_checker=recipient_checker)
        return status, self.email

    def get_email(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self.email

    def __str__(self) -> str:
        return self.email
