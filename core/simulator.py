from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
from datetime import datetime
import os

class WindowsCliSimulator:
    """Windows 命令行模拟器类，用于模拟 Windows 命令行的行为。"""
    
    def __init__(self) -> None:
        """初始化模拟器，设置虚拟文件系统和当前工作目录。"""
        self.file_system: Dict[str, Union[str, Dict]] = {
            'C:': {
                'Users': {
                    'Player': {
                        'Documents': {},
                        'Desktop': {}
                    }
                }
            }
        }
        self.cwd: str = 'C:\\Users\\Player'
        self.last_command_with_args: Optional[Tuple[str, List[str]]] = None
        
    def _normalize_path(self, path: str) -> str:
        """规范化路径，处理相对路径和绝对路径。
        
        Args:
            path: 输入的路径字符串
            
        Returns:
            规范化后的路径字符串
        """
        if not path:
            return self.cwd
            
        # 处理驱动器切换
        if path.endswith(':'):
            return path + '\\'
            
        # 处理绝对路径
        if path.startswith('C:\\'):
            return path
            
        # 处理相对路径
        return os.path.join(self.cwd, path)
        
    def _get_path_parts(self, path: str) -> List[str]:
        """将路径分解为部分。
        
        Args:
            path: 路径字符串
            
        Returns:
            路径部分列表
        """
        return [p for p in path.split('\\') if p]
        
    def _get_directory(self, path: str) -> Optional[Union[str, Dict]]:
        """获取指定路径的目录内容或文件内容。
        
        Args:
            path: 目标路径
            
        Returns:
            目录内容字典、文件内容字符串或 None（如果不存在）
        """
        current = self.file_system
        for part in self._get_path_parts(path):
            if part not in current:
                return None
            current = current[part]
        return current
        
    def _get_parent_directory(self, path: str) -> Optional[Dict]:
        """获取指定路径的父目录。
        
        Args:
            path: 目标路径
            
        Returns:
            父目录字典或 None（如果不存在）
        """
        parent_path = os.path.dirname(path)
        if not parent_path:
            return None
        return self._get_directory(parent_path)
        
    def simulate_dir(self, path: Optional[str] = None, options: Optional[List[str]] = None) -> str:
        """模拟 dir 命令的输出。
        
        Args:
            path: 目标路径
            options: 命令选项列表
            
        Returns:
            模拟的 dir 命令输出
        """
        self.last_command_with_args = ('dir', [path] if path else [] + (options or []))
        
        target_path = self._normalize_path(path) if path else self.cwd
        directory = self._get_directory(target_path)
        
        if directory is None or isinstance(directory, str):
            return f"系统找不到指定的路径。\n{target_path}"
            
        output = []
        output.append(f" {target_path} 的目录\n")
        
        # 处理 /w 选项（宽格式显示）
        if options and '/w' in options:
            # 宽格式显示：只显示文件名，每行多个
            names = []
            for name, content in directory.items():
                if isinstance(content, dict):
                    names.append(f"[{name}]")
                else:
                    names.append(name)
            # 每行显示5个文件名
            for i in range(0, len(names), 5):
                output.append(' '.join(names[i:i+5]))
            return '\n'.join(output)
            
        # 处理 /p 选项（分页显示）
        if options and '/p' in options:
            # 分页显示：每页显示20个项目
            items = []
            if target_path != 'C:\\':
                items.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}    <DIR>          ..")
            for name, content in directory.items():
                if isinstance(content, dict):
                    items.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}    <DIR>          {name}")
                else:
                    items.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}                 {len(content)} {name}")
            # 每页显示20个项目
            for i in range(0, len(items), 20):
                output.extend(items[i:i+20])
                if i + 20 < len(items):
                    output.append("\n按任意键继续...")
            return '\n'.join(output)
            
        # 默认显示格式
        if target_path != 'C:\\':
            output.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}    <DIR>          ..")
            
        for name, content in directory.items():
            if isinstance(content, dict):
                output.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}    <DIR>          {name}")
            else:
                output.append(f"{datetime.now().strftime('%Y-%m-%d  %H:%M')}                 {len(content)} {name}")
                
        return '\n'.join(output)
        
    def simulate_cd(self, target_path: str) -> str:
        """模拟 cd 命令。
        
        Args:
            target_path: 目标路径
            
        Returns:
            命令执行结果消息
        """
        if not target_path:
            return self.cwd
            
        # 处理特殊路径
        if target_path == '..':
            new_path = os.path.dirname(self.cwd)
            if new_path:
                self.cwd = new_path
                return self.cwd
            return "系统找不到指定的路径。"
            
        if target_path == '\\':
            self.cwd = 'C:\\'
            return self.cwd
            
        # 处理驱动器切换
        if target_path.endswith(':'):
            if target_path in self.file_system:
                self.cwd = target_path + '\\'
                return self.cwd
            return "系统找不到指定的驱动器。"
            
        # 处理普通路径
        new_path = self._normalize_path(target_path)
        if self._get_directory(new_path) is not None and isinstance(self._get_directory(new_path), dict):
            self.cwd = new_path
            return self.cwd
        return "系统找不到指定的路径。"
        
    def simulate_mkdir(self, dir_name: str) -> str:
        """模拟 mkdir 命令。
        
        Args:
            dir_name: 要创建的目录名
            
        Returns:
            命令执行结果消息
        """
        if not dir_name:
            return "语法错误。"
            
        target_path = self._normalize_path(dir_name)
        parent_path = os.path.dirname(target_path)
        new_dir_name = os.path.basename(target_path)
        
        parent_dir = self._get_directory(parent_path)
        if parent_dir is None or isinstance(parent_dir, str):
            return "系统找不到指定的路径。"
            
        if new_dir_name in parent_dir:
            return f"子目录或文件 {new_dir_name} 已经存在。"
            
        parent_dir[new_dir_name] = {}
        return f"已创建目录 {target_path}"
        
    def simulate_copy(self, source: str, destination: str) -> str:
        """模拟 copy 命令。
        
        Args:
            source: 源文件路径
            destination: 目标文件路径
            
        Returns:
            命令执行结果消息
        """
        if not source or not destination:
            return "语法错误。"
            
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)
        
        source_content = self._get_directory(source_path)
        if source_content is None:
            return f"系统找不到指定的文件。\n{source_path}"
            
        if isinstance(source_content, dict):
            return "无法复制目录。"
            
        dest_parent = self._get_parent_directory(dest_path)
        if dest_parent is None:
            return "系统找不到指定的路径。"
            
        dest_name = os.path.basename(dest_path)
        dest_parent[dest_name] = source_content
        return f"已复制         1 个文件。"
        
    def simulate_del(self, target: str, options: Optional[List[str]] = None) -> str:
        """模拟 del 命令。
        
        Args:
            target: 目标文件路径
            options: 命令选项列表
            
        Returns:
            命令执行结果消息
        """
        self.last_command_with_args = ('del', [target] + (options or []))
        
        if not target:
            return "语法错误。"
            
        target_path = self._normalize_path(target)
        parent_dir = self._get_parent_directory(target_path)
        
        if parent_dir is None:
            return "系统找不到指定的路径。"
            
        target_name = os.path.basename(target_path)
        if target_name not in parent_dir:
            return f"系统找不到指定的文件。\n{target_path}"
            
        if isinstance(parent_dir[target_name], dict):
            return "无法删除目录。"
            
        # 模拟只读文件
        if target_name == 'readonly.txt':
            if not options or ('/F' not in options):
                return "拒绝访问。"
                
        # 模拟确认提示
        if not options or ('/Q' not in options):
            return "是否确认(Y/N)?"
            
        del parent_dir[target_name]
        return "文件已删除。"
        
    def simulate_type(self, filename: str) -> str:
        """模拟 type 命令。
        
        Args:
            filename: 要显示内容的文件名
            
        Returns:
            文件内容或错误消息
        """
        if not filename:
            return "语法错误。"
            
        file_path = self._normalize_path(filename)
        file_content = self._get_directory(file_path)
        
        if file_content is None:
            return f"系统找不到指定的文件。\n{file_path}"
            
        if isinstance(file_content, dict):
            return "无法显示目录内容。"
            
        return file_content
        
    def simulate_echo(self, text: str, operator: Optional[str] = None, filename: Optional[str] = None) -> str:
        """模拟 echo 命令。
        
        Args:
            text: 要输出的文本
            operator: 操作符（> 或 >>）
            filename: 目标文件名
            
        Returns:
            命令执行结果消息
        """
        if not text:
            return ""
            
        if not operator or not filename:
            return text
            
        file_path = self._normalize_path(filename)
        parent_dir = self._get_parent_directory(file_path)
        
        if parent_dir is None:
            return "系统找不到指定的路径。"
            
        file_name = os.path.basename(file_path)
        
        if operator == '>':
            parent_dir[file_name] = text
            return ""
        elif operator == '>>':
            if file_name in parent_dir and isinstance(parent_dir[file_name], str):
                parent_dir[file_name] += '\n' + text
            else:
                parent_dir[file_name] = text
            return ""
        else:
            return text
            
    def simulate_move(self, source: str, destination: str) -> str:
        """模拟 move 命令。
        
        Args:
            source: 源文件路径
            destination: 目标文件路径
            
        Returns:
            命令执行结果消息
        """
        if not source or not destination:
            return "语法错误。"
            
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(destination)
        
        source_content = self._get_directory(source_path)
        if source_content is None:
            return f"系统找不到指定的文件。\n{source_path}"
            
        if isinstance(source_content, dict):
            return "无法移动目录。"
            
        dest_parent = self._get_parent_directory(dest_path)
        if dest_parent is None:
            return "系统找不到指定的路径。"
            
        dest_name = os.path.basename(dest_path)
        dest_parent[dest_name] = source_content
        
        # 删除源文件
        source_parent = self._get_parent_directory(source_path)
        if source_parent is not None:
            source_name = os.path.basename(source_path)
            if source_name in source_parent:
                del source_parent[source_name]
                
        return f"已移动         1 个文件。" 