# Architecture

## Layers

```
core/            shared library — config, models, repositories, prompt library,
                  frontmatter helper, episode generator, logging, CLI

automation/       orchestration — depends on core/ and the provider packages
  ├── step.py             PipelineStep abstract base, StepResult
  ├── pipeline.py         Pipeline, build_default_pipeline()
  └── steps/              one module per stage — each calls a provider, never
                           a concrete SDK

editor/  video/  image/  voice/  upload/  storage/     provider abstraction
  each package: base.py (an ABC + get_provider(settings)) plus one module per
  concrete provider (e.g. editor/davinci.py, video/runway.py, ...). Provider
  choice is a config value (config/providers.yaml), never a code change.

episodes/{id}/    a self-contained episode workspace — episode.yaml, script.md,
                   checklist.md, prompts/, assets/, renders/, exports/. See
                   "Episode workspaces" below.

<shared folders>  characters/ prompts/ assets/ voices/ music/ templates/ logs/
                   — reused across many episodes, referenced by path from an
                   episode rather than copied into it.
```

`core/` has no dependency on `automation/` or the provider packages. `automation/steps/*` depend on `core/` and on exactly one provider package's `base.py` (never a concrete provider module directly) — that's what makes providers swappable. This keeps the data layer (models, repositories, prompt library) usable on its own, e.g. from the CLI, without pulling in any provider machinery.

## Provider abstraction

Every external capability the studio will eventually need — editing/rendering, video generation, image generation, voice synthesis, platform upload, storage — is behind a small `ABC` in that category's `base.py`, plus a `get_provider(settings) -> XProvider` factory that looks up `settings.providers.<category>` (from `config/providers.yaml`) in a `{name: class}` registry.

```
automation/steps/generate_assets.py
    → image.base.get_provider(settings)   → image.gpt_image.GPTImage   (or image.flux.FluxImage)
    → video.base.get_provider(settings)   → video.runway.RunwayVideo   (or veo / kling)
    → voice.base.get_provider(settings)   → voice.elevenlabs.ElevenLabsVoice (or cartesia)
```

Swapping `image: "gpt_image"` to `image: "flux"` in `config/providers.yaml` changes what runs — nothing in `automation/` or `core/` changes. All provider implementations are typed, documented stubs (`NotImplementedError`) except `storage/local.py`, which is genuinely implemented — a local filesystem copy needs no external API, so it proves the whole pattern end-to-end today.

## Episode workspaces

```
episodes/{id}/
    episode.yaml     # core.models.episode.Episode
    script.md         # frontmatter (id/episode_id/status/version) + markdown body
    checklist.md       # same frontmatter convention
    prompts/
        image.yaml       # core.models.prompt_record.PromptRecord
        video.yaml
        voice.yaml
        thumbnail.yaml
    assets/            # this episode's generated images/video/voice
    renders/            # this episode's editor render output
    exports/             # this episode's final, platform-ready file
```

Everything specific to one episode lives in its workspace, so a provider can operate on an episode without searching the rest of the project. `core/episode_generator.py`'s `create_episode()` scaffolds all of it in one call; `core/episode_repository.py` owns reading/writing `episode.yaml` and knows the workspace layout (`workspace_dir(id)`).

Shared resources — character records, the reusable prompt *template* library (`prompts/claude/`, `prompts/image/`, etc. — distinct from a workspace's `prompts/*.yaml` instances), the music/SFX library, and voice reference samples — stay in their own top-level folders and are referenced by path from an episode, not duplicated into every workspace.

## Design principles

- **Config-driven, not hardcoded.** Paths, render/video defaults, automation stage toggles, and provider selection all live in `config/*.yaml`, loaded once into a typed `Settings` object (`core.config.get_settings()`).
- **Secrets never touch YAML.** API keys are environment-only (`.env`, gitignored), read into `APISettings`.
- **The app talks to interfaces, not providers.** `automation/steps/*` import a category's `base.py`, never `editor.davinci` or `voice.elevenlabs` directly.
- **One responsibility per module.** A repository only does CRUD; a pipeline step only does one stage; each provider module implements exactly one provider.
- **Stub honestly.** Unimplemented providers/stages have full signatures, type hints, and docstrings describing intended behavior, and raise `NotImplementedError` rather than silently no-op-ing or faking success.
