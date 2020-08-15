from exts import db
import pymysql
pymysql.install_as_MySQLdb()

class student(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    #学号
    name = db.Column(db.String(20),default="请输入完整信息")
    # 姓名
    grade = db.Column(db.String(20),default="请输入完整信息")
    #年级
    gender = db.Column(db.String(20),default="请输入完整信息")
    #性别
    age = db.Column(db.String(20),default="请输入完整信息")
    #年龄
    major = db.Column(db.String(20),default="请输入完整信息")
    #专业
    score = db.Column(db.Integer,default=0)
    #成绩
