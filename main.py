from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def osszesites(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 10000)  # Példának 10000 Ft-os árat állítunk be egy egyszemélyes szobára

    def osszesites(self):
        return self.ar

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 15000)  # Példának 15000 Ft-os árat állítunk be egy kétszemélyes szobára

    def osszesites(self):
        return self.ar

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

def foglalas_lehetseges(szalloda, szobaszam, datum):
    for foglalas in szalloda.foglalasok:
        if foglalas.datum == datum and foglalas.szoba.szobaszam == szobaszam:
            return False
    return True

def foglalas(szalloda, szobaszam, datum):
    if foglalas_lehetseges(szalloda, szobaszam, datum):
        for szoba in szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                szalloda.foglalasok.append(Foglalas(szoba, datum))
                return f"A(z) {szobaszam} szoba foglalása sikeres."
    else:
        return "A foglalás nem lehetséges."

def foglalas_lemondas(szalloda, szobaszam, datum):
    for foglalas in szalloda.foglalasok:
        if foglalas.datum == datum and foglalas.szoba.szobaszam == szobaszam:
            szalloda.foglalasok.remove(foglalas)
            return f"A(z) {szobaszam} szoba foglalásának lemondása sikeres."
    return "A lemondás nem lehetséges, mert a foglalás nem található."

def foglalasok_listazasa(szalloda):
    if szalloda.foglalasok:
        return "\n".join([f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}" for foglalas in szalloda.foglalasok])
    else:
        return "Nincsenek foglalások."

# Szalloda, szobák és foglalások létrehozása
hotel = Szalloda("Példa Hotel")
hotel.uj_szoba(EgyagyasSzoba("101"))
hotel.uj_szoba(EgyagyasSzoba("102"))
hotel.uj_szoba(KetagyasSzoba("201"))

hotel.foglalasok = [
    Foglalas(hotel.szobak[0], datetime(2024, 5, 20)),
    Foglalas(hotel.szobak[1], datetime(2024, 5, 22)),
    Foglalas(hotel.szobak[2], datetime(2024, 5, 25)),
    Foglalas(hotel.szobak[1], datetime(2024, 5, 27)),
    Foglalas(hotel.szobak[0], datetime(2024, 7, 30))
]

# Felhasználói interfész
while True:
    print("\n1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")
    valasztas = input("Válassz egy műveletet: ")

    if valasztas == "1":
        szobaszam = input("Add meg a foglalandó szoba számát: ")
        datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            if datum < datetime.now():
                print("A foglalás dátuma nem lehet múltbeli.")
                continue
            if foglalas_lehetseges(hotel, szobaszam, datum):
                print(foglalas(hotel, szobaszam, datum))
            else:
                print("A foglalás nem lehetséges.")
        except ValueError:
            print("Hibás dátum formátum.")
    elif valasztas == "2":
        szobaszam = input("Add meg a lemondandó foglalás szobaszámát: ")
        datum = input("Add meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d")
            print(foglalas_lemondas(hotel, szobaszam, datum))
        except ValueError:
            print("Hibás dátum formátum.")
    elif valasztas == "3":
        print(foglalasok_listazasa(hotel))
    elif valasztas == "4":
        break
    else:
        print("Nem megfelelő választás.")
