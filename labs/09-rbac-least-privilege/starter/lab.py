"""Lab 09 - Least-privilege RBAC for AI teams."""
from fnmatch import fnmatch

from labkit import cfg, show
from labkit.clients import arm

# Ordered from least to most privileged.
ROLES = {
    "Foundry User": "53ca6127-db72-4b80-b1b0-d745d6d5456d",
    "Foundry Project Manager": "eadc314b-1a2d-4efa-be10-5d325db5065e",
    "Foundry Account Owner": "e47c6f54-e4a2-4754-9501-8e0985b135e1",
    "Foundry Owner": "c883944f-8b7b-4483-af10-35834be79c4a",
}

OPERATIONS = {
    "build_agents": ("data", "Microsoft.CognitiveServices/accounts/AIServices/agents/write"),
    "call_models": ("data", "Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action"),
    "deploy_models": ("control", "Microsoft.CognitiveServices/accounts/deployments/write"),
    "create_projects": ("control", "Microsoft.CognitiveServices/accounts/projects/write"),
    "assign_roles": ("control", "Microsoft.Authorization/roleAssignments/write"),
}


def fetch_role(role_id: str) -> dict:
    # TODO 1: GET /subscriptions/{sub}/providers/Microsoft.Authorization/roleDefinitions/{id} and return the first permissions block
    raise NotImplementedError("TODO 1: GET /subscriptions/{sub}/providers/Microsoft.Authorization/roleDefinitions/{id} and return the first permissions block  (see README step and solution/ if stuck)")


def _match(op: str, patterns: list[str]) -> bool:
    return any(fnmatch(op.lower(), p.lower()) for p in patterns)


def allows(perms: dict, operation: str) -> bool:
    kind, op = OPERATIONS[operation]
    # TODO 2: Allowed if it matches actions/dataActions and does NOT match notActions/notDataActions
    raise NotImplementedError("TODO 2: Allowed if it matches actions/dataActions and does NOT match notActions/notDataActions  (see README step and solution/ if stuck)")


def least_privilege(needs: list[str], role_perms: dict[str, dict]) -> str | None:
    # TODO 3: Return the first role (in ROLES order) that allows every operation in needs
    raise NotImplementedError("TODO 3: Return the first role (in ROLES order) that allows every operation in needs  (see README step and solution/ if stuck)")


def main() -> dict:
    role_perms = {name: fetch_role(rid) for name, rid in ROLES.items()}

    show.title("Capability matrix (computed from live role definitions)")
    matrix = {name: {op: allows(p, op) for op in OPERATIONS} for name, p in role_perms.items()}
    show.table([[name, *("yes" if matrix[name][op] else "-" for op in OPERATIONS)] for name in ROLES],
               ["role", *OPERATIONS])

    requests_ = {
        "developer": ["build_agents", "call_models"],
        "team_lead": ["build_agents", "assign_roles"],
        "platform_admin": ["deploy_models", "create_projects"],
        "full_stack_admin": ["build_agents", "deploy_models"],
    }
    picks = {persona: least_privilege(needs, role_perms) for persona, needs in requests_.items()}
    show.title("Least-privilege picks")
    show.kv(picks)

    show.step("Your role assignments on the Foundry resource")
    # TODO 4: List role assignments at the Foundry resource scope (atScope filter) and collect role definition IDs
    raise NotImplementedError("TODO 4: List role assignments at the Foundry resource scope (atScope filter) and collect role definition IDs  (see README step and solution/ if stuck)")
    names = {v: k for k, v in ROLES.items()}
    show.kv({"assigned roles at this scope": [names.get(r, r) for r in mine]})

    return {"matrix": matrix, "picks": picks, "assigned_role_ids": mine}


if __name__ == "__main__":
    show.result(main())
