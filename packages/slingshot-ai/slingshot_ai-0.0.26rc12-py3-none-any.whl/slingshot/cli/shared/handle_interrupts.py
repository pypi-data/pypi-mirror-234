import asyncio
import signal
from contextlib import contextmanager
from typing import Any, Generator


@contextmanager
def handle_interrupts() -> Generator[asyncio.Event, None, None]:
    interrupt_event = asyncio.Event()

    def handler(signum: int, frame: Any) -> None:
        nonlocal interrupt_event
        if interrupt_event.is_set():
            raise KeyboardInterrupt()
        interrupt_event.set()

    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handler)

    try:
        yield interrupt_event
    finally:
        signal.signal(signal.SIGINT, original_handler)
