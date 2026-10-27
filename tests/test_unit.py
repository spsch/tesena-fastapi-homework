import pytest
from pydantic import ValidationError
from app.schemas import ItemCreate, ItemUpdate

def test_item_create_valid_schema():
    data = {"name": "VISA CC", "description": "Testovací", "price": 99.9}
    item = ItemCreate(**data)
    assert item.name == "VISA CC"
    assert item.price == 99.9

def test_item_create_invalid_price():
    data = {"name": "MasterCard ccc", "price": -10.0}
    with pytest.raises(ValidationError):
        ItemCreate(**data)

def test_item_update_partial_schema():
    update_data = ItemUpdate(price=199.0)
    dumped = update_data.model_dump(exclude_unset=True)
    assert dumped == {"price": 199.0}
    assert "name" not in dumped