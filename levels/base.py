from dataclasses import dataclass
from typing import Callable, List
from core.simulator import WindowsCliSimulator

@dataclass
class Level:
    """关卡定义类"""
    level_number: int
    title: str
    description: str
    setup_state: Callable[[WindowsCliSimulator], None]
    check_success: Callable[[WindowsCliSimulator], bool]
    hints: List[str] 