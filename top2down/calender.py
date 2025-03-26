def calender():
    year = get_year()
    year = int(year)
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
       week_of_first_day = print_one_month(year,month,week_of_first_day)
    
def print_one_month(year,month,first):
    days_num = days(year,month)
    month_en = month_num2en(month)
    title = month_en
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

def month_num2en(month):
    en = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    return en[month-1]

def next_month_first(days_num,first):
    return (first + days_num) % 7


def month_data(first,days_num):
    data = 42*[" "]
    j = first
    for i in range(1,days_num+1):
        data[j] = i
        j = j + 1
    return data



def print_table(data,title,header,row,col,width):
    total_width = col * width
    print_title(title,total_width)
    print("")
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
        print("\n")

def print_list_with_fixed_width(lst, width):
    # 使用列表推导式格式化每个元素
    formatted_elements = [f"{item:^{width}}" for item in lst]
    # 将格式化后的元素用空格连接并打印
    print(" ".join(formatted_elements))


if __name__ == "__main__":
    calender()