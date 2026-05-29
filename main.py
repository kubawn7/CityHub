from services.auth_service import AuthService
from services.event_service import EventService
from services.ticket_service import TicketService
from services.payment_service import PaymentService
import sys
import time

def print_separator():
    print("-" * 40)

def main():
    # Dodajemy domyślne konto organizatora dla ułatwienia testów
    AuthService.register("Admin", "Szef", "admin@test.pl", "admin123", "ORGANIZER")
    
    current_user = None

    while True:
        print_separator()
        if current_user is None:
            print("=== MENU GŁÓWNE (GOŚĆ) ===")
            print("1. Zaloguj się")
            print("2. Zarejestruj się jako Klient")
            print("3. Przeglądaj wydarzenia")
            print("0. Wyjdź")
            
            choice = input("Wybierz opcję: ")
            
            if choice == "1":
                email = input("Email: ")
                password = input("Hasło: ")
                current_user = AuthService.login(email, password)
                time.sleep(2) 
            elif choice == "2":
                imie = input("Imię: ")
                nazwisko = input("Nazwisko: ")
                email = input("Email: ")
                haslo = input("Hasło: ")
                AuthService.register(imie, nazwisko, email, haslo, "USER")
                time.sleep(2) 
            elif choice == "3":
                EventService.list_events()
                input("Naciśnij Enter, aby kontynuować...")
            elif choice == "0":
                print("Do widzenia!")
                sys.exit()
            else:
                print("Nieprawidłowy wybór.")
                time.sleep(2) 

        elif current_user.role == "ORGANIZER":
            print(f"=== MENU ORGANIZATORA ({current_user.first_name}) ===")
            print("1. Utwórz wydarzenie")
            print("2. Dodaj pulę biletów do wydarzenia")
            print("3. Lista wydarzeń")
            print("4. Lista biletów w systemie")
            print("5. Waliduj bilet na bramce")
            print("0. Wyloguj")
            
            choice = input("Wybierz opcję: ")
            
            if choice == "1":
                title = input("Nazwa wydarzenia: ")
                location = input("Lokalizacja: ")
                date = input("Data (RRRR-MM-DD): ")
                EventService.create_event(title, location, date, current_user.user_id)
                time.sleep(2)
            elif choice == "2":
                try:
                    event_id = int(input("ID wydarzenia: "))
                except ValueError:
                    print("Nieprawidłowe ID wydarzenia. Musi być liczbą.")
                    time.sleep(2)
                    continue
                
                from data_store import events
                if not any(e.event_id == event_id for e in events):
                    print("Nie znaleziono wydarzenia o podanym ID.")
                    time.sleep(2)
                    continue
                
                typ = input("Typ biletu (Standard / VIP): ")
                try:
                    price = float(input("Cena: "))
                    quantity = int(input("Ilość biletów w tej puli: "))
                except ValueError:
                    print("Cena i ilość muszą być wartościami liczbowymi.")
                    time.sleep(2)
                    continue
                    
                TicketService.create_ticket(event_id, typ, price, quantity)
                time.sleep(2)
            elif choice == "3":
                EventService.list_events()
                input("Naciśnij Enter, aby kontynuować...")
            elif choice == "4":
                TicketService.list_tickets()
                input("Naciśnij Enter, aby kontynuować...")
            elif choice == "5":
                try:
                    ticket_id = int(input("Podaj ID biletu do sprawdzenia: "))
                    TicketService.validate_ticket(ticket_id)
                except ValueError:
                    print("Nieprawidłowe ID biletu. Musi być liczbą.")
                time.sleep(2) 
            elif choice == "0":
                current_user = None
            else:
                print("Nieprawidłowy wybór.")
                time.sleep(2) 

        elif current_user.role == "USER":
            print(f"=== MENU UŻYTKOWNIKA ({current_user.first_name}) ===")
            print("1. Przeglądaj wydarzenia i kup bilet")
            print("2. Pokaż moje bilety")
            print("0. Wyloguj")
            
            choice = input("Wybierz opcję: ")
            
            if choice == "1":
                print("\n--- DOSTĘPNE WYDARZENIA ---")
                EventService.list_events()
                print_separator()
                try:
                    event_id_str = input("Podaj ID wydarzenia, na które chcesz kupić bilet (lub 0, aby wrócić): ")
                    event_id = int(event_id_str)
                    
                    if event_id != 0:
                        event_tickets = TicketService.get_available_tickets(event_id)
                        
                        if not event_tickets:
                            print("Niestety, brak biletów na to wydarzenie w systemie.")
                            time.sleep(2)
                        else:
                            print("\n--- DOSTĘPNE BILETY NA TO WYDARZENIE ---")
                            for t in event_tickets:
                                print(t)
                                
                            ticket_id = int(input("\nPodaj ID biletu, który chcesz kupić: "))
                            order = TicketService.buy_ticket(current_user.user_id, ticket_id)
                            
                            if order:
                                price = next((t.price for t in event_tickets if t.ticket_id == ticket_id), 0)
                                print(f"Kwota do zapłaty: {price} PLN")
                                potwierdzenie = input("Czy chcesz opłacić zamówienie? (t/n): ")
                                
                                if potwierdzenie.lower() == 't':
                                    PaymentService.process_payment(order, price)
                                    time.sleep(2)
                                else:
                                    print("Anulowano płatność. Zamówienie ma status PENDING.")
                                    time.sleep(2)
                except ValueError:
                    print("Nieprawidłowa wartość. Wprowadź poprawny numer ID.")
                    time.sleep(2)

            elif choice == "2":
                print("\n=== MOJE BILETY ===")
                from data_store import orders, tickets, events
                
                user_orders = [o for o in orders if o.user_id == current_user.user_id]
                
                if not user_orders:
                    print("Nie masz jeszcze żadnych biletów.")
                else:
                    for order in user_orders:
                        ticket = next((t for t in tickets if t.ticket_id == order.ticket_id), None)
                        if ticket:
                            event = next((e for e in events if e.event_id == ticket.event_id), None)
                            event_name = event.title if event else f"Wydarzenie #{ticket.event_id}"
                            
                            print(f"ZAMÓWIENIE #{order.order_id} [{order.status}] | Bilet #{ticket.ticket_id} ({ticket.ticket_type}) na: {event_name}")
                            
                input("\nNaciśnij Enter, aby kontynuować...")
                
            elif choice == "0":
                current_user = None
                time.sleep(1) 
            else:
                print("Nieprawidłowy wybór.")
                time.sleep(2) 

if __name__ == "__main__":
    main()