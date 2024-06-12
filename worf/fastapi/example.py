from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from sqlalchemy.types import Boolean
from worf.models.base import PkType, Unicode

class User(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    # display name of the user
    display_name: str = Field(sa_type=Unicode(30), nullable=True)

    # primary e-mail of the user
    email: str = Field(sa_type=Unicode, nullable=True, unique=True)

    # primary language of the user
    language: str = Field(sa_type=Unicode, sa_column_kwargs={"server_default": "en"}, nullable=False)

    # whether this is a superuser (for the given tenant)
    superuser: bool = Field(sa_type=Boolean, default=False, sa_column_kwargs={"server_default": "FALSE"}, nullable=False)

    # whether the account is verified
    account_verified: bool = Field(
        sa_type=Boolean, default=False, sa_column_kwargs={"server_default": "FALSE"}, nullable=False
    )

    # new e-mail that was requested an e-mail change code
    new_email: str = Field(sa_type=Unicode, nullable=True)
    email_change_code: str = Field(sa_type=Unicode, nullable=True)

    # whether the user is disabled
    disabled: bool = Field(sa_type=Boolean, default=False, sa_column_kwargs={"server_default": "FALSE"}, nullable=False)

    # describes the roles that a user has within a tenant
    tenant_roles: str = Field(sa_type=Unicode, default="", sa_column_kwargs={"server_default": ""}, nullable=True)

    # links to the given tenant
    # tenant_id: int = Field(foreign_key="tenant.id", sa_type=PkType, nullable=False)

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes