"""Exceptions for flexdown."""


class TemplateEvaluationError(Exception):
    """An error when evaluating a template placeholder."""


class RenderError(Exception):
    """An error when rendering a block."""
