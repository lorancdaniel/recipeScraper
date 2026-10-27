from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Definicja modelu tabeli przepisy – jedyne miejsce, w którym opisany jest schemat
class Przepis(Base):
    __tablename__ = "przepisy"
    id = Column(Integer, primary_key=True)
    nazwa = Column(String(255), nullable=False)
    czas_przygotowania = Column(Integer)  # w minutach
    zdjecie_url = Column(String(255))
    opis = Column(Text)
    instrukcja = Column(Text)
    skladniki = Column(Text)
    zrodlo_url = Column(String(255))
