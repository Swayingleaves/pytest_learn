# Pytest学习项目

## 项目简介
这是一个专为pytest初学者设计的自动化测试学习项目，采用工程化、模块化的结构，帮助你系统地学习pytest测试框架。

## 项目结构

```
pytest_learn/
├── .gitignore          # Git忽略配置
├── README.md           # 项目说明文档
├── pytest.ini          # pytest配置文件
├── conftest.py         # pytest全局fixtures和钩子函数
├── requirements.txt    # 完整依赖(包含API/UI测试)
├── requirements-minimal.txt  # 最小依赖(仅运行基础测试)
├── src/                # 工具类和配置
│   ├── utils/          # 工具类
│   │   ├── logger.py          # 日志工具
│   │   └── request_util.py    # HTTP请求工具
│   └── config/         # 配置模块
│       └── settings.py        # 全局配置
├── tests/              # 测试目录
│   ├── test_learn/     # 学习测试示例
│   │   ├── test_basic/        # 基础测试示例
│   │   │   ├── test_first_test.py     # 第一个测试
│   │   │   ├── test_assertions.py     # 断言示例
│   │   │   └── test_parametrize.py    # 参数化测试
│   │   ├── test_advanced/     # 高级测试示例
│   │   │   ├── test_fixtures.py       # fixtures深入
│   │   │   └── test_marks.py          # 自定义标记
│   │   ├── test_api/          # API测试示例
│   │   │   └── test_api_demo.py       # API测试示例
│   │   └── test_playwright/   # Playwright UI测试示例
│   │       ├── test_page.html         # 本地HTML测试页面
│   │       └── test_playwright_demo.py # Playwright测试示例
│   └── test_work/      # 工作测试用例
│       # 存放真实的测试用例
├── docs/               # 文档目录
│   ├── pytest_hooks_guide.md       # pytest钩子函数使用指南
│   ├── api_cookie_auth_guide.md    # API Cookie认证测试指南
│   └── playwright_guide.md         # Pytest-Playwright测试指南
└── data/               # 测试数据
    └── test_data.json              # 示例测试数据
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 方式1：安装最小依赖（推荐初学者）
# 仅包含pytest核心，可运行test_basic目录下的所有基础测试
pip install -r requirements-minimal.txt

# 方式2：安装完整依赖（包含API和UI测试）
# 包含所有测试所需的功能模块
pip install -r requirements.txt
```

> **提示**: 如果你是pytest初学者，建议先使用`requirements-minimal.txt`，专注于学习pytest核心功能。需要学习API或UI测试时，再安装完整依赖。

### 2. 运行测试

```bash
# 运行所有测试
pytest

# 运行学习测试（test_learn目录）
pytest tests/test_learn/

# 运行工作测试（test_work目录）
pytest tests/test_work/

# 运行指定目录
pytest tests/test_learn/test_basic/

# 运行指定文件
pytest tests/test_learn/test_basic/test_first_test.py

# 运行指定测试函数（不在类中）
pytest tests/test_learn/test_basic/test_first_test.py::TestBasicConcepts::test_hello_world

# 使用-k参数匹配测试名（推荐，无需指定完整路径）
pytest tests/test_learn/test_basic/test_first_test.py -k test_hello_world

# 生成HTML报告
pytest --html=reports/report.html

# 显示详细信息
pytest -v
```

> **注意**: 当测试函数位于测试类中时，需要指定完整路径：`pytest [文件]::[类名]::[测试函数名]`。如果不确定完整路径，可以使用 `-k` 参数来匹配测试名称。

## 学习路径

### 初级阶段（/tests/test_learn/test_basic/）
1. `test_first_test.py` - 编写第一个测试
2. `test_assertions.py` - 学习各种断言方式
3. `test_parametrize.py` - 学习参数化测试

### 进阶阶段（/tests/test_learn/test_advanced/）
4. `test_fixtures.py` - 深入理解fixtures
5. `test_hooks.py` - pytest钩子概念
6. `test_hooks_examples.py` - pytest钩子实际示例
7. `test_marks.py` - 自定义标记和分类

### 实战阶段（/tests/test_learn/test_api/ 和 /tests/test_learn/test_playwright/）
8. `test_api_demo.py` - API接口测试
   - 包含Cookie认证场景示例
9. `test_playwright_demo.py` - Playwright现代化UI测试
    - 自动等待机制
    - 多浏览器支持（Chromium、Firefox、WebKit）

## 核心概念

### Fixture
Fixture是pytest的核心功能，用于：
- 准备测试数据
- 设置测试环境
- 清理测试资源
- 管理测试认证（如Cookie认证）

```python
@pytest.fixture
def user_data():
    """返回测试用户数据"""
    return {"username": "test_user", "email": "test@example.com"}

@pytest.fixture
def auth_cookies():
    """返回认证Cookie"""
    return {
        "session_id": "abc123",
        "auth_token": "token123",
        "user_role": "admin"
    }
```

### 参数化测试
使用`@pytest.mark.parametrize`实现数据驱动测试：

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (2, 3, 5),
])
def test_add(a, b, expected):
    assert a + b == expected
```

### 断言
pytest提供简洁的断言语法：

```python
assert actual == expected
assert result is True
assert "error" not in message
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `pytest` | 运行所有测试 |
| `pytest -v` | 详细输出 |
| `pytest -s` | 打印print输出 |
| `pytest --collect-only` | 列出所有测试 |
| `pytest -k "test_name"` | 运行匹配的测试 |
| `pytest -m smoke` | 运行特定标记的测试 |
| `pytest -m "not slow"` | 排除慢速测试 |
| `pytest --tb=short` | 短格式错误信息 |
| `pytest tests/test_playwright/ --browser chromium` | 运行Playwright测试（Chromium） |
| `pytest tests/test_playwright/ --browser firefox` | 运行Playwright测试（Firefox） |
| `pytest tests/test_playwright/ --headed` | 显示浏览器窗口（用于调试） |

## Playwright可视化调试

Playwright测试已配置为可视化调试模式，方便观察测试执行过程：

### 默认配置
- **慢动作模式**：每个操作间隔500毫秒
- **显示浏览器窗口**：非无头模式，可以看到浏览器操作过程
- **失败自动截图**：测试失败时自动截图保存到screenshots目录（已被.gitignore）

### 调试建议
```bash
# 运行单个测试，清楚观察每个步骤
pytest tests/test_learn/test_playwright/test_playwright_demo.py::TestCsdnSearch::test_search_pytest_on_csdn -v -s

# 修改慢动作速度（编辑根目录conftest.py中的browser_type_launch_args fixture）
# "slow_mo": 500  # 改为1000会更慢，100会更快
```

### 配置文件位置
- Playwright配置：[conftest.py](conftest.py) (根目录，已合并所有配置)
- 浏览器启动参数（第170-184行）：控制慢动作模式和窗口显示
- 浏览器上下文参数（第187-211行）：控制viewport、User-Agent等

## HTML测试报告

### 基本用法

pytest-html插件用于生成美观的HTML测试报告。

```bash
# 生成HTML报告（基本用法）
pytest --html=reports/report.html

# 生成自包含报告（推荐，可独立分享）
pytest --html=reports/report.html --self-contained-html
```

**参数说明**：
- `--html=reports/report.html` - 指定报告生成路径
- `--self-contained-html` - 将CSS和JavaScript嵌入HTML，使报告可独立分享

### 指定特定测试用例生成报告

报告只会统计你实际运行的测试用例，不会自动包含所有用例。

#### 1. 指定目录生成报告
```bash
# 只为test_basic目录下的测试生成报告
pytest tests/test_basic/ --html=reports/basic_tests.html --self-contained-html
```

#### 2. 指定单个测试文件
```bash
# 只为test_first_test.py生成报告
pytest tests/test_basic/test_first_test.py --html=reports/single_file.html --self-contained-html
```

#### 3. 使用-k参数过滤测试名称
```bash
# 只运行名称包含"addition"的测试并生成报告
pytest tests/test_basic/ -k "addition" --html=reports/filtered_tests.html --self-contained-html
```

#### 4. 指定单个测试类
```bash
# 只运行TestParametrizeBasic类的测试
pytest tests/test_basic/test_parametrize.py::TestParametrizeBasic --html=reports/single_class.html --self-contained-html
```

#### 5. 指定单个测试函数
```bash
# 只运行test_addition测试函数
pytest tests/test_basic/test_first_test.py::TestMathOperations::test_addition --html=reports/single_test.html --self-contained-html
```

#### 6. 使用标记过滤
```bash
# 只运行带smoke标记的测试
pytest -m smoke --html=reports/smoke_tests.html --self-contained-html

# 排除慢速测试
pytest -m "not slow" --html=reports/fast_tests.html --self-contained-html
```

### 报告内容说明

生成的HTML报告包含：
- **Summary**: 测试总数、通过数、失败数、跳过数、执行时间
- **Test Results**: 每个测试的详细信息
  - 测试名称和状态
  - 执行时间
  - 错误堆栈（失败时）
  - 日志输出（如果有）

### 高级用法

```bash
# 生成带时间戳的报告（避免覆盖）
pytest --html=reports/report_$(date +%Y%m%d_%H%M%S).html --self-contained-html

# 同时生成详细输出和报告
pytest --html=reports/report.html --self-contained-html -v -s
```

### 查看报告

```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

### 注意事项

- 报告内容取决于运行的测试范围，不会自动包含所有用例
- reports目录会自动创建（如果不存在）
- 使用`--self-contained-html`确保报告样式可以离线查看

## 文档资源

### 详细文档
- [pytest钩子函数使用指南](docs/pytest_hooks_guide.md) - 深入理解pytest钩子函数的生命周期和使用场景
- [API Cookie认证测试指南](docs/api_cookie_auth_guide.md) - 学习如何使用Cookie进行API认证测试
- [Pytest-Playwright测试指南](docs/playwright_guide.md) - 学习如何使用Playwright进行现代化浏览器自动化测试

### 测试示例
- **基础测试**: [test_learn/test_basic/](tests/test_learn/test_basic/) - 测试编写入门
- **高级测试**: [test_learn/test_advanced/](tests/test_learn/test_advanced/) - fixtures、钩子、标记
- **API测试**: [test_learn/test_api/](tests/test_learn/test_api/) - API接口测试和Cookie认证
- **Playwright测试**: [test_learn/test_playwright/](tests/test_learn/test_playwright/) - 现代化浏览器自动化测试
- **工作测试**: [test_work/](tests/test_work/) - 存放真实的测试用例

## 依赖包说明

### 最小依赖（requirements-minimal.txt）
| 依赖包 | 用途 | 是否必需 |
|--------|------|---------|
| `pytest>=7.0.0` | 测试框架核心 | ✅ 必需 |

### 完整依赖（requirements.txt）
| 依赖包 | 用途 | 是否必需 |
|--------|------|---------|
| `pytest` | 测试框架核心 | ✅ 必需 |
| `pytest-html` | HTML报告生成 | ❌ 可选 |
| `pytest-xdist` | 并行测试执行 | ❌ 可选 |
| `requests` | HTTP请求库(API测试) | ❌ 可选 |
| `httpx` | 异步HTTP请求库(API测试) | ❌ 可选 |
| `selenium` | Selenium UI自动化测试 | ❌ 可选 |
| `webdriver-manager` | 浏览器驱动管理 | ❌ 可选 |
| `playwright` | 现代化浏览器自动化测试 | ❌ 可选 |
| `pytest-playwright` | pytest-playwright插件 | ❌ 可选 |
| `pyyaml` | YAML配置文件解析 | ❌ 可选 |
| `python-dotenv` | 环境变量管理 | ❌ 可选 |

> **注意**: 运行`test_basic`目录下的基础测试只需要最小依赖即可，学习高级功能和实战案例时需要完整依赖。使用Playwright测试前还需要运行 `playwright install` 安装浏览器驱动。

## 版本信息

- 版本：1.0.0
- 作者：Test Engineer
- 日期：2025/01/01
