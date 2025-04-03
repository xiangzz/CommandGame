from dataclasses import dataclass
from typing import Callable, List
from win_cli_simulator import WindowsCliSimulator

@dataclass
class Level:
    """关卡定义类"""
    level_number: int
    title: str
    description: str
    setup_state: Callable[[WindowsCliSimulator], None]
    check_success: Callable[[WindowsCliSimulator], bool]
    hints: List[str]

def setup_level1(simulator: WindowsCliSimulator) -> None:
    """设置第一关的初始状态"""
    pass

def check_level1_success(simulator: WindowsCliSimulator) -> bool:
    """检查第一关是否完成"""
    return simulator.cwd == 'C:\\Users\\Player\\Documents'

def setup_level2(simulator: WindowsCliSimulator) -> None:
    """设置第二关的初始状态"""
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\test_dir')

def check_level2_success(simulator: WindowsCliSimulator) -> bool:
    """检查第二关是否完成"""
    target_dir = simulator._get_directory('C:\\Users\\Player\\Documents\\my_folder')
    return target_dir is not None

def setup_level3(simulator: WindowsCliSimulator) -> None:
    """设置第三关的初始状态"""
    # 创建测试文件和目录
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\source')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\target')
    simulator.simulate_echo('Hello, this is a test file!', '>', 'C:\\Users\\Player\\Documents\\source\\test.txt')

def check_level3_success(simulator: WindowsCliSimulator) -> bool:
    """检查第三关是否完成"""
    # 检查文件是否被复制到目标目录
    target_file = simulator._get_directory('C:\\Users\\Player\\Documents\\target\\test.txt')
    return target_file is not None

def setup_level4(simulator: WindowsCliSimulator) -> None:
    """设置第四关的初始状态"""
    # 创建测试文件
    simulator.simulate_echo('This is a file to be deleted.', '>', 'C:\\Users\\Player\\Documents\\delete_me.txt')

def check_level4_success(simulator: WindowsCliSimulator) -> bool:
    """检查第四关是否完成"""
    # 检查文件是否被删除
    target_file = simulator._get_directory('C:\\Users\\Player\\Documents\\delete_me.txt')
    return target_file is None

def setup_level5(simulator: WindowsCliSimulator) -> None:
    """设置第五关的初始状态"""
    # 创建测试文件
    simulator.simulate_echo('Original content', '>', 'C:\\Users\\Player\\Documents\\append.txt')

def check_level5_success(simulator: WindowsCliSimulator) -> bool:
    """检查第五关是否完成"""
    # 检查文件内容是否被追加
    file_content = simulator._get_directory('C:\\Users\\Player\\Documents\\append.txt')
    return file_content == 'Original content\nAppended content'

def setup_level6(simulator: WindowsCliSimulator) -> None:
    """设置第六关的初始状态"""
    # 创建测试目录结构
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6\\subdir1')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level6\\subdir2')
    simulator.simulate_echo('Test file 1', '>', 'C:\\Users\\Player\\Documents\\level6\\file1.txt')
    simulator.simulate_echo('Test file 2', '>', 'C:\\Users\\Player\\Documents\\level6\\subdir1\\file2.txt')

def check_level6_success(simulator: WindowsCliSimulator) -> bool:
    """检查第六关是否完成"""
    # 检查文件是否被移动到新位置
    old_file = simulator._get_directory('C:\\Users\\Player\\Documents\\level6\\file1.txt')
    new_file = simulator._get_directory('C:\\Users\\Player\\Documents\\level6\\subdir2\\file1.txt')
    return old_file is None and new_file is not None

def setup_level7(simulator: WindowsCliSimulator) -> None:
    """设置第七关的初始状态"""
    # 创建测试目录结构
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7\\subdir1')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\level7\\subdir2')
    # 创建多个测试文件
    for i in range(1, 6):
        simulator.simulate_echo(f'Test file {i}', '>', f'C:\\Users\\Player\\Documents\\level7\\file{i}.txt')
    # 创建一个只读文件
    simulator.simulate_echo('Read-only file', '>', 'C:\\Users\\Player\\Documents\\level7\\readonly.txt')

def check_level7_success(simulator: WindowsCliSimulator) -> None:
    """检查第七关是否完成"""
    # 检查是否使用了正确的参数组合
    return simulator.last_command_with_args == ('del', ['/Q', '/F', 'readonly.txt'])

# 定义所有关卡
ALL_LEVELS: List[Level] = [
    Level(
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
        setup_state=setup_level1,
        check_success=check_level1_success,
        hints=[
            "使用 dir 命令查看当前目录内容",
            "使用 cd Documents 进入 Documents 目录",
            "如果输入错误，可以使用 cd .. 返回上一级目录"
        ]
    ),
    Level(
        level_number=2,
        title="创建目录",
        description="""第二关：创建目录
目标：在当前目录下创建一个名为 'my_folder' 的目录

可用命令：
- dir：显示当前目录的内容
- mkdir 目录名：创建新目录
- cd 目录名：进入指定目录

提示：
1. 使用 dir 命令确认当前目录
2. 使用 mkdir 命令创建新目录
3. 使用 dir 命令验证目录是否创建成功
""",
        setup_state=setup_level2,
        check_success=check_level2_success,
        hints=[
            "使用 mkdir my_folder 创建目录",
            "使用 dir 命令确认目录创建成功",
            "确保目录名称完全匹配：my_folder"
        ]
    ),
    Level(
        level_number=3,
        title="文件复制",
        description="""第三关：文件复制
目标：将 source 目录下的 test.txt 文件复制到 target 目录中

可用命令：
- dir：显示当前目录的内容
- cd 目录名：进入指定目录
- copy 源文件 目标文件：复制文件
- type 文件名：查看文件内容

提示：
1. 使用 dir 命令查看 source 目录中的文件
2. 使用 copy 命令复制文件
3. 使用 dir 和 type 命令验证复制结果
""",
        setup_state=setup_level3,
        check_success=check_level3_success,
        hints=[
            "使用 cd source 进入源目录",
            "使用 copy test.txt ..\\target\\test.txt 复制文件",
            "使用 dir ..\\target 确认文件已复制"
        ]
    ),
    Level(
        level_number=4,
        title="文件删除",
        description="""第四关：文件删除
目标：删除 Documents 目录下的 delete_me.txt 文件

可用命令：
- dir：显示当前目录的内容
- del 文件名：删除文件
- type 文件名：查看文件内容

提示：
1. 使用 dir 命令确认文件存在
2. 使用 del 命令删除文件
3. 使用 dir 命令验证文件已被删除
""",
        setup_state=setup_level4,
        check_success=check_level4_success,
        hints=[
            "使用 dir 命令查看文件",
            "使用 del delete_me.txt 删除文件",
            "使用 dir 命令确认文件已删除"
        ]
    ),
    Level(
        level_number=5,
        title="文件追加",
        description="""第五关：文件追加
目标：向 append.txt 文件追加内容 "Appended content"

可用命令：
- type 文件名：查看文件内容
- echo 内容 >> 文件名：向文件追加内容

提示：
1. 使用 type 命令查看文件当前内容
2. 使用 echo 命令和 >> 操作符追加内容
3. 使用 type 命令验证追加结果
""",
        setup_state=setup_level5,
        check_success=check_level5_success,
        hints=[
            "使用 type append.txt 查看文件内容",
            "使用 echo Appended content >> append.txt 追加内容",
            "使用 type append.txt 验证追加结果"
        ]
    ),
    Level(
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
        setup_state=setup_level6,
        check_success=check_level6_success,
        hints=[
            "使用 cd level6 进入目录",
            "使用 move file1.txt subdir2\\file1.txt 移动文件",
            "使用 dir subdir2 确认文件已移动"
        ]
    ),
    Level(
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
        setup_state=setup_level7,
        check_success=check_level7_success,
        hints=[
            "使用 dir /w 查看文件列表",
            "尝试 del readonly.txt 看看会发生什么",
            "使用 del /Q /F readonly.txt 强制删除文件",
            "参数可以组合使用，顺序不重要"
        ]
    )
] 