import uuid
from unittest.mock import AsyncMock, MagicMock

from .update_id import update_id_function


async def test_update_id():
    actor = AsyncMock()
    actor.generate_new_object_id = lambda: str(uuid.uuid4())

    data = {"id": "id"}
    result = await update_id_function(data, actor)
    assert result["id"] != "id"

    data = {"object": "test"}
    result = await update_id_function(data, actor)
    assert result["id"]

    # if in store; id is not updated
    data = {"object": {"id": "id"}}
    result = await update_id_function(data, actor)
    assert result["object"]["id"] == "id"

    actor.retrieve.return_value = None
    data = {"object": {"id": "id"}}
    result = await update_id_function(data, actor)
    assert result["object"]["id"] != "id"


async def test_update_id_for_actor_update():
    actor = MagicMock(actor_id="my_actor")
    actor.generate_new_object_id = lambda: str(uuid.uuid4())

    data = {"type": "Update", "object": {"id": actor.actor_id}}

    data = await update_id_function(data, actor)

    assert data["object"]["id"] == actor.actor_id
