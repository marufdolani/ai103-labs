"""Lab 17 - Chat app with the Responses API: single turn, streaming, stateful multi-turn."""
from labkit import cfg, show
from labkit.clients import openai

INSTRUCTIONS = "You are Contoso's internal IT helpdesk assistant. Be concise."


def single_turn(question: str) -> str:
    # >>> TODO 1: One request with instructions + input; return output_text
    resp = openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS, input=question,
                                     reasoning={"effort": "low"}, max_output_tokens=1500)
    return resp.output_text
    # <<<


def streamed(question: str) -> list[str]:
    # >>> TODO 2: stream=True and collect the text deltas (event.type == 'response.output_text.delta')
    chunks = []
    stream = openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS, input=question,
                                       reasoning={"effort": "low"}, max_output_tokens=1500, stream=True)
    for event in stream:
        if event.type == "response.output_text.delta":
            chunks.append(event.delta)
            print(event.delta, end="", flush=True)
    print()
    return chunks
    # <<<


def chained_turns() -> str:
    # >>> TODO 3: Two turns linked with previous_response_id (server keeps the history)
    first = openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS,
                                      input="Hi, I'm Priya and I manage the Sydney office.",
                                      reasoning={"effort": "low"}, max_output_tokens=800)
    second = openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS,
                                       input="What's my name and which office do I manage?",
                                       previous_response_id=first.id, reasoning={"effort": "low"}, max_output_tokens=800)
    return second.output_text
    # <<<


def conversation_turns() -> tuple[str, int]:
    # >>> TODO 4: Create a conversation object, run two turns inside it, then count its items
    conv = openai().conversations.create(metadata={"lab": "17"})
    openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS, conversation=conv.id,
                              input="My laptop asset tag is LT-5521.", reasoning={"effort": "low"}, max_output_tokens=800)
    last = openai().responses.create(model=cfg("CHAT_MODEL"), instructions=INSTRUCTIONS, conversation=conv.id,
                                     input="Which asset tag did I give you?", reasoning={"effort": "low"},
                                     max_output_tokens=800)
    items = list(openai().conversations.items.list(conv.id))
    openai().conversations.delete(conv.id)
    return last.output_text, len(items)
    # <<<


def main() -> dict:
    show.step("Single turn")
    one = single_turn("How do I reset my MFA device? Two bullet points.")
    show.text("Answer", one)
    show.step("Streaming")
    chunks = streamed("Give me three tips for a faster laptop.")
    show.step("previous_response_id")
    chained = chained_turns()
    show.text("Answer", chained)
    show.step("Conversations API")
    conv_answer, item_count = conversation_turns()
    show.kv({"answer": conv_answer, "items in conversation": item_count})
    return {"single": one, "stream_chunks": len(chunks), "chained": chained,
            "conversation_answer": conv_answer, "conversation_items": item_count}


if __name__ == "__main__":
    show.result(main())
