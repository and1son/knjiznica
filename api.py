from flask import Flask, render_template, request, redirect, flash, session
from flaskext.mysql import MySQL
from flask import jsonify # <- `jsonify` instead of `json`

app = Flask(__name__)
app.secret_key ="super secret key"

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'andibasic'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)


  
@app.route('/izdavanje')
def izdavanje():
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT * FROM izdavanje''')
    data = cursor.fetchall()
    return render_template('izdavanje.html', izdavanje=data)
    #return str(data)
    #return str(rv)

@app.route('/izdavanje/<sifra>')
def izdavanje_sifra(sifra):
    cursor = mysql.connect().cursor()
    cursor.execute('''select * FROM izdavanje where sifra = %s ''', (sifra))
    r = [dict((cursor.description[i][0], value)
         for i, value in enumerate(row)) for row in cursor.fetchall()]
    return render_template('izdavanje_sifra.html', sifra=r[0])
    #return str(r)
    #return jsonify({'results': r})

@app.route('/izdavanje/obrisi/<int:sifra>')
def izdavanje_obrisi(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM izdavanje where sifra=%s", (sifra))
    conn.commit()
    return redirect('/izdavanje')

@app.route('/izdavatelj')
def izdavatelj():
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT * FROM izdavatelj''')
    data = cursor.fetchall()
    return render_template('izdavatelj.html', izdavatelj=data)
    #return str(data)
    #return str(rv)

@app.route('/izdavatelj/<sifra>')
def izdavatelj_sifra(sifra):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT * FROM izdavatelj where sifra = %s''', (sifra))
    r = [dict((cursor.description[i][0], value)
    	 for i, value in enumerate(row)) for row in cursor.fetchall()]
    return render_template('izdavatelj_sifra.html', sifra=r[0])
    #return str(data)
    #return str(rv)

@app.route('/izdavatelj/obrisi/<int:sifra>')
def izdavatelj_obrisi(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM izdavatelj where sifra=%s", (sifra))
    conn.commit()
    return redirect('/izdavatelj')


@app.route('/knjiga')
def knjiga():
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT * FROM knjiga ''')
    data = cursor.fetchall()
    return render_template('knjiga.html', knjiga=data)

@app.route ('/knjiga/dodaj')
def dodaj_knjiga_view():
    return render_template('knjiga_dodaj.html')

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
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knjiga where sifra=%s",sifra)
    row = cursor.fetchone()
    if row:
        return render_template('knjiga_edit.html', row=row)
    else:
        return 'Error loading #{id}'.format(sifra=sifra)

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
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knjiga where sifra=%s", (sifra))
    conn.commit()
    return redirect('/knjiga')

@app.route('/knjiga/<sifra>')
def knjiga_sifra(sifra):
    cursor = mysql.get_db().cursor()
    cursor.execute(''' SELECT * FROM knjiga where sifra = %s ''', (sifra))
    r = [dict((cursor.description[i][0], value)
         for i, value in enumerate(row)) for row in cursor.fetchall()]
    return render_template('knjiga_sifra.html', sifra=r[0])

@app.route('/nakladnici')
def nakladnici():
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT * FROM nakladnik''')
    data = cursor.fetchall()
    #return jsonify({'results': data})
    return render_template('nakladnici.html', nakladnici=data)

@app.route('/nakladnici/<nakladnici_sifra>')
def nakladnici_sifra(nakladnici_sifra):
    cursor = mysql.connect().cursor()
    cursor.execute('''select * FROM nakladnik where sifra = %s ''', (nakladnici_sifra))
    r = [dict((cursor.description[i][0], value)
         for i, value in enumerate(row)) for row in cursor.fetchall()]
    return render_template('nakladnici_sifra.html', nakladnici_sifra=r[0])
    #return str(r)
    #return jsonify({'results': r})

@app.route ('/nakladnici/dodaj')
def dodaj_nakladnik_view():
    return render_template('nakladnici_dodaj.html')

@app.route('/nakladnici_dodaj', methods=['POST'])
def insert_nakladnici():
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

@app.route('/nakladnici/obrisi/<int:sifra>')
def nakladnici_obrisi(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nakladnik where sifra=%s", (sifra))
    conn.commit()
    return redirect('/nakladnici')

@app.route('/nakladnici_edit/<int:sifra>')
def edit_nakladnici_view(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nakladnik where sifra=%s",sifra)
    row = cursor.fetchone()
    if row:
        return render_template('nakladnici_edit.html', row=row)
    else:
        return 'Error loading #{id}'.format(sifra=sifra)

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



@app.route ('/izdavanje/dodaj')
def izdavanje_dodaj():
    return render_template('izdavanje_dodaj.html')

@app.route('/dodaj_izdavanje', methods=['POST'])
def insert_izdavanje():
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




@app.route ('/izdavatelj/dodaj')
def izdavatelj_dodaj():
    return render_template('izdavatelj_dodaj.html')

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




if __name__ == '__main__':
    app.run(debug=True)