from typing import cast, Any

from .perception import Perception
from .content_type import MessageContentType, MessageContentSimpleType, MessageContentBaseType


class Message(Perception):
    '''
    This class specifies a wrapper for a message that is sent to a multiple recipients, and its metadata.

    * The content is specified by the `content` field. This field's type is `MessageContentType`.
    * The recipients are specified by the `recipient_ids` field. This field's type is `list[str]`.
    * The sender is specified by the `sender_id` field. This field's type is `str`.
    '''
    def __init__(self, content: MessageContentType, sender_id: str, recipient_ids: list[str]=[]) -> None:
        self.validate_content(content)
        self.validate_sender_id(sender_id)
        self.validate_recipients_ids(recipient_ids)

        self.__content: MessageContentType = content
        self.__sender_id: str = sender_id
        self.__recipient_ids: list[str] = recipient_ids

    def get_content(self) -> MessageContentType:
        '''
        Returns the content of the message as a `MessageContentType`.
        '''
        return self.__content

    def get_sender_id(self) -> str:
        '''
        Returns the sender's ID as a `str`.
        '''
        return self.__sender_id

    def get_recipients_ids(self) -> list[str]:
        '''
        Returns the recipients' IDs as a `list[str]`.

        In case this `Message` is a `BccMessage`, this method returns a `list[str]`containing only one ID.
        '''
        return self.__recipient_ids

    def override_recipients(self, recipient_ids: list[str]) -> None:
        '''
        WARNING: this method needs to be public, but it is not part of the public API.
        '''
        self.__recipient_ids = recipient_ids

    def validate_content(self, content: Any, must_be_simple: bool=False) -> None:
        if content is None:
            raise ValueError(f"Invalid content: {content}.")
        elif must_be_simple and not isinstance(content, MessageContentSimpleType):
            raise ValueError(f"Invalid content type: {type(content)}. The content of a message must be of type `MessageContentSimpleType`.")
        elif not isinstance(content, MessageContentBaseType):
            raise ValueError(f"Invalid content type: {type(content)}. The content of a message must be of type `MessageContentType`, including recursive content.")
        elif isinstance(content, list):
            for element in cast(list[Any], content):
                self.validate_content(element)
        elif isinstance(content, dict):
            for key, value in cast(dict[Any, Any], content).items():
                self.validate_content(key, must_be_simple=True)
                self.validate_content(value)

    def validate_sender_id(self, sender_id: Any) -> None:
        if not sender_id:
            raise ValueError(f"Invalid sender ID: {sender_id}.")
        elif not isinstance(sender_id, str):
            raise ValueError(f"Invalid sender ID type: {type(sender_id)}. The sender ID must be of type `str`.")

    def validate_recipients_ids(self, recipient_ids: Any) -> None:
        if recipient_ids is None:
            raise ValueError(f"Invalid recipient IDs: {recipient_ids}.")
        elif not isinstance(recipient_ids, list):
            raise ValueError(f"Invalid recipient IDs type: {type(recipient_ids)}. The recipient IDs must be of type `list[str]`.")

        list_of_recipient_ids: list[Any] = cast(list[Any], recipient_ids)

        for recipient_id in list_of_recipient_ids:
            if not isinstance(recipient_id, str):
                raise ValueError(f"Invalid recipient ID: {recipient_id}. All recipient IDs must be of type `str`.")


class BccMessage(Message):
    '''
    This class specifies a wrapper for a message that is sent to a single recipient, and its metadata.

    * The content is specified by the `content` field. This field's type is `MessageContentType`.
    * The recipient is specified by the `recipient_id` field. This field's type is `str`.
    * The sender is specified by the `sender_id` field. This field's type is `str`.
    '''
    def __init__(self, content: MessageContentType, sender_id: str, recipient_id: str) -> None:
        assert content is not None

        super(BccMessage, self).__init__(content=self.__deep_copy_content(content), sender_id=sender_id, recipient_ids=[recipient_id])

    def __deep_copy_content(self, content: MessageContentType) -> MessageContentType:
        self.validate_content(content)

        if isinstance(content, (MessageContentSimpleType, bytes)):
            return content
        elif isinstance(content, list):
            return [self.__deep_copy_content(element) for element in cast(list[Any], content)]
        elif isinstance(content, dict):
            return {cast(MessageContentSimpleType, self.__deep_copy_content(key)): self.__deep_copy_content(value) for key, value in cast(dict[Any, Any], content).items()}
        else:
            raise ValueError(f"Invalid content type: {type(content)}. The content of a message must be of type `MessageContentSimpleType`.")

    def __str__(self) -> str:
        return "message:(from: {}, content: {})".format(self.get_sender_id(), self.get_content())
