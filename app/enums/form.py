import enum


class FormStatus(str, enum.Enum):
    DRAFTING = "drafting"
    PENDING = "pending"
    IN_MODERATION = "in moderation"
    APPROVED = "approved"
    REJECTED = "rejected"


class ModFormStatus(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"