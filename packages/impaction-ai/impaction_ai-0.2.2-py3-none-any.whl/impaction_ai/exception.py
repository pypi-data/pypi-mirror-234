class APIError(Exception):
    def __init__(self, status_code: int, err_msg: str):
        self.status_code = status_code
        self.err_msg = err_msg

    def __str__(self):
        return f"APIError: {str(self.status_code)} {self.err_msg}"
