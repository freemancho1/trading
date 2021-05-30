from datetime import datetime

if 19 < int(datetime.now().strftime('%H')) < 22:
    print('True')
else:
    print('False')