# Operate Tools

[![OSCS Status](https://www.oscs1024.com/platform/badge/Joker-desire/operate-tools.svg?size=small)](https://www.oscs1024.com/project/Joker-desire/operate-tools?ref=badge_small)

Python操作工具合集

**`Author: Joker-desire`**

## OSCS

[![OSCS Status](https://www.oscs1024.com/platform/badge/Joker-desire/operate-tools.svg?size=large)](https://www.oscs1024.com/project/Joker-desire/operate-tools?ref=badge_large)

## 安装

```shell
pip3 install operate-tools

# v1.0.5版本对整体进行了重写，对于之前的版本请使用以下方式进行安装
pip3 install operate-tools==1.0.4
```

## 功能如下

1. [X] 日期操作
2. [X] 星期操作
3. [X] 时间操作
4. [X] 文件操作
5. [ ] ……

## 功能说明

### 时间日期工具-Date

```python
from operate_tools import Date
```

#### 方法

##### 1. 获取当前日期

```python
Date.now(fmt="%Y-%m-%d %H:%M:%S")
```

##### 2. 获取前几天的日期

```python
Date.days_before(days=31)
```

#### 3. 获取后几天的日期

```python
Date.days_after(days=31)
```

##### 4. 获取昨天的日期

```python
Date.yesterday(fmt="%Y-%m-%d")
```

##### 5. 获取明天的日期

```python
Date.tomorrow(fmt="%Y-%m-%d")
```

##### 6. 获取上周的日期

```python
Date.last_week(fmt="%Y-%m-%d")
```

#### 7. 获取下周的日期

```python
Date.next_week(fmt="%Y-%m-%d")
```

##### 8. 获取上个月的日期

```python
Date.last_month(fmt="%Y-%m-%d")
```

##### 9. 获取下个月的日期

```python
Date.next_month(fmt="%Y-%m-%d")
```

##### 10. 获取开始到结束日期的每一天日期

```python
Date.every_day("2021-01-01", "2021-01-05")
```

##### 11. 计算时间差

```python
Date.time_difference("2022-03-17 16:15:38", "2022-03-17 16:15:40")
```

##### 12. 判断当前时间是否在指定时间范围内

```python
Date.is_within_time_range(start="00:00", end="09:00")
```

##### 13. 时间戳转时间

```python
Date.timestamp_to_time("1626441600000", unit="ms")
Date.timestamp_to_time("1626441600", unit="s")
Date.timestamp_to_time("1626441600000", unit="ms", fmt="%Y-%m-%d")
```

##### 14. 获取当前星期

```python
Date.now_week()
Date.now_week(lang='zh')
Date.now_week(lang='en')
```

##### 15. 获取某一日期的星期

```python
Date.week("2023-07-19")
Date.week(date="2023-07-19", lang="zh")
Date.week(date="2023-07-19", lang="en")
```

### 文件工具-File

```python
from operate_tools import File
```

#### 方法

##### 1. 获取文件的编码格式

```python
File.encode("test/file.txt")
```

##### 2. 编码格式转换

```python
res = File.convert_encode("test/file.txt", "utf-8")
```



