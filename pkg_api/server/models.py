"""Define the user model for the database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
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
