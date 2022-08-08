from flask import Flask, render_template, request, flash, url_for
import sqlite3
from werkzeug.utils import redirect

app=Flask(__name__)
app.config['SECRET_KEY'] ='WER213'
#CREATE DB
db = sqlite3.connect('db_telefon.sqlite3')
cursor = db.cursor()
cursor.execute("""create table if not exists telefons(
    id integer primary key,
    name varchar(30),
    number varchar(200)
)""")
cursor.close()
db.close()
#END

@app.route('/process_data/<name>/',methods=['POST'])
def index_process(name=''):
    print(name)
    db = sqlite3.connect('db_telefon.sqlite3')
    cursor = db.cursor()
    cursor.execute("""DELETE from telefons where name = ?""", (name,))
    cursor.close()
    db.commit()
    cursor = db.cursor()
    cursor.execute("""select name, number from telefons""")
    posts = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html',posts=posts)

@app.route('/edit/<name>/<number>',methods=['POST'])
def index_process_get(name,number):
    if request.method == 'POST':
        try:
            if request.form['submit_button']=='Do Something':
                name_to_edit = request.form.get('name', '')
                number_to_edit = request.form.get('telefon', '')
                print(f'Edit {name} to {name_to_edit} and {number} to {number_to_edit}')
                #UPDATE BD
                try:
                    db = sqlite3.connect('db_telefon.sqlite3')
                    cursor = db.cursor()
                    cursor.execute('UPDATE telefons SET number=?,name=? WHERE name = ? and number = ?',
                                   (number_to_edit,name_to_edit, name, number,))
                    cursor.close()
                    db.commit()
                    db.close()
                except:
                    pass
                db = sqlite3.connect('db_telefon.sqlite3')
                cursor = db.cursor()
                cursor.execute("""select name, number from telefons""")
                posts = cursor.fetchall()
                cursor.close()
                db.close()
                return render_template('index.html',posts=posts)
        except:
            print('save')
            return render_template('edit.html', name=name, telefon=number)
    else:
        print('ERROR')
        return render_template('edit.html')
@app.route('/')
def index():
    db = sqlite3.connect('db_telefon.sqlite3')
    cursor = db.cursor()
    cursor.execute("""select name, number from telefons""")
    posts = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html',posts=posts)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name = request.form.get('name', '')
        telefon = request.form.get('telefon', '')
        if name and telefon:
            print('OK')
            #Save to DB
            db = sqlite3.connect('db_telefon.sqlite3')
            cursor = db.cursor()
            cursor.execute("""insert into telefons (name,number) values (?,?)""",(name,telefon))
            cursor.close()
            db.commit()
            db.close()
            #End save to DB
            flash('telefon has been added')
            return redirect(url_for('index'))
        else:
            print('No ok')
            #message='Name or telefon '
    return render_template('add.html')



@app.route('/search',methods=['GET'])
def search():
    name1=request.args.get('search_name')
    print(name1)

    db = sqlite3.connect('db_telefon.sqlite3')
    cursor = db.cursor()
    quere=f"select name, number from telefons where name LIKE '%{name1}%' "
    cursor.execute(quere)
    posts = cursor.fetchall()
    print(posts)
    cursor.close()
    db.close()
    return render_template('index.html', posts=posts)
if __name__ == '__main__':
    app.run(debug=True,port = 5001)