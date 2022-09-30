from typing import Dict

from jinja2 import Environment


class TemplateRender:
    def __init__(self) -> None:
        self.env = Environment(enable_async=True)

    async def render(self, context: Dict, template: str) -> str:
        _template = self.env.from_string(template)
        return await _template.render_async(**context)

    async def __call__(self, context: Dict, template: str) -> str:
        return await self.render(context, template)
