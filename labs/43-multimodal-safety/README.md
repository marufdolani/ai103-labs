# Lab 43 · Responsible AI for images

**Scenario.** Contoso's helpdesk accepts screenshots, and Marketing publishes AI-generated images. You must moderate images, defend against instructions hidden in screenshot text, label AI-generated media, and enforce brand rules.

**Exam objectives.** D3 › *Implement filters to classify unsafe or disallowed visual content*; *detect and mitigate indirect prompt injection by using embedded text in images*; *enforce visual policy rules, such as applying watermarks, flagging prohibited symbols, upholding brand usage requirements*.

**You will learn**
- Content Safety **image analysis** (hate, sexual, violence, self-harm with severity levels).
- Treating text inside images as an **indirect attack** channel: transcribe → Prompt Shields (documents) → defensive instructions.
- Visible watermarks + embedded provenance metadata (and C2PA credentials on generated images, lab 39).
- Policy checks as structured vision output (logo present, prohibited symbols, inappropriate content).

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `image:analyze` moderation. | Block unsafe uploads and generations. |
| 2 | Screenshot guard: transcribe, shield, answer with spotlighted instructions. | Multimodal prompt injection is real. |
| 3 | Watermark + PNG provenance metadata. | Transparency for AI-generated media. |
| 4 | Brand policy check with `responses.parse`. | Turn written policy into enforceable checks. |

## Run and test
```bash
./lab run 43 && ./lab validate 43      # one click: ./lab solve 43
```

## Explore
- Guardrails on a deployment also apply to **image inputs**. Configure image harm thresholds in lab 11's policy.
- Train a custom category in Content Safety for brand-specific prohibited imagery.

## Exam reflexes
- Unsafe image content → **Content Safety image moderation / guardrails**. Hidden instructions in image text → **indirect prompt injection** defence (Prompt Shields on extracted text + spotlighting).
- Label AI media → **watermarks + C2PA provenance**. Brand rules → **classification checks** (Content Understanding classify fields or vision model + schema).

## Clean up
Delete `.out/lab43`.
