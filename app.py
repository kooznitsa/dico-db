import sys
from flask import Flask, request, render_template, redirect, url_for
import pymysql

db = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='akulabutaforia42',
                                    database='dico_db',
                                    charset='utf8')

app = Flask(__name__)


@app.route('/add-row')
def add_row():
    return render_template('add-row.html', the_title='Добавьте новый термин')


@app.route('/update')
def notify():
    return render_template('update.html')


@app.route('/add-row', methods=['POST'])
def update():
    cursor = db.cursor()

    fr = request.form['fr']
    ru = request.form['ru']
    comment = request.form['comment']
    category = request.form['category']

    sql = "INSERT INTO dico(id, fr, ru, comment, category) VALUES (DEFAULT, %s, %s, %s, %s)"
    cursor.execute(sql, (fr, ru, comment, category))
    db.commit()
    return render_template('update.html', message='Термин добавлен в словарь.')


@app.route('/', methods=['GET'])
def show_table():
    cursor = db.cursor()

    total_rows = cursor.execute("SELECT * FROM dico")
    shown_rows = cursor.execute("SELECT * FROM dico LIMIT 10")
    results = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT CONCAT(UCASE(LEFT(category, 1)), \
                            SUBSTRING(category, 2)) FROM dico ORDER BY category""")
    options = cursor.fetchall()

    category = 'all'

    return render_template('dictionary.html', 
                                            results=results,
                                            options=options,
                                            the_title='Французско-русский словарь', 
                                            total_rows=total_rows, 
                                            shown_rows=shown_rows)


@app.route('/search', methods=['GET'])
def search_items():
    cursor = db.cursor()

    user_input = request.args['phrase']
    category = request.args['category']
    sorting = request.args.get('sort', 'id')

    sql = "SELECT * FROM dico"

    conditions = []

    if user_input:
        conditions.append("(fr LIKE CONCAT('%','{}','%') OR ru LIKE CONCAT('%','{}','%'))".format(user_input, user_input))

    if category != 'all':
        conditions.append("category = '{}'".format(category.lower()))

    if len(conditions):
        sql += " WHERE " + " AND ".join(conditions) + " ORDER BY {}".format(sorting)
    print(sql, file=sys.stdout)

    shown_rows = cursor.execute(sql)
    results = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT CONCAT(UCASE(LEFT(category, 1)), \
                        SUBSTRING(category, 2)) FROM dico ORDER BY category""")
    options = cursor.fetchall()

    return render_template('dictionary.html', 
                                            results=results,
                                            options=options,
                                            the_title='Французско-русский словарь', 
                                            total_rows=cursor.execute("SELECT * FROM dico"),
                                            shown_rows=shown_rows,
                                            user_input=user_input,
                                            category=category)


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        cursor = db.cursor()

        sql = "SELECT * FROM dico WHERE id = %s"
        cursor.execute(sql, (id))
        results = cursor.fetchall()

        id = int(id)
        fr_item = ''.join([col[1] for col in results])
        ru_item = ''.join([col[2] for col in results])
        comment_item = ''.join([col[3] for col in results])
        category_item = ''.join([col[4] for col in results])

        return render_template('edit.html', 
                                                the_title='Отредактируйте термин',
                                                fr_item=fr_item,
                                                ru_item=ru_item,
                                                comment_item=comment_item,
                                                category_item=category_item)
    
    elif 'edit' in request.form:
        cursor = db.cursor()        
        select = "SELECT * FROM dico WHERE id = %s"
        cursor.execute(select, (id))
        results = cursor.fetchall()

        id = int(id)
        fr_item = ''.join([col[1] for col in results])
        ru_item = ''.join([col[2] for col in results])
        comment_item = ''.join([col[3] for col in results])
        category_item = ''.join([col[4] for col in results])

        fr_input = request.form['fr']
        ru_input = request.form['ru']
        comment_input = request.form['comment']
        category_input = request.form['category']

        update = "UPDATE dico SET fr = %s, \
                                        ru = %s, \
                                        comment = %s, \
                                        category = %s WHERE id = {}" \
                                        .format(id)

        cursor.execute(update, (fr_input, ru_input, comment_input, category_input))
        db.commit()
        return render_template('update.html', message='Термин изменен.')

    elif 'delete' in request.form:
        cursor = db.cursor() 
        delete = "DELETE FROM dico_db.dico WHERE id = %s"
        cursor.execute(delete, (id))
        db.commit()
        return render_template('update.html', message='Термин удален.')


if __name__ == '__main__':
    app.run(debug=True)