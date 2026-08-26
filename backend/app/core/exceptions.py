"""
Small set of typed exceptions raised by the service layer.

Routes never translate errors themselves — a single exception handler in
main.py maps each of these to an HTTP status code. This keeps API routes
thin and means the same service methods could later be called from an
agent tool (Phase 6 of the plan) and raise the same typed errors there too.
"""


class CampusPilotError(Exception):
    """Base class for all domain errors."""


class NotFoundError(CampusPilotError):
    """A requested resource does not exist."""


class ConflictError(CampusPilotError):
    """The request conflicts with existing state (e.g. duplicate registration)."""


class ValidationError(CampusPilotError):
    """The request is well-formed but violates a business rule (e.g. past cutoff)."""


class PermissionError_(CampusPilotError):
    """The current actor is not allowed to perform this action."""
