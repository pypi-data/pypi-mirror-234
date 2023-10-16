import importlib
import pkg_resources
from datetime import datetime
from typing import TypedDict

from impaction_ai import ImpactionAI
from impaction_ai.constants import ROLE_ASSISTANT, ROLE_USER, DEFAULT_ASSISTANT_ID

try:
    langchain = importlib.import_module("langchain")
    langchain_version = pkg_resources.get_distribution("langchain").version
    if pkg_resources.parse_version(langchain_version) < pkg_resources.parse_version("0.0.221"):
        raise ImportError("You must install langchain>=0.0.221 to use ImpactionChatMessageHistory.")
    
    BaseChatMessageHistory = importlib.import_module("langchain.schema").BaseChatMessageHistory
    message_schema = importlib.import_module("langchain.schema.messages")
    BaseMessage, HumanMessage, AIMessage = (
        message_schema.BaseMessage,
        message_schema.HumanMessage,
        message_schema.AIMessage,
    )
except ModuleNotFoundError:
    raise ImportError("You must install 'langchain' to use ImpactionChatMessageHistory.")


class UserInfo(TypedDict):
    display_name: str | None
    email: str | None
    ip: str | None
    country_code: str | None
    create_time: datetime | None


class ImpactionChatMessageHistory(BaseChatMessageHistory):
    def __init__(
        self,
        history_backend: BaseChatMessageHistory,
        impaction_client: ImpactionAI,
        session_id: str,
        user_id: str,
        assistant_id: str = DEFAULT_ASSISTANT_ID,
        user_info: UserInfo | None = None,
    ):
        """Initialize ImpactionChatMessageHistory. When initialized, open_session event is emitted to ImpactionAI.

        Args:
            history_backend (BaseChatMessageHistory): Chat message history backend from LangChain. Reference: https://python.langchain.com/docs/modules/memory/chat_messages/
            impaction_client (ImpactionAI): ImpactionAI SDK client.
            session_id (str): Session ID.
            user_id (str): User ID.
            assistant_id (str, optional): Assistant ID. Defaults to 'DEFAULT'.
            user_info (UserInfo | None, optional): Providing at least one user information will trigger identify_user event upon initialization. Defaults to None.
        """
        self.backend = history_backend
        self.imp = impaction_client
        self.session_id = session_id
        self.user_id = user_id
        self.imp.open_session(session_id=session_id, user_id=user_id, assistant_id=assistant_id)
        if user_info:
            self.identify_user(
                email=user_info.get("email", None),
                ip=user_info.get("ip", None),
                country_code=user_info.get("country_code", None),
                create_time=user_info.get("create_time", None),
                display_name=user_info.get("display_name", None),
            )

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the chat history. If the message is human or assistant message, create_message event will be emitted to ImpactionAI.

        Args:
            message (BaseMessage): One of HumanMessage, AIMessage, or SystemMessage.
        """
        if isinstance(message, (HumanMessage, AIMessage)):
            self.imp.create_message(
                session_id=self.session_id,
                message_index=self._next_message_idx,
                role=ROLE_USER if isinstance(message, HumanMessage) else ROLE_ASSISTANT,
                content=message.content,
            )
        self.backend.add_message(message)

    def clear(self) -> None:
        """Clear the chat history.
        """
        self.backend.clear()

    def identify_user(
        self,
        display_name: str | None = None,
        email: str | None = None,
        ip: str | None = None,
        country_code: str | None = None,
        create_time: datetime | None = None,
    ) -> None:
        """Send identify_user event to ImpactionAI. The user_id provided upon initialization will be used.

        Args:
            email (str | None, optional): User email address. Defaults to None.
            ip (str | None, optional): User IPv4 address. Provide either ip or country code for user location. If both are given, country code overrides ip. Defaults to None.
            country_code (str | None, optional): User country code in ISO Alpha-2. Provide either ip or country code for user location. If both are given, country code overrides ip. Defaults to None.
            create_time (datetime | None, optional): User creation time. Defaults to None.
            display_name (str | None, optional): User display name. Defaults to None.
        """
        self.imp.identify_user(
            user_id=self.user_id,
            email=email,
            ip=ip,
            country_code=country_code,
            create_time=create_time,
            display_name=display_name,
        )

    def close(self) -> None:
        """Close the ImpactionAI session. Do not send additional message after calling this method.
        """
        self.imp.close_session(session_id=self.session_id)

    @property
    def messages(self) -> list[BaseMessage]:
        """Retrieve the chat history.

        Returns:
            list[BaseMessage]: List of messages consisting of one of BaseMessage, HumanMessage, AIMessage, or SystemMessage.
        """
        return self.backend.messages

    @property
    def _next_message_idx(self) -> int:
        return len([message for message in self.messages if isinstance(message, (HumanMessage, AIMessage))]) + 1
