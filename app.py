from flask import Flask,request,url_for,redirect,render_template
import config
from models import student
from exts import db
from sqlalchemy import or_,and_
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
admin = Admin(name=u'北网后台管理系统')
admin.init_app(app)
app.config.from_object(config)
app.jinja_env.auto_reload = True
db.init_app(app)
admin.add_view(ModelView(student,db.session))



@app.route('/',endpoint="index",methods=["GET","POST"])
def index():
    # db.drop_all()
    # db.create_all()
    all = student.query.all()
    i_id = request.args.get('i_id')

    if request.method == "POST":
        name = request.form.get("name")
        id = request.form.get("id")
        gender = request.form.get("sex")
        grade = request.form.get("grade")
        age = request.form.get("age")
        major = request.form.get('major')
        score = request.form.get('score')
        search = request.form.get('search')
        print(name, id, gender, grade, age, major,score)

        if name:
            data = student.query.filter_by(name=name,id=id).first()
            if data:
                return render_template("index.html",all=all)
            else:
                student_list = student(id=id,name=name,age=age,gender=gender,grade=grade,major=major,score=score)
                db.session.add(student_list)
                db.session.commit()
                print("成功")
                return redirect(url_for("index",all=all))
        elif search:
            if request.form.get('search_name'):
                data = student.query.filter(
                    or_(student.name.like("%" + search + "%"), (student.id.contains(search)))).all()
                return render_template('index.html', all=data)
            elif request.form.get('search_subject'):
                data = student.query.filter(student.major.like("%" + search + "%")).all()
                return render_template('index.html', all=data)
            elif request.form.get('search_score'):
                print(search)
                new=search.split('~')
                data = student.query.filter(student.score.between(int(new[0]),int(new[1]))).all()
                return render_template('index.html',all=data)


    elif i_id:
        student.query.filter_by(id=i_id).delete()
        db.session.commit()
        print('删除成功')
        return redirect(url_for('index'))

    return render_template("index.html",all=all)


@app.route('/update/',endpoint="update",methods=["GET","POST"])
def update():
    b_id = request.args.get('b_id')
    all = student.query.filter_by(id=b_id).all()
    if request.method == "POST":
        name = request.form.get("name")
        id = request.form.get("id")
        gender = request.form.get("sex")
        grade = request.form.get("grade")
        age = request.form.get("age")
        score = request.form.get('score')
        major = request.form.get('major')
        print('修改后',name, id, gender, grade, age, major,score)
        student.query.filter_by(id=b_id).update({"id":id,"name":name,"age":age,"gender":gender,"grade":grade,"major":major,"score":score})
        db.session.commit()
        print('修改成功')
        return redirect(url_for('index'))

    return render_template('update.html',all=all)

if __name__ == '__main__':
    app.run(debug=True)
