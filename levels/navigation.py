from core.simulator import WindowsCliSimulator
from .base import Level

def setup_navigation_level(simulator: WindowsCliSimulator) -> None:
    """设置导航关卡的初始状态"""
    pass

def check_navigation_level(simulator: WindowsCliSimulator) -> bool:
    """检查导航关卡是否完成"""
    return simulator.cwd == 'C:\\Users\\Player\\Documents'

NAVIGATION_LEVEL = Level(
    level_number=1,
    title="基础导航",
    description="""欢迎来到 Windows 命令行学习游戏！

第一关：基础导航
目标：使用 cd 命令进入 Documents 目录

可用命令：
- dir：显示当前目录的内容
- cd 目录名：进入指定目录
- cd ..：返回上一级目录

提示：
1. 首先使用 dir 命令查看当前目录下有哪些文件夹
2. 使用 cd 命令进入 Documents 目录
""",
    setup_state=setup_navigation_level,
    check_success=check_navigation_level,
    hints=[
        "使用 dir 命令查看当前目录内容",
        "使用 cd Documents 进入 Documents 目录",
        "如果输入错误，可以使用 cd .. 返回上一级目录"
    ]
) 