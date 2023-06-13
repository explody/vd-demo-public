from flask import make_response, abort
from models import Company, CompanySchema
from query import model_list_query
from utils import dump_single


def read_companies(
    column_filter=None,
    q=None,
    limit=0,
    page=0,
    order_by=None,
    sort_dir="asc",
    expand=None,
):

    return model_list_query(
        CompanySchema,
        column_filter=column_filter,
        q=q,
        limit=limit,
        page=page,
        order_by=order_by,
        sort_dir=sort_dir,
        expand=expand,
    )


def read_company(pid, expand=None):

    person = Company.query.filter(Company.id == pid).one_or_none()
    if person:
        return dump_single(person, CompanySchema, expand)
    else:
        abort(404, f"Company with id {id} not found")
