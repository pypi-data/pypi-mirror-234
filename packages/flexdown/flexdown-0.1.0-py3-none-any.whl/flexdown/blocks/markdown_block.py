import reflex as rx

from flexdown import types, utils
from flexdown.blocks.block import Block


class MarkdownBlock(Block):
    """A block of Markdown."""

    type = "markdown"
    line_transforms = [
        utils.evaluate_templates,
    ]

    def render(self, env: types.Env, component_map: types.ComponentMap) -> rx.Component:
        return rx.markdown(self.get_content(env), component_map=component_map)
