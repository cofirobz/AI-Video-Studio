# Getting Started

## Install

From `studio/`:

```
pip install -e ".[dev]"
```

This installs `core`, `automation`, and the provider packages (`editor`, `video`, `image`, `voice`, `upload`, `storage`) as editable packages plus their dependencies (`pydantic`, `pyyaml`, `python-dotenv`, and `pytest` for the dev extra).

## Configure

Settings live in `config/*.yaml` — see `docs/architecture.md` for what each file controls, including `config/providers.yaml` (which concrete provider each category uses). Defaults work out of the box; edit them as needed, nothing is hardcoded in the Python.

Future API keys go in a `.env` file at the project root, not in YAML:

```
cp .env.example .env
# then fill in the keys you have
```

## Use the CLI

```
python -m core.cli new-episode --title "My First Episode"
python -m core.cli new-character --name "My First Character"
python -m core.cli list-episodes
python -m core.cli run-pipeline --episode-id my-first-episode
```

`new-episode` scaffolds a complete workspace: `episodes/my-first-episode/episode.yaml`, `script.md`, `checklist.md`, `prompts/{image,video,voice,thumbnail}.yaml`, and empty `assets/`, `renders/`, `exports/` subfolders.

`run-pipeline` runs the real `generate_prompts` stage and then stops cleanly at `generate_script` (or whichever stage comes first and isn't implemented yet), logging why. That's expected until the providers in `docs/roadmap.md`'s Phase 3 are implemented.

## Run tests

```
pytest
```

## Where things are

- An episode's everything (script, checklist, prompts, generated assets, renders, exports) → `episodes/{id}/`
- Characters (shared across episodes) → `characters/`
- The reusable prompt *template* library → `prompts/<category>/`
- Which provider each category uses → `config/providers.yaml`
- Logs → `logs/studio.log`
- Full architecture → `docs/architecture.md`
