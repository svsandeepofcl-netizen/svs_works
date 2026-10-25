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
                cls._instance.pool_lock=threading.Lock()
                # cls._instance.available=[]
                return cls._instance
            else:
                print("Already object is created")
                return cls._instance
        

    def acquired_connection(self):
        start_time = time.time()

        while True:
            with self.pool_lock:
                if self.connection_pool:
                    conn = self.connection_pool.pop()
                    print(f"Acquired {conn} for {threading.current_thread().name}")
                    return conn
                else:
                    print(f"Waiting for connection... {threading.current_thread().name}")
                    time.sleep(0.5)
              


    def close_connection(self, connection):
        with self.pool_lock:
            print(f"Released Connection {connection}")
            self.connection_pool.append(connection)




# we are creating a custom function to execute after sometime, which will close the connection and when the while loop runs again since one connection is appended it will run again
# def delayed_close_connection(obj,connection):
#     time.sleep(6)
#     obj.close_connection(connection)


# db=DBConnection()
# c1=db.aqcuired_connection()
# c2=db.aqcuired_connection()
# new_thread=threading.Thread(target=delayed_close_connection, args=(db,c2)).start()
# c3=db.aqcuired_connection()
# c4=db.aqcuired_connection()


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



