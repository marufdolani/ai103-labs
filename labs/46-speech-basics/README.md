# Lab 46 · Speech to text, text to speech, SSML, translation

**Scenario.** Contoso Travel's booking line needs spoken confirmations with correct pacing, transcripts of calls with **who said what**, and live English-to-French/Japanese translation for agents in Tokyo.

**Exam objectives.** D4 › *Implement workflows to convert speech to text and text to speech*; *integrate speech as an agent modality, including custom speech models*; *translate speech into other languages by using Foundry Tools*.

**You will learn**
- Keyless Speech SDK: `SpeechConfig(endpoint=<custom domain>, token_credential=...)`.
- **SSML**: neural voice, `prosody` (rate/pitch), `break`, `say-as`. Several `<voice>` elements in one document produce a multi-speaker recording.
- **Phrase list** boosts rare names at runtime with no training. Reach for **Custom Speech** (training on text, or audio + human transcripts) only if accuracy is still poor.
- Three transcription modes: **real-time** (live captions), **fast transcription** (one file, synchronous, faster than real time, optional **diarization**), **batch transcription** (many files in Blob, asynchronous).
- **Speech translation**: `TranslationRecognizer` with several target languages; it can also synthesise translated speech.

## Set up
- Linux/Codespaces need the ALSA library for the Speech SDK: `sudo apt-get install -y libasound2` (the dev container does this for you).
- No microphone needed: the lab synthesises WAV files and recognises from them.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | `SpeechConfig(endpoint, token_credential)` | Entra ID needs the custom-domain endpoint. |
| 2 | SSML with `prosody`, `break`, `say-as` | Control pace, pauses and how references are read. |
| 3 | `PhraseListGrammar.addPhrase(...)` | Quick accuracy win for names like *Fabrikam*. |
| 4 | `POST /speechtotext/transcriptions:transcribe` with `diarization` | Speaker-labelled transcript in one call. |
| 5 | `SpeechTranslationConfig` + `add_target_language` | English in, French and Japanese out. |

## Run and test
```bash
./lab run 46 && ./lab validate 46      # one click: ./lab solve 46
```
Listen to the generated WAV files in `.out/lab46/`.

## Explore
- Add `mstts:express-as style="cheerful"` (namespace `http://www.w3.org/2001/mstts`) and compare.
- Set `config.voice_name = "fr-FR-DeniseNeural"` on the translation config and subscribe to `synthesizing` to get translated audio.
- Batch transcription: `POST /speechtotext/transcriptions:submit` with `contentUrls` pointing at Blob files. It's asynchronous: poll, then download the result files.

## Exam reflexes
- Live captions → **real-time STT**. One recording back fast → **fast transcription**. A backlog of recordings → **batch transcription**.
- Who spoke when → **diarization**. Misrecognised names → **phrase list**, then **Custom Speech**.
- Pace, pauses, pronunciation → **SSML** (`prosody`, `break`, `phoneme`, `say-as`).
- Spoken language A → text/voice in language B → **speech translation**.

## Clean up
Nothing is created in Azure.
