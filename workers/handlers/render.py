from typing import Dict
from jinja2 import Environment, BaseLoader


class EmailRender:
    def __init__(self) -> None:
        self.env = Environment(loader=BaseLoader, enable_async=True)

    async def render(self, context: Dict, template: str) -> str:
        template = self.env.from_string(template)
        return await template.render_async(**context)

    async def __call__(self, context: Dict, template: str):
        return await self.render(context, template)
