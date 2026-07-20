# episodes/

One self-contained workspace folder per episode: `{id}/episode.yaml` (matching `core.models.episode.Episode`) plus `script.md`, `checklist.md`, `prompts/`, `assets/`, `renders/`, `exports/`. See `docs/architecture.md` for the full layout.

Managed via `core.episode_repository.EpisodeRepository` and `core.episode_generator.create_episode()` — don't hand-rename a workspace folder, it must match `episode.yaml`'s `id`.

Create one with `python -m core.cli new-episode --title "..."`.
