## 项目介绍
```angular2html
主要为flask项目模板，包括国际化，启停命令封装，日志，数据库链接，分页，ldap校验，邮箱短信发送
```
## 环境准备

#### 安装mysql支持
```angular2html
yum install mysql-devel
```
#### 安装ldap支持
```angular2html
yum install openldap-devel
```

#### 安装virtualenv
```angular2html
yum install python-virtualenv
```

## 部署步骤
```angular2html
git clone 项目github地址
cd 项目
virtualenv env -p python2.7版本的bin路径
source env/bin/activate
pip install -r requirements.txt -i http://pypi.douban.com/simple/
```

## 系统启动
```angular2html
./control start      #启动
./control stop       #停止
./control restart    #重启
./control status     #查看状态
./control tail       #查看日志
./control kill9      #强制停止
./control version    #查看当前的Git版本
