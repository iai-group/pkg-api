"""Define the user and service models for the database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # type: ignore
    # Typing issue is ignored here. For more information, see:
    # https://github.com/python/mypy/issues/8603
    """User model for database."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    uri = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return (
            f"User {self.id}:\n\tusername: {self.username}\n\turi: {self.uri}"
        )
    
class Service(db.Model):  # type: ignore
    # Typing issue is ignored here. For more information, see:
    # https://github.com/python/mypy/issues/8603
    """Service model for database."""

    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), unique=True, nullable=False)
    service_uri = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the service."""
        return (
            f"Service {self.service_id}:\n\tservice name: {self.service_name}\n\tservice uri: {self.service_uri}"
        )

class ServiceAccess(db.Model):  # type: ignore
    # Typing issue is ignored here. For more information, see:
    # https://github.com/python/mypy/issues/8603
    """Service model for database."""

    service_fact_id = db.Column(db.Integer, primary_key=True)
    service_uri = db.Column(db.String(120), unique=False, nullable=False)
    fact_uri = db.Column(db.String(120), unique=False, nullable=False)
    access_read = db.Column(db.Boolean, unique=False, nullable=False)
    access_write = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self) -> str:
        """Return a string representation of the service/fact access rights."""
        return (
            f"Service {self.service_uri}:\n\tFact: {self.fact_uri}\n\tWrite access: {self.access_write}\n\tRead access: {self.access_read}"
        )