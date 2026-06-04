# CityHub

Prototyp aplikacji CLI do zarządzania eventami masowymi. Umożliwia organizatorom tworzenie wydarzeń i pul biletów, a użytkownikom — przeglądanie, zakup i opłacanie biletów. Aplikacja działa w trybie konsolowym z danymi przechowywanymi w pamięci.

## Funkcjonalności

**Dla organizatora:**

* Tworzenie wydarzeń (nazwa, lokalizacja, data)
* Dodawanie pul biletów do wydarzenia (typ Standard/VIP, cena, ilość)
* Przeglądanie wszystkich wydarzeń i biletów w systemie
* Walidacja biletów na bramce (sprawdzanie statusu PAID + flagi `is\_used`)

**Dla użytkownika:**

* Rejestracja i logowanie
* Przeglądanie dostępnych wydarzeń
* Zakup biletu i opłacenie zamówienia
* Podgląd własnych biletów z historią zamówień

## Stack

|||
|-|-|
|Język|Python 3.x|
|Interfejs|CLI (terminal)|
|Architektura|Serwisy + modele|

## Struktura projektu

```
CityHub/
├── main.py                  # Punkt wejścia, pętla menu CLI
├── data\_store.py            # Globalne listy danych (users, events, tickets, orders, payments)
├── models/
│   ├── user.py              # Model użytkownika (role: USER / ORGANIZER)
│   ├── events.py            # Model wydarzenia
│   ├── ticket.py            # Model biletu (Standard / VIP, flaga is\_used)
│   ├── order.py             # Model zamówienia (statusy: PENDING → PAID)
│   └── payment.py           # Model płatności
├── services/
│   ├── auth\_service.py      # Rejestracja i logowanie
│   ├── event\_service.py     # Tworzenie i listowanie wydarzeń
│   ├── ticket\_service.py    # Tworzenie pul, zakup, walidacja bramkowa
│   └── payment\_service.py   # Przetwarzanie płatności
└── utils/
    └── generator.py         # Generator losowych ID (1000–9999)
```

## Uruchomienie

```bash
# Sklonuj repozytorium
git clone https://github.com/kubawn7/CityHub.git
cd CityHub

# Uruchom aplikację (wymagany Python 3.x, brak zewnętrznych zależności)
python main.py
```

Po uruchomieniu automatycznie tworzony jest domyślny konto organizatora:

```
Email:  admin@test.pl
Hasło:  admin123
```

## Przepływ działania

```
Organizator                        Użytkownik
──────────────────────────────     ──────────────────────────────
1. Utwórz wydarzenie               1. Zarejestruj się / zaloguj
2. Dodaj pulę biletów              2. Przeglądaj wydarzenia
                                   3. Kup bilet → status PENDING
                                   4. Opłać zamówienie → status PAID
Organizator
──────────────────────────────
5. Waliduj bilet na bramce
   ✓ istnieje → ✓ PAID → ✓ nieużyty → wpuszcza
```

## ograniczenia (prototyp)

* Dane są przechowywane wyłącznie w pamięci — reset przy każdym uruchomieniu
* Hasła przechowywane jako plain text
* Generator ID może tworzyć kolizje (zakres 1000–9999)
* Brak warstwy sieciowej / API

