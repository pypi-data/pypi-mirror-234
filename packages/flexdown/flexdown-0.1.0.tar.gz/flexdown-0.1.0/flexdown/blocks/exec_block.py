import importlib
import os
import sys

import reflex as rx

from flexdown import types
from flexdown.blocks.block import Block


MODULES = "modules"


class ExecBlock(Block):
    """A block of executable Python code."""

    type = "exec"
    starting_indicator = "```python exec"
    ending_indicator = "```"

    def render(self, **_) -> rx.Component:
        # Return an empty component.
        return rx.fragment()

    @classmethod
    def process_blocks(cls, blocks: list[Block], env: types.Env):
        """Execute all the exec blocks.

        Args:
            blocks: The blocks to process.
            env: The environment to use for processing.
        """
        # Get all the exec blocks.
        exec_blocks = [block for block in blocks if block.type == cls.type]

        # Concat the content of all the exec blocks.
        content = "\n".join([block.get_content(env) for block in exec_blocks])

        # Get the path to the directory where the module should be saved.
        flexdown_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        module_dir = os.path.join(flexdown_dir, MODULES)

        # Write the content to a file in the module directory.
        os.makedirs(module_dir, exist_ok=True)
        module_name = rx.vars.get_unique_variable_name()
        module_path = os.path.join(module_dir, f"{module_name}.py")
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Import the module to execute the code.
        module_name = f"flexdown.{MODULES}.{module_name}"
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        env.update(vars(module))
