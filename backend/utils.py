from models import (
    Person,
    Company,
    Location,
    people_schema,
    person_schema,
    company_schema,
    location_schema,
)
from sqlalchemy import or_, and_, func


def expand_attribute(obj, model, attribute):
    if not attributes:
        pass


def dump_expanded(objs, schema, expand_attrs):

    if expand_attrs:
        expandable_attrs = schema.Meta.model.expandable
        expand = [a for a in expand_attrs if a in expandable_attrs]

    if not expand:
        return schema(many=True).dump(objs)

    expanded_objs = []
    for obj in objs:

        obj_dict = schema().dump(obj)

        for e_attr in expand:
            # print("Expanding", e_attr)
            e_schema = eval(expandable_attrs[e_attr])
            if e_attr in obj_dict:
                # print(f"Attr {e_attr} is in the obj_dict")
                # if it's None or empty, just continue
                if not obj_dict[e_attr]:
                    # print(f"attr value is empty or none")
                    continue

                if isinstance(obj_dict[e_attr], list):
                    # print(f"{e_attr} is a list")
                    expanded_list = []
                    for attr_inst in obj_dict[e_attr]:
                        # print(f"{e_attr} value is {obj_dict[e_attr]}")
                        attr_inst = e_schema.Meta.model.query.get(attr_inst)
                        if attr_inst:
                            expanded_list.append(e_schema.dump(attr_inst))
                    obj_dict[e_attr] = expanded_list
                else:
                    # print(f"{e_attr} is a single, value is {obj_dict[e_attr]}")
                    # print("Model is ", e_schema.Meta.model)
                    attr_inst = e_schema.Meta.model.query.get(obj_dict[e_attr])
                    if attr_inst:
                        obj_dict[e_attr] = e_schema.dump(attr_inst)
        expanded_objs.append(obj_dict)

    return expanded_objs


def dump_list(objs, schema, expand, meta):

    if expand:
        data = dump_expanded(objs, schema, expand.split(","))
    else:
        data = schema(many=True).dump(objs)

    return {
        "_meta": meta,
        "data": data,
    }


def dump_single(obj, schema, expand):

    if expand:
        return dump_expanded(obj, schema, expand.split(","))
    else:
        return schema().dump(obj)
