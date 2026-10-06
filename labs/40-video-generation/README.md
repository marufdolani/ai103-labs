# Lab 40 · Generate and remix video

**Scenario.** Contoso Coffee wants three short social clips: a product shot from text, an animation that starts from its storefront sign, and a night-time variant of the first clip.

**Exam objectives.** D3 › *Generate videos from text prompts and reference media*; *implement workflows to edit generated videos*; *select and apply generation and editing controls*.

**You will learn**
- Video generation is an **asynchronous job**: create → poll status → download (`create_and_poll` wraps it).
- Controls: `seconds` (4/8/12), `size` (1280x720, 720x1280, …), `input_reference` (image-to-video).
- **Remix**: edit a generated video with a new prompt while keeping its structure.

## Set up
```bash
azd env set DEPLOY_VIDEO_MODEL true && azd provision
```
Sora is **preview** with frequent version changes. If provisioning fails, check *Model retirement schedule* on Learn, update the `videoModelVersion` default in `infra/core.bicep`, and run `azd provision` again. Videos cost noticeably more than text; this lab makes three 4-second clips.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Text-to-video with `create_and_poll`. | The async job pattern. |
| 2 | Image-to-video with `input_reference`. | Brand-consistent first frames. |
| 3 | Remix and poll. | Iterate without starting over. |

## Run and test
```bash
./lab run 40 && ./lab validate 40      # one click: ./lab solve 40
```
Files land in `.out/lab40/`.

## Exam reflexes
- Video generation → async job: **create, poll, download**. Change an existing clip → **remix**. Start from a picture → **image-to-video (input reference)**.
- Analysing existing video (not generating) → **Content Understanding video analyzer** (lab 42).

## Clean up
Delete `.out/lab40`. Disable the deployment when done (`DEPLOY_VIDEO_MODEL false`, `azd provision`).
