import java.util.ArrayList;
import java.util.stream.IntStream;

class Counter {
    int count;
    Counter() {
        this.count = 0;
    }
}

class TestTask implements Runnable {
    int s;
    Counter c;

    TestTask(int st, Counter c) {
        this.s = st;
        this.c = c;
    }

    @Override
    public void run() {
        for(int i = 0; i < this.s; i++){
            c.count += 1;
        }
    }
}

class ThreadManager {
    ArrayList<Thread> allThreads;

    ThreadManager() {
        this.allThreads = new ArrayList<Thread>();
    }

    void addThread(Runnable r) {
        Thread th = new Thread(r);
        allThreads.add(th);
    }

    void startThreads() {
        for(Thread th: this.allThreads) {
            th.start();
        }
    }

    void joinAll() throws InterruptedException {
        for(Thread th: this.allThreads) {
            th.join();
        }
    }

    void addMultipleThreads(int threadCount, int count, Counter c) {
        IntStream.range(0, threadCount)
                    .forEach(x -> {
                        TestTask t = new TestTask(count, c);
                        this.addThread(t);
                    });
    }
}

public class BadCounter {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Start Things");
        Counter c = new Counter();
        ThreadManager th = new ThreadManager();
        th.addMultipleThreads(1000, 10000, c);
        th.startThreads();
        th.joinAll();
        System.out.println("Done" + " " + c.count);
    }
}

