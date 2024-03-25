from .base import Base, PkType

from sqlalchemy import Column, Unicode, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = "user"

    # display name of the user
    display_name = Column(Unicode(30), nullable=True)

    # primary e-mail of the user
    email = Column(Unicode, nullable=True, unique=True)

    # primary language of the user
    language = Column(Unicode, server_default="en", nullable=False)

    # whether this is a superuser (for the given tenant)
    superuser = Column(Boolean, default=False, server_default="FALSE", nullable=False)

    # whether the account is verified
    account_verified = Column(
        Boolean, default=False, server_default="FALSE", nullable=False
    )

    # new e-mail that was requested an e-mail change code
    new_email = Column(Unicode, nullable=True)
    email_change_code = Column(Unicode, nullable=True)

    # whether the user is disabled
    disabled = Column(Boolean, default=False, server_default="FALSE", nullable=False)

    # describes the roles that a user has within a tenant
    tenant_roles = Column(Unicode, default="", server_default="", nullable=True)

    # links to the given tenant
    tenant_id = Column(PkType, ForeignKey("tenant.id"), nullable=False)
    tenant = relationship(
        "Tenant", backref=backref("users", cascade="all,delete,delete-orphan")
    )

    def export(self, full=True):
        return {
            "email": self.email if full else "",
            "id": self.ext_id,
            "data": self.data if full else "",
            "display_name": self.display_name if full else "",
            "disabled": self.disabled,
            "new_email": self.new_email if full else "",
            "superuser": self.superuser,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "language": self.language,
        }

    @classmethod
    def get_by_email(cls, session, tenant, email):
        return (
            session.query(User)
            .filter(User.tenant == tenant, User.email == email)
            .one_or_none()
        )

    @classmethod
    def get_by_ext_id(cls, session, tenant, ext_id):
        return (
            session.query(User)
            .filter(User.tenant == tenant, User.ext_id == ext_id)
            .one_or_none()
        )
