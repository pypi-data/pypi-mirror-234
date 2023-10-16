# 项目描述

分布式主键生成器，支持多机器\|多进程\|多线程并发生成。

# 作者信息

昵称：lcctoor.com

域名：lcctoor.com

邮箱：lcctoor@outlook.com

[主页](https://lcctoor.github.io/arts/) \| [微信](https://lcctoor.github.io/arts/arts/static/static-files/WeChatQRC.jpg) \| [Python交流群](https://lcctoor.github.io/arts/arts/static/static-files/PythonWeChatGroupQRC.jpg) \| [捐赠](https://lcctoor.github.io/arts/arts/static/static-files/DonationQRC-1rmb.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/arts/issues)、[微信](https://lcctoor.github.io/arts/arts/static/static-files/WeChatQRC.jpg) 与我联系。

# 教程

#### 导入

```python
from arts.increment import incrementer
```

#### 创建生成器

```python
inc = incrementer()
```

#### 使用创建生成器时的时间

```python
inc.pk1()
# >>> 'lg85x42f_gsdo_258_1'

inc.pk1()
# >>> 'lg85x42f_gsdo_258_2'

# 'lg85x42f'是创建生成器时的时间
```

#### 使用当前时间

```python
inc.pk2()
# >>> 'lg8657cj_gsdo_258_3'

# 'lg8657cj'是当前时间
```

#### 只返回自增主键

```python
inc.pk3()
# >>> '4'

inc.pk3()
# >>> '5'
```
