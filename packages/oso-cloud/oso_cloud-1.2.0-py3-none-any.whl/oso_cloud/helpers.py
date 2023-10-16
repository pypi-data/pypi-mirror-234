from . import api


def to_value(instance):
    if isinstance(instance, api.Value):
        return instance

    if instance is None:
        return api.Value(None, None)
    if isinstance(instance, str):
        if instance == "":
            raise TypeError(
                "Oso: Instance cannot be an empty string. "
                + "For wildcards, use the empty dict ({}) or None."
            )
        return api.Value("String", instance)
    if "id" not in instance or instance["id"] is None:
        if "type" not in instance or instance["type"] is None:
            return api.Value(None, None)
        return api.Value(instance["type"], None)

    if "type" not in instance or instance["type"] is None:
        raise TypeError(f"Oso: Instances with an ID must also have a type: {instance}")
    return api.Value(instance["type"], instance["id"])


def from_value(value):
    if isinstance(value, dict):
        return value
    if value.type == "String":
        return value.id
    if value.type is None and value.id is None:
        return None
    return {"id": value.id, "type": value.type}


def param_to_fact(param):
    return api.Fact(param["name"], [to_value(a) for a in param["args"]])


def map_params_to_facts(params):
    if not params:
        return []
    return [param_to_fact(param) for param in params]


def fact_to_param(fact):
    if isinstance(fact, api.Fact):
        return {"name": fact.predicate, "args": [from_value(a) for a in fact.args]}
    assert False


def map_facts_to_params(facts):
    if not facts:
        return []
    return [fact_to_param(fact) for fact in facts]
