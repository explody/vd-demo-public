from config import db, ma
from datetime import datetime
from marshmallow import fields, ValidationError
from sqlalchemy.ext.hybrid import hybrid_property
import pprint


class CompanyRole(db.Model):
    __tablename__ = "company_role"

    person_id = db.Column(db.ForeignKey("person.id"), primary_key=True)
    company_id = db.Column(db.ForeignKey("company.id"), primary_key=True)
    role = db.Column(db.String(128))
    primary = db.Column(db.Boolean(), default=False)

    person = db.relationship("Person", back_populates="company_roles")
    company = db.relationship("Company", back_populates="people")

    db.UniqueConstraint(person_id, company_id, primary, name="uix_1"),


class LocationTenancy(db.Model):
    __tablename__ = "location_tenancy"

    location_id = db.Column(db.ForeignKey("location.id"), primary_key=True)
    company_id = db.Column(db.ForeignKey("company.id"), primary_key=True)
    description = db.Column(db.String(128))
    primary = db.Column(db.Boolean(), default=False)

    location = db.relationship("Location", back_populates="companies")
    company = db.relationship("Company", back_populates="locations")

    db.UniqueConstraint(location_id, company_id, primary, name="lix_1"),


class Company(db.Model):
    __tablename__ = "company"

    def __repr__(self):
        return f'<Company {self.id} "{self.name}">'

    expandable = {
        "people": "person_schema",
    }

    searchable = ["name", "full_name", "description"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    full_name = db.Column(db.String(64))
    description = db.Column(db.Text())
    domain = db.Column(db.String(64))
    website = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(64))
    logo = db.Column(db.String(64))
    people = db.relationship("CompanyRole", back_populates="company")
    locations = db.relationship("LocationTenancy", back_populates="company")

    @hybrid_property
    def hq(self):
        hq = LocationTenancy.query.filter_by(company_id=self.id, primary=True).first()
        if hq:
            return Location.query.get(hq.location_id)
        return None


class Person(db.Model):
    __tablename__ = "person"

    def __repr__(self):
        return f'<Person {self.id} "{self.first_name} {self.last_name}">'

    expandable = {
        "manager": "person_schema",
        "reports": "person_schema",
        "assigned_office": "location_schema",
        "primary_company": "company_schema",
    }

    searchable = [
        "preferred_name",
        "first_name",
        "additional_name",
        "last_name",
        "nickname",
    ]

    id = db.Column(db.Integer, primary_key=True)
    preferred_name = db.Column(db.String(32))
    first_name = db.Column(db.String(32), nullable=False)
    additional_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32), nullable=False)
    name_prefix = db.Column(db.String(32))
    name_suffix = db.Column(db.String(32))
    nickname = db.Column(db.String(32))
    pronouns = db.Column(db.String(32))
    title = db.Column(db.String(128))
    assigned_office_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    work_location = db.Column(db.String(32))

    primary_phone = db.Column(db.String(24))
    mobile_phone = db.Column(db.String(24))

    primary_email = db.Column(db.String(32))
    secondary_email = db.Column(db.String(32))
    personal_email = db.Column(db.String(32))

    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    country = db.Column(db.String(32))
    timezone = db.Column(db.String(32))
    division = db.Column(db.String(32))
    department = db.Column(db.String(32))
    photo_url = db.Column(db.String(255))
    description = db.Column(db.Text())

    manager_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    reports = db.relationship("Person", back_populates="manager")
    manager = db.relationship(
        "Person",
        back_populates="reports",
        remote_side=[id],
        foreign_keys="Person.manager_id",
    )

    company_roles = db.relationship("CompanyRole", back_populates="person")

    last_update = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @hybrid_property
    def primary_company(self):
        cr = CompanyRole.query.filter_by(person_id=self.id, primary=True).first()
        if cr:
            return Company.query.get(cr.company_id)
        return None


class Location(db.Model):
    __tablename__ = "location"

    def __repr__(self):
        return f'<Location {self.id} "{self.site_code}">'

    expandable = {
        "people": "person_schema",
        "companies": "company_schema",
    }

    searchable = ["site_name", "site_code"]

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(32))
    site_code = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(64))
    address2 = db.Column(db.String(64))
    address3 = db.Column(db.String(64))
    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    postal_code = db.Column(db.String(16))
    country = db.Column(db.String(32))
    people = db.relationship("Person", backref="assigned_office")
    companies = db.relationship("LocationTenancy", back_populates="location")


class CompanyRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyRole
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class PersonSchema(ma.SQLAlchemyAutoSchema):

    # companies = ma.Nested(lambda: CompanyRoleSchema(), many=True)
    primary_company = fields.Method("render_primary_company")
    company_roles = fields.Method("render_companies")

    def render_primary_company(self, obj):
        if obj.primary_company:
            return getattr(obj.primary_company, "id", "Unknown")
        return None

    def render_companies(self, obj):
        return [
            {"company_id": r.company_id, "role": r.role, "primary": r.primary}
            for r in obj.company_roles
        ]

    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class CompanySchema(ma.SQLAlchemyAutoSchema):

    hq = fields.Method("render_hq")
    people = fields.Method("render_people")
    locations = fields.Method("render_locations")

    def render_hq(self, obj):
        return getattr(obj.hq, "id", "Unknown")

    def render_locations(self, obj):
        return [
            {
                "location_id": l.location_id,
                "description": l.description,
                "primary": l.primary,
            }
            for l in obj.locations
        ]

    def render_people(self, obj):
        return [p.person_id for p in obj.people]

    class Meta:
        model = Company
        load_instance = True
        sqla_session = db.session
        include_relationships = True


company_role_schema = CompanyRoleSchema()
company_roles_schema = CompanyRoleSchema(many=True)

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
