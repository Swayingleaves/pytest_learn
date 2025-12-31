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
- `test_api/` - API测试示例
- `test_ui/` - UI测试示例(Page Object模式)

### 关键设计模式

1. **Fixture依赖注入**: pytest通过参数注入的方式提供fixtures,支持scope参数控制生命周期(session/module/function/class)

2. **单例模式**: Settings配置类使用单例模式,确保测试过程中配置信息一致

3. **钩子机制**: 通过pytest钩子函数(pytest_configure, pytest_runtest_setup等)自定义测试执行流程

4. **模块化设计**: fixtures按功能分类(api/data/ui),便于管理和复用

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
```
