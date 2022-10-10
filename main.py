from models import engine, Testas, VartotojoAtsakymas, Sprendimas, Atsakymas
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()


while True:
    testai = session.query(Testas).all()
    for testas in testai:
        print(testas)
    pasirinkto_id = int(input("Įveskite testo ID: "))
    sprendimas = Sprendimas(data=datetime.today(), vartotojas_id=1, testas_id=pasirinkto_id)
    taskai = 0
    session.add(sprendimas)
    session.commit()
    testas = session.query(Testas).get(pasirinkto_id)
    for klausimas in testas.klausimai:
        print(klausimas)
        teisingi_atsakymai = {}
        counter = 0
        for atsakymas in klausimas.atsakymai:
            counter += 1
            print(f"\t {counter} - {atsakymas.tekstas}")
            teisingi_atsakymai[counter] = atsakymas.id
        vartotojo_pasirinkimai = input("Pasirinkite atsakymą (-us) be tarpų")
        ar_atsakymas_teisingas = True
        for indeksas, atsakymo_id in teisingi_atsakymai.items():
            if str(indeksas) in vartotojo_pasirinkimai:
                vartotojo_atsakymas = VartotojoAtsakymas(sprendimas_id=sprendimas.id, klausimas_id=klausimas.id, atsakymas_id=atsakymo_id)
                session.add(vartotojo_atsakymas)
                session.commit()
                aktyvus_atsakymas = session.query(Atsakymas).get(atsakymo_id)
                if aktyvus_atsakymas.ar_teisingas != 1:
                    ar_atsakymas_teisingas = False
        if ar_atsakymas_teisingas:
            taskai += 1
            print("Taškai: ", taskai)

    break