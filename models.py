from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    is_notified = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Event #{self.id} {self.title!r} {self.event_time}>"
