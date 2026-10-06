"""Lab 46 - Speech: SSML text to speech, speech to text (phrase list), fast transcription with diarization,
speech translation. All keyless on the Foundry resource."""
import json
import threading

import azure.cognitiveservices.speech as speechsdk
import requests

from labkit import cfg, out_path, show
from labkit.clients import credential, token

CONFIRMATION = ("Your Contoso Fabrikam booking is confirmed. Check-in is on the fourteenth of November "
                "at Shinjuku Gyoen Hotel.")
DIALOGUE = [("en-US-AndrewMultilingualNeural", "Hello, I'd like to change my booking to the fifteenth of November."),
            ("en-US-AvaMultilingualNeural", "Of course. I've moved your booking to the fifteenth. Anything else?"),
            ("en-US-AndrewMultilingualNeural", "No, that's everything. Thank you very much."),
            ("en-US-AvaMultilingualNeural", "You're welcome. Have a great trip to Tokyo.")]


def speech_config() -> speechsdk.SpeechConfig:
    # TODO 1: Keyless SpeechConfig: custom-domain endpoint + token credential
    raise NotImplementedError("TODO 1: Keyless SpeechConfig: custom-domain endpoint + token credential  (see README step and solution/ if stuck)")


def synthesize(ssml: str, filename: str) -> str:
    path = str(out_path("lab46", filename))
    synth = speechsdk.SpeechSynthesizer(speech_config=speech_config(),
                                        audio_config=speechsdk.audio.AudioOutputConfig(filename=path))
    result = synth.speak_ssml_async(ssml).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"TTS failed: {result.cancellation_details.error_details}")
    return path


def confirmation_ssml() -> str:
    # TODO 2: SSML with a neural voice, slower prosody and a pause; spell the reference with say-as
    raise NotImplementedError("TODO 2: SSML with a neural voice, slower prosody and a pause; spell the reference with say-as  (see README step and solution/ if stuck)")


def dialogue_ssml() -> str:
    voices = "".join(f"<voice name='{v}'>{line}<break time='300ms'/></voice>" for v, line in DIALOGUE)
    return f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>{voices}</speak>"


def transcribe_file(path: str, phrases: list[str] | None = None) -> str:
    """Continuous recognition over a WAV file, optionally boosted with a phrase list."""
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config(),
                                            audio_config=speechsdk.audio.AudioConfig(filename=path),
                                            language="en-US")
    # TODO 3: Add a phrase list (no training) so rare names are recognised
    raise NotImplementedError("TODO 3: Add a phrase list (no training) so rare names are recognised  (see README step and solution/ if stuck)")
    texts, done = [], threading.Event()
    recognizer.recognized.connect(lambda e: texts.append(e.result.text) if e.result.text else None)
    recognizer.session_stopped.connect(lambda e: done.set())
    recognizer.canceled.connect(lambda e: done.set())
    recognizer.start_continuous_recognition()
    done.wait(timeout=120)
    recognizer.stop_continuous_recognition()
    return " ".join(texts)


def fast_transcribe(path: str) -> dict:
    # TODO 4: Fast transcription REST API with diarization (synchronous, multipart: audio + definition)
    raise NotImplementedError("TODO 4: Fast transcription REST API with diarization (synchronous, multipart: audio + definition)  (see README step and solution/ if stuck)")
    phrases = [{"speaker": p.get("speaker"), "text": p["text"]} for p in body.get("phrases", [])]
    return {"text": body["combinedPhrases"][0]["text"], "phrases": phrases,
            "speakers": sorted({p["speaker"] for p in phrases if p["speaker"] is not None})}


def translate_speech(path: str) -> dict:
    # TODO 5: Speech translation: English audio in, French and Japanese text out
    raise NotImplementedError("TODO 5: Speech translation: English audio in, French and Japanese text out  (see README step and solution/ if stuck)")
    if result.reason != speechsdk.ResultReason.TranslatedSpeech:
        raise RuntimeError(f"Translation failed: {result.reason}")
    return {"source": result.text, **dict(result.translations)}


def main() -> dict:
    show.title("Text to speech with SSML")
    confirm_wav = synthesize(confirmation_ssml(), "confirmation.wav")
    dialogue_wav = synthesize(dialogue_ssml(), "dialogue.wav")
    show.ok(f"wrote {confirm_wav} and {dialogue_wav}")

    show.title("Speech to text: without and with a phrase list")
    plain = transcribe_file(confirm_wav)
    boosted = transcribe_file(confirm_wav, phrases=["Contoso", "Fabrikam", "Shinjuku Gyoen"])
    show.text("Plain", plain)
    show.text("Phrase list", boosted)

    show.title("Fast transcription with diarization")
    fast = fast_transcribe(dialogue_wav)
    show.table([[p["speaker"], p["text"]] for p in fast["phrases"]], ["speaker", "text"])

    show.title("Speech translation")
    tr = translate_speech(confirm_wav)
    show.kv(tr)
    return {"plain": plain, "boosted": boosted, "fast": fast, "translation": tr}


if __name__ == "__main__":
    show.result(main())
