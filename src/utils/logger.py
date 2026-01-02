"""
日志工具模块

提供统一的日志配置和日志记录功能。
支持控制台和文件两种输出方式。

@author Test Engineer
@date 2025/01/01
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class LoggerUtil:
    """
    日志工具类

    使用单例模式，提供统一的日志配置。
    支持日志级别设置、格式定制、文件输出等功能。
    """

    # 单例实例
    _instance: Optional['LoggerUtil'] = None
    # 日志器实例
    _logger: Optional[logging.Logger] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._logger is None:
            self._initialize_logger()

    def _initialize_logger(self):
        """
        初始化日志配置

        配置日志格式、级别和输出方式
        """
        # 创建日志器
        logger = logging.getLogger("pytest_learn")
        # 设置最低打印日志级别 DEBUG < INFO < WARNING < ERROR < CRITICAL
        logger.setLevel(logging.DEBUG)

        # 创建格式器 - 定义日志输出格式
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 创建控制台处理器 - 输出到控制台
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 创建文件处理器 - 输出到文件
        # 获取项目根目录
        project_root = Path(__file__).parent.parent.parent
        logs_dir = project_root / "logs"
        # 确保日志目录存在
        logs_dir.mkdir(exist_ok=True)

        # 日志文件按日期命名
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = logs_dir / f"pytest_{today}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 保存日志器实例
        self._logger = logger

    def get_logger(self) -> logging.Logger:
        """
        获取日志器实例

        @return logging.Logger 日志器对象
        """
        return self._logger

    def debug(self, message: str):
        """
        记录debug级别日志

        @param message 日志消息
        """
        self._logger.debug(message)

    def info(self, message: str):
        """
        记录info级别日志

        @param message 日志消息
        """
        self._logger.info(message)

    def warning(self, message: str):
        """
        记录warning级别日志

        @param message 日志消息
        """
        self._logger.warning(message)

    def error(self, message: str):
        """
        记录error级别日志

        @param message 日志消息
        """
        self._logger.error(message)

    def critical(self, message: str):
        """
        记录critical级别日志

        @param message 日志消息
        """
        self._logger.critical(message)

# 提供便捷的日志获取方法
def get_logger() -> logging.Logger:
    """
    获取日志器的便捷函数

    @return logging.Logger 日志器对象
    """
    return logger_util.get_logger()
