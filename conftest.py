"""
Pytest全局配置文件

此文件是pytest的配置文件，会自动被pytest加载。
在这里定义全局可用的fixtures和钩子函数。

@author Test Engineer
@date 2025/01/01
"""

import pytest
import sys
from pathlib import Path

# ========================================
# 路径配置 - 将src目录添加到Python路径
# ========================================
# 这样可以在测试文件中直接导入src包下的模块
def add_src_to_path():
    """
    将src目录添加到Python路径

    这样测试文件可以直接使用：
        from src.utils.logger import get_logger
    """
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

add_src_to_path()


# ========================================
# 全局Fixtures
# ========================================

@pytest.fixture(scope="session")
def settings():
    """
    全局配置fixture

    提供对全局配置对象Settings的访问。
    使用session作用域，确保整个测试会话期间只创建一次。

    @return Settings 配置对象实例
    """
    from src.config.settings import Settings
    return Settings()


@pytest.fixture(scope="session")
def logger():
    """
    日志器fixture

    提供统一的日志记录功能。
    使用session作用域，确保日志器在整个会话期间一致。

    @return LoggerUtil 日志工具实例
    """
    from src.utils.logger import LoggerUtil
    return LoggerUtil()


@pytest.fixture(scope="function")
def timer():
    """
    测试计时器fixture

    用于测量测试执行时间，帮助识别慢测试。

    使用示例：
        def test_something(timer):
            with timer:
                # 执行测试代码
                pass
            print(f"测试耗时: {timer.elapsed:.2f}秒")

    @return TimerContext 测试计时器上下文
    """
    import time

    class Timer:
        """计时器类"""

        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.elapsed = 0

        def __enter__(self):
            """进入上下文时开始计时"""
            self.start_time = time.time()
            return self

        def __exit__(self, *args):
            """退出上下文时停止计时"""
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time

    return Timer()


# ========================================
# Pytest Hooks (钩子函数)
# ========================================

def pytest_configure(config):
    """
    pytest配置钩子

    在pytest初始化时调用，可以进行自定义配置。

    使用场景：
    - 注册自定义标记
    - 添加全局配置
    - 初始化插件

    @param config pytest配置对象
    """
    # 注册自定义标记，避免运行时警告
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "api: API测试")
    config.addinivalue_line("markers", "ui: UI测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "slow: 慢速测试")
    config.addinivalue_line("markers", "fast: 快速测试")

    # 打印配置信息
    print("\n" + "="*60)
    print("🚀 Pytest 配置初始化")
    print(f"📂 项目根目录: {config.rootpath}")
    print("="*60)


def pytest_collection_modifyitems(config, items):
    """
    测试用例收集修改钩子

    在测试用例收集完成后、排序前调用。
    可以用于修改、过滤或排序测试用例。

    使用场景：
    - 自动添加标记
    - 动态修改测试顺序
    - 根据条件过滤测试
    - 添加测试ID

    @param config pytest配置对象
    @param items 收集到的测试用例列表
    """
    # 示例1：给所有测试用例添加通用标记
    for item in items:
        # 根据测试名称添加快速/慢速标记
        if "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
        else:
            item.add_marker(pytest.mark.fast)

    # 示例2：统计测试数量
    print(f"\n📊 收集到 {len(items)} 个测试用例")

    # 示例3：按测试名称排序（可选）
    # items.sort(key=lambda x: x.nodeid)


def pytest_runtest_setup(item):
    """
    测试执行前钩子

    在每个测试用例执行前调用。

    使用场景：
    - 测试前的数据准备
    - 检查测试前置条件
    - 打印测试开始信息
    - 记录测试开始时间

    @param item 当前执行的测试用例
    """
    # 打印测试用例名称
    print(f"\n▶️  开始测试: {item.name}")

    # 检查是否包含特定标记
    if item.get_closest_marker("slow"):
        print("  ⚠️  这是一个慢速测试")


def pytest_runtest_teardown(item, nextitem):
    """
    测试执行后钩子

    在每个测试用例执行后调用（无论成功或失败）。

    使用场景：
    - 清理测试数据
    - 关闭资源（文件、数据库连接等）
    - 打印测试结束信息

    @param item 当前执行的测试用例
    @param nextitem 下一个要执行的测试用例（可能是None）
    """
    # 打印测试完成信息
    print(f"✅ 测试完成: {item.name}")

    if nextitem:
        print(f"  ⏭️  下一个: {nextitem.name}")
    else:
        print("  🏁 所有测试已完成")


def pytest_runtest_makereport(item, call):
    """
    测试结果报告钩子

    在测试结果生成时调用，可以用于自定义报告。

    使用场景：
    - 生成自定义测试报告
    - 记录测试结果到日志
    - 根据测试结果执行特定操作
    - 添加测试截图（失败时）

    @param item 当前执行的测试用例
    @param call 测试执行调用信息
    """
    # 当测试执行完成时（when = 'call'）
    if call.when == "call":
        # 测试通过时打印信息
        if call.excinfo is None:
            print(f"  🎉 测试通过!")
        # 测试失败时打印信息
        elif call.excinfo and call.excinfo.typename not in ("Skipped", "XFailed"):
            print(f"  ❌ 测试失败")
        # 测试跳过时打印信息
        elif call.excinfo and call.excinfo.typename == "Skipped":
            print(f"  ⏭️  测试跳过")


def pytest_sessionstart(session):
    """
    测试会话开始钩子

    在整个测试会话开始时调用一次。

    使用场景：
    - 初始化测试环境
    - 打开数据库连接
    - 创建测试数据目录
    - 记录会话开始时间

    @param session 测试会话对象
    """
    print("\n" + "🌟"*30)
    print("📋 测试会话开始")
    print(f"⏰ 开始时间: {session.config._inicache.get('python_version', 'N/A')}")
    print("🌟"*30)


def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束钩子

    在整个测试会话结束时调用一次。

    使用场景：
    - 清理测试环境
    - 关闭数据库连接
    - 生成最终报告
    - 发送测试结果通知

    @param session 测试会话对象
    @param exitstatus 退出状态码
    """
    print("\n" + "🌟"*30)
    print("📋 测试会话结束")
    print(f"📊 退出状态: {exitstatus}")
    print("🌟"*30)
