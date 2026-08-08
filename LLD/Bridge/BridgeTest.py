"""
Bridge Pattern Demo
===================
Two independent hierarchies connected by a single reference (the "bridge"):

    RemoteControl  --has a-->  Device
    (abstraction)              (implementor)

The remote is the WHAT (high-level intentions: power, volume).
The device is the HOW  (low-level operations on real hardware).

Only two devices exist here (TV and Radio), controlled by one remote.
"""

from abc import ABC, abstractmethod


# ============================================================
#  IMPLEMENTOR SIDE  ("how it actually happens")
# ============================================================
class Device(ABC):
    """The interface every device must satisfy. The remote only ever
    talks to THIS, never to a concrete TV or Radio."""

    @abstractmethod
    def is_enabled(self) -> bool: ...

    @abstractmethod
    def enable(self) -> None: ...

    @abstractmethod
    def disable(self) -> None: ...

    @abstractmethod
    def get_volume(self) -> int: ...

    @abstractmethod
    def set_volume(self, percent: int) -> None: ...


class TV(Device):
    def __init__(self):
        self._on = False
        self._volume = 30

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True
        print("[TV] powered ON")

    def disable(self) -> None:
        self._on = False
        print("[TV] powered OFF")

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        print(f"[TV] volume -> {self._volume}%")


class Radio(Device):
    def __init__(self):
        self._on = False
        self._volume = 20

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True
        print("[Radio] powered ON")

    def disable(self) -> None:
        self._on = False
        print("[Radio] powered OFF")

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int) -> None:
        self._volume = max(0, min(100, percent))
        print(f"[Radio] volume -> {self._volume}%")


# ============================================================
#  ABSTRACTION SIDE  ("what the user wants to do")
# ============================================================
class RemoteControl:
    """Holds a reference to a Device. THIS reference is the bridge.
    Every method is a high-level intention that delegates down to
    the device's concrete operation."""

    def __init__(self, device: Device):
        self.device = device          # <-- the bridge

    def toggle_power(self) -> None:
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_up(self) -> None:
        self.device.set_volume(self.device.get_volume() + 10)

    def volume_down(self) -> None:
        self.device.set_volume(self.device.get_volume() - 10)


# ============================================================
#  DEMO
# ============================================================
def main():
    tv = TV()
    radio = Radio()

    # ONE remote class. Point it at whichever device you like.
    print("--- Controlling the TV ---")
    remote = RemoteControl(tv)
    remote.toggle_power()   # TV powered ON
    remote.volume_up()      # TV volume -> 40%
    remote.volume_up()      # TV volume -> 50%
    remote.volume_down()    # TV volume -> 40%
    remote.toggle_power()   # TV powered OFF

    print("\n--- Same remote class, different device ---")
    remote = RemoteControl(radio)
    remote.toggle_power()   # Radio powered ON
    remote.volume_up()      # Radio volume -> 30%
    remote.toggle_power()   # Radio powered OFF


if __name__ == "__main__":
    main()