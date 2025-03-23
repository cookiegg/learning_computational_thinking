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
    




