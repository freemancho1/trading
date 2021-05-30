# TRADING

## Install packages

```
pip install -r config/sysfiles/requirements.txt
```

## System files

### config/sysfiles/code.csv
코드 테이블 초기 데이터

### config/sysfiles/parameters
시스템 파라미터 저장 파일들터
* common.py - 시스템 공통 파라미터
* trading.py - 거래 관련 파라미터
* crawling.py - 크롤링 관련 파라미터
* modeling.py - 모델링 관련 파라미터
* model.py - 모델 관련 파라미터
* log.py - 로그 관련 파라미터

## DBMS

```
create user 'aaa'*'localhost' identified by 'bbb';
```

```
create database mydb default character set utf8 collate utf8_general_ci;
```

```
grant all privileges on mydb.* to aaa@localhost;
grant all privileges on *.* to aaa@localhost;
flush privileges;
```

``` 
show grants for 'aaa'@'localhost';
```


