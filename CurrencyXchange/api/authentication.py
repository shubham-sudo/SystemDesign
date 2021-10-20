from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """
    [description]
    """

    keyword = "Bearer"
