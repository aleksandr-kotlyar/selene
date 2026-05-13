from typing import Iterable

from typing_extensions import assert_type

from selene import have
from selene.core.condition import Condition
from selene.core.entity import Collection, Element


def issue_541_condition_each_can_be_passed_to_collection_should(
    collection: Collection,
) -> None:
    condition = have.text('').each

    assert_type(condition, Condition[Iterable[Element]])

    collection.should(condition)
