class MoodleScrapperInvalidCredentialsException(Exception):
    def __init__(self, msg='Invalid Credentials', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class MoodleScrapperBadLoginURLException(Exception):
    def __init__(self, msg='Configured LOGIN URL is invalid', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

class MoodleScrapperQuizNotFoundException(Exception):
    def __init__(self, msg='Can not find quiz', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)