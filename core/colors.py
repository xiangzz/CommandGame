from colorama import init, Fore, Back, Style

# 初始化 colorama
init()

class Colors:
    """颜色工具类，用于管理游戏中的颜色显示"""
    
    # 标题颜色
    TITLE = Fore.CYAN + Style.BRIGHT
    
    # 描述文本颜色
    DESCRIPTION = Fore.WHITE
    
    # 提示信息颜色
    HINT = Fore.YELLOW
    
    # 成功信息颜色
    SUCCESS = Fore.GREEN
    
    # 错误信息颜色
    ERROR = Fore.RED
    
    # 命令提示符颜色
    PROMPT = Fore.BLUE
    
    # 命令输出颜色
    OUTPUT = Fore.WHITE
    
    # 重置颜色
    RESET = Style.RESET_ALL
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """为文本添加颜色
        
        Args:
            text: 要添加颜色的文本
            color: 颜色代码
            
        Returns:
            添加了颜色的文本
        """
        return f"{color}{text}{cls.RESET}" 