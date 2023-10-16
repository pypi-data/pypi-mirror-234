from dspace.dspace_objects import DSpaceError


class DSpaceSessionExpiredError(Exception):

    def __init__(self):
        super().__init__()


class DSpaceAuthenticationError(Exception):
    def __init__(self):
        super().__init__()


class DSpaceApiError(Exception):

    def __init__(self, dspace_error: DSpaceError):
        super().__init__()
        self.dspace_error = dspace_error