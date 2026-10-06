# Lab 39 · Generate and edit images

**Scenario.** Contoso Marketing needs product shots for a new mug: a studio photo, a lifestyle version with a café background (product untouched), and a colour variant, without a photo shoot.

**Exam objectives.** D3 › *Generate images from text prompts and reference media*; *configure image-editing workflows, including inpainting, mask-based edits, and prompt-driven modifications*; *select and apply generation and editing controls*. D1 › *Implement auditing through … provenance metadata*.

**You will learn**
- `images.generate`: prompt, `size`, `quality`, `n`, `background`, `output_format`.
- `images.edit` with a **mask**: transparent pixels mark the region to regenerate; opaque pixels are preserved.
- `images.edit` with **reference images** and no mask: prompt-driven restyling.
- Provenance: Azure OpenAI image outputs carry **C2PA content credentials** that identify AI generation.

## Set up
```bash
azd env set DEPLOY_IMAGE_MODEL true && azd provision    # deploys gpt-image-1-mini (some image models need an access request)
```
Images are written to `.out/lab39/`.

## Steps
| TODO | Build | Why |
|---|---|---|
| 1 | Generate the studio photo. | Text-to-image with explicit controls. |
| 2 | Inpaint the top half using a mask. | Change the background, keep the product. |
| 3 | Restyle from the original as a reference. | Variants without masks. |

## Run and test
```bash
./lab run 39 && ./lab validate 39      # one click: ./lab solve 39
```
The test checks that pixels changed **more inside the mask than outside**.

## Explore
- `background="transparent"` + `output_format="png"` for cut-out product images.
- `input_fidelity="high"` preserves faces and logos more closely in edits.
- Run lab 43 on your generated images (moderation + watermark policy).

## Exam reflexes
- Change one region → **mask-based edit (inpainting)**. Restyle whole image from a reference → **edit with reference image**. New image → **generate**.
- Prove AI origin → **C2PA content credentials / provenance metadata**.

## Clean up
Delete `.out/lab39`. To stop paying for capacity, set `DEPLOY_IMAGE_MODEL false` and re-provision.
