"""Lab 47 - Speech as an agent modality: voice in -> agent with tools -> voice out, plus reasoning over audio."""
import base64
import json

from azure.ai.projects.models import FunctionTool, PromptAgentDefinition

from labkit import cfg, out_path, show
from labkit.agents import ask, delete_agent
from labkit.clients import aoai, openai, project

AGENT = "lab47-voice-concierge"
STT, TTS, AUDIO = "gpt-4o-mini-transcribe", "gpt-4o-mini-tts", "gpt-audio-mini"
CALLER = "Hi, this is booking B-4471. My flight was delayed again and I need to push check-in to the sixteenth. This is the third time!"
BOOKINGS = {"B-4471": {"guest": "M. Dolan", "hotel": "Shinjuku Gyoen Hotel", "check_in": "2026-11-14"}}
LOOKUP = {"name": "change_check_in", "description": "Change the check-in date of a hotel booking",
          "parameters": {"type": "object", "additionalProperties": False, "required": ["booking_id", "new_date"],
                         "properties": {"booking_id": {"type": "string"},
                                        "new_date": {"type": "string", "description": "ISO date, year 2026"}}}}


def change_check_in(booking_id: str, new_date: str) -> dict:
    if booking_id not in BOOKINGS:
        return {"error": "booking not found"}
    BOOKINGS[booking_id]["check_in"] = new_date
    return {"ok": True, "booking_id": booking_id, "check_in": new_date, "confirmation": "CF-2210"}


def speak(text: str, filename: str, instructions: str) -> bytes:
    # >>> TODO 1: Text to speech with an instructable voice model (style via natural-language instructions), WAV out
    audio = aoai().audio.speech.create(model=TTS, voice="coral", input=text, instructions=instructions,
                                       response_format="wav").read()
    # <<<
    out_path("lab47", filename).write_bytes(audio)
    return audio


def transcribe(audio: bytes, name: str) -> str:
    # >>> TODO 2: Speech to text with a transcription model
    return aoai().audio.transcriptions.create(model=STT, file=(name, audio)).text
    # <<<


def caller_mood(audio: bytes) -> str:
    # >>> TODO 3: Multimodal reasoning on the AUDIO itself (tone of voice), not on the transcript
    resp = aoai().chat.completions.create(model=AUDIO, modalities=["text"], messages=[{"role": "user", "content": [
        {"type": "text", "text": "From the speaker's tone of voice, classify their mood as exactly one word: "
                                 "calm, happy, frustrated or sad."},
        {"type": "input_audio", "input_audio": {"data": base64.b64encode(audio).decode(), "format": "wav"}},
    ]}])
    return resp.choices[0].message.content.strip().lower().strip(".")
    # <<<


def run_agent(agent, text: str, mood: str) -> tuple[str, list[dict]]:
    conv = openai().conversations.create()
    resp = ask(agent, f"[caller mood: {mood}] {text}", conversation=conv.id)
    calls = []
    # >>> TODO 4: Agent turn: execute function calls and feed results back until the agent answers
    for _ in range(4):
        pending = [i for i in resp.output if i.type == "function_call"]
        if not pending:
            break
        outputs = []
        for c in pending:
            args = json.loads(c.arguments)
            result = change_check_in(**args)
            calls.append({"name": c.name, "args": args, "result": result})
            outputs.append({"type": "function_call_output", "call_id": c.call_id, "output": json.dumps(result)})
        resp = ask(agent, outputs, conversation=conv.id)
    # <<<
    openai().conversations.delete(conv.id)
    return resp.output_text, calls


def main() -> dict:
    show.title("1. Caller speaks (synthetic, frustrated voice)")
    caller_audio = speak(CALLER, "caller.wav", "Sound tired and clearly frustrated, sighing slightly.")

    show.title("2. Speech in: transcript + tone from the audio")
    transcript = transcribe(caller_audio, "caller.wav")
    mood = caller_mood(caller_audio)
    show.kv({"transcript": transcript, "mood (from audio)": mood})

    show.title("3. Agent decides and acts")
    delete_agent(AGENT)
    agent = project().agents.create_version(agent_name=AGENT, definition=PromptAgentDefinition(
        model=cfg("CHAT_MODEL"),
        instructions=("You are a hotel voice concierge. Replies are spoken aloud: two short sentences, no lists, "
                      "no markdown. If the caller is frustrated, acknowledge it first. Use change_check_in to change "
                      "dates (year 2026) and read back the confirmation code."),
        tools=[FunctionTool(name=LOOKUP["name"], description=LOOKUP["description"],
                            parameters=LOOKUP["parameters"], strict=True)]))
    reply, calls = run_agent(agent, transcript, mood)
    show.text("Agent reply", reply)

    show.title("4. Speech out, and in Japanese for the Tokyo front desk")
    reply_audio = speak(reply, "reply.wav", "Warm, calm and reassuring, like a five-star concierge.")
    heard = transcribe(reply_audio, "reply.wav")
    ja = openai().responses.create(model=cfg("CHAT_MODEL"), reasoning={"effort": "low"}, max_output_tokens=1500,
                                   instructions="Translate into polite Japanese. Keep codes like CF-2210 unchanged.",
                                   input=reply).output_text.strip()
    speak(ja, "reply_ja.wav", "Polite and calm.")
    show.kv({"reply as heard (round trip)": heard, "Japanese": ja})
    return {"transcript": transcript, "mood": mood, "calls": calls, "reply": reply, "heard": heard,
            "japanese": ja, "booking": BOOKINGS["B-4471"]}


def cleanup() -> None:
    delete_agent(AGENT)


if __name__ == "__main__":
    show.result(main())
