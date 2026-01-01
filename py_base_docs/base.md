
## 0. 运行Python工程的基本步骤
1. 先编写.py测试文件，测试文件中会import一些依赖包
2. 使用 `pip freeze > requirements.txt` 命令将所有我import过的依赖包都统一归总为依赖列表到requirements.txt中
3. 运行py测试文件前需要使用`pip install -r requirements.txt` 安装依赖列表中的所有依赖
4. 使用`pytest`运行所有测试文件

## 1. requirements.txt 依赖管理
- `requirements.txt` 用于管理项目的 Python 依赖包
- 包含项目运行和测试所需的所有库及其版本

## 2. 方法定义位置和访问范围

### 2.1 方法写在类外（函数）
- 可以被同一文件或其他文件下的所有方法调用
- 不需要实例化，可直接调用(在pytest中，模块级别的测试函数可以直接访问)
```python
# 直接调用类外函数
result1 = function_outside_class()  # 可以直接调用
```

### 2.2 方法写在类内

```python
class TestClass:
    class_attribute = "I'm a class attribute"  # 类属性

    def __init__(self): 
        """默认类实例初始化方法，Python 会自动提供一个默认的 __init__方法，它什么都不做（不初始化任何实例属性），因此可以隐藏不展示"""
    def __init__(self, base_url="https://api.example.com"): 
        """自定义类实例初始化方法，传入实例属性变量和默认值，用于实例属性初始化"""
        self.base_url = base_url #  实例属性
    def method_inside_class(self, username, password):
        """定义在类内的实例方法，必须包含 `self` 参数，用于访问实例属性和方法"""
        return "called from inside class"
    # 在类里随便调用和访问
        # 访问实例属性
        self.base_url="https://api.example.com"
        # 调用实例方法
        result1 = method_inside_class("edy", "123456")

    # 在类外需要实例化后调用实例方法，访问实例属性
        # 实例化
        test_instance1 = TestClass() # 根据默认类实例初始化方法创建类实例，无需任何参数
        test_instance2 = TestClass() # 根据自定义类实例初始化方法创建类实例，不传参数
        test_instance3 = TestClass("https://api.exa.com") # 根据自定义类实例初始化方法创建类实例，传入自定义参数
        # 访问实例属性，test_instance1无实例属性
        test_instance2.base_url="https://api.example.com"
        test_instance3.base_url="https://api.exa.com"
        # 调用实例方法
        result4 = test_instance1.method_inside_class("edy", "123456")     # 实例方法需要通过实例调用

    @staticmethod
    def static_method_inside_class():
        """定义在类内的静态方法，使用 `@staticmethod` 装饰器，不需要 `self`"""
        return "static method called from inside class"

    # 无论在类外还是类里，都通过类名直接调用类内的静态方法
    result2 = TestClass.static_method_inside_class()  # 静态方法可以通过类名直接调用

    @classmethod
    def class_method_inside_class(cls):
        """定义在类内的类方法，使用 `@classmethod` 装饰器，使用 `cls` 参数代替 `self`"""
        # 类方法内-访问类属性
        cls.class_attribute = "I'm a class attribute" # cls可以访问类属性，不能访问实例属性，cls.base_url 会报错，因为实例属性不属于类
        return "class method called from inside class"

    # 无论在类外还是类里，都通过类名直接调用类内的类方法
    result3 = TestClass.class_method_inside_class()   # 类方法可以通过类名直接调用
    # 类方法外-访问类属性，无论在类外还是类里，都通过类名直接调访问类属性
    TestClass.class_attribute = "I'm a class attribute"
```
- **实例方法、实例属性**：在类外都需要先实例化类，再通过类的实例来调用和访问；在类里都可以直接调用和访问
- **静态方法**：无论在类外还是类里，都可以通过类名直接调用，不需要实例化
- **类方法、类属性**：无论在类外还是类里，都可以通过类名直接调用和访问，不需要实例化



