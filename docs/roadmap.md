# Roadmap

## Phase 1 — Foundation (done)
Config system, typed Episode/Character models, YAML repositories, the reusable prompt template library, automation engine interface, CLI, docs, tests.

## Phase 2 — Provider abstraction + episode workspaces + episode generator (done)
- Six provider categories (`editor/`, `video/`, `image/`, `voice/`, `upload/`, `storage/`), each an `ABC` in `base.py` plus stub implementations, selected via `config/providers.yaml`. `storage/local.py` is the one real implementation.
- Self-contained episode workspaces: `episodes/{id}/episode.yaml`, `script.md`, `checklist.md`, `prompts/*.yaml` (`PromptRecord`), `assets/`, `renders/`, `exports/`.
- Machine-readable metadata (id, episode_id, created, updated, status, version) on every generated file.
- `python -m core.cli new-episode --title "..."` scaffolds a complete workspace in one call via `core.episode_generator.create_episode()`.
- `automation/steps/*` call through provider interfaces instead of raising `NotImplementedError` themselves directly.

## Phase 3 — Real providers
- Implement `editor/davinci.py` against the real DaVinci Resolve Studio scripting API (prerequisites documented in that file); `import_to_editor`, `render`, `export` steps go from stub to working.
- Implement `GenerateScriptStep` against the Anthropic API using the `script_generator` prompt (`prompts/claude/`); write the result into the episode workspace's `script.md`.
- Implement at least one real provider per category (`image/gpt_image.py`, `video/runway.py`, `voice/elevenlabs.py`) so `GenerateAssetsStep` produces real assets.
- Generate real captions from voice-line timing (episode workspace's `assets/`).

## Phase 4 — Publishing automation
- Implement `upload/youtube.py` and/or `upload/tiktok.py`; add `UploadStep` to `build_default_pipeline()`.
- Scheduling/queueing for upload times.
- Optional: sync `Episode.stage`/`publishing_status` back into the vault's Episode Progress Tracker, so the human planning layer reflects automated progress without manual updates.
- Batch mode: run the pipeline across the whole backlog, not just one episode at a time.

Each phase should ship with tests for anything that isn't a raw external API call, and an update to this roadmap marking what moved from "stub" to "implemented."
