import time
import threading

class DBConnection:
    _instance=None
    _timeout=10
    _lock=threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                print("Creating object")
                cls._instance=super().__new__(cls)
                cls._instance.connection_pool=["con1", "con2", "con3"]
                cls._instance.semaphore= threading.Semaphore(len( cls._instance.connection_pool))
                cls._instance.pool_lock=threading.Lock()
                # cls._instance.available=[]
                return cls._instance
            else:
                print("Already object is created")
                return cls._instance
        

    def acquired_connection(self):
        self.semaphore.acquire()
        with self.pool_lock:
            if len(self.connection_pool) >0:
                print(f"Connection established for thread {threading.current_thread().name}")
                return self.connection_pool.pop()
              

    def close_connection(self, connection):
        with self.pool_lock:
            print(f"Released Connection {connection}")
            self.connection_pool.append(connection)
        
        self.semaphore.release()


def worker():
    db=DBConnection()
    conn=db.acquired_connection()
    time.sleep(5)
    db.close_connection(conn)

threads=[]

for i in range(5):
    thread=threading.Thread(target=worker, name = f"Thread-{i}")
    threads.append(thread)
    thread.start()


for thead in threads:
    thread.join()



