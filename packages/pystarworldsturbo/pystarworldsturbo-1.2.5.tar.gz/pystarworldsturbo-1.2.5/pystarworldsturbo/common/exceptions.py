class ActionException(Exception):
    def __init__(self, message: str):
        super(ActionException, self).__init__(message)


class ActorException(Exception):
    def __init__(self, message: str):
        super(ActorException, self).__init__(message)


class IdentityException(ActorException):
    def __init__(self, message: str):
        super(IdentityException, self).__init__(message)


class EnvironmentException(Exception):
    def __init__(self, message: str):
        super(EnvironmentException, self).__init__(message)


class PhysicsException(EnvironmentException):
    def __init__(self, message: str):
        super(PhysicsException, self).__init__(message)


class PerceptionException(Exception):
    def __init__(self, message: str):
        super(PerceptionException, self).__init__(message)


class CommunicationException(Exception):
    def __init__(self, message: str):
        super(CommunicationException, self).__init__(message)


class MessageException(CommunicationException):
    def __init__(self, message: str):
        super(MessageException, self).__init__(message)
