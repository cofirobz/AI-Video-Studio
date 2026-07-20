# Folder Structure

| Folder | Kind | Purpose |
|---|---|---|
| `core/` | code | Config, data models, repositories, prompt library, frontmatter helper, episode generator, logging, CLI |
| `automation/` | code | Pipeline orchestration: `step.py`, `pipeline.py`, `steps/` — each step calls a provider, never a concrete SDK |
| `editor/` | code | Editing/render provider abstraction: `base.py` + `davinci.py`, `remotion.py`, `ffmpeg.py` |
| `video/` | code | Video generation provider abstraction: `base.py` + `runway.py`, `veo.py`, `kling.py` |
| `image/` | code | Image generation provider abstraction: `base.py` + `gpt_image.py`, `flux.py` |
| `voice/` | code | Voice (TTS) provider abstraction: `base.py` + `elevenlabs.py`, `cartesia.py` |
| `upload/` | code | Platform upload provider abstraction: `base.py` + `youtube.py`, `tiktok.py` |
| `storage/` | code | Storage provider abstraction: `base.py` + `local.py` (the one fully implemented provider) |
| `episodes/{id}/` | data | Self-contained episode workspace — `episode.yaml`, `script.md`, `checklist.md`, `prompts/`, `assets/`, `renders/`, `exports/`. See `docs/architecture.md`. |
| `characters/` | data | One YAML per character (`core.models.character.Character`), shared across episodes |
| `prompts/` | data | Shared, reusable prompt *template* library, by category: `claude/`, `claude_code/`, `image/`, `video/`, `voice/`, `thumbnail/` — distinct from a workspace's `episodes/{id}/prompts/*.yaml` instances |
| `assets/` | data | Shared brand assets: `characters/`, `backgrounds/`, `logos/`, `fonts/` |
| `voices/` | data | Shared voice reference samples, reused across episodes |
| `music/` | data | Shared music/SFX library: `tracks/`, `sound_effects/` |
| `logs/` | data | Rotating app log (gitignored) |
| `config/` | config | One YAML file per settings concern, including `providers.yaml` — see `core/config.py` for the schema |
| `templates/` | config | Blank scaffolds matching the Episode/Character/PromptRecord schemas plus `script_template.md`/`checklist_template.md`, used by `core.episode_generator` and `core.cli` |
| `docs/` | docs | This file and its siblings |
| `tests/` | code | Pytest suite |

Every shared data folder has its own `README.md` explaining what belongs there. An episode workspace is self-documenting by its fixed layout (see `docs/architecture.md`).
