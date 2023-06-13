# Intended to be run by django management shell

from models import Person, Location, Company, CompanyRole, LocationTenancy
from factories import PersonFactory, LocationFactory, CompanyFactory
import factory
import glob
import os
import random
from sqlalchemy.sql.expression import func


from config import app, db


def create_rand_amount(max, factory, qs):
    return [qs.add(factory()) for _ in range(random.randrange(1, max))]


# def assign_images(instance):
#     randimg_start = random.randint(0, len(available_images) - 1)
#     randimg_end = random.randint(0, len(available_images) - 1) + randimg_start
#     for img in available_images[randimg_start:randimg_end]:
#         instance.collection.images.add(img)
#     instance.primary_image = available_images[randimg_start]
#     instance.save()


print("Creating people and related objects")
with app.app_context():

    for c in range(1, 6):
        LocationFactory()

    for c in range(1, 11):
        icon = "https://placehold.co/50x50"
        logo = "https://placehold.co/250x100"

        location = Location.query.order_by(func.random()).first()
        location2 = Location.query.order_by(func.random()).first()
        while location2.id == location.id:
            location2 = Location.query.order_by(func.random()).first()

        c = CompanyFactory(icon=icon, logo=logo)

        tenancy1 = LocationTenancy(location_id=location.id, primary=True)
        tenancy2 = LocationTenancy(location_id=location2.id)

        c.locations.append(tenancy1)
        c.locations.append(tenancy2)

    for c in range(1, 1001):
        company = Company.query.order_by(func.random()).first()
        office = Location.query.order_by(func.random()).first()

        managers = [1, 2, 3, 4, 5]

        if 20 > c > 5:
            manager = Person.query.filter_by(id=random.choice(managers)).first()
        elif c > 19:
            manager = Person.query.filter_by(id=random.choice(range(18, c))).first()
        else:
            manager = None

        photo_url = "https://placehold.co/50x50"

        if manager:
            person = PersonFactory(
                assigned_office_id=office.id, manager_id=manager.id, photo_url=photo_url
            )
        else:
            person = PersonFactory(assigned_office_id=office.id, photo_url=photo_url)

        role = CompanyRole(primary=True)
        role.person_id = person.id
        company.people.append(role)

        for i in range(1, random.choice(range(1, 5))):

            addtl_company = Company.query.order_by(func.random()).first()
            if (
                CompanyRole.query.filter_by(
                    person_id=person.id, company_id=addtl_company.id
                ).count()
                == 0
            ):
                role = CompanyRole(primary=False)
                role.person_id = person.id
                addtl_company.people.append(role)
        # person.companies.append(company)
