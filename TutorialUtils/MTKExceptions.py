class BaseError(Exception):
    def __init__(self, ErrorCd, Data=None, message="Base Error occured"):
        self.Data = Data
        self.message = message
        self.ErrorCd = ErrorCd
        super().__init__(self.message)


class UnknownError(BaseError):
    def __init__(self, message="An unknown error occured"):
        self.message = message
        super().__init__(message=self.message, ErrorCd=1)


class DBError(BaseError):
    def __init__(self, sql, message="An error occured with the database"):
        self.sql = sql
        self.message = message
        super().__init__(Data=sql, message=self.message, ErrorCd=2)


class FileError(BaseError):
    def __init__(self, message="File Error occured"):
        self.message = message
        super().__init__(message=self.message, ErrorCd=3)


class DataError(BaseError):
    def __init__(self, message="Data Error occured"):
        self.message = message
        super().__init__(message=self.message, ErrorCd=4)


class FileFormatError(BaseError):
    def __init__(self, message="File Error occured"):
        self.message = message
        super().__init__(message=self.message, ErrorCd=5)


class InputError(BaseError):
    def __init__(self, message="Input value not usable"):
        self.message = message
        super().__init__(message=self.message, ErrorCd=6)
