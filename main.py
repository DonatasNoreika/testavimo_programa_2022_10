from models import engine, Testas, VartotojoAtsakymas, Sprendimas, Atsakymas, Vartotojas
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from random import shuffle

Session = sessionmaker(bind=engine)
session = Session()

vardas = input("Įveskite vardą")
pavarde = input("Įveskite pavardę")
vartotojai = session.query(Vartotojas).all()
aktyvus_vartotojas = False
for vartotojas in vartotojai:
    if vartotojas.vardas == vardas and vartotojas.pavarde == pavarde:
        print(f"{vardas} {pavarde}, sveikiname prisijungus!")
        aktyvus_vartotojas = vartotojas
        break
else:
    naujas_vartotojas = Vartotojas(vardas=vardas, pavarde=pavarde)
    aktyvus_vartotojas = naujas_vartotojas
    session.add(naujas_vartotojas)
    session.commit()
    print(f"Naujas vartotojas {naujas_vartotojas} sukurtas")

while True:
    testai = session.query(Testas).all()
    for testas in testai:
        print(testas)
    pasirinkto_id = int(input("Įveskite testo ID: "))
    sprendimas = Sprendimas(data=datetime.today(), vartotojas_id=aktyvus_vartotojas.id, testas_id=pasirinkto_id)
    taskai = 0
    session.add(sprendimas)
    session.commit()
    testas = session.query(Testas).get(pasirinkto_id)
    for klausimas in testas.klausimai:
        print(klausimas)
        teisingi_atsakymai = {}
        counter = 0
        klausimo_atsakymai = klausimas.atsakymai
        shuffle(klausimo_atsakymai)
        for atsakymas in klausimo_atsakymai:
            counter += 1
            print(f"\t {counter} - {atsakymas.tekstas}")
            teisingi_atsakymai[counter] = atsakymas.id
        vartotojo_pasirinkimai = input("Pasirinkite atsakymą (-us) be tarpų")
        ar_atsakymas_teisingas = True
        for indeksas, atsakymo_id in teisingi_atsakymai.items():
            aktyvus_atsakymas = session.query(Atsakymas).get(atsakymo_id)
            if str(indeksas) in vartotojo_pasirinkimai:
                vartotojo_atsakymas = VartotojoAtsakymas(sprendimas_id=sprendimas.id, klausimas_id=klausimas.id, atsakymas_id=atsakymo_id)
                session.add(vartotojo_atsakymas)
                session.commit()
                if aktyvus_atsakymas.ar_teisingas != 1:
                    ar_atsakymas_teisingas = False
            else:
                if aktyvus_atsakymas.ar_teisingas == 1:
                    ar_atsakymas_teisingas = False
        if ar_atsakymas_teisingas:
            taskai += 1
        print("Taškai: ", taskai)
    sprendimas.rezultatas = f"{taskai} / {len(testas.klausimai)}"
    session.commit()
    break