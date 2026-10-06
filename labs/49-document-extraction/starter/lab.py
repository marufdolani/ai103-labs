"""Lab 49 - Document extraction: Document Intelligence (deterministic OCR/layout/prebuilt models) vs
Content Understanding (schema-driven extract/classify/generate with grounding, markdown for RAG)."""
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from PIL import Image, ImageDraw

from labkit import cfg, out_path, show
from labkit.clients import credential
from labkit.cu import analyze_bytes, create_analyzer, delete_analyzer, field_value, set_defaults
from labkit.images import _font, to_bytes

ANALYZER = "lab49_invoice"
TOTAL = 1284.00


def invoice_image() -> bytes:
    """A scanned-looking invoice with a table and two checkboxes (Paid ticked, Disputed empty)."""
    img = Image.new("RGB", (1240, 1650), "white")
    d = ImageDraw.Draw(img)
    f, big = _font(26), _font(40)
    d.text((80, 70), "Fabrikam Industrial Supply", fill="black", font=big)
    d.text((80, 130), "200 Harbour St, Sydney NSW 2000", fill="black", font=f)
    d.text((820, 70), "INVOICE", fill="black", font=big)
    for i, (k, v) in enumerate([("Invoice #", "FAB-20931"), ("Date", "2026-10-02"), ("Due", "2026-11-01"),
                                ("PO", "PO-55812")]):
        d.text((820, 140 + i * 40), f"{k}: {v}", fill="black", font=f)
    d.text((80, 260), "Bill to: Contoso Ltd, 1 Microsoft Way, Redmond WA 98052", fill="black", font=f)
    y = 360
    d.rectangle([80, y, 1160, y + 50], outline="black", width=2)
    for x, h in [(95, "Description"), (700, "Qty"), (820, "Unit price"), (1010, "Amount")]:
        d.text((x, y + 12), h, fill="black", font=f)
    rows = [("Valve XJ-4471-B", 12, 85.00), ("Gasket kit G-200", 20, 9.50), ("Torque wrench 40-60Nm", 1, 72.00)]
    for i, (desc, qty, price) in enumerate(rows):
        ry = y + 50 + i * 50
        d.rectangle([80, ry, 1160, ry + 50], outline="black", width=1)
        for x, val in [(95, desc), (700, str(qty)), (820, f"{price:.2f}"), (1010, f"{qty * price:.2f}")]:
            d.text((x, ry + 12), val, fill="black", font=f)
    subtotal = sum(q * p for _, q, p in rows)          # 1,282.00 -> + 2.00 freight below
    d.text((820, 600), f"Subtotal: {subtotal:.2f}", fill="black", font=f)
    d.text((820, 640), "Freight: 2.00", fill="black", font=f)
    d.text((820, 690), f"TOTAL AUD: {TOTAL:,.2f}", fill="black", font=big)
    d.text((80, 800), "Payment status:", fill="black", font=f)
    for i, (label, ticked) in enumerate([("Paid", True), ("Disputed", False)]):
        x = 320 + i * 220
        d.rectangle([x, 795, x + 32, 827], outline="black", width=3)
        if ticked:
            d.line([x + 4, 799, x + 28, 823], fill="black", width=4)
            d.line([x + 28, 799, x + 4, 823], fill="black", width=4)
        d.text((x + 45, 800), label, fill="black", font=f)
    d.text((80, 900), "Notes: Late delivery of the torque wrench; vendor waived freight surcharge on next order.",
           fill="black", font=f)
    data = to_bytes(img, "PNG")
    out_path("lab49", "invoice.png").write_bytes(data)
    return data


def di_client() -> DocumentIntelligenceClient:
    # TODO 1: Keyless Document Intelligence client on the Foundry resource
    raise NotImplementedError("TODO 1: Keyless Document Intelligence client on the Foundry resource  (see README step and solution/ if stuck)")


def document_intelligence(doc: bytes) -> dict:
    client = di_client()
    # TODO 2: prebuilt-invoice: typed fields with confidence
    raise NotImplementedError("TODO 2: prebuilt-invoice: typed fields with confidence  (see README step and solution/ if stuck)")
    # TODO 3: prebuilt-layout with Markdown output: tables + checkbox (selection mark) states
    raise NotImplementedError("TODO 3: prebuilt-layout with Markdown output: tables + checkbox (selection mark) states  (see README step and solution/ if stuck)")
    return {"invoice": invoice, "markdown": layout.content, "tables": len(layout.tables or []), "selection_marks": marks}


def content_understanding(doc: bytes) -> dict:
    set_defaults()
    # TODO 4: Custom analyzer on prebuilt-document: extract (literal), classify (from the checkboxes), generate
    raise NotImplementedError("TODO 4: Custom analyzer on prebuilt-document: extract (literal), classify (from the checkboxes), generate  (see README step and solution/ if stuck)")
    return {
        "fields": {k: field_value(v) for k, v in fields.items()},
        "confidence": {k: v.get("confidence") for k, v in fields.items()},
        "grounding": {k: v.get("source") for k, v in fields.items() if v.get("source")},
        "markdown": content.get("markdown", ""),
    }


def main() -> dict:
    doc = invoice_image()
    show.title("Document Intelligence")
    di = document_intelligence(doc)
    show.kv(di["invoice"])
    show.kv({"tables": di["tables"], "checkboxes": di["selection_marks"]})
    show.text("Layout markdown", di["markdown"], 500)

    show.title("Content Understanding")
    cu = content_understanding(doc)
    show.table([[k, v, cu["confidence"].get(k), "yes" if k in cu["grounding"] else ""] for k, v in cu["fields"].items()],
               ["field", "value", "confidence", "grounded"])
    return {"di": di, "cu": cu}


def cleanup() -> None:
    delete_analyzer(ANALYZER)


if __name__ == "__main__":
    show.result(main())
