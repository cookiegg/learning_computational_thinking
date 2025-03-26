# 从一个例子来实践自顶向下的程序设计
+ 首先是对自顶向下设计思路的实践
+  然后是代码测试优化过程

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
    for month in range(12):
        first = print_one_month(year,month,first)
 ```

 >需要注意的是,并不要拘泥于每次严格逐个分层的实现, 一般来说, 实现过程是顶层任务分块,确定各个模块间接口数据结构,然后就专注在其中一个子模块的实现上, 对于这个子模块的实现又可以重复上述过程(任务分块,确定模块接口,数据结构,专注于子模块实现). 聪明的很快就会联想到这类似于树的遍历, 首先进行节点的广度优先搜素,层序遍历,列出子函数,然后深入其中一个子函数(这里又类似深度优先搜索中的前序遍历)


## 第三层
### first_day子函数
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


### print_cal子函数
 #### print_one_month的实现
 每个月的日历显示形式如下

              X月
 |Sun|Mon|Tue|Wen|Tur|Fri|Sat|
 |---|---|---|---|---|---|---|
 |||x|x|x|x|x|
 ||||...||||

+ 首先一行要显示当前月份
+ 然后是打印星期名称
+ 之后的日期应该与星期对齐，也就是打印显示为制表符号隔开
+ 从第一行月首日星期数开始填数，当为星期天时换行
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


## 第四层
### days 的实现
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
    return days_num
```

可以看到这里同样出现需要判断某一年是否是闰年的任务，这时候，可以直接用之前已经定义好的is_leapyear函数， 这也告诉我们，将一些重复使用的功能抽象出来，定义为函数，可以提高代码复用，减少重复编写相同的代码块。

### next_month_first的实现
输入的first是当前月份的第一天的星期数， 

```python
def next_month_first(days_num,first):
    return first + (days_num % 7)
```

### print_every_of_month打印日历表格的功能实现

#### **ver1**
+ 每个月的日历是一个标题为 month， 
+ 一共7列的一个表格
+ 所以这里可以抽象为如何打印一个表格
    + 表格分为数据data与样式，
    + 对于日历这样的简单实现(刚开始实现不要盲目增加复杂度，先完成，然后再慢慢完善)表格有行数，列数，每列宽度三个属性，定义一个打印指定行数列数宽度的表格函数 print_table(data,row,col,width)
    + 日历项目中列数很简单，设置为7
    + 行数需要进行计算，交给函数 rows_month(first,days_num)
    + 每列宽度要怎么确定，还不太清楚，先不管

对应的print_every_of_month函数代码为:
```python
def print_every_of_month(month,days_num,first):
    cols_num = 7
    rows_num = rows_month(first,days_num)
    width = 3 #随便定义的一个单元格宽度，具体是否合适，之后再作调整
    data
    print_table(data,row,col,width)

```

#### **ver2**
+ 编写代码的时候切记不要盲目的追求通用化, 因为很多代码其实都是一次性的, 解决当前问题就行,不要想着一来就搞出个万世不移的代码框架
+ 上一个版本中想着rows_num对每个月是可变动的,但是在实际显示中还不如每个月的显示行数都是固定的,注意到每个月的天数都不会超过35,就算某月第一天是星期六,那最多的占用格数也不会超过42, 索性就固定为6行7列的显示表格
+ 表格宽度: 表头每个单词都为3个字母, 之间隔着一个空格符, 同时每月天数最多就是两位数,因此表格宽度设置为4就够了
    + 但是这又带来了一个新的问题: 我们如何实现类似制表一样,在每4个字符宽度中填入内容,不管是否填满,下一个print语句就移动到后续4字符宽度的地方打印输出?
        + 该去什么地方找到这个问题的答案?
        + 想出来的解决方法
        
        ```python
        if i < 10:
            print(" "+" "+str(i),end=" ")
        else:
            print(" "+str(i),end=" ")
        ```
        这样就实现了两位数以内的右对齐显示

这时候在回过头来看一下print_one_month 的前期抽象分解
```python
def print_one_month(year,month,first):
    days_num = days(year,month)
    next_first = next_month_first(days_num,first)
    print_header(month)
    print_every_of_month(month,days_num,first)  
```
随着我们认识的深入, 会发现由于每月的日历可以视为一个表格,那么header就没必要单独用一个函数表示, 因为表格一般都有表头,标题,表格内容等元素. 因此,我们不如直接定义一个print_table的函数, 它以表格形状,表头内容,表格数据内容,单元格宽度作为输入,直接打印输出表格. 在这样的认识基础上,我们可以重新组织print_one_month:

```python
def print_one_month(year,month,first):
    days_num = days(year,month)
    week_header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    next_first = next_month_first(days_num,first)
    data = month_data(first,days_num)
    print_table(data,week_header,row,col,width)
    return next_first
```

## 第五层

### month_data的实现

+ 假设我们已经有一个能通过输入data打印对应行列数的制表函数print_table(data,row,col,width)
+ 这时候思考其中的data应该如何填入?
    + 直接顺序逐个单元格循环填入就行
    + 因此这个问题转化为: 在长度为42的数组中插入[1,...,days_num]这串整数,其中1的位置为first确定

对应我们可以得到如下函数

```python
def month_data(first,days_num):
    data = 42*[" "]
    j = first
    for i in range(1,days_num+1):
        data[first] = i
        j = j + 1
    return data
```

接下来就是将这个data传入print_table进行打印

### print_table的实现

我们设计对应的表格打印器具有如下功能
+ 打印标题
+ 打印表头
+ 打印表体

```python
def print_table(data,row,col,width,title,header):
    print_title(title)
    print_header(header)
    print_body(data)
```

接下来分别实现其中子函数

+ 我们希望月份标题居中显示,这个目标可以理解为:
    + 在col*width的宽度内,居中显示标题
+ 打印表头可以理解为,在col*width个字符位中,每个width宽度内,显示表头内容
+ 同理, 打印表体也就是这样重复打印对应的行数
+ 因此print_header(header,width) 与print_body(data,width) 可以抽象出来一个打印对应每行对齐元素的函数print_list_with_fixed_width(lst, width)

因此可以进一步改写上面的print_table函数实现
```python
def print_table(...):
    total_width = col * width
    print_title(title,total_width)
    print_header(header,width)
    print_body(data,row,col,width)
```

我们会发现在上述三个任务中均涉及到关于**字符对齐**之类的问题,总不能全用空格占位实现, 有没有系统性的解决方法, 当然有,这就是python中字符串的格式化输出. 所以其实到了这里才需要专门的去学习与我们任务相关的编程知识. 这也是这种项目式学习的基本范式: 不要一来就去啃大部头,而是对任务进行逐步分解, 直到简化到每个细小模块都能做出来,或者感觉应该有现成的解决方案为止.然后再去研究现成解决方案的接口输入输出数据格式,觉得符合任务需求,就直接拿来用就行.
记住,重要的是做出东西,输入的再多,没有输出就是0.

很容易找到python中关于打印**字符对齐**的内容:
```python
print(f"{'left':<10}")  # 左对齐，宽度10
print(f"{'right':>10}")  # 右对齐，宽度10
print(f"{'center':^10}")  # 居中对齐，宽度10
```
其中 字符串前面的f 称之为 f-string,专门用于表示后面跟着的字符串是格式化的字符串.

#### print_title的实现
有了上面格式化字符串的知识, 实现起来就变得很简单了

```python
def print_title(title,total_width):
    print(f"{title:^{total_width}}")
```

#### print_header的实现
直接调用print_list_with_fixed_width(lst, width)
```python
def print_header(header,width):
    """
    header: 列表,长度==col

    """
    print_list_with_fixed_width(header, width)
```

### print_body的实现

```python
def print_body(data,row,col,width):
    """
    也就是重复调用row行数次打印每一行
    """
    for i in range(row):
        data_i = data[i*col:(i+1)*col]
        print_list_with_fixed_width(data_i, width)
```

#### print_list_with_fixed_width的实现

```python
def print_list_with_fixed_width(lst, width):
    # 使用列表推导式格式化每个元素
    formatted_elements = [f"{item:^{width}}" for item in lst]
    # 将格式化后的元素用空格连接并打印
    print(" ".join(formatted_elements))
```


## 开始编写代码
直到这时候才开始编写代码的,通过上面的分析你会发现, 完成一个代码项目, 最关键的是理清整个项目的逻辑结构, 进行任务分解. 边分解任务,边编写容易编写的代码, 但最重要的是你一定要在写代码与分析任务上花足够的时间.
```python
def calender():
    year = get_year()
    w = first_day(year)
    print_cal(year,w)


def get_year():
    year = input("Please input the year(after 1900s)")
    return year

def first_day(year):
    # 首先知道1900年1月1日是星期几， 然后直接按照year与1900年的所差天数来推算
    w_19000101 = get_base_year_week()
    #计算当前年份与1900年的相差天数
    days_num = days_between(year)
    #计算当前年份1月1日是星期几
    w = get_the_week_of_firstday(w_19000101,days_num)
    return w

def get_base_year_week():
    #1900年0101是周一
    return 1

def days_between(year):
    #其中k是 这期间的闰年数
    k = leapyears(year)
    days_num = (year-1900)*365+ k
    return days_num

def get_the_week_of_firstday(w_19000101,days_num):
    week_of_firstday = (days_num+1) % 7
    return week_of_firstday

def leapyears(year):
    #计算1900到year之间的闰年数
    #从1900循环到year，逐年判断是否是闰年，是的话计数器+1
    #注意，我们是不需要判断year是否是闰年的，因为只需要到year0101
    leapyear_num = 0
    for i in range(year-1900):
        leapyear_num += is_leapyear(1900+i)

    return leapyear_num

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



def print_cal(year,w):
   #输入: year
   #       w： 这一年0101对应的星期
   print("\n")
   print("=============="+ "calender of "+str(year)+"==============")
   week_of_first_day = w
   for month in range(12):
       first = print_one_month(year,month,first)
    
def print_one_month(year,month,first):
    days_num = days(year,month)
    title = str(month)
    week_header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    row = 6
    col = 7
    width = 4

    next_first = next_month_first(days_num,first)
    data = month_data(first,days_num)
    print_table(data,title,week_header,row,col,width)
    return next_first

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
    return days_num

def next_month_first(days_num,first):
    return first + (days_num % 7)


def month_data(first,days_num):
    data = 42*[" "]
    j = first
    for i in range(1,days_num+1):
        data[first] = i
        j = j + 1
    return data



def print_table(data,title,header,row,col,width):
    total_width = col * width
    print_title(title,total_width)
    print_header(header,width)
    print_body(data,row,col,width)

def print_title(title,total_width):
    print(f"{title:^{total_width}}")

def print_header(header,width):
    """
    header: 列表,长度==col

    """
    print_list_with_fixed_width(header, width)

def print_body(data,row,col,width):
    """
    也就是重复调用row行数次打印每一行
    """
    for i in range(row):
        data_i = data[i*col:(i+1)*col]
        print_list_with_fixed_width(data_i, width)

def print_list_with_fixed_width(lst, width):
    # 使用列表推导式格式化每个元素
    formatted_elements = [f"{item:^{width}}" for item in lst]
    # 将格式化后的元素用空格连接并打印
    print(" ".join(formatted_elements))

```

## 测试

上面就是这个日历显示项目的完整代码. 但是这个只是将逻辑思路实现的结果,具体是否能正常运行, 需要进行测试. 当然我们可以直接运行整个项目代码, 然后看报错一点一点的修改.

但是, 如果项目变得很大, 每次运行需要很长时间,那么这样做就很浪费时间. 因此, 我们应该对每个函数分别检查其正确性, 这也就是所谓的单元测试.

测试,然后修改代码, debug, 反复重复该过程是编写程序的必由之路.

上面完成的ver0.1版本的代码其实有很多错误以及可以提升改进的地方, 比如

+ 我们在第一层设计中约定year为整数, 但是 get_year返回的是str型, 需要进行类型转换
+ next_month_first函数有误
+ print_cal函数有错误
+ month_data函数有错误
+ 月份显示建议从数字改为英文
+ 有的函数太琐碎,可以合并(但是这种琐碎的过程是前期搭建代码逻辑框架的时候必走的路. 在构思项目框架的前期时候,不要为了优化代码结构而折损思考过程, 也就是说先别管代码结构是不是优雅啥的, 先把框架搭出来,然后再优化,分清主次)
