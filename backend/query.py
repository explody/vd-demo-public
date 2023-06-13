from flask import make_response, abort
from sqlalchemy import or_, and_, desc, text, func
from utils import dump_list


def model_list_query(
    schema,
    column_filter=None,
    q=None,
    limit=0,
    page=0,
    order_by=None,
    sort_dir="asc",
    expand=None,
):

    model = schema.Meta.model

    if page <= 1:
        offset = 0
    else:
        offset = (page - 1) * limit

    print(f"offset: {offset}")
    search_query = model.query
    total_count = search_query.count()

    if limit == 0:
        limit = total_count

    if order_by and order_by != "company.name":
        search_query = search_query.order_by(text(f"{order_by} {sort_dir}"))

    if column_filter and ":" in column_filter:
        search_query = column_filters(model, search_query, column_filter)

    if q and len(q) > 1:
        search_terms = q.split()

        filter = []
        for term in search_terms:
            for searchable_field in model.searchable:
                filter.append(getattr(model, searchable_field).ilike(f"%{term}%"))

        unpaged_count = search_query.filter(or_(*filter)).count()
        search_query = search_query.filter(or_(*filter)).limit(limit).offset(offset)
    else:
        unpaged_count = search_query.filter().count()
        search_query = search_query.limit(limit).offset(offset)

    meta = {
        "total_count": total_count,
        "count": unpaged_count,
        "page": page,
        "limit": limit,
    }

    results = search_query.all()

    # custom sorting on fields that are hard to do in SQL
    if order_by == "company.name":
        sorted_results = sorted(results, key=lambda x: x.primary_company.name)
        if sort_dir == "desc":
            sorted_results.reverse()
        return dump_list(sorted_results, schema, expand, meta)

    return dump_list(results, schema, expand, meta)


def column_filters(model, query, filters):

    if "," in filters:
        column_filters = filters.split(",")
    else:
        column_filters = [filters]

    for column_filter in column_filters:
        if ".." in column_filter:
            join_to, multi_attrs = column_filter.split("..")

            joined_filter = {}
            for attrval in multi_attrs.split("|"):
                attr, val = attrval.split(":")
                joined_filter[attr] = val

            query = query.join(getattr(model, join_to)).filter_by(**joined_filter)
        elif "." in column_filter:
            join_to, single_attr = column_filter.split(".")
            attr, val = single_attr.split(":")
            query = query.join(getattr(model, join_to)).filter_by(
                **{f"{attr}": f"{val}"}
            )
        else:
            column, val = column_filter.split(":")
            query = query.filter(
                and_(func.lower(getattr(model, column)) == func.lower(val))
            )

    return query
