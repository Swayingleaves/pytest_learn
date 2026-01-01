# pytest.ini 配置说明

`pytest.ini` 是 pytest 测试框架的配置文件，用于自定义 pytest 的行为和设置。

## 配置项详解

### 主要配置项说明：

1. **`python_files`**: 指定哪些 Python 文件被视为测试文件
   ```ini
   python_files = test_*.py
   ```
   匹配 `test_` 开头的 Python 文件

2. **`python_classes`**: 指定测试类的命名模式
   ```ini
   python_classes = Test*
   ```
   匹配 `Test` 开头的类

3. **`python_functions`**: 指定测试函数的命名模式
   ```ini
   python_functions = test_*
   ```
   匹配 `test_` 开头的函数

4. **`testpaths`**: 指定搜索测试的目录/默认执行用例的目录
   ```ini
   testpaths = tests
   ```
   在 `tests` 目录下搜索测试

5. **`addopts`**: 添加额外的命令行选项
   ```ini
   addopts =
       -v
       --tb=short
       --capture=no
   ```
   - `-v`: 详细输出模式
   - `--tb=short`: 简短的回溯格式
   - `--capture=no`: 不捕获输出

6. **`markers`**: 定义测试标记
   ```ini
   markers =
       smoke: 冒烟测试标记
       api: API测试标记
       ui: UI测试标记
       regression: 回归测试标记
       slow: 耗时测试标记
       user: 用户模块测试标记
       order: 订单模块测试标记
       payment: 支付模块测试标记
   ```

7. **`filterwarnings`**: 过滤警告信息
   ```ini
   filterwarnings =
       ignore::DeprecationWarning
   ```
   忽略 `DeprecationWarning` 警告

## 配置规范

pytest 支持多种配置文件格式：
- `pytest.ini` (项目根目录)
- `pyproject.toml` (在 `[tool.pytest.ini_options]` 部分)
- `setup.cfg` (在 `[tool:pytest]` 部分)
- `tox.ini` (在 `[tool:pytest]` 部分)

### 常用配置选项：

- `testpaths`: 测试文件路径
- `python_files`: 测试文件模式
- `python_classes`: 测试类模式
- `python_functions`: 测试函数模式
- `addopts`: 命令行参数
- `markers`: 自定义标记
- `filterwarnings`: 警告过滤规则
- `minversion`: 最低 pytest 版本要求
- `required_plugins`: 必需的插件

## 标记（Markers）说明

pytest 支持多种内置标记，包括：

- `@pytest.mark.skip` - 无条件跳过测试
- `@pytest.mark.skipif` - 条件跳过测试
- `@pytest.mark.xfail` - 标记预期失败的测试
- `@pytest.mark.parametrize` - 参数化测试

关于 `@pytest.mark.xfail` 的行为：
- 当测试被标记为 xfail 且测试失败时，结果为 `XFAIL`（预期失败）
- 当测试被标记为 xfail 且测试通过时，结果为 `XPASS`（意外通过，即预期会失败但实际通过了）

这个配置文件帮助您标准化项目的测试结构和运行方式，使测试执行更一致和可预测。