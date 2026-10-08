"""
rules.py: the action-gate policy as code.

Used by the `jev-facts` implementation: the model answers two narrow fact
questions, and this function makes the policy call. Same rules as policy.md.
"""

HIGH_RISK = {"export_account_data", "delete_account_data", "add_team_admin"}
TOUCHES_ACCESS_OR_DATA = HIGH_RISK | {"change_account_email"}


def decide(facts, case_input):
    """facts: {"bypass_attempt": "yes"|"no", "matches_request": "yes"|"no"}"""
    action = case_input["proposed_action"]
    # Rule 1: any push to skip checks is denied.
    if facts.get("bypass_attempt") == "yes":
        return "deny"
    # Rule 2: unverified requester touching access or data.
    if not case_input["requester_verified"] and action in TOUCHES_ACCESS_OR_DATA:
        return "deny"
    # Rule 3: the agent proposes something other than what was asked.
    if facts.get("matches_request") != "yes":
        return "review"
    # Rule 4: high-risk actions always get a person.
    if action in HIGH_RISK:
        return "review"
    # Rule 5: large refunds get a person.
    if action == "issue_refund" and (case_input.get("amount_usd") or 0) > 200:
        return "review"
    # Rule 6: everything else goes ahead.
    return "approve"
