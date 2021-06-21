from datetime import datetime


def str_to_int_test():
    if 19 < int(datetime.now().strftime('%H')) < 22:
        print('True')
    else:
        print('False')


def weekday_test():
    days = ['월', '화', '수', '목', '금', '토', '일']
    today_index = datetime.date(datetime.now()).weekday()
    print(f'{days[today_index]}({today_index})')


if __name__ == '__main__':
    # str_to_int_test()
    weekday_test()