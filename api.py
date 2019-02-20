from flask import Flask, render_template, request, redirect, flash, session, url_for, g
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import bcrypt
from flask import jsonify

app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'andibasic'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)

''' 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('admin', None)

        if request.form['password'] == 'user':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))

        if request.form['password'] == 'admin' and request.form['username'] == 'admin':
            session['admin'] = request.form['username']
            return redirect(url_for('protected'))

        if ((request.form['password'] == 'employee') and (request.form['username'] == 'employee')):
            session['employee'] = request.form['username']
            return redirect(url_for('protected'))


    return render_template('index.html')

@app.route('/protected')
def protected():
    if g.user or g.admin or g.employee:
        return render_template('protected.html')

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    g.admin = None
    g.employee = None 
    if 'user' in session:
        g.user = session['user']
    if 'admin' in session:
        g.admin = session['admin']
    if 'employee' in session:
        g.employee = session['employee']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    if 'admin' in session:
        return session['admin']
    if 'employee' in session:
        return session['employee']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    session.pop('admin', None)
    session.pop('employee', None)
    return 'Dropped!'
    '''

@app.route('/')
def home():
    return render_template('home.html')

 
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO korisnici (name,email,password) VALUES (%s,%s,%s)", (name,email,hash_password,))
        conn.commit()
        session['name'] = name
        session['email'] = email
        return redirect(url_for("home"))

@app.route('/login1', methods=['GET','POST'])
def login():
    if request.method =="POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.get_db().cursor(DictCursor)
        cursor.execute("SELECT * FROM korisnici WHERE email=%s",(email))
        user = cursor.fetchone()
        cursor.close()
        

        if len(user) > 0:
            if bcrypt.hashpw(password, user['password']) == user['password']:
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password or user not match"
        else:
            return "Error password or user not match"
                
    else:
        return render_template("login1.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/izdavanje')
def izdavanje():
    #if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM izdavanje''')
        data = cursor.fetchall()
        return render_template('izdavanje.html', izdavanje=data)
    #flash("You dont have credentials to access this page")
    #return redirect(url_for('index'))


@app.route('/izdavanje/<sifra>')
def izdavanje_sifra(sifra):
    if g.user or g.admin or g.employee:
        cursor = mysql.connect().cursor()
        cursor.execute('''select * FROM izdavanje where sifra = %s ''', (sifra))
        r = [dict((cursor.description[i][0], value)
             for i, value in enumerate(row)) for row in cursor.fetchall()]
        return render_template('izdavanje_sifra.html', sifra=r[0])
    return redirect(url_for('index'))
    #return str(r)
    #return jsonify({'results': r})

@app.route('/izdavanje/obrisi/<int:sifra>')
def izdavanje_obrisi(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM izdavanje where sifra=%s", (sifra))
        conn.commit()
        return redirect('/izdavanje')
    return redirect(url_for('index'))

@app.route ('/izdavanje/dodaj')
def izdavanje_dodaj():
    return render_template('izdavanje_dodaj.html')

@app.route('/dodaj_izdavanje', methods=['POST'])
def insert_izdavanje():
    if g.admin or g.employee:
        if request.method == 'POST':
            _datum_izdavanja = request.form['datum_izdavanja']
            _datum_povratka = request.form['datum_povratka']
            _cijena = request.form['cijena']
            _izdavatelj = request.form['izdavatelj']
            sql = '''INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES (%s, %s, %s, %s)'''
            data = (_datum_izdavanja, _datum_povratka, _cijena, _izdavatelj)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            #flash('user added successfully')
            return redirect('/izdavanje')
                #return render_template('/nakladnici')
        else:
                return 'Error adding user'
    return redirect (url_for('izdavanje'))

@app.route('/izdavanje_edit/<int:sifra>')
def edit_izdavanje_view(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM izdavanje where sifra=%s",sifra)
        row = cursor.fetchone()
        if row:
            return render_template('izdavanje_edit.html', row=row)
        else:
            return 'Error loading #{id}'.format(sifra=sifra)
    return redirect(url_for('izdavanje'))

@app.route('/edit_izdavanje', methods=['POST'])
def edit_izdavanje():
    if request.method == 'POST':
        _datum_izdavanja = request.form['datum_izdavanja']
        _datum_povratka = request.form['datum_povratka']
        _cijena = request.form['cijena']
        _izdavatelj = request.form['izdavatelj']
        _sifra = request.form['sifra']
        sql = "UPDATE izdavanje SET datum_izdavanja=%s, datum_povratka=%s, cijena=%s, izdavatelj=%s WHERE sifra=%s"
        data = (_datum_izdavanja, _datum_povratka, _cijena, _izdavatelj, _sifra)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        return redirect('/izdavanje')
    else:
        return 'Error while updating user'

@app.route('/izdavatelj')
def izdavatelj():
    if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM izdavatelj''')
        data = cursor.fetchall()
        return render_template('izdavatelj.html', izdavatelj=data)
    return redirect(url_for('index'))


@app.route('/izdavatelj/<sifra>')
def izdavatelj_sifra(sifra):
    if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM izdavatelj where sifra = %s''', (sifra))
        r = [dict((cursor.description[i][0], value)
             for i, value in enumerate(row)) for row in cursor.fetchall()]
        return render_template('izdavatelj_sifra.html', sifra=r[0])
        #return str(data)
        #return str(rv)
    return redirect(url_for('index'))

@app.route('/izdavatelj/obrisi/<int:sifra>')
def izdavatelj_obrisi(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM izdavatelj where sifra=%s", (sifra))
        conn.commit()
        return redirect('/izdavatelj')
    return redirect(url_for('izdavatelj'))


@app.route ('/izdavatelj/dodaj')
def izdavatelj_dodaj():
    if g.admin or g.employee:
        return render_template('izdavatelj_dodaj.html')
    return redirect(url_for('izdavatelj'))

@app.route('/dodaj_izdavatelj', methods=['POST'])
def insert_izdavatelj():
    if request.method == 'POST':
        _ime = request.form['Ime']
        _prezime = request.form['Prezime']
        _adresa = request.form['Adresa']
        _mjesto = request.form['Mjesto']
        _postanskibroj = request.form['Postanski_broj']
        sql = '''INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES (%s, %s, %s, %s, %s)'''
        data = (_ime,_prezime,_adresa,_mjesto,_postanskibroj)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        #flash('user added successfully')
        return redirect('/izdavatelj')
            #return render_template('/nakladnici')
    else:
            return 'Error adding user'

@app.route('/izdavatelj_edit/<int:sifra>')
def izdavatelj_edit_view(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM izdavatelj where sifra=%s",sifra)
        row = cursor.fetchone()
        if row:
            return render_template('izdavatelj_edit.html', row=row)
        else:
            return 'Error loading #{id}'.format(sifra=sifra)
    return redirect(url_for('izdavatelj'))

@app.route('/edit_izdavatelj', methods=['POST'])
def edit_izdavatelj():
    if request.method == 'POST':
        _ime = request.form['Ime']
        _prezime = request.form['Prezime']
        _adresa = request.form['Adresa']
        _mjesto = request.form['Mjesto']
        _postanskibroj = request.form['Postanski_broj']
        _sifra = request.form['sifra']
        sql = "UPDATE izdavatelj SET Ime=%s, Prezime=%s, Adresa=%s, Mjesto=%s, Postanski_broj=%s WHERE sifra=%s"
        data = (_ime, _prezime, _adresa, _mjesto, _postanskibroj, _sifra)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        return redirect('/izdavatelj')
    else:
        return 'Error while updating user'


@app.route('/knjiga')
def knjiga():
    if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM knjiga ''')
        data = cursor.fetchall()
        return render_template('knjiga.html', knjiga=data)
    return redirect(url_for('index'))


@app.route ('/knjiga/dodaj')
def dodaj_knjiga_view():
    if g.admin or g.employee:
        return render_template('knjiga_dodaj.html')
    return redirect(url_for('knjiga'))

@app.route('/dodaj_knjiga', methods=['POST'])
def insert_knjiga():
    if request.method == 'POST':
        _naslov = request.form['Naslov']
        _zanr = request.form['Zanr']
        _autor = request.form['Autor']
        _nakladnik = request.form['nakladnik']
        _izdavanje = request.form['izdavanje']
        sql = '''INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES (%s, %s, %s, %s, %s)'''
        data = (_naslov, _zanr, _autor, _nakladnik, _izdavanje)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()

        #flash('user added successfully')
        return redirect('/knjiga')
            #return render_template('/nakladnici')
    else:
            return 'Error adding user'

@app.route('/knjiga_edit/<int:sifra>')
def edit_view(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM knjiga where sifra=%s",sifra)
        row = cursor.fetchone()
        if row:
            return render_template('knjiga_edit.html', row=row)
        else:
            return 'Error loading #{id}'.format(sifra=sifra)
    return redirect(url_for('knjiga'))

@app.route('/update', methods=['POST'])
def edit_knjiga():
    if request.method == 'POST':
        _naslov = request.form['Naslov']
        _zanr = request.form['Zanr']
        _autor = request.form['Autor']
        _nakladnik = request.form['nakladnik']
        _izdavanje = request.form['izdavanje']
        _sifra = request.form['sifra']
        sql = "UPDATE knjiga SET Naslov=%s, Zanr=%s, Autor=%s, nakladnik=%s, izdavanje=%s WHERE sifra=%s"
        data = (_naslov, _zanr, _autor, _nakladnik, _izdavanje, _sifra)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        return redirect('/knjiga')
    else:
        return 'Error while updating user'


@app.route('/knjiga/obrisi/<int:sifra>')
def obrisi_knjiga(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM knjiga where sifra=%s", (sifra))
        conn.commit()
        return redirect('/knjiga')
    return redirect(url_for('knjiga'))

@app.route('/knjiga/<sifra>')
def knjiga_sifra(sifra):
    if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute(''' SELECT * FROM knjiga where sifra = %s ''', (sifra))
        r = [dict((cursor.description[i][0], value)
             for i, value in enumerate(row)) for row in cursor.fetchall()]
        return render_template('knjiga_sifra.html', sifra=r[0])
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if g.admin or g.employee:
        if request.method == "POST":
            conn = mysql.connect()
            cursor = conn.cursor()
            search = '%%' + request.form['search'] + '%%'
            cursor.execute("""SELECT * FROM knjiga where (Naslov LIKE %s) or (Zanr LIKE %s) or (Autor LIKE %s);""", (search, search, search))
            return render_template('knjiga.html', records=cursor.fetchall())
    return redirect(url_for('index'))

@app.route('/nakladnici')
def nakladnici():
    if g.user or g.admin or g.employee:
        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM nakladnik''')
        data = cursor.fetchall()
        #return jsonify({'results': data})
        return render_template('nakladnici.html', nakladnici=data)
    return redirect(url_for('index'))

@app.route('/nakladnici/<nakladnici_sifra>')
def nakladnici_sifra(nakladnici_sifra):
    if g.user or g.admin or g.employee:
        cursor = mysql.connect().cursor()
        cursor.execute('''select * FROM nakladnik where sifra = %s ''', (nakladnici_sifra))
        r = [dict((cursor.description[i][0], value)
             for i, value in enumerate(row)) for row in cursor.fetchall()]
        return render_template('nakladnici_sifra.html', nakladnici_sifra=r[0])
    #return str(r)
    #return jsonify({'results': r})
    return redirect(url_for('index'))

@app.route ('/nakladnici/dodaj')
def dodaj_nakladnik_view():
    if g.admin or g.employee:
        return redirect(url_for('knjiga'))
    return render_template('nakladnici_dodaj.html')

@app.route('/nakladnici_dodaj', methods=['POST'])
def insert_nakladnici():
    if g.admin or g.employee:
        if request.method == 'POST':
            _naziv = request.form['Naziv']
            _mjesto = request.form['Mjesto']
            sql = '''INSERT INTO nakladnik(Naziv,Mjesto) VALUES (%s, %s)'''
            data = (_naziv, _mjesto)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            #flash('user added successfully')
            return redirect('/nakladnici')
                #return render_template('/nakladnici')
        else:
                return 'Error adding user'
    return redirect(url_for('nakladnici'))

@app.route('/nakladnici/obrisi/<int:sifra>')
def nakladnici_obrisi(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nakladnik where sifra=%s", (sifra))
        conn.commit()
        return redirect('/nakladnici')
    return redirect(url_for('nakladnici'))

@app.route('/nakladnici_edit/<int:sifra>')
def edit_nakladnici_view(sifra):
    if g.admin or g.employee:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nakladnik where sifra=%s",sifra)
        row = cursor.fetchone()
        if row:
            return render_template('nakladnici_edit.html', row=row)
        else:
            return 'Error loading #{id}'.format(sifra=sifra)
    return redirect(url_for('nakladnici'))

@app.route('/update_nakladnik', methods=['POST'])
def edit_nakladnici():
    if request.method == 'POST':
        _naziv = request.form['Naziv']
        _mjesto = request.form['Mjesto']
        _sifra = request.form['sifra']
        sql = "UPDATE nakladnik SET Naziv=%s, Mjesto=%s WHERE sifra=%s"
        data = (_naziv, _mjesto, _sifra)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        return redirect('/nakladnici')
    else:
        return 'Error while updating user'

if __name__ == '__main__':
    app.secret_key ="asdklaASD023#!^"
    app.run(debug=True)