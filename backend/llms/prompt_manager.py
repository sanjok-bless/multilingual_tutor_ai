"""Prompt template management using Jinja2."""

from pathlib import Path

import jinja2
from jinja2 import FileSystemLoader, Template
from jinja2.sandbox import SandboxedEnvironment

from backend.enums import Language, Level
from backend.errors import TemplateNotFoundError


class PromptManager:
    """Manages prompt templates for AI tutoring."""

    def __init__(self, templates_dir: Path | None = None) -> None:
        """Initialize with templates directory."""
        if templates_dir is None:
            # Get backend/prompts/ directory relative to this file
            backend_dir = Path(__file__).parent.parent
            templates_dir = backend_dir / "prompts"

        self.templates_dir = templates_dir
        self.templates_dir.mkdir(exist_ok=True)  # Create if doesn't exist

        # Initialize secure Jinja2 environment with sandboxing
        self.env = SandboxedEnvironment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def load_template(self, template_name: str) -> Template:
        """Load template."""
        template_path = self.templates_dir / template_name

        if not template_path.exists():
            raise TemplateNotFoundError(f"Template '{template_name}' not found at {template_path}")

        try:
            return self.env.get_template(template_name)
        except jinja2.TemplateNotFound as e:
            raise TemplateNotFoundError(f"Template '{template_name}' not found") from e

    def render_system_prompt(self, language: Language, level: Level) -> str:
        """Render system prompt."""
        template = self.load_template("system.j2")
        return template.render(language=language.value, level=level.value)

    def render_tutoring_prompt(self, user_message: str, language: Language, level: Level) -> str:
        """Render tutoring prompt."""
        template = self.load_template("tutoring.j2")
        return template.render(user_message=user_message, language=language.value, level=level.value)

    def render_start_message(self, language: Language, level: Level) -> str:
        """Render level-appropriate welcome message."""
        template = self.load_template("start_message.j2")
        return template.render(language=language.value, level=level.value)
