from core.simulator import WindowsCliSimulator
from .base import Level

def setup_file_move_level(simulator: WindowsCliSimulator) -> None:
    """设置文件移动关卡的初始状态"""
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6\\subdir1')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6\\subdir2')
    simulator.simulate_echo('Test file 1', '>', 'C:\\Users\\Player\\Documents\\level6\\file1.txt')
    simulator.simulate_echo('Test file 2', '>', 'C:\\Users\\Player\\Documents\\level6\\subdir1\\file2.txt')

def check_file_move_level(simulator: WindowsCliSimulator) -> bool:
    """检查文件移动关卡是否完成"""
    old_file = simulator._get_directory('C:\\Users\\Player\\Documents\\level6\\file1.txt')
    new_file = simulator._get_directory('C:\\Users\\Player\\Documents\\level6\\subdir2\\file1.txt')
    return old_file is None and new_file is not None

def setup_command_args_level(simulator: WindowsCliSimulator) -> None:
    """设置命令行参数关卡的初始状态"""
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7\\subdir1')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7\\subdir2')
    for i in range(1, 6):
        simulator.simulate_echo(f'Test file {i}', '>', f'C:\\Users\\Player\\Documents\\level7\\file{i}.txt')
    simulator.simulate_echo('Read-only file', '>', 'C:\\Users\\Player\\Documents\\level7\\readonly.txt')

def check_command_args_level(simulator: WindowsCliSimulator) -> bool:
    """检查命令行参数关卡是否完成"""
    return simulator.last_command_with_args == ('del', ['/Q', '/F', 'readonly.txt'])

FILE_MOVE_LEVEL = Level(
    level_number=6,
    title="文件移动",
    description="""第六关：文件移动
目标：将 level6 目录下的 file1.txt 移动到 subdir2 目录中

可用命令：
- dir：显示当前目录的内容
- cd 目录名：进入指定目录
- move 源文件 目标文件：移动文件
- type 文件名：查看文件内容

提示：
1. 使用 dir 命令查看文件位置
2. 使用 move 命令移动文件
3. 使用 dir 命令验证移动结果
""",
    setup_state=setup_file_move_level,
    check_success=check_file_move_level,
    hints=[
        "使用 cd level6 进入目录",
        "使用 move file1.txt subdir2\\file1.txt 移动文件",
        "使用 dir subdir2 确认文件已移动"
    ]
)

COMMAND_ARGS_LEVEL = Level(
    level_number=7,
    title="命令行参数",
    description="""第七关：命令行参数
目标：使用带参数的 del 命令删除 readonly.txt 文件

可用命令：
- dir：显示当前目录的内容
  - /w：使用宽格式显示
  - /p：分页显示
- del：删除文件
  - /Q：安静模式，不询问确认
  - /F：强制删除只读文件

提示：
1. 使用 dir /w 查看当前目录下的文件（宽格式显示更清晰）
2. 尝试直接删除 readonly.txt 文件，观察结果
3. 使用 del /Q /F readonly.txt 强制删除只读文件

注意：
- 命令行参数通常以 / 开头
- 多个参数可以组合使用
- 参数顺序通常不重要
""",
    setup_state=setup_command_args_level,
    check_success=check_command_args_level,
    hints=[
        "使用 dir /w 查看文件列表",
        "尝试 del readonly.txt 看看会发生什么",
        "使用 del /Q /F readonly.txt 强制删除文件",
        "参数可以组合使用，顺序不重要"
    ]
) 