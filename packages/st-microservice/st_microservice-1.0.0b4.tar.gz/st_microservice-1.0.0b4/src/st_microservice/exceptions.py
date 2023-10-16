class DatabaseQueryError(BaseException):
    """ Errors related to database queries """


class DatabaseResultError(BaseException):
    """ Errors related to database results """


class MultipleRowsError(DatabaseResultError):
    """ Multiple rows returned instead of 1 or 0 """


class NoRowsError(DatabaseResultError):
    """ No rows were returned """
