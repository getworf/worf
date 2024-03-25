from worf.models.base import Base, EncryptedData, PkType
from sqlalchemy import Column, Unicode, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

import datetime
import hashlib

from sqlalchemy.sql import and_


class SignupRequest(Base):
    __tablename__ = "signup_request"

    email_hash = Column(Unicode, nullable=True, unique=True)
    encrypted_data = Column(EncryptedData)

    tenant_id = Column(PkType, ForeignKey("tenant.id"), nullable=False)
    tenant = relationship(
        "Tenant", backref=backref("signup_requests", cascade="all,delete,delete-orphan")
    )

    @classmethod
    def get_by_ext_id(cls, session, tenant, ext_id):
        return (
            session.query(SignupRequest)
            .filter(SignupRequest.tenant == tenant, SignupRequest.ext_id == ext_id)
            .one_or_none()
        )

    @classmethod
    def get(cls, session, tenant, email_hash):
        return (
            session.query(SignupRequest)
            .filter(
                SignupRequest.tenant == tenant, SignupRequest.email_hash == email_hash
            )
            .one_or_none()
        )

    @classmethod
    def get_or_create(cls, session, tenant, email_hash):
        request = (
            session.query(SignupRequest)
            .filter(
                SignupRequest.tenant == tenant, SignupRequest.email_hash == email_hash
            )
            .one_or_none()
        )
        if not request:
            request = SignupRequest(email_hash=email_hash, tenant=tenant)
            session.add(request)
        return request

    def export(self):
        return {
            "id": self.ext_id,
            "data": self.data,
            "encrypted_data": self.encrypted_data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "email_hash": self.email_hash,
        }
