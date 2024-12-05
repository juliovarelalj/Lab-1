from datetime import datetime
import threading
import time

INITIAL_TIMESTAMP = datetime.now()

def get_elapsed_seconds() -> float:
    return round((datetime.now() - INITIAL_TIMESTAMP).total_seconds(), 1)

def simulate_store(customers: [dict], ticket_price: float, max_occupancy: int, n_vips: int) -> float:

    earnings = 0.0
    vip_remaining = n_vips  
    
    occupancy_sem = threading.Semaphore(max_occupancy) 
    vip_mutex = threading.Semaphore(1)                  
    regular_sem = threading.Semaphore(0)               
   
    threads = []

    
    def customer_behavior(customer: dict):
        nonlocal earnings, vip_remaining

        name = customer['name']
        ticketCount = customer['ticketCount']
        timeInStore = customer['timeInStore']
        joinDelay = customer['joinDelay']
        VIP = customer['VIP']

        
        time.sleep(joinDelay)

        if VIP:
            
            occupancy_sem.acquire()

            
            print(f"{get_elapsed_seconds()}s: {name} (entering)")

            
            time.sleep(timeInStore)

            
            vip_mutex.acquire()
            earnings += ticket_price * ticketCount
            vip_mutex.release()

           
            print(f"{get_elapsed_seconds()}s: {name} (leaving)")

           
            occupancy_sem.release()

            
            vip_mutex.acquire()
            vip_remaining -= 1
            if vip_remaining == 0:
                
                for _ in range(max_occupancy):
                    regular_sem.release()
            vip_mutex.release()

        else:
           
            
            regular_sem.acquire()

            
            occupancy_sem.acquire()

            
            print(f"{get_elapsed_seconds()}s: {name} (entering)")

            
            time.sleep(timeInStore)

            
            vip_mutex.acquire()
            earnings += ticket_price * ticketCount
            vip_mutex.release()

            
            print(f"{get_elapsed_seconds()}s: {name} (leaving)")

            
            occupancy_sem.release()

    
    for customer in customers:
        thread = threading.Thread(target=customer_behavior, args=(customer,), name=customer['name'])
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    return earnings
