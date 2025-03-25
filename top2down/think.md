# 从一个例子来实践自顶向下的程序设计
+ 首先是对自顶向下设计思路的实践
+  然后是代码优化过程

## 任务
```
程序： calender
输入: 公元年份 year(1900以后)
输出: year 年的年历
```

## 任务分解
+ 输入年份 year
+ 计算year年01月01日是星期几
+ 得到全年年历

对应的顶层代码抽象为:

```python
def calender():
    year = get_year()
    w = first_day(year)
    print_cal(year,w)
```
在这层中我们主要做如下两件事
+ 总体任务模块划分
+ 模块间输出数据结构确定
  + year为形如1902,2022这样的整数
  + 星期几w 为[0,1,2,3...,6]这样的整数


## 第二层
### get_year实现
由于只是输入年份，所以在第二层就可以将get_year的函数完全实现

```python
def get_year():
    year = input("Please input the year(after 1900s)")
    return year
```

### first_day实现
+ 总体思路： 我们首先确定一个基准日，例如19000101是星期几，然后后续年份year的1月1日的星期几可以按照间隔天数来推算
+ 任务分解
    + 首先获取基准日19000101的星期数
    + 计算year0101与基准日间隔天数
    + 计算year0101星期数

对应代码
```python
def first_day(year):
    # 首先知道1900年1月1日是星期几， 然后直接按照year与1900年的所差天数来推算
    w_19000101 = get_base_year_week()
    #计算当前年份与1900年的相差天数
    days_num = days_between(year)
    #计算当前年份1月1日是星期几
    w = get_the_week_of_firstday(w_19000101,days_num)
    return w

```

#### get_base_year_week实现
我们已经知道19000101是星期一，所以有

```python
def get_base_year_week():
    #1900年0101是周一
    return 1
```

#### days_between实现
+ 总体思路： 计算年份间天数主要需要注意闰年这种现象, 但我们先不管它，先将first_day的主要组件都构建出来

```python
def days_between(year):
    #其中k是 这期间的闰年数
    k = leapyears(year)
    days_num = (year-1900)*365+ k
    return days_num
```

#### get_the_week_of_firstday 实现
我们在获取了year0101与19000101之间的间隔天数后，可以直接计算year0101的星期数

```python
def get_the_week_of_firstday(w_19000101,days_num):
    week_of_firstday = (days_num+1) % 7
    return week_of_firstday
```

#### leapyears 的实现
+ 总体思路: 从1900年循环到year,逐年判断是否是闰年，是的话计数器+1
  + 注意，我们不需要判断year是否是闰年，因为只需要到year0101
  + 判断是否是闰年这个功能暂时不考虑如何实现

```python
def leapyears(year):
    #计算1900到year之间的闰年数
    leapyear_num = 0
    for i in range(year-1900):
        leapyear_num += is_leapyear(1900+i)

    return leapyear_num
```

#### is_leapyear 的实现
+ 总体思路: 根据查找到的资料显示： 如果year能被100整除，那么 如果year能被400整除的年份是闰年， 否则， 如果年份能被4整除的年份是闰年

从而可以实现对应的代码

```python
def is_leapyear(year):
    # 如果year能被100整除，那么 如果year能被400整除的年份是闰年
    # 否则， 如果年份能被4整除的年份是闰年
    if year%100 == 0:
        if year%400==0:
            return 1
        else:
            return 0
    elif year%4 == 0:
        return 1
    else:
        return 0
```

### print_cal的实现

这个实现的关键是我们想以什么样的形式显示日历，可以是一年365天显示为如下很长的列表

| 01/01| 02/01 | 03/01 |...|
| ----- | ----- | ----- |-----|
| 7 | 1 | 2 |...|


 但参考常见日历的显示形式，经常是逐月显示，7天一行

 + 十二个月显然可以用一个循环实现
 + 循环调用一个打印一个月内日历的函数就行

 对应的代码为

 ```python
 def print_cal(year,w):
    #输入: year
    #       w： 这一年0101对应的星期
    print("\n")
    print("=============="+ "calender of "+str(year)+"==============")
    week_of_first_day = w
    for i in range(12):
        first = print_one_month(year,month,first)
 ``` 

 #### print_one_month的实现
 每个月的日历显示形式如下

              X月
 |Mon|Tue|Wen|Tur|Fri|Sat|Sun|
 |---|---|---|---|---|---|---|
 |||x|x|x|x|x|
 ||||...||||

+ 首先一行要显示当前月份
+ 然后是打印星期名称
+ 之后的日期应该与星期对齐，也就是打印显示为制表符号隔开
+ 从第一行月首日星期数开始填数，当时期星期数为1时换行
+ 每个月天数不一定，需要计算月份天数

对上述需求抽象一下分别对应:
+ days(year,month)
  + 每个月天数不一定，需要计算月份天数
+ header
  + 首先一行要显示当前月份
  + 然后是打印星期名称
+ layouts()
  + 安排月内每天的表格位置
+ 打印
+ 计算下一个月的第一天是星期几,并返回,以便后续计算

```python
def print_one_month(year,month,first):
    days_num = days(year,month)
    next_first = next_month_first(days_num,first)
    print_header(month)
    print_every_of_month(month,days_num,first)  
```

#### days 的实现
+ 总体思路: 
    + 主要判断大小月，
    + 以及是否闰年，闰年2月需要多加一天

```python
def days(year,month):
    if month in (1,3,5,7,8,10,12):
        days_num=31
    elif month == 2:
        if is_leapyear(year):
            days_num = 29
        else:
            days_num = 28
    else:
        days_num = 30
```

可以看到这里同样出现需要判断某一年是否是闰年的任务，这时候，可以直接用之前已经定义好的is_leapyear函数， 这也告诉我们，将一些重复使用的功能抽象出来，定义为函数，可以提高代码复用，减少重复编写相同的代码块。

#### next_month_first的实现
输入的first是当前月份的第一天的星期数， 

```python
def next_month_first(days_num,first):
    return first + (days_num % 7)
```

#### 打印日历表格的功能实现
+ 每个月的日历是一个标题为 month， 
+ 一共7列的一个表格
+ 所以这里可以抽象为如何打印一个表格
    + 对于日历这样的简单实现(刚开始实现不要盲目增加复杂度，先完成，然后再慢慢完善)表格有行数，列数，每列宽度三个属性