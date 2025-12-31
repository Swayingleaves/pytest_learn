# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个pytest自动化测试学习项目,采用工程化、模块化的结构设计,用于系统地学习pytest测试框架。项目包含基础测试、高级测试、API测试和UI测试等完整的学习路径。

## 开发环境配置

### 激活虚拟环境
```bash
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate      # Windows
```

### 安装依赖
```bash
# 方式1：最小依赖（推荐初学者）
pip install -r requirements-minimal.txt

# 方式2：完整依赖（包含API和UI测试）
pip install -r requirements.txt
```

## 常用命令

### 测试执行
```bash
# 运行所有测试
pytest

# 运行指定目录
pytest tests/test_basic/

# 运行指定文件
pytest tests/test_basic/test_first_test.py

# 运行指定测试函数
pytest tests/test_basic/test_first_test.py::TestBasicConcepts::test_hello_world

# 显示详细输出
pytest -v

# 显示print输出
pytest -s
```

### 测试筛选
```bash
# 运行匹配名称的测试
pytest -k "test_add"

# 运行特定标记的测试
pytest -m smoke
pytest -m api
pytest -m "not slow"

# 并行执行测试
pytest -n auto
```

### 报告生成
```bash
# 生成HTML报告
pytest --html=reports/report.html

# 短格式错误信息
pytest --tb=short

# 只列出测试不执行
pytest --collect-only
```

## 代码架构

### 核心配置文件

**conftest.py** - 项目根目录的全局配置
- 自动将`src`目录添加到Python路径,允许测试文件直接导入`src`模块
- 提供全局fixtures: `settings`(配置单例), `logger`(日志工具), `timer`(测试计时)
- 定义pytest钩子函数,用于测试生命周期的自定义处理

**pytest.ini** - pytest框架配置
- 定义测试发现规则(文件名、类名、函数名模式)
- 配置默认参数: `-v`(详细模式), `--tb=short`(简短错误信息), `--capture=no`(不捕获输出)
- 定义测试标记: smoke, api, ui, regression, slow, user, order, payment

### 目录结构说明

**src/** - 源代码目录
- `fixtures/` - 自定义测试fixtures
  - `api_fixture.py` - API测试fixtures(api_base_url, api_session, valid_user_data等)
  - `data_fixture.py` - 测试数据fixtures
  - `ui_fixture.py` - UI测试fixtures
- `utils/` - 工具类
  - `logger.py` - 日志工具
  - `request_util.py` - HTTP请求工具
- `config/` - 配置模块
  - `settings.py` - 全局配置类(单例模式,包含API URL、超时设置、测试数据路径等)

**tests/** - 测试目录
- `conftest.py` - 测试目录级别的fixtures(会继承根目录的conftest)
- `test_basic/` - 基础测试示例(测试编写入门)
- `test_advanced/` - 高级测试示例(fixtures深入、钩子、标记)
  - `test_hooks.py` - pytest钩子概念介绍
  - `test_hooks_examples.py` - pytest钩子实际示例(配合conftest.py中的钩子函数)
- `test_api/` - API测试示例
  - `test_api_demo.py` - 包含Cookie认证场景的API测试
- `test_ui/` - UI测试示例(Page Object模式)
- `test_playwright/` - Playwright现代化UI测试示例
  - `conftest.py` - Playwright配置和失败截图钩子
  - `test_playwright_demo.py` - Playwright测试示例(基础/高级/断言/表单/等待)

**docs/** - 文档目录
- `pytest_hooks_guide.md` - pytest钩子函数完整使用指南
- `api_cookie_auth_guide.md` - API Cookie认证测试指南
- `playwright_guide.md` - Pytest-Playwright测试完整指南

**data/** - 测试数据
- `test_data.json` - 示例测试数据文件

### 关键设计模式

1. **Fixture依赖注入**: pytest通过参数注入的方式提供fixtures,支持scope参数控制生命周期(session/module/function/class)

2. **单例模式**: Settings配置类使用单例模式,确保测试过程中配置信息一致

3. **钩子机制**: 通过pytest钩子函数(pytest_configure, pytest_runtest_setup等)自定义测试执行流程
   - conftest.py中定义了7个常用钩子函数
   - test_hooks_examples.py演示钩子的实际效果

4. **模块化设计**: fixtures按功能分类(api/data/ui),便于管理和复用

5. **Cookie认证模式**: 通过fixture管理认证信息
   - 静态Cookie: 测试环境使用固定认证信息
   - 动态Cookie: 通过登录API获取实时认证信息
   - RequestUtil支持cookies参数,在GET/POST请求中携带认证信息

## 命名规范

- 测试文件: `test_*.py` 或 `*_test.py`
- 测试函数: `test_*`
- 测试类: `Test*`
- Fixture函数: 通过`@pytest.fixture`装饰器定义,名称即为fixture名称

## 全局配置访问

在测试中可直接使用以下全局fixtures:
```python
def test_example(settings, logger, timer):
    # settings - Settings配置实例
    # logger - LoggerUtil日志工具
    # timer - 测试计时器
    pass
```

## 导入说明

由于conftest.py已将src目录添加到Python路径,测试文件中可直接导入:
```python
from src.utils.logger import LoggerUtil
from src.config.settings import Settings
from src.fixtures.api_fixture import api_fixtures
from src.utils.request_util import RequestUtil
```

## 核心功能特性

### 1. pytest钩子函数系统
项目在conftest.py中实现了完整的钩子函数系统,包括:
- `pytest_configure` - 配置初始化和标记注册
- `pytest_collection_modifyitems` - 测试收集和自动标记
- `pytest_runtest_setup` - 测试执行前钩子
- `pytest_runtest_teardown` - 测试执行后钩子
- `pytest_runtest_makereport` - 测试结果报告钩子
- `pytest_sessionstart` - 会话开始钩子
- `pytest_sessionfinish` - 会话结束钩子

运行`pytest tests/test_advanced/test_hooks_examples.py -v -s`可查看钩子效果。

### 2. Cookie认证支持
RequestUtil工具类已扩展支持Cookie认证:
- GET方法支持cookies参数
- POST方法支持cookies参数
- 提供静态和动态两种认证fixture模式

示例:
```python
# 使用静态Cookie
def test_with_auth(self, settings, auth_cookies):
    response = RequestUtil.get(url, cookies=auth_cookies)

# 使用动态Cookie
def test_with_dynamic_auth(self, settings, dynamic_auth_token):
    response = RequestUtil.post(url, json=data, cookies=dynamic_auth_token)
```

详细文档请参考: [docs/api_cookie_auth_guide.md](docs/api_cookie_auth_guide.md)

### 3. 全局Fixtures
- `settings` - Settings配置单例,提供API URL、超时等配置
- `logger` - LoggerUtil日志工具,支持测试日志记录
- `timer` - 测试计时器,记录每个测试的执行时间

### 4. 测试标记系统
项目支持以下测试标记:
- `smoke` - 冒烟测试
- `api` - API测试
- `ui` - UI测试
- `regression` - 回归测试
- `slow` - 慢速测试
- `fast` - 快速测试(自动添加)

使用示例:
```bash
# 只运行冒烟测试
pytest -m smoke

# 排除慢速测试
pytest -m "not slow"
```
