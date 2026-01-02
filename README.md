# Pytest自动化测试框架案例项目

## 项目简介
这是一个专为pytest初学者设计的自动化测试学习项目，采用工程化、模块化的结构，帮助你系统地学习pytest测试框架。

## 一、项目初始化

### 1.1 创建项目目录

也可以直接在IDE页面上创建项目
```bash
mkdir pytest_project
cd pytest_project
```

### 1.2 创建虚拟环境

需要进入到项目目录下执行以下命令
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 1.3 安装依赖

创建 `requirements.txt` 文件，添加以下内容：
```
# Pytest学习项目依赖
# 版本：1.0.0

# ============================================
# 核心依赖
# ============================================
pytest>=7.0.0
pytest-html>=4.0.0
pytest-xdist>=3.0.0

# ============================================
# API测试依赖
# ============================================
requests>=2.28.0
httpx>=0.24.0

# ============================================
# UI测试依赖
# ============================================
webdriver-manager>=4.0.0
playwright>=1.40.0
pytest-playwright>=0.4.0

# ============================================
# 工具依赖
# ============================================
pyyaml>=6.0
python-dotenv>=1.0.0
```

安装依赖：
```bash
# 安装全部依赖
pip install -r requirements.txt
# 安装 playwright 浏览器驱动
playwright install
```

## 项目结构
```
pytest_learn/
├── .gitignore          # Git 忽略需要提交的代码文件
├── README.md           # 项目框架说明文档
├── pytest.ini          # pytest配置文件
├── conftest.py         # pytest 全局配置和 fixtures
├── requirements.txt    # 完整依赖(包含API/UI测试)
├── src/                # 工具类和配置
│   ├── utils/          # 工具类
│   │   ├── logger.py          # 日志工具，封装日志记录功能，配置日志格式、级别(如 info、error 等)和输出方式
│   │   └── request_util.py    # HTTP请求工具---规范结构，无实际实用意义，可不看，也可以不创建
│   └── config/         # 配置模块，存放全局配置（如 URL、超时时间等）---规范结构，无实际实用意义，可不看，也可以不创建
│       └── settings.py        # 全局配置---规范结构，无实际实用意义，可不看，也可以不创建
└── data/               # 测试数据、资源等
│   └── test_data.json         # 测试数据文件，存放测试用例中需要使用的静态数据（如用户信息、测试场景等）
│   └── test_img/              # 测试图片文件夹，存放测试用例中需要使用的静态图片，如头像、封面图等（表格数据等可以继续新建一个表格文件夹，专门存放测试需要使用的表格数据）
├── reports/                   # 测试用例执行完毕，输出的测试报告文件存放目录
├── screenshots/               # UI测试用例执行失败时的截图存放目录，可不创建
└── logs/                      # 测试用例执行完毕，输出的日志文件存放目录，一般都是按日期存放
├── tests/              # 测试目录
│   ├── test_learn/     # 测试用例学习示例---实际项目不创建
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
│   └── test_work/      # 测试用例实景案例，包含api和ui，实际项目在这下面写测试用例
│       └── test_01_case_api               # api测试用例
│       └── test_01_case_ui               # ui测试用例
├── docs/               # 自动化测试部分教学文档目录
│   ├── pytest_fixtures详解.md          # pytest fixtures 详细解析文档
│   └── pytest_ini配置说明.md        # pytest.ini 配置说明文档
├── py_base_docs/              # python基础知识教学文档目录
│   ├── base.md          # 基础知识文档
```
## 常用命令

| 命令 | 说明 |
|------|------|
| `pytest` | 运行所有测试 |
| `pytest tests/test_work/test_01_case_ui.py` | 运行指定测试用例，可精确到具体文件，也可定位到某个文件夹 |
| `pytest -v` | 详细输出 |
| `pytest -s` | 打印print输出 |
| `pytest --collect-only` | 列出所有测试 |
| `pytest -k "test_name"` | 运行匹配的测试 |
| `pytest -m smoke` | 运行特定标记的测试 |
| `pytest -m "not slow"` | 排除慢速测试 |
| `pytest --tb=short` | 短格式错误信息 |

## HTML测试报告

### 基本用法
直接使用pytest-html插件，生成美观的HTML测试报告。

```bash
# 生成自包含报告（推荐，可独立分享） 如果不指定执行用例的目录会默认执行所有用例后生成报告
pytest --html=reports/report_$(date +%Y%m%d_%H%M%S).html --self-contained-html -v -s
#  指定执行单个测试用例文件并输出报告
pytest tests/test_work/test_01_case_ui.py --html=reports/report_$(date +%Y%m%d_%H%M%S).html --self-contained-html -v -s
```
**参数说明**：
- `--html=reports/report.html` - 指定报告生成路径
- `--self-contained-html` - 将CSS和JavaScript嵌入HTML，使报告可独立分享

### 使用标记过滤
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

### 查看报告
使用浏览器打开报告HTML文件（如Chrome、Firefox等）即可查看。

### 注意事项
- 报告内容取决于运行的测试范围，不会自动包含所有用例
- reports目录会自动创建（如果不存在）
- 使用`--self-contained-html`确保报告样式可以离线查看

## 实战案例路径（/tests/test_work/）
1. `/tests/test_work/test_01_case_api/` - API测试用例
2. `/tests/test_work/test_01_case_ui/` - UI测试用例

## 学习路径
### 初级阶段（/tests/test_learn/test_basic/）
1. `test_first_test.py` - 编写第一个测试
2. `test_assertions.py` - 学习各种断言方式
3. `test_parametrize.py` - 学习参数化测试
### 进阶阶段（/tests/test_learn/test_advanced/）
4. `test_fixtures.py` - 深入理解fixtures
5. `test_marks.py` - 自定义标记和分类
### 实战阶段（/tests/test_learn/test_api/ 和 /tests/test_learn/test_playwright/）
6. `test_api_demo.py` - API接口测试
   - 包含Cookie认证场景示例
7. `test_playwright_demo.py` - Playwright现代化UI测试
    - 自动等待机制
    - 多浏览器支持（Chromium、Firefox、WebKit）

## 文档资源

### 详细文档
- [pytest fixtures 详解](docs/pytest_fixtures详解.md) - 深入理解pytest fixtures的生命周期和使用场景
- [pytest.ini配置说明](docs/pytest_ini配置说明.md) - 学习如何配置pytest.ini文件

### 测试用例示例
- **基础测试用例**: [test_learn/test_basic/](tests/test_learn/test_basic/) - 测试编写入门
- **高级测试用例**: [test_learn/test_advanced/](tests/test_learn/test_advanced/) - fixtures、标记
- **API测试用例**: [test_learn/test_api/](tests/test_learn/test_api/) - API接口测试和Cookie认证
- **Playwright测试用例**: [test_learn/test_playwright/](tests/test_learn/test_playwright/) - Web端UI自动化测试
- **实战测试用例**: [test_work/](tests/test_work/) - 存放真实的测试用例，用于实际项目测试

## 核心概念---可看可不看，实战案例看懂即可

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