import threading

barCount = 0

def foo():
    for i in range(10):
        print("Foo")

def bar():
    for i in range(10):
        print("Bar")

def threadTest():
    threads = [threading.Thread(target=foo), threading.Thread(target=bar)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("Done")

threadTest()