drop database if exists test;
create database test character set utf8;

use test;

create table knjiznica(
	sifra int not null PRIMARY KEY auto_increment,
	Naziv varchar(100) not null,
	Mjesto varchar(200) not null,
	Adresa varchar(200) not null,
	Postanski_broj varchar(200) not null
);

create table knjiga(
	sifra int not null PRIMARY KEY auto_increment,
	Naslov varchar(100) not null,
	Zanr varchar(100) not null,
	Autor varchar(100) not null,
	nakladnik int,
	izdavanje int

);

create table izdavatelj(
	sifra int not null PRIMARY KEY auto_increment,
	Ime varchar(100) not null,
	Prezime varchar(100) not null,
	Adresa varchar(100) not null,
	Mjesto varchar(100) not null,
	Postanski_broj varchar(100) not null
);

create table nakladnik(
	sifra int not null PRIMARY KEY auto_increment,
	Naziv varchar(100) not null,
	Mjesto varchar(100) not null
);

create table izdavanje(
	sifra int not null PRIMARY KEY auto_increment,
	datum_izdavanja date,
	datum_povratka date,
	cijena float,
	izdavatelj int
);

alter table knjiga ADD FOREIGN KEY (nakladnik) REFERENCES nakladnik(sifra);
alter table knjiga ADD FOREIGN KEY (izdavanje) REFERENCES izdavanje(sifra);
alter table izdavanje ADD FOREIGN KEY (izdavatelj) REFERENCES izdavatelj(sifra);

INSERT INTO knjiznica(Naziv,Mjesto,Adresa,Postanski_broj) VALUES('Gradska knjiznica Osijek','Osijek','Stjepana Radića 4','31000');
INSERT INTO knjiznica(Naziv,Mjesto,Adresa,Postanski_broj) VALUES('Gornjograska knjiznica','Osijek','Petra Preradovića 2','31000');
INSERT INTO knjiznica(Naziv,Mjesto,Adresa,Postanski_broj) VALUES('Naziv1','Zagreb','Petra Nazića 123','10000');
INSERT INTO knjiznica(Naziv,Mjesto,Adresa,Postanski_broj) VALUES('Naziv2','Zagreb2','Petra Nazića 1231','10001');
INSERT INTO knjiznica(Naziv,Mjesto,Adresa,Postanski_broj) VALUES('Naziv3','Zagreb3','Petra Nazića 1213','10002');

INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv','Zagreb');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv1','Osijek');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv2','Nova Gradiška');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv3','Zagreb');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv4','Poreč');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv5','Pula');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv6','Ogulin');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv7','Sisak');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv8','Koprivnica');
INSERT INTO nakladnik(Naziv,Mjesto) VALUES('Naziv9','Varaždin');

INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime','Prezime','Adresa','Mjesto','1023123');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime1','Prezime1','Adresa1','Mjesto1','1023123');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime2','Prezime2','Adres2','Mjesto2','4234424');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime3','Prezime3','Adresa3','Mjesto3','243242');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime4','Prezime4','Adresa4','Mjesto4','763655');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime5','Prezime5','Adresa5','Mjesto5','4324211');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime6','Prezime6','Adresa6','Mjesto6','1231356');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime7','Prezime7','Adresa7','Mjesto7','5136436');
INSERT INTO izdavatelj(Ime,Prezime,Adresa,Mjesto,Postanski_broj) VALUES('Ime8','Prezime8','Adresa8','Mjesto8','431243124312');


INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-02-05','1993-03-05','15.00',1);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-02-06','1993-03-10','15.00',2);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-03-01','1993-03-15','15.00',3);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-03-05','1993-03-20','15.00',2);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-02-02','1993-03-25','15.00',1);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-02-03','1993-03-14','15.00',4);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-02-07','1993-04-13','15.00',3);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-05-10','1993-06-11','15.00',2);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-04-22','1993-05-02','15.00',5);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-05-23','1993-06-25','15.00',2);
INSERT INTO izdavanje(datum_izdavanja,datum_povratka,cijena,izdavatelj) VALUES('1993-06-29','1993-07-21','15.00',7);

INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov1','Zanr1','Autor1',3 ,2 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov2','Zanr2','Autor2',4 ,4 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov3','Zanr3','Autor3',5 ,5 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov4','Zanr4','Autor4',6 ,6 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov5','Zanr5','Autor5',2 ,7 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov6','Zanr6','Autor6',4 ,2 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov7','Zanr7','Autor7',6 ,1 );
INSERT INTO knjiga(Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES('Naslov8','Zanr8','Autor8',7 ,4 );



