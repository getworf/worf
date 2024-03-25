from .base import Base

from sqlalchemy import Column, Unicode, Boolean


class Tenant(Base):
    __tablename__ = "tenant"

    name = Column(Unicode(60), nullable=False)
    email = Column(Unicode, nullable=True, unique=True)

    account_verified = Column(
        Boolean, default=False, server_default="FALSE", nullable=False
    )
    new_email = Column(Unicode, nullable=True)
    email_change_code = Column(Unicode, nullable=True)

    disabled = Column(Boolean, default=False, server_default="FALSE", nullable=False)

    # which domain this tenant is associated with
    domain = Column(Unicode, nullable=True)

    def export(self, full=True):
        return {
            "email": self.email if full else "",
            "id": self.ext_id,
            "data": self.data if full else "",
            "name": self.display_name if full else "",
            "disabled": self.disabled,
            "domain": self.domain,
            "new_email": self.new_email if full else "",
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def get_by_domain(cls, session, domain):
        return session.query(Tenant).filter(Tenant.domain == domain).one_or_none()

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(Tenant).filter(Tenant.name == name).one_or_none()

    @classmethod
    def get_by_email(cls, session, email):
        return session.query(Tenant).filter(Tenant.email == email).one_or_none()

    @classmethod
    def get_by_ext_id(cls, session, ext_id):
        return session.query(Tenant).filter(Tenant.ext_id == ext_id).one_or_none()
