"""Command-line entry point: python -m core.cli <subcommand>"""

from __future__ import annotations

import argparse
import logging

from core.character_repository import CharacterRepository
from core.config import get_settings
from core.episode_generator import create_episode
from core.episode_repository import EpisodeRepository
from core.logging_setup import configure_logging
from core.models.character import Character
from core.utils import load_yaml_template, slugify

logger = logging.getLogger(__name__)


def cmd_new_episode(args: argparse.Namespace) -> None:
    scaffold = create_episode(args.title)
    print(f"Created episode '{scaffold.episode.id}'")
    print(f"  workspace:  {scaffold.workspace_dir}")
    print(f"  episode:    {scaffold.episode_path}")
    print(f"  script:     {scaffold.script_path}")
    print(f"  checklist:  {scaffold.checklist_path}")
    for kind, path in scaffold.prompt_paths.items():
        print(f"  {kind} prompt: {path}")


def cmd_new_character(args: argparse.Namespace) -> None:
    settings = get_settings()
    data = load_yaml_template(settings, "character_template.yaml")
    data["id"] = slugify(args.name)
    data["name"] = args.name
    character = Character.model_validate(data)
    path = CharacterRepository(settings).save(character)
    print(f"Created character '{character.id}' -> {path}")


def cmd_list_episodes(_: argparse.Namespace) -> None:
    episodes = EpisodeRepository().list_all()
    if not episodes:
        print("No episodes yet. Create one with: python -m core.cli new-episode --title \"...\"")
        return
    for episode in episodes:
        print(f"{episode.id:30} {episode.stage.value:10} {episode.publishing_status.value:15} {episode.title}")


def cmd_run_pipeline(args: argparse.Namespace) -> None:
    from automation.pipeline import build_default_pipeline

    episode = EpisodeRepository().get(args.episode_id)
    pipeline = build_default_pipeline()
    pipeline.run(episode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-shorts-studio")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new-episode", help="Create an episode from templates/episode_template.yaml")
    p.add_argument("--title", required=True)
    p.set_defaults(func=cmd_new_episode)

    p = sub.add_parser("new-character", help="Create a character from templates/character_template.yaml")
    p.add_argument("--name", required=True)
    p.set_defaults(func=cmd_new_character)

    p = sub.add_parser("list-episodes", help="List all episodes and their status")
    p.set_defaults(func=cmd_list_episodes)

    p = sub.add_parser("run-pipeline", help="Run the automation pipeline for an episode")
    p.add_argument("--episode-id", required=True)
    p.set_defaults(func=cmd_run_pipeline)

    return parser


def main() -> None:
    configure_logging(get_settings())
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
