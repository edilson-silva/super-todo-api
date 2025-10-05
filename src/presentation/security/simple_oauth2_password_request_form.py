from fastapi.security import OAuth2PasswordRequestForm


class SimpleOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """
    A custom OAuth2PasswordRequestForm to request only email and password.
    Currently, it behaves the same as OAuth2PasswordRequestForm.
    """

    def __init__(self, email: str, password: str):
        super().__init__(
            username=email,
            password=password,
            scope='',
            grant_type=None,
            client_secret=None,
        )
