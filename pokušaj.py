@app.route('/nakladnici/insert', methods = ['POST'])
def insert_nakladnici():
    if request.method == "POST":    
        cursor = mysql.get_db().cursor()
        Naziv = request.form['nakladnik_naziv']
        Mjesto = request.form['nakladnik_mjesto']    
        cursor = conn.cursor()
        cursor.execute("INSERT INTO nakladnik (Naziv,Mjesto) VALUES (%s,%s)", ('Novi naziv','Novo mjesto'))
        #cursor.execute('Novi naziv', 'Novo mjesto')
        conn.commit()
        #return redirect(url_for('nakladnici.html'))
        return json.dumps({'message':'Korisnik kreiran'})


@app.route('/dodaj', methods=['POST'])
def insert_nakladnici():
    try:
        _naziv = request.form['Naziv']
        _mjesto = request.form['Mjesto']
        if _naziv and _mjesto and request.method == 'POST':
            sql = '''INSERT INTO nakladnik(Naziv,Mjesto) VALUES (%s, %s)'''
            data = (_naziv, _mjesto)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            flash('user added successfully')
            return redirect('/')
            #return render_template('/nakladnici')
        else:
            return 'Error adding user'
    except Exception as e:
          print(e)
    finally:
         cursor.close()
         conn.close()

         -------------------


@app.route('/knjiga/edit/<int:sifra>')
def edit_knjiga_view():
    return render_template('knjiga_edit.html')

@app.route('/knjiga/edit')
def edit_knjiga():
    if request.method == 'POST':
        _naslov = request.form['Naslov']
        _zanr = request.form['Zanr']
        _autor = request.form['Autor']
        _nakladnik = request.form['nakladnik']
        _izdavanje = request.form['izdavanje']
        _sifra = request.form['sifra']
        sql = "UPDATE knjiga set Naslov=%s, Zanr=%s, Autor=%s, Nakladnik=%s, Izdavanje=%s WHERE sifra=%s"
        data = (_naslov, _zanr, _autor, _nakladnik, _izdavanje, _sifra)
        conn = mysql.connect()
        cursor = conn.cursor()
        return redirect('/knjiga')
    else:
        return 'Error while updating user'

/usr/bin mysqk -u root -p < /home/andi/Documents/Code/knjiznica/baza.sql

cd Documents/Code/knjiznica
. venv/bin/activate
python api.py

---
github

cd Documents/github/knjiznica
git add .
git commit - ""
git push origin master