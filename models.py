from sqlalchemy import (Column,
                        create_engine,
                        Integer,
                        String,
                        ForeignKey,
                        Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///testai.db')
Base = declarative_base()

class Vartotojas(Base):
    __tablename__ = 'vartotojas'
    id = Column(Integer, primary_key=True)
    vardas = Column("Vardas", String)
    pavarde = Column("Pavarde", String)

    def __str__(self):
        return f"{self.id} - {self.vardas} {self.pavarde}"

class Testas(Base):
    __tablename__ = "testas"
    id = Column(Integer, primary_key=True)
    pavadinimas = Column("Pavadinimas", String)
    klausimai = relationship('Klausimas', back_populates="testas")

    def __str__(self):
        return f'{self.id} - {self.pavadinimas}'

class Klausimas(Base):
    __tablename__ = "klausimas"
    id = Column(Integer, primary_key=True)
    tekstas = Column("Tekstas", String)
    testas_id = Column(Integer, ForeignKey('testas.id'))
    testas = relationship('Testas', back_populates='klausimai')
    atsakymai = relationship("Atsakymas", back_populates='klausimas')

    def __str__(self):
        return f"{self.id} - {self.tekstas}"

class Atsakymas(Base):
    __tablename__ = "atsakymas"
    id = Column(Integer, primary_key=True)
    klausimas_id = Column(Integer, ForeignKey('klausimas.id'))
    tekstas = Column("Tekstas", String)
    ar_teisingas = Column("Ar teisingas", Boolean)
    klausimas = relationship("Klausimas", back_populates='atsakymai')

    def __str__(self):
        return f"{self.id} - {self.tekstas}"


class Sprendimas(Base):
    __tablename__ = "sprendimas"
    id = Column(Integer, primary_key=True)
    data = Column("Data", String)
    testas_id = Column(Integer, ForeignKey('testas.id'))
    vartotojas_id = Column(Integer, ForeignKey('vartotojas.id'))
    rezultatas = Column("Rezultatas", String)

class VartotojoAtsakymas(Base):
    __tablename__ = "vartotojo_atsakymas"
    id = Column(Integer, primary_key=True)
    sprendimas_id = Column(Integer, ForeignKey('sprendimas.id'))
    klausimas_id = Column(Integer, ForeignKey('klausimas.id'))
    atsakymas_id = Column(Integer, ForeignKey('atsakymas.id'))

Base.metadata.create_all(engine)