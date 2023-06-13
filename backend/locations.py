from flask import make_response, abort
from models import Location, location_schema, locations_schema


def read_all():
    locations = Location.query.all()
    return locations_schema.dump(locations)


def read_company(lid):
    location = Location.query.filter(Location.id == lid).one_or_none()

    if location is not None:
        return location_schema.dump(location)
    else:
        abort(404, f"Location with id {id} not found")
