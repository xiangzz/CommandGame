from core.simulator import WindowsCliSimulator
from .base import Level

def setup_directory_creation_level(simulator: WindowsCliSimulator) -> None:
    """设置目录创建关卡的初始状态"""
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\test_dir')

def check_directory_creation_level(simulator: WindowsCliSimulator) -> bool:
    """检查目录创建关卡是否完成"""
    target_dir = simulator._get_directory('C:\\Users\\Player\\Documents\\my_folder')
    return target_dir is not None

def setup_file_copy_level(simulator: WindowsCliSimulator) -> None:
    """设置文件复制关卡的初始状态"""
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\source')
    simulator.simulate_mkdir('C:\\Users\\Player\\Documents\\target')
    simulator.simulate_echo('Hello, this is a test file!', '>', 'C:\\Users\\Player\\Documents\\source\\test.txt')

def check_file_copy_level(simulator: WindowsCliSimulator) -> bool:
    """检查文件复制关卡是否完成"""
    target_file = simulator._get_directory('C:\\Users\\Player\\Documents\\target\\test.txt')
    return target_file is not None

def setup_file_deletion_level(simulator: WindowsCliSimulator) -> None:
    """设置文件删除关卡的初始状态"""
    simulator.simulate_echo('This is a file to be deleted.', '>', 'C:\\Users\\Player\\Documents\\delete_me.txt')

def check_file_deletion_level(simulator: WindowsCliSimulator) -> bool:
    """检查文件删除关卡是否完成"""
    target_file = simulator._get_directory('C:\\Users\\Player\\Documents\\delete_me.txt')
    return target_file is None

def setup_file_append_level(simulator: WindowsCliSimulator) -> None:
    """设置文件追加关卡的初始状态"""
    simulator.simulate_echo('Original content', '>', 'C:\\Users\\Player\\Documents\\append.txt')

def check_file_append_level(simulator: WindowsCliSimulator) -> bool:
    """检查文件追加关卡是否完成"""
    file_content = simulator._get_directory('C:\\Users\\Player\\Documents\\append.txt')
    return file_content == 'Original content\nAppended content'

DIRECTORY_CREATION_LEVEL = Level(
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
    setup_state=setup_directory_creation_level,
    check_success=check_directory_creation_level,
    hints=[
        "使用 mkdir my_folder 创建目录",
        "使用 dir 命令确认目录创建成功",
        "确保目录名称完全匹配：my_folder"
    ]
)

FILE_COPY_LEVEL = Level(
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
    setup_state=setup_file_copy_level,
    check_success=check_file_copy_level,
    hints=[
        "使用 cd source 进入源目录",
        "使用 copy test.txt ..\\target\\test.txt 复制文件",
        "使用 dir ..\\target 确认文件已复制"
    ]
)

FILE_DELETION_LEVEL = Level(
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
    setup_state=setup_file_deletion_level,
    check_success=check_file_deletion_level,
    hints=[
        "使用 dir 命令查看文件",
        "使用 del delete_me.txt 删除文件",
        "使用 dir 命令确认文件已删除"
    ]
)

FILE_APPEND_LEVEL = Level(
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
    setup_state=setup_file_append_level,
    check_success=check_file_append_level,
    hints=[
        "使用 type append.txt 查看文件内容",
        "使用 echo Appended content >> append.txt 追加内容",
        "使用 type append.txt 验证追加结果"
    ]
) 