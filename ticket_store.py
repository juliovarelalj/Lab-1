from threading import Semaphore, Thread
import time
from datetime import datetime


INITIAL_TIMESTAMP = datetime.now()
total_earnings = 0
semaphore = None


def get_elapsed_seconds() -> float:
    
    return round((datetime.now() - INITIAL_TIMESTAMP).total_seconds(), 1)


def simulate_store(customers: [dict], ticket_price: float, max_occupancy: int, n_vips: int) -> float:
   
    global semaphore, total_earnings
    semaphore = Semaphore(max_occupancy)
    total_earnings = 0

    def customer_behavior(name, ticket_count, time_in_store, join_delay):
        
        global total_earnings

        
        time.sleep(join_delay)

        
        semaphore.acquire()
        print(f"{get_elapsed_seconds()}s: {name} (entering)")

       
        time.sleep(time_in_store)

        
        print(f"{get_elapsed_seconds()}s: {name} (leaving)")
        semaphore.release()
        total_earnings += ticket_count * ticket_price

    
    threads = []
    for customer in customers:
        thread = Thread(
            target=customer_behavior,
            args=(
                customer["name"],
                customer["ticketCount"],
                customer["timeInStore"],
                customer["joinDelay"],
            ),
            name=customer["name"],  
        )
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    return total_earnings


