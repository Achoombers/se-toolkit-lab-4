"""Unit tests for edge cases and boundary values in interaction models."""

from datetime import datetime, timezone

from app.models.interaction import InteractionLog, InteractionLogCreate, InteractionModel
from backend.tests.unit.test_interactions import _make_log
from app.routers.interactions import _filter_by_item_id


# KEPT: covers empty string
def test_create_with_empty_string_kind_is_accepted() -> None:
    """Empty string for 'kind' field is accepted by Pydantic (no constraint)."""
    log = InteractionLogCreate(learner_id=1, item_id=1, kind="")
    assert log.kind == ""


# KEPT: negative id
def test_create_with_negative_ids_is_accepted() -> None:
    """Negative IDs are accepted by Pydantic (int has no positivity constraint)."""
    log = InteractionLogCreate(learner_id=-1, item_id=-99, kind="attempt")
    assert log.learner_id == -1
    assert log.item_id == -99


# KEPT: very long strings
def test_create_with_very_long_kind_string() -> None:
    """Very long 'kind' string (1000+ chars) should be accepted."""
    long_kind = "a" * 1000
    log = InteractionLogCreate(learner_id=1, item_id=1, kind=long_kind)
    assert log.kind == long_kind
    assert len(log.kind) == 1000


# DISCARDED: duplicates test_filter_returns_interaction_with_matching_ids
def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1