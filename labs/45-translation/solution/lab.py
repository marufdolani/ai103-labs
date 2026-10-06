"""Lab 45 - Translate text and documents: Translator (fast, glossary-aware) and LLM translation (tone, register)."""
import time

from azure.core.exceptions import HttpResponseError

from azure.ai.translation.document import DocumentTranslationClient, SingleDocumentTranslationClient
from azure.ai.translation.document.models import DocumentTranslateContent, TranslationGlossary
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import TranslateInputItem, TranslationTarget

from labkit import cfg, show
from labkit.clients import blob_service, credential, openai

NOTICE = "Your Contoso Cloud subscription renews on 1 November. Please update your payment details to avoid interruption."
GERMAN = "Der Vertrag endet am 30. Juni. Bitte kontaktieren Sie Contoso Cloud für eine Verlängerung."
POLICY_HTML = ("<html><body><h1>Remote work policy</h1><p>Employees may work remotely up to three days a week. "
               "Contoso Cloud accounts must use multi-factor authentication.</p></body></html>")
GLOSSARY_TSV = "Contoso Cloud\tContoso Cloud\nremote work\ttélétravail\n"   # source<TAB>target: keep the brand untranslated
SRC, OUT = "translate-src", "translate-out"


def text_client() -> TextTranslationClient:
    # >>> TODO 1: Keyless Translator client on the Foundry resource (custom endpoint + Entra ID, no trailing slash)
    return TextTranslationClient(endpoint=cfg("FOUNDRY_ENDPOINT").rstrip("/"), credential=credential())
    # <<<


def translate_text() -> dict:
    client = text_client()
    # >>> TODO 2: One call, three target languages, source auto-detected (no from_language)
    items = client.translate(body=[GERMAN], to_language=["en", "fr", "ja"])
    detected = items[0].detected_language.language
    multi = {t.language: t.text for t in items[0].translations}
    # <<<
    return {"detected": detected, "translations": multi}


def translate_with_llm() -> dict:
    """LLM-powered translation: first via Translator targeting your model deployment, else via the Responses API."""
    # >>> TODO 3: Formal Japanese for a customer notice. Try Translator's LLM option (deployment_name + tone), fall back to a prompt
    try:
        item = TranslateInputItem(text=NOTICE, targets=[TranslationTarget(
            language="ja", deployment_name=cfg("LARGE_MODEL"), tone="formal", allow_fallback=False)])
        out = text_client().translate(body=[item])[0].translations[0].text
        path = "translator+llm"
    except Exception as exc:  # noqa: BLE001 - the LLM option isn't available for every model/region
        show.warn(f"Translator LLM option unavailable ({type(exc).__name__}); using the Responses API")
        out = openai().responses.create(
            model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=2000,
            instructions=("Translate into Japanese using formal keigo suitable for a customer notice. "
                          "Keep the product name 'Contoso Cloud' in English. Return only the translation."),
            input=NOTICE).output_text.strip()
        path = "responses-api"
    # <<<
    return {"path": path, "text": out}


def translate_document_sync() -> str:
    # >>> TODO 4: Single-document translation (synchronous, no storage) with a glossary that keeps the brand name
    client = SingleDocumentTranslationClient(endpoint=cfg("FOUNDRY_ENDPOINT"), credential=credential())
    content = DocumentTranslateContent(
        document=("policy.html", POLICY_HTML.encode(), "text/html"),
        glossary=[("glossary.tsv", GLOSSARY_TSV.encode(), "text/tab-separated-values")])
    return b"".join(client.translate(body=content, target_language="fr")).decode("utf-8")
    # <<<


def translate_documents_batch() -> list[dict]:
    """Batch Document Translation: Blob container in, Blob container out. The Foundry resource's managed identity
    reads and writes storage (Storage Blob Data Contributor), so no SAS tokens are needed."""
    blobs = blob_service()
    run = time.strftime("%Y%m%d%H%M%S")
    src = blobs.get_container_client(SRC)
    src.upload_blob(f"lab45/{run}/policy.html", POLICY_HTML.encode(), overwrite=True)
    src.upload_blob(f"lab45/{run}/notice.txt", NOTICE.encode(), overwrite=True)
    src.upload_blob(f"glossaries/lab45-fr.tsv", GLOSSARY_TSV.encode(), overwrite=True)
    base = cfg("STORAGE_BLOB_ENDPOINT").rstrip("/")
    # >>> TODO 5: begin_translation(source container, target container, 'fr', prefix=this run, glossary) and wait
    client = DocumentTranslationClient(endpoint=cfg("FOUNDRY_ENDPOINT"), credential=credential())
    poller = client.begin_translation(
        f"{base}/{SRC}", f"{base}/{OUT}", "fr", prefix=f"lab45/{run}/",
        glossaries=[TranslationGlossary(glossary_url=f"{base}/{SRC}/glossaries/lab45-fr.tsv", file_format="tsv")])
    statuses = [{"source": d.source_document_url.rsplit("/", 1)[-1], "status": str(d.status),
                 "chars": d.characters_charged} for d in poller.result()]
    # <<<
    return statuses


def main() -> dict:
    show.title("Text translation")
    text = translate_text()
    show.kv({"detected": text["detected"], **text["translations"]})

    show.title("LLM-powered translation with tone")
    llm = translate_with_llm()
    show.kv(llm)

    show.title("Single-document translation (sync) with glossary")
    html_fr, doc_error = "", ""
    try:
        html_fr = translate_document_sync()
        show.text("French HTML", html_fr, 500)
    except HttpResponseError as exc:  # e.g. document translation not offered on this resource type/region
        doc_error = f"{exc.status_code}: {exc.message}"
        show.warn(doc_error)

    show.title("Batch Document Translation (async, Blob to Blob, managed identity)")
    batch, batch_error = [], ""
    try:
        batch = translate_documents_batch()
        show.table([[b["source"], b["status"], b["chars"]] for b in batch], ["document", "status", "chars charged"])
    except HttpResponseError as exc:
        batch_error = f"{exc.status_code}: {exc.message}"
        show.warn(batch_error)
    return {"text": text, "llm": llm, "document_fr": html_fr, "document_error": doc_error,
            "batch": batch, "batch_error": batch_error}


if __name__ == "__main__":
    show.result(main())
