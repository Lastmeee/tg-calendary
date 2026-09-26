import logging
import threading
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import config
from models import Event, db
from notifier import run_notifier

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
app.config["SECRET_KEY"] = config.SECRET_KEY

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return redirect(url_for("events_list"))


@app.route("/events")
def events_list():
    events = Event.query.order_by(Event.event_time.asc()).all()
    return render_template("events.html", events=events)


@app.route("/events/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        raw_time = request.form.get("event_time", "")

        if not title:
            flash("Введите название события.")
            return render_template("add_event.html"), 400

        try:
            event_time = datetime.fromisoformat(raw_time)
        except ValueError:
            flash("Неверный формат даты и времени.")
            return render_template("add_event.html"), 400

        if event_time <= datetime.now():
            flash("Время события уже прошло. Выберите момент в будущем.")
            return render_template("add_event.html"), 400

        db.session.add(Event(title=title, event_time=event_time))
        db.session.commit()
        flash(f"Событие «{title}» добавлено.")
        return redirect(url_for("events_list"))

    return render_template("add_event.html")


@app.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        abort(404)
    db.session.delete(event)
    db.session.commit()
    flash(f"Событие «{event.title}» удалено.")
    return redirect(url_for("events_list"))


if __name__ == "__main__":
    threading.Thread(target=run_notifier, args=(app,), daemon=True).start()
    # use_reloader=False, иначе Flask запустит второй поток уведомлений
    app.run(debug=True, use_reloader=False)
