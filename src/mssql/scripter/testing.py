import threading
import Queue

q = Queue.Queue()
q.put(None)
q.get()

if __name__ == '__main__':
    main()   