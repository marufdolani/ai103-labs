"""Lab 19 - Structured outputs for downstream systems."""
import json
from typing import Literal

from pydantic import BaseModel

from labkit import cfg, show
from labkit.clients import openai

INVOICE_TEXT = """FABRIKAM OFFICE SUPPLY - Invoice INV-2026-0419 - billed in Australian dollars
3 x Ergonomic chair @ 349.00
10 x USB-C dock @ 129.50
1 x Standing desk @ 899.00
Thank you for your business."""

TICKET = ("I've been a customer for six years and this is the third outage this month. Your Sydney data centre "
          "went down again during our end-of-quarter close. Our CFO Maria Chen wants a call by Friday.")


class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float


class Invoice(BaseModel):
    vendor: str
    invoice_number: str
    currency: Literal["AUD", "USD", "EUR"]
    line_items: list[LineItem]
    total: float


INSIGHTS_SCHEMA = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative", "mixed"]},
        "tone": {"type": "string", "description": "one or two words, e.g. frustrated, polite"},
        "topics": {"type": "array", "items": {"type": "string"}},
        "entities": {
            "type": "array",
            "items": {"type": "object",
                      "properties": {"text": {"type": "string"},
                                     "category": {"type": "string", "enum": ["Person", "Location", "Organization", "Role", "DateTime"]}},
                      "required": ["text", "category"], "additionalProperties": False},
        },
        "summary": {"type": "string"},
        "escalate": {"type": "boolean"},
    },
    "required": ["sentiment", "tone", "topics", "entities", "summary", "escalate"],
    "additionalProperties": False,
}


def parse_invoice() -> Invoice:
    # >>> TODO 1: responses.parse with text_format=Invoice; return output_parsed
    resp = openai().responses.parse(model=cfg("CHAT_MODEL"), instructions="Extract the invoice. Compute total = sum of quantity * unit_price.",
                                    input=INVOICE_TEXT, text_format=Invoice, reasoning={"effort": "low"},
                                    max_output_tokens=3000)
    return resp.output_parsed
    # <<<


def ticket_insights() -> dict:
    # >>> TODO 2: Raw json_schema format with strict=True; json.loads the output_text
    resp = openai().responses.create(
        model=cfg("CHAT_MODEL"),
        instructions="Analyze the customer ticket.",
        input=TICKET,
        text={"format": {"type": "json_schema", "name": "ticket_insights", "schema": INSIGHTS_SCHEMA, "strict": True}},
        reasoning={"effort": "low"},
        max_output_tokens=3000,
    )
    return json.loads(resp.output_text)
    # <<<


def json_mode() -> dict:
    # >>> TODO 3: JSON mode (type json_object) for contrast: valid JSON, but no schema guarantee
    resp = openai().responses.create(model=cfg("CHAT_MODEL"), input=f"Return JSON describing this ticket: {TICKET}",
                                     text={"format": {"type": "json_object"}}, reasoning={"effort": "low"},
                                     max_output_tokens=3000)
    return json.loads(resp.output_text)
    # <<<


def main() -> dict:
    invoice = parse_invoice()
    show.title("Invoice (Pydantic-validated)")
    show.table([[li.description, li.quantity, li.unit_price] for li in invoice.line_items], ["item", "qty", "unit"])
    computed = round(sum(li.quantity * li.unit_price for li in invoice.line_items), 2)
    show.kv({"vendor": invoice.vendor, "number": invoice.invoice_number, "currency": invoice.currency,
             "total (model)": invoice.total, "total (computed)": computed})

    insights = ticket_insights()
    show.title("Ticket insights (strict JSON schema)")
    show.kv(insights)
    loose = json_mode()
    show.title("JSON mode keys (no schema)")
    show.kv({"keys": sorted(loose)})
    return {"invoice": invoice.model_dump(), "computed_total": computed, "insights": insights,
            "json_mode_keys": sorted(loose)}


if __name__ == "__main__":
    show.result(main())
