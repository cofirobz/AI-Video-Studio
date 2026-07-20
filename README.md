# AI Shorts Studio

Python foundation for an AI-powered YouTube Shorts / TikTok production pipeline: self-contained episode workspaces, a reusable prompt library, and a swappable provider layer (editing, video, image, voice, upload, storage) tied together by an automation engine.

**Status: Phase 2.** Episode/character data models, config, repositories, the prompt library, and the episode generator (`new-episode`) are functional today. Every external capability — DaVinci Resolve, Runway, ElevenLabs, YouTube/TikTok upload, etc. — sits behind a provider interface (`editor/`, `video/`, `image/`, `voice/`, `upload/`, `storage/`); concrete providers are documented, typed stubs (`storage/local.py` is the one real implementation) selected via `config/providers.yaml`, until implemented in later phases — see [docs/roadmap.md](docs/roadmap.md).

## Quick start

See [docs/getting_started.md](docs/getting_started.md).

```
pip install -e ".[dev]"
python -m core.cli new-episode --title "My First Episode"
python -m core.cli list-episodes
pytest
```

## Docs

- [docs/architecture.md](docs/architecture.md) — layers and data flow
- [docs/folder_structure.md](docs/folder_structure.md) — what every folder is for
- [docs/coding_standards.md](docs/coding_standards.md) — conventions for this codebase
- [docs/roadmap.md](docs/roadmap.md) — Phase 2/3/4

## Companion vault

The Obsidian vault one level up (`../📊 Dashboard` etc.) is the human planning layer — ideas, scripts drafts, checklists. This project is independent of it by design (see architecture doc).
