from unittest.mock import AsyncMock

from bovine_process.types import ProcessingItem

from .by_activity_type import ByActivityType, do_nothing


async def test_do_nothing():
    item = ProcessingItem("submitter", "item")

    assert await do_nothing(item, "other arg") == item
    assert await do_nothing(item, "other arg", {"more": "arguments"}) == item


async def test_by_activity_type():
    item = ProcessingItem("submitter", {"type": "Test"})

    mock = AsyncMock()
    mock.return_value = "mock"

    by_activity_type = ByActivityType({"Test": mock})

    result = await by_activity_type.act(item)

    assert result == "mock"
    mock.assert_awaited_once()


async def test_build_do_for_types():
    follow_item = ProcessingItem("submitter", {"type": "Follow"})
    create_item = ProcessingItem("submitter", {"type": "Create"})

    mock = AsyncMock()
    mock.return_value = "mock"

    processor = ByActivityType({"Follow": mock}).act

    assert await processor(follow_item) == "mock"
    assert await processor(create_item) == create_item

    mock.assert_awaited_once()
