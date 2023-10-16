# -*- coding: utf-8 -*-
"""Single item queue."""

import asyncio
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class SingleItemQueue(Generic[T]):
    """A queue that can only hold one item at a time."""

    def __init__(self) -> None:
        """Initialize the queue."""
        self._item: Optional[T] = None
        self._event = asyncio.Event()

    def put_nowait(self, item: T) -> None:
        """Put an item in the queue. Upserts the item is one was already present."""
        self._item = item
        self._event.set()

    async def get(self) -> T:
        """Get an item from the queue. Blocks until an item is available."""
        await self._event.wait()
        self._event.clear()
        if self._item is None:
            raise ValueError("No item in the queue")
        item = self._item
        self._item = None
        return item
