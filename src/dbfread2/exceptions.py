class DBFNotFoundError(IOError):
    """Raised if the DBF file was not found."""
    pass


class MissingMemoFileError(IOError):
    """Raised if the corresponding memo file was not found."""


__all__ = ['DBFNotFoundError', 'MissingMemoFileError']
