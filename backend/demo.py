import pprint

from config import db, app
from models import (
    Person,
    Location,
    Company,
    CompanyRole,
    person_schema,
    company_schema,
    company_role_schema,
)
from sqlalchemy.sql.expression import func

with app.app_context():

    for p in Person.query.limit(2):
        print(f"## {p}")
        # print(f"Company: {p.company}")
        # print(f"Office: {p.assigned_office}")
        # print(f"Manager: {p.manager}")
        # print(f"Reports: {p.reports}")
        pprint.pp(person_schema.dump(p))
        # pprint.pp(dir(p))

    for c in Company.query.limit(2):
        print(f"## {c}")
        pprint.pp(company_schema.dump(c))

    # for c in CompanyRole.query.limit(2):
    #     print(f"## {c}")
    #     pprint.pp(company_role_schema.dump(c))
