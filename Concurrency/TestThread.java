import java.util.ArrayList;
import java.util.stream.IntStream;

class ThreadManager {
   ArrayList<Thread> allThreads = new ArrayList();

   ThreadManager() {
   }

   void addThread(Runnable var1) {
      Thread var2 = new Thread(var1);
      this.allThreads.add(var2);
   }

   void startThreads() {
      for(Thread var2 : this.allThreads) {
         var2.start();
      }

   }

   void joinAll() throws InterruptedException {
      for(Thread var2 : this.allThreads) {
         var2.join();
      }

   }

   void addMultipleThreads(int var1, int var2, Counter var3) {
      IntStream.range(0, var1).forEach((var3x) -> {
         TestTask var4 = new TestTask(var2, var3);
         this.addThread(var4);
      });
   }
}


public class TestThread {
    public static void main(String[] args) {
        System.out.println("ABCD");
        ThreadManager tm = new ThreadManager();
        
    }    
}
