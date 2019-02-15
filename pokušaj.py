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