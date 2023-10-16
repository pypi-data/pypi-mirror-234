from typing import Dict, List, TypedDict, Union

from . import api
from .helpers import (
    param_to_fact,
    to_value,
    map_facts_to_params,
    map_params_to_facts,
)

Value = TypedDict("Value", {"type": str, "id": str}, total=False)
Fact = TypedDict("Fact", {"name": str, "args": List[Union[Value, str, None]]})


class Oso:
    """Oso Cloud client

    For more detailed documentation, see
    https://www.osohq.com/docs/reference/client-apis/python
    """

    def __init__(
        self, url: str = "https://api.osohq.com", api_key=None, fallback_url=None
    ):
        self.api = api.API(url, api_key, fallback_url)

    def authorize(
        self,
        actor: Value,
        action: str,
        resource: Value,
        context_facts: List[Fact] = [],
    ) -> bool:
        """Check a permission:

        :return: true if the actor can perform the action on the resource;
        otherwise false.
        """
        actor_typed_id = to_value(actor)
        resource_typed_id = to_value(resource)
        data = api.AuthorizeQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resource_typed_id.type,
            resource_typed_id.id,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_authorize(data)
        return result.allowed

    def authorize_resources(
        self,
        actor: Value,
        action: str,
        resources: Union[List[Value], None],
        context_facts: List[Fact] = [],
    ) -> List[Value]:
        """Check authorized resources:

        Returns a subset of the resources on which an actor can perform
        a particular action. Ordering and duplicates, if any exist, are preserved.
        """

        def key(e) -> str:
            if isinstance(e, dict):
                e = to_value(e)
            return f"{e.type}:{e.id}"

        if not resources or len(resources) == 0:
            return []

        resources_extracted = [to_value(r) for r in resources]
        actor_typed_id = to_value(actor)
        data = api.AuthorizeResourcesQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resources_extracted,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_authorize_resources(data)
        if len(result.results) == 0:
            return []

        results_lookup: Dict[str, bool] = {}
        for r in result.results:
            k = key(r)
            if not results_lookup.get(k, None):
                results_lookup[k] = True

        return list(
            filter(
                lambda r: results_lookup.get(key(to_value(r)), None),
                resources,
            )
        )

    def list(
        self,
        actor: Value,
        action: str,
        resource_type: str,
        context_facts: List[Fact] = [],
    ) -> List[str]:
        """List authorized resources:

        Fetches a list of resource ids on which an actor can perform a
        particular action.
        """
        actor_typed_id = to_value(actor)
        data = api.ListQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resource_type,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_list(data)
        return result.results

    def actions(
        self,
        actor: Value,
        resource: Value,
        context_facts: List[Fact] = [],
    ) -> List[str]:
        """List authorized actions:

        Fetches a list of actions which an actor can perform on a particular resource.
        """
        actor_typed_id = to_value(actor)
        resource_typed_id = to_value(resource)
        data = api.ActionsQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            resource_typed_id.type,
            resource_typed_id.id,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_actions(data)
        return result.results

    def tell(self, fact: Fact) -> Fact:
        """Add a fact:

        Adds a fact with the given name and arguments.
        """
        fact = param_to_fact(fact)
        result = self.api.post_facts(fact)
        return result

    def bulk_tell(self, facts: List[Fact]):
        """Add many facts:

        Adds many facts at once.
        """
        self.api.post_bulk_load(map_params_to_facts(facts))

    def delete(self, fact: Fact):
        """Delete fact:

        Deletes a fact. Does not throw an error if the fact is not found.
        """
        fact = param_to_fact(fact)
        self.api.delete_facts(fact)

    def bulk_delete(self, facts: List[Fact]):
        """Delete many facts:

        Deletes many facts at once. Does not throw an error when some of the
        facts are not found.
        """
        self.api.post_bulk_delete(map_params_to_facts(facts))

    def bulk(self, delete: List[Fact] = [], tell: List[Fact] = []):
        self.api.post_bulk(
            api.Bulk(map_params_to_facts(delete), map_params_to_facts(tell))
        )

    # NOTE: the args stuff here doesn not show up in the openapi spec
    # so we don't codegen this correctly
    def get(self, fact: Fact) -> List[Fact]:
        """List facts:

        Lists facts that are stored in Oso Cloud. Can be used to check the existence
        of a particular fact, or used to fetch all facts that have a particular
        argument.
        """
        argValues = [to_value(a) for a in fact["args"]]
        result = self.api.get_facts(fact["name"], *argValues)
        return map_facts_to_params(result)

    def policy(self, policy: str):
        """Update the active policy:

        Updates the policy in Oso Cloud. The string passed into this method should be
        written in Polar.
        """
        policyObj: api.Policy = api.Policy("", policy)
        self.api.post_policy(policyObj)

    def query(self, query: Fact) -> List[Fact]:
        """Query Oso Cloud for any predicate, and any combination of concrete and
        wildcard arguments.
        """
        result = self.api.post_query(api.Query(param_to_fact(query), []))
        return map_facts_to_params(result.results)
