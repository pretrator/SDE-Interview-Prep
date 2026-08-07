/**
 * bevarageMakerTest
 */

abstract class BeverageMaker {
    void step1() {
        System.out.println("Bhagona on the flame");
    }
    
    void step2() {
        System.out.println("Pani in the bhagona");
    }

    void step3() {
        System.out.println("Switch on the gas");
    }
    void step4() {
        System.out.println("Doodh daalo");
    }
    void step5() {
        System.out.println("Cheeni Daalo");
    }

    abstract void step6();

    void step7() {
        System.out.println("Adrak daalo");
    }
    void step8() {
        System.out.println("Wait for 10 min");
    }
    void step9() {
        System.out.println("Filter in the cup");
    }
    
    void makeBeverage() {
        this.step1();
        this.step2();
        this.step3();
        this.step4();
        this.step5();
        this.step6();
        this.step7();
        this.step8();
        this.step9();

    }

}

class Tea extends BeverageMaker {
   @Override
   void step6() {
    System.out.println("chai patti daalo");
   } 
}

class Coffee extends BeverageMaker {
    @Override
    void step2() {
        
    }
    
    @Override
    void step6() {
        System.out.println("Coffee daalo");
    }

    @Override
    void step7() {
    }
}

public class bevarageMakerTest {
    public static void main(String[] args) {
        BeverageMaker t = new Tea();
        t.makeBeverage();
        System.out.println("//////////////////");
        BeverageMaker c = new Coffee();
        c.makeBeverage();
    }
}
