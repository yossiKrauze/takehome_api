from takehome_api.src.config.database import db
from takehome_api.src.models.model import State, Insurance, Provider, provider_states, provider_insurances, Patient, Appointment
from takehome_api.src.config.config import get_logger
from sqlalchemy.orm import Session
import datetime

logger = get_logger("populate_db")


def populate_database():
    logger.info("Destorying DB...")
    db.drop_all()
    db.create_all()
    db.session.commit()

    logger.info("Populating database...")

    logger.info("Populating patients")
    _populate_patients(db.session)

    ca = State(state="CA")
    db.session.add(ca)
    logger.info("Added CA state")

    ny = State(state="NY")
    db.session.add(ny)
    logger.info("Added NY state")

    ma = State(state="MA")
    db.session.add(ma)
    logger.info("Added MA state")

    aetna = Insurance(name="Aetna")
    db.session.add(aetna)
    logger.info("Added Aetna insurance")

    bcbs = Insurance(name="Blue Cross")
    db.session.add(bcbs)
    logger.info("Added Blue Cross insurance")

    provider1 = Provider(first_name="Cheryl", last_name="Crow")
    db.session.add(provider1)
    logger.info("Added Cheryl Crow provider")

    provider2 = Provider(first_name="John", last_name="Coltrane")
    db.session.add(provider2)
    logger.info("Added John Coltrane provider")

    provider3 = Provider(first_name="Bob", last_name="Marley")
    db.session.add(provider3)
    logger.info("Added Bob Marley provider")

    db.session.flush()

    # Creating the relationships
    db.session.execute(provider_states.insert().values(
        provider_id=provider1.id, state_id=ca.id))
    db.session.execute(provider_states.insert().values(
        provider_id=provider1.id, state_id=ny.id))
    logger.info("Added Cheryl Crow provider states")

    db.session.execute(provider_insurances.insert().values(
        provider_id=provider1.id, insurance_id=aetna.id))
    db.session.execute(provider_insurances.insert().values(
        provider_id=provider1.id, insurance_id=bcbs.id))
    logger.info("Added Cheryl Crow provider insurances")

    db.session.execute(provider_states.insert().values(
        provider_id=provider2.id, state_id=ma.id))
    db.session.execute(provider_states.insert().values(
        provider_id=provider2.id, state_id=ny.id))
    logger.info("Added John Coltrane provider states")

    db.session.execute(provider_insurances.insert().values(
        provider_id=provider2.id, insurance_id=aetna.id))
    db.session.execute(provider_insurances.insert().values(
        provider_id=provider2.id, insurance_id=bcbs.id))
    logger.info("Added John Coltrane provider insurances")

    db.session.execute(provider_states.insert().values(
        provider_id=provider3.id, state_id=ma.id))
    db.session.execute(provider_states.insert().values(
        provider_id=provider3.id, state_id=ca.id))
    logger.info("Added Bob Marley provider states")

    db.session.execute(provider_insurances.insert().values(
        provider_id=provider3.id, insurance_id=aetna.id))
    db.session.execute(provider_insurances.insert().values(
        provider_id=provider3.id, insurance_id=bcbs.id))
    logger.info("Added Bob Marley provider insurances")

    db.session.flush()
    _populate_available_appointments(db.session)

    db.session.commit()

    logger.info("Populated DB")


def _populate_patients(session: Session):
    patient1 = Patient(
        first_name="Cold",
        last_name="Play",
        email="cold.play@example.com",
        state="CA",
        insurance="Aetna"
    )
    session.add(patient1)
    patient2 = Patient(
        first_name="The",
        last_name="Beatles",
        email="the.beatles@example.com",
        state="NY",
        insurance="Blue Cross"
    )
    session.add(patient2)
    patient3 = Patient(
        first_name="Guns",
        last_name="N' Roses",
        email="guns.n_roses@example.com",
        state="MA",
        insurance="Aetna"
    )
    session.add(patient3)
    patient4 = Patient(
        first_name="Beach",
        last_name="Boys",
        email="beach.boys@example.com",
        state="CA",
        insurance="Blue Cross"
    )
    session.add(patient4)
    patient5 = Patient(
        first_name="Pearl",
        last_name="Jam",
        email="pearl.jam@example.com",
        state="MA",
        insurance="Blue Cross"
    )
    session.add(patient5)
    patient6 = Patient(
        first_name="Poster",
        last_name="Child",
        email="poster.child@example.com",
        state="MA",
        insurance="Blue Cross"
    )
    session.add(patient6)
    patient7 = Patient(
        first_name="Foo",
        last_name="Fighters",
        email="foo.fighters@example.com",
        state="CA",
        insurance="Blue Cross"
    )
    session.add(patient7)
    patient8 = Patient(
        first_name="The",
        last_name="Who",
        email="the.who@example.com",
        state="MA",
        insurance="Blue Cross"
    )
    session.add(patient8)
    patient9 = Patient(
        first_name="Black",
        last_name="Sabbath",
        email="black.sabbath@example.com",
        state="MA",
        insurance="Blue Cross"
    )
    session.add(patient9)
    patient10 = Patient(
        first_name="Deep",
        last_name="Purple",
        email="deep.purple@example.com",
        state="MA",
        insurance="Blue Cross"
    )
    session.add(patient10)
    session.flush()

    logger.info("Populated patients")


def _populate_available_appointments(session: Session):
    logger.info("Populating available appointments")
    providers = session.query(Provider).all()
    for provider in providers:
        appointment = Appointment(
            provider_id=provider.id,
            insurance_id=provider.insurances[0].id,
            time=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        session.add(appointment)
    session.flush()
    logger.info("Populated available appointments")
