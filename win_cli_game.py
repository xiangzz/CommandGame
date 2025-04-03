from typing import List, Optional, Tuple
from core.simulator import WindowsCliSimulator
from core.colors import Colors
from levels import Level, ALL_LEVELS
import base64

class GameManager:
    """游戏管理器类，负责管理游戏状态和流程"""
    
    def __init__(self) -> None:
        """初始化游戏管理器"""
        self.simulator = WindowsCliSimulator()
        self.current_level_index = 0
        self.levels = ALL_LEVELS
        
    def generate_password(self, student_info: str) -> str:
        """生成密码
        
        Args:
            student_info: 学号+姓名
            
        Returns:
            生成的密码
        """
        # 将输入字符串转换为字节数组
        input_bytes = student_info.encode('utf-8')
        # 将'OOP'转换为字节数组并重复到与输入长度相同
        key_bytes = ('OOP' * (len(input_bytes) // 3 + 1))[:len(input_bytes)].encode('utf-8')
        # 对每个字节进行异或运算
        result_bytes = bytes(a ^ b for a, b in zip(input_bytes, key_bytes))
        # 将结果转换为base64字符串
        return base64.b64encode(result_bytes).decode('utf-8')
        
    def verify_password(self, password: str) -> str:
        """验证密码
        
        Args:
            password: 密码
            
        Returns:
            原始学号+姓名信息
        """
        try:
            # 将密码从base64转换回字节数组
            result_bytes = base64.b64decode(password)
            # 将'OOP'转换为字节数组并重复到与密码长度相同
            key_bytes = ('OOP' * (len(result_bytes) // 3 + 1))[:len(result_bytes)].encode('utf-8')
            # 对每个字节进行异或运算
            input_bytes = bytes(a ^ b for a, b in zip(result_bytes, key_bytes))
            # 将结果转换回字符串
            return input_bytes.decode('utf-8')
        except:
            return ""
            
    def collect_student_info(self) -> Optional[str]:
        """收集学生信息
        
        Returns:
            学号+姓名的组合，如果验证失败则返回None
        """
        print(Colors.colorize("\n请输入您的学号和姓名（格式：学号+姓名）", Colors.DESCRIPTION))
        first_input = input().strip()
        print(Colors.colorize("请再次输入您的学号和姓名以确认", Colors.DESCRIPTION))
        second_input = input().strip()
        
        if first_input != second_input:
            print(Colors.colorize("两次输入不一致，请重新开始游戏。", Colors.ERROR))
            return None
            
        return first_input
        
    def get_current_level(self) -> Optional[Level]:
        """获取当前关卡"""
        if self.current_level_index < len(self.levels):
            return self.levels[self.current_level_index]
        return None
        
    def parse_command(self, command: str) -> Tuple[str, List[str]]:
        """解析用户输入的命令
        
        Args:
            command: 用户输入的原始命令字符串
            
        Returns:
            命令名称和参数列表的元组
        """
        parts = command.strip().split()
        if not parts:
            return "", []
        return parts[0], parts[1:]
        
    def execute_command(self, command: str, args: List[str]) -> str:
        """执行用户输入的命令
        
        Args:
            command: 命令名称
            args: 命令参数列表
            
        Returns:
            命令执行结果
        """
        command = command.lower()
        
        if command == 'help':
            current_level = self.get_current_level()
            if current_level:
                return "\n".join(Colors.colorize(hint, Colors.HINT) for hint in current_level.hints)
            return Colors.colorize("没有可用的提示。", Colors.ERROR)
            
        if command == 'exit':
            return Colors.colorize("游戏结束。", Colors.DESCRIPTION)
            
        if command == 'dir':
            path = args[0] if args else None
            options = args[1:] if len(args) > 1 else None
            return self.simulator.simulate_dir(path, options)
            
        if command == 'cd':
            path = args[0] if args else ""
            return self.simulator.simulate_cd(path)
            
        if command == 'mkdir':
            dir_name = args[0] if args else ""
            return self.simulator.simulate_mkdir(dir_name)
            
        if command == 'copy':
            if len(args) < 2:
                return Colors.colorize("语法错误。", Colors.ERROR)
            return self.simulator.simulate_copy(args[0], args[1])
            
        if command == 'del':
            if not args:
                return Colors.colorize("语法错误。", Colors.ERROR)
            options = args[1:] if len(args) > 1 else None
            return self.simulator.simulate_del(args[0], options)
            
        if command == 'type':
            if not args:
                return Colors.colorize("语法错误。", Colors.ERROR)
            return self.simulator.simulate_type(args[0])
            
        if command == 'echo':
            if not args:
                return ""
            # 处理重定向操作符
            if '>' in args or '>>' in args:
                operator = '>' if '>' in args else '>>'
                parts = ' '.join(args).split(operator)
                if len(parts) != 2:
                    return Colors.colorize("语法错误。", Colors.ERROR)
                text = parts[0].strip()
                filename = parts[1].strip()
                return self.simulator.simulate_echo(text, operator, filename)
            return self.simulator.simulate_echo(' '.join(args))
            
        if command == 'move':
            if len(args) < 2:
                return Colors.colorize("语法错误。", Colors.ERROR)
            return self.simulator.simulate_move(args[0], args[1])
            
        return Colors.colorize(f"'{command}' 不是内部或外部命令，也不是可运行的程序或批处理文件。", Colors.ERROR)
        
    def run(self) -> None:
        """运行游戏主循环"""
        print(Colors.colorize("欢迎来到 Windows 命令行学习游戏！", Colors.TITLE))
        print(Colors.colorize("输入 'help' 获取提示，输入 'exit' 退出游戏。\n", Colors.DESCRIPTION))
        
        while True:
            current_level = self.get_current_level()
            if not current_level:
                print(Colors.colorize("\n恭喜你完成了所有关卡！", Colors.SUCCESS))
                
                # 收集学生信息
                student_info = self.collect_student_info()
                if student_info:
                    # 生成密码
                    password = self.generate_password(student_info)
                    print(Colors.colorize(f"\n恭喜您通关，您的通关码为：{password}", Colors.SUCCESS))
                    print(Colors.colorize("请务必牢记，然后通过钉钉发送给老师", Colors.DESCRIPTION))
                break
                
            # 显示当前关卡信息
            print(Colors.colorize(f"\n=== 第 {current_level.level_number} 关：{current_level.title} ===", Colors.TITLE))
            print(Colors.colorize(current_level.description, Colors.DESCRIPTION))
            
            # 设置关卡初始状态
            current_level.setup_state(self.simulator)
            
            # 关卡主循环
            while True:
                # 显示命令提示符
                print(Colors.colorize(f"\n{self.simulator.cwd}>", Colors.PROMPT), end=" ")
                
                # 获取用户输入
                user_input = input().strip()
                if not user_input:
                    continue
                    
                # 解析并执行命令
                command, args = self.parse_command(user_input)
                result = self.execute_command(command, args)
                
                # 显示命令执行结果
                print(Colors.colorize(result, Colors.OUTPUT))
                
                # 检查是否完成关卡
                if current_level.check_success(self.simulator):
                    print(Colors.colorize(f"\n恭喜你完成了第 {current_level.level_number} 关！", Colors.SUCCESS))
                    self.current_level_index += 1
                    break
                    
                # 处理退出命令
                if command == 'exit':
                    return

def main() -> None:
    """游戏入口函数"""
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main() 