import enum


class UserType(str, enum.Enum):
    ORDINARY = "ordinary"
    MODERATOR = "moderator"