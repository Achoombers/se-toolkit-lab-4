"""Unit tests for edge cases and boundary values in interaction models."""

from datetime import datetime, timezone

from app.models.interaction import InteractionLog, InteractionLogCreate, InteractionModel


def test_create_with_empty_string_kind_is_accepted() -> None:
    """Empty string for 'kind' field is accepted by Pydantic (no constraint)."""
    log = InteractionLogCreate(learner_id=1, item_id=1, kind="")
    assert log.kind == ""


def test_create_with_negative_ids_is_accepted() -> None:
    """Negative IDs are accepted by Pydantic (int has no positivity constraint)."""
    log = InteractionLogCreate(learner_id=-1, item_id=-99, kind="attempt")
    assert log.learner_id == -1
    assert log.item_id == -99


def test_create_with_very_long_kind_string() -> None:
    """Very long 'kind' string (1000+ chars) should be accepted."""
    long_kind = "a" * 1000
    log = InteractionLogCreate(learner_id=1, item_id=1, kind=long_kind)
    assert log.kind == long_kind
    assert len(log.kind) == 1000


def test_create_with_zero_values_for_ids() -> None:
    """Zero values for learner_id and item_id should be accepted."""
    log = InteractionLogCreate(learner_id=0, item_id=0, kind="view")
    assert log.learner_id == 0
    assert log.item_id == 0


def test_interaction_log_with_none_created_at_defaults_to_none() -> None:
    """InteractionLog created_at defaults to None when not provided."""
    log = InteractionLog(id=1, learner_id=1, item_id=1, kind="click")
    assert log.created_at is None


def test_interaction_log_with_explicit_none_created_at() -> None:
    """InteractionLog accepts explicit None for created_at."""
    log = InteractionLog(id=1, learner_id=1, item_id=1, kind="click", created_at=None)
    assert log.created_at is None


def test_interaction_log_with_datetime_now() -> None:
    """InteractionLog accepts current datetime for created_at."""
    now = datetime.now(timezone.utc)
    log = InteractionLog(id=1, learner_id=1, item_id=1, kind="click", created_at=now)
    assert log.created_at == now


def test_interaction_model_with_past_datetime() -> None:
    """InteractionModel accepts datetime from the past."""
    past = datetime(2020, 1, 1, tzinfo=timezone.utc)
    model = InteractionModel(id=1, learner_id=1, item_id=1, kind="view", created_at=past)
    assert model.created_at == past


def test_interaction_model_with_future_datetime() -> None:
    """InteractionModel accepts datetime from the future."""
    future = datetime(2030, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    model = InteractionModel(id=999, learner_id=999, item_id=999, kind="submit", created_at=future)
    assert model.created_at == future


def test_interaction_model_with_special_characters_in_kind() -> None:
    """InteractionModel accepts kind with special characters."""
    special_kind = "view_@#$%^&*()_+-=[]{}|;':\",./<>?"
    model = InteractionModel(id=1, learner_id=1, item_id=1, kind=special_kind, created_at=datetime.now(timezone.utc))
    assert model.kind == special_kind


def test_interaction_model_with_unicode_kind() -> None:
    """InteractionModel accepts kind with unicode characters."""
    unicode_kind = "просмотр_👁️_查看"
    model = InteractionModel(id=1, learner_id=1, item_id=1, kind=unicode_kind, created_at=datetime.now(timezone.utc))
    assert model.kind == unicode_kind
