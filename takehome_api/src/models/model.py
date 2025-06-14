from takehome_api.src.config.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

provider_states = db.Table(
    "provider_states",
    db.Column("provider_id", UUID(as_uuid=True), db.ForeignKey(
        "providers.id"), primary_key=True),
    db.Column("state_id", UUID(as_uuid=True), db.ForeignKey(
        "states.id"), primary_key=True),
)

provider_insurances = db.Table(
    "provider_insurances",
    db.Column("provider_id", UUID(as_uuid=True), db.ForeignKey(
        "providers.id"), primary_key=True),
    db.Column("insurance_id", UUID(as_uuid=True), db.ForeignKey(
        "insurances.id"), primary_key=True),
)


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Per the Flask documentation, this is the "old" way. The more modern way is "mapped_column"
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # not everyone has an email...
    email = db.Column(db.String(255), unique=True, nullable=True)
    state = db.Column(db.String(2), nullable=False)
    insurance = db.Column(db.String(100), nullable=True)

    # The more modern way
    # id: Mapped[int] = mapped_column(primary_key=True)
    # email: Mapped[str] = mapped_column(unique=True, nullable=False)
    # state: Mapped[str] = mapped_column(length=2, nullable=False)
    # insurance: Mapped[str | None] = mapped_column(nullable=True)


class Appointment(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = db.Column(UUID(as_uuid=True), db.ForeignKey("providers.id"))
    # Hack for now - if there's no patient ID, the appointment is available
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        "patients.id"), nullable=True)
    insurance_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("insurances.id"), nullable=True)
    time = db.Column(db.DateTime, nullable=False)


class Provider(db.Model):
    __tablename__ = "providers"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(10), nullable=True, default="Dr.")
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    states = db.relationship(
        "State", secondary=provider_states, backref="providers")
    insurances = db.relationship(
        "Insurance", secondary=provider_insurances, backref="providers")


class State(db.Model):
    __tablename__ = "states"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = db.Column(db.String(2), unique=True, nullable=False)


class Insurance(db.Model):
    __tablename__ = "insurances"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), unique=True, nullable=False)
