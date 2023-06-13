import datetime
import factory
import io
import pytz
import random
import tempfile

from models import Person, Location, Company
from faker import Faker
from PIL import Image

from config import app, db
from sqlalchemy.orm import scoped_session, sessionmaker

with app.app_context():
    session = scoped_session(sessionmaker(bind=db.engine))

# Locations
class LocationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Location
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    site_name = factory.Faker("bs")
    site_code = factory.Faker("word")
    address = factory.Faker("street_address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    country = factory.Faker("country_code")


# People/groups
class PersonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Person
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    preferred_name = factory.Faker("first_name")
    first_name = factory.Faker("first_name")
    additional_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    name_prefix = factory.Faker("prefix")
    name_suffix = factory.Faker("suffix")
    nickname = factory.Faker("first_name")
    title = factory.Faker("job")
    description = factory.Faker(
        "paragraph", nb_sentences=18, variable_nb_sentences=True
    )

    work_location = "here"

    primary_phone = factory.Faker("phone_number")
    mobile_phone = factory.Faker("phone_number")

    primary_email = factory.Faker("company_email")
    secondary_email = factory.Faker("company_email")
    personal_email = factory.Faker("company_email")

    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    country = factory.Faker("country_code")
    timezone = factory.Faker("timezone")
    division = factory.Faker("bs")
    department = factory.Faker("bs")


class CompanyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Company
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    full_name = factory.Faker("company")
    description = factory.Faker("paragraph", nb_sentences=5, variable_nb_sentences=True)
    website = factory.Faker("url")
    icon = factory.Faker("url")
    logo = factory.Faker("url")
