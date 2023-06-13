from flask import abort
from models import Person, PersonSchema
from query import model_list_query
from utils import dump_single


def read_people(
    column_filter=None,
    q=None,
    limit=0,
    page=0,
    order_by=None,
    sort_dir="asc",
    expand=None,
):
    print(f"q: {q}")
    print(f"page: {page}")
    print(f"limit: {limit}")
    print(f"column_filter: {column_filter}")
    return model_list_query(
        PersonSchema,
        column_filter=column_filter,
        q=q,
        limit=limit,
        page=page,
        order_by=order_by,
        sort_dir=sort_dir,
        expand=expand,
    )


def read_person(pid, expand=None):

    person = Person.query.filter(Person.id == pid).one_or_none()
    if person:
        return dump_single(person, PersonSchema, expand)
    else:
        abort(404, f"Person with id {id} not found")
