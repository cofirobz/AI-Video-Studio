# Coding Standards

- **Type hints everywhere.** Every function signature and class attribute is typed. Use `from __future__ import annotations` and PEP 604 unions (`str | None`), not `Optional[str]`.
- **Pydantic for data, not dicts.** Anything that crosses a file/API boundary (episodes, characters, prompts, settings) is a Pydantic `BaseModel`. Don't pass around raw `dict`s for structured data.
- **Logging, not print.** Library code (`core/`, `automation/`, and the provider packages) logs via `logging.getLogger(__name__)`. `print()` is reserved for `core/cli.py`'s direct user-facing output.
- **No bare `except`.** Catch specific exceptions. `automation/pipeline.py`'s `Pipeline.run()` is the one place that catches broadly, deliberately, so one bad stage doesn't take down the process — everywhere else, be specific.
- **One responsibility per module.** A repository does CRUD, nothing else. A pipeline step does one stage. Each provider module implements exactly one provider. If a module starts doing two things, split it.
- **The app talks to interfaces, not providers.** Code outside a provider package imports that category's `base.py` (`editor.base.get_provider`, `voice.base.get_provider`, ...) — never `editor.davinci` or `voice.elevenlabs` directly. If you find yourself importing a concrete provider module from `automation/` or `core/`, that's a bug.
- **Comments explain why, not what.** Docstrings on public classes/functions describe intended behavior (especially for stubs — see below). Don't narrate obvious code.
- **Stubs are honest.** An unimplemented function has a full signature, type hints, and a docstring, and raises `NotImplementedError("<what's missing> — see docs/roadmap.md")`. Never a silent `pass` or a fake success return.

## Adding a new provider
1. Create `<category>/<name>.py` with a class extending that category's `ABC` from `base.py`.
2. Implement every abstract method — stub with `NotImplementedError("requires <the real API> — see docs/roadmap.md")` if it's not wired up yet.
3. Register it in the `registry` dict inside `<category>/base.py`'s `get_provider()`.
4. To make it the active provider, set it in `config/providers.yaml` — no code elsewhere changes.

## Adding a new pipeline step
1. Create `automation/steps/<name>.py` with a class extending `PipelineStep` (see `automation/step.py`).
2. `name = "<snake_case>"`, implement `run(self, episode, context) -> StepResult`. If it needs an external capability, get it via `<category>.base.get_provider(settings)` — don't call a provider SDK directly.
3. Add it to `build_default_pipeline()` in `automation/pipeline.py` in the right order.
4. Add a matching entry to `config/automation.yaml`.

## Adding a new prompt template (the shared library)
1. Copy `templates/prompt_template.yaml` into `prompts/<category>/<name>.yaml`.
2. Every `{placeholder}` in `template` must be listed in `variables` — `PromptLibrary.render()` validates against that list, but `str.format()` will still raise if you miss one.
3. `PromptLibrary().render("<name>", **kwargs)` to use it.

This is the reusable *template* library — distinct from a specific episode's `episodes/{id}/prompts/{kind}.yaml` (a `PromptRecord`, that episode's actual editable prompt).

## Adding a new config concern
1. Add a `BaseModel` to `core/config.py`.
2. Add it as a field on `Settings`.
3. Add a matching `config/<name>.yaml` with commented defaults.
4. Load it in `get_settings()`.
