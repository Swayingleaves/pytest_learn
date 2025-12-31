"""
全局配置模块

提供测试项目所需的全局配置信息，包括：
- 基础URL配置
- 超时设置
- 测试数据路径
- 报告配置

@author Test Engineer
@date 2025/01/01
"""


class Settings:
    """
    全局配置类

    使用单例模式，确保整个测试过程中配置信息一致
    """

    # 单例实例
    _instance = None

    def __new__(cls):
        """
        创建单例实例

        @return Settings实例
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        初始化配置信息

        在这里定义所有测试所需的配置项
        """
        # ========================================
        # 基础配置
        # ========================================
        # 项目根目录
        self.BASE_DIR = self._get_base_dir()

        # ========================================
        # API配置
        # ========================================
        # 基础URL - 可以根据环境切换
        self.BASE_URL = "https://jsonplaceholder.typicode.com"

        # 请求超时时间（秒）
        self.TIMEOUT = 30

        # ========================================
        # UI配置
        # ========================================
        # 浏览器类型
        self.BROWSER = "chrome"

        # 隐式等待时间（秒）
        self.IMPLICIT_WAIT = 10

        # 显式等待时间（秒）
        self.EXPLICIT_WAIT = 30

        # ========================================
        # 测试数据配置
        # ========================================
        # 测试数据目录
        self.DATA_DIR = self.BASE_DIR / "data"

        # 测试数据文件
        self.TEST_DATA_FILE = self.DATA_DIR / "test_data.json"

        # ========================================
        # 报告配置
        # ========================================
        # 报告输出目录
        self.REPORT_DIR = self.BASE_DIR / "reports"

        # 截图保存目录
        self.SCREENSHOT_DIR = self.BASE_DIR / "screenshots"

        # ========================================
        # 日志配置
        # ========================================
        # 日志级别
        self.LOG_LEVEL = "INFO"

        # 日志文件
        self.LOG_FILE = self.BASE_DIR / "logs" / "test.log"

    def _get_base_dir(self):
        """
        获取项目根目录

        @return Path对象，项目根目录路径
        """
        import pathlib
        return pathlib.Path(__file__).parent.parent.parent

    def get_api_url(self, endpoint):
        """
        获取完整的API URL

        @param endpoint API端点
        @return 完整的URL字符串
        """
        return f"{self.BASE_URL}/{endpoint.lstrip('/')}"


# 创建全局配置实例
settings = Settings()
