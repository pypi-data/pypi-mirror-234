from google.protobuf import empty_pb2 as _empty_pb2
from opus_protobuf import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Post(_message.Message):
    __slots__ = ["id", "approved"]
    ID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    id: str
    approved: bool
    def __init__(self, id: _Optional[str] = ..., approved: bool = ...) -> None: ...

class Posts(_message.Message):
    __slots__ = ["posts"]
    POSTS_FIELD_NUMBER: _ClassVar[int]
    posts: _containers.RepeatedCompositeFieldContainer[Post]
    def __init__(self, posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ...) -> None: ...

class UserReport(_message.Message):
    __slots__ = ["user", "socialNetwork", "score"]
    USER_FIELD_NUMBER: _ClassVar[int]
    SOCIALNETWORK_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    user: str
    socialNetwork: str
    score: str
    def __init__(self, user: _Optional[str] = ..., socialNetwork: _Optional[str] = ..., score: _Optional[str] = ...) -> None: ...

class PostReport(_message.Message):
    __slots__ = ["report_likes", "report_comment", "positive_comment", "negative_comment"]
    REPORT_LIKES_FIELD_NUMBER: _ClassVar[int]
    REPORT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_COMMENT_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_COMMENT_FIELD_NUMBER: _ClassVar[int]
    report_likes: int
    report_comment: int
    positive_comment: int
    negative_comment: int
    def __init__(self, report_likes: _Optional[int] = ..., report_comment: _Optional[int] = ..., positive_comment: _Optional[int] = ..., negative_comment: _Optional[int] = ...) -> None: ...

class ResponseRight(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class Industries(_message.Message):
    __slots__ = ["industry"]
    INDUSTRY_FIELD_NUMBER: _ClassVar[int]
    industry: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, industry: _Optional[_Iterable[str]] = ...) -> None: ...
