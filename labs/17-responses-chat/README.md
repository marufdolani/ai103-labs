# Lab 17 · Chat app with the Responses API

**Scenario.** Contoso's IT helpdesk wants a chat assistant in its portal: fast first tokens (streaming) and memory of the conversation without the app resending the whole history every turn.

**Exam objectives.** D2 › *Deploy and consume LLMs*; *integrate generative workflows into applications by using Foundry SDKs*; *configure an application to connect to a Foundry project*; *define … conversation-tracking approach*.

**You will learn**
- Responses API basics: `instructions`, `input`, `output_text`, `max_output_tokens`.
- Streaming events (`response.output_text.delta`).
- Two server-side state options: **`previous_response_id`** chaining, or a durable **conversation** object (the same one agents use).

## Set up
Nothing extra.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Single turn with `instructions` + `input`. | The base call everything else builds on. |
| 2 | Streaming: iterate events and print deltas. | Perceived latency drops to time-to-first-token. |
| 3 | Chain two turns with `previous_response_id`. | Stateful without resending history. |
| 4 | Create a conversation, run two turns, list its items, delete it. | Durable, inspectable state you can share across sessions. |

## Run and test
```bash
./lab run 17 && ./lab validate 17      # one click: ./lab solve 17
```

## Explore
- Chat Completions is **stateless**: you resend `messages` each turn. Compare the token bill for a 10-turn chat.
- `store=False` disables server-side storage. Then `previous_response_id` can't work, and that's the privacy trade-off.

## Exam reflexes
- Server-side multi-turn state → **Conversations** (agents) or **`previous_response_id`** (Responses API). Classic **threads → conversations**, **runs → responses**.
- Streaming improves perceived latency, not total latency.

## Clean up
The lab deletes its conversation.
