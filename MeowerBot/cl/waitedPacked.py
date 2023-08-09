from dataclasses import dataclass

@dataclass
class WaitedPacked:
	ok: bool
	packet: dict
	listener: str

	