class Colors:
    RESET = "\033[0m"

    @staticmethod
    def red(text: str) -> str:
        return f"\033[31m{text}{Colors.RESET}"

    @staticmethod
    def green(text: str) -> str:
        return f"\033[32m{text}{Colors.RESET}"

    @staticmethod
    def yellow(text: str) -> str:
        return f"\033[33m{text}{Colors.RESET}"

    @staticmethod
    def blue(text: str) -> str:
        return f"\033[34m{text}{Colors.RESET}"

    @staticmethod
    def magenta(text: str) -> str:
        return f"\033[35m{text}{Colors.RESET}"

    @staticmethod
    def cyan(text: str) -> str:
        return f"\033[36m{text}{Colors.RESET}"

    @staticmethod
    def white(text: str) -> str:
        return f"\033[37m{text}{Colors.RESET}"

    @staticmethod
    def bold(text: str) -> str:
        return f"\033[1m{text}{Colors.RESET}"