from dataclasses import dataclass

@dataclass
class TokenExpiredError(BaseException):
    status_code: int
    message: str
    error: str
    
    def __repr__(self) -> str:
        return f"""
        \r{30*'-'}
        \rStatus Code: {self.status_code}
        \rError: {self.error}
        \rError Message: {self.message}
    """
    
    def __str__(self) -> str:
        return f"""
        \r{30*'-'}
        \rStatus Code: {self.status_code}
        \rError: {self.error}
        \rError Message: {self.message}
    """