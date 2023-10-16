class BaseError(Exception):
    """Base class for exceptions in `tesseract_olap` module."""
    code = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
