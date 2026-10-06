"""Lab 18 - Prompt engineering and generation parameters."""
import openai as openai_sdk

from labkit import cfg, enabled, show
from labkit.clients import aoai, openai

TICKETS = [
    ("The invoice charged us twice this month.", "P3-billing"),
    ("Entire EU region cannot log in since 08:00, sales blocked.", "P1-access"),
    ("Please add dark mode to the dashboard.", "P4-request"),
    ("Two users get 'password expired' even after reset.", "P2-access"),
    ("Production API returns 500 for all customers.", "P1-outage"),
    ("Can we get a copy of last year's invoices?", "P3-billing"),
]
LABELS = "P1-outage, P1-access, P2-access, P3-billing, P4-request"
FEW_SHOT = """Definitions:
- P1-outage: a service is down for many customers.
- P1-access: many users cannot sign in, business blocked.
- P2-access: a few users have sign-in problems.
- P3-billing: invoices, charges, payments.
- P4-request: new features or nice-to-haves.
Examples:
Ticket: "Checkout page down for everyone" -> P1-outage
Ticket: "One user locked out after MFA change" -> P2-access
Ticket: "Refund not received" -> P3-billing
"""


def classify(ticket: str, few_shot: bool) -> str:
    # TODO 1: Use a system instruction with delimiters; add FEW_SHOT definitions/examples when few_shot is True
    raise NotImplementedError("TODO 1: Use a system instruction with delimiters; add FEW_SHOT definitions/examples when few_shot is True  (see README step and solution/ if stuck)")


def accuracy(few_shot: bool) -> float:
    return sum(label in classify(t, few_shot) for t, label in TICKETS) / len(TICKETS)


def truncation() -> dict:
    # TODO 2: Force truncation with a tiny max_output_tokens; read status and incomplete_details.reason
    raise NotImplementedError("TODO 2: Force truncation with a tiny max_output_tokens; read status and incomplete_details.reason  (see README step and solution/ if stuck)")


def verbosity(level: str) -> int:
    # TODO 3: Same prompt with text={'verbosity': level}; return output tokens
    raise NotImplementedError("TODO 3: Same prompt with text={'verbosity': level}; return output tokens  (see README step and solution/ if stuck)")


def temperature_lesson() -> dict:
    # TODO 4: Try temperature on the reasoning chat model; if LEGACY_CHAT_MODEL is set, measure diversity at 0 vs 1.3
    raise NotImplementedError("TODO 4: Try temperature on the reasoning chat model; if LEGACY_CHAT_MODEL is set, measure diversity at 0 vs 1.3  (see README step and solution/ if stuck)")


def main() -> dict:
    show.step("Zero-shot vs few-shot (small model)")
    zero, few = accuracy(False), accuracy(True)
    show.kv({"zero-shot accuracy": zero, "few-shot accuracy": few})
    show.step("max_output_tokens truncation")
    trunc = truncation()
    show.kv(trunc)
    show.step("Verbosity")
    low, high = verbosity("low"), verbosity("high")
    show.kv({"low": low, "high": high})
    show.step("Temperature")
    temp = temperature_lesson()
    show.kv(temp)
    return {"zero_shot": zero, "few_shot": few, "truncation": trunc, "verbosity_low": low, "verbosity_high": high,
            "temperature": temp}


if __name__ == "__main__":
    show.result(main())
