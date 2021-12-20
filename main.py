from flask import Flask, render_template,url_for,request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gungun@07'
app.config['MYSQL_DB'] = 'sparksintern'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transfer')
def transerPage():
    cur = mysql.connection.cursor()
    rows = cur.execute('SELECT * FROM transactions')
    if rows > 0:
        details = cur.fetchall()
        return render_template('transfer.html', infos=details)

@app.route('/moneyTransfer', methods=['POST','GET'])
def moneyTransfer():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        act = request.form['accNo']
        ifsc = request.form['ifsc']
        amt = request.form['amt']

        cur = mysql.connection.cursor()

        rows = cur.execute('SELECT balance FROM transactions WHERE fname=%s AND lname=%s',(fname,lname))
        if rows>0:
            infos=cur.fetchall()
            bal = str(int(infos[0][0]) + int(amt))
            cur.execute("UPDATE transactions SET balance=%s WHERE ifsc=%s",(bal,ifsc))
            rows2 = cur.execute('SELECT * FROM transactions')
            if rows2 > 0:
                details = cur.fetchall()
            cur.connection.commit()
            cur.close()
            return render_template('transfer.html', msg='Money transferred successfully..!', infos=details, color='success')
        else:
            rows2 = cur.execute('SELECT * FROM transactions')
            if rows2 > 0:
                details = cur.fetchall()
            return render_template('transfer.html', msg='Money transfer failed..!', infos=details, color='danger')


if __name__ =='__main__':
    app.run(debug=True)