# Lab 47 · Speech as an agent modality

**Scenario.** Contoso Hotels wants a phone concierge: a caller speaks, the agent understands the request **and the caller's mood**, changes the booking with a tool, and answers by voice. The front desk in Tokyo gets the same answer in Japanese.

**Exam objectives.** D4 › *Implement workflows to convert speech to text and text to speech for agentic interactions*; *integrate speech as an agent modality*; *enable multimodal reasoning from audio inputs*; *translate speech into other languages by using language models*.

**You will learn**
- A voice pipeline: **STT model** (`gpt-4o-mini-transcribe`) → **agent with tools** → **instructable TTS** (`gpt-4o-mini-tts`, style set with `instructions`).
- **Audio reasoning**: an audio-capable model (`gpt-audio-mini`) hears tone, hesitation and emotion that a transcript loses.
- Spoken-reply design: short sentences, no markdown, read back codes.
- LLM translation of the reply, then speak it in Japanese.

## Set up (optional models)
```bash
azd env set DEPLOY_AUDIO_MODELS true && azd provision
```
The lab is skipped until `AUDIO_MODELS_ENABLED=True` is in `.env`. Check the model versions in `infra/core.bicep` against the Foundry model catalog for your region before provisioning.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `audio.speech.create(model, voice, input, instructions, response_format="wav")` | Instructable voice style. |
| 2 | `audio.transcriptions.create(model, file)` | Speech in. |
| 3 | `chat.completions.create(model=gpt-audio-mini, input_audio=...)` | Reason over the audio itself. |
| 4 | Function-call loop with the prompt agent | Voice is just another input to the same agent. |

## Run and test
```bash
./lab run 47 && ./lab validate 47      # one click: ./lab solve 47
```
Listen to `.out/lab47/caller.wav`, `reply.wav` and `reply_ja.wav`.

## Explore: Voice Live
For production phone or voice bots, the **Voice Live API** gives you one low-latency speech-to-speech WebSocket session with noise suppression, echo cancellation, semantic end-of-turn detection, barge-in (interruptions) and optional avatars, and it can drive a Foundry agent. See the Learn module *Develop an Azure Speech Voice Live agent*.

## Exam reflexes
- Natural, interruptible, low-latency voice agent → **Voice Live API**.
- Tone, emotion or background sounds matter → **audio-capable model**, not transcript-only.
- Speech in language A, spoken reply in language B → **speech translation** (lab 46), or **STT → LLM translate → TTS**.
- Domain vocabulary in a voice agent → **phrase list** / **Custom Speech** for the STT stage.

## Clean up
`./lab clean 47` deletes the agent.
