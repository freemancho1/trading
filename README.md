# TRADING

## Install packages

```
pip install -r config/sysfiles/requirements.txt
```

## System files

### config/sysfiles/code.csv
코드 테이블 초기 데이터

### config/sysfiles/parameters.py
시스템 공통, 크롤링, 모델링, 트레이딩, 로그 등 파라미터

## DBMS

```
create user 'aaa'@'localhost' identified by 'bbb';
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

## Django

```
django-admin startapp new-app
```
