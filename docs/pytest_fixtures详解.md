# pytest fixtures 详解

## 什么是 fixtures
`pytest fixtures` 是 pytest 框架中用于设置测试前置条件、提供测试数据和资源的机制。fixtures 用于在测试执行前准备必要的环境，并在测试结束后清理资源。

## fixtures 的基本概念

### 1. 定义 fixture
使用 `@pytest.fixture` 装饰器来定义一个 fixture：

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "test", "value": 42}
```

### 2. 使用 fixture
在测试函数中通过参数名来使用 fixture：

```python
def test_example(sample_data):
    assert sample_data["name"] == "test"
    assert sample_data["value"] == 42
```

## fixture 的作用域（Scope）
fixture 的作用域决定了 fixture 的创建和销毁时机：
@pytest.fixture()方法写在class里只能被该class里的方法调用，不能被该class外的方法调用。
@pytest.fixture()方法写在class外或其他文件下，可以被该文件下或其他文件下的所有方法调用。

```python
@pytest.fixture(scope="function") # scope="class"\scope="module"\scope="session"
def temp_file():
    file = create_temp_file()
    yield file
    os.remove(file)
```
### function（默认）
- 每执行一个调用fixture的测试函数，都需要跑一次fixture对应函数，返回一次新的结果---执行前创建，测试结束后销毁
- 适用于每个测试都需要独立实例的场景

### class
- 每个类里任意/多个函数调用fixture的测试函数，只跑一次fixture对应函数，返回一次结果；多个类则跑多次，返回多次结果---每个测试类执行前创建，类中所有测试执行完毕后销毁
- 适用于整个测试类共享资源的场景

### module
- 每个模块(文件)执行前创建，模块中所有测试执行完毕后销毁
- 适用于整个模块共享资源的场景

### session
- 整个测试会话(一次pytest运行)期间只创建一次，所有测试执行完毕后销毁
- 适用于昂贵的设置操作，如数据库连接


## fixture 依赖
一个 fixture 可以依赖于其他 fixture：

```python
@pytest.fixture
def user_data():
    return {"id": 1, "name": "test_user"}

@pytest.fixture
def authenticated_user(user_data):
    # 依赖于 user_data fixture
    user = create_user(user_data)
    login_user(user)
```
## 与 setup/teardown 的比较
相比于传统的 `setup_method`/`teardown_method`，fixtures 提供了更灵活的依赖注入机制，允许更复杂的测试设置场景。