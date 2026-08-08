

class OverloadedDemo {
    void overload1(int i) {
        System.out.println("Integer overloading Single");
    }

    void overload1(int i, int j) {
        System.out.println("Integer overloading Double");
    }

    void overload1(String st) {
        System.out.println("String OVerloading");
    }

    void overload1() {
        System.out.println("String OVerloading Nothing");
    }
}

public class Overloading {
    public static void main(String[] args) {
        System.out.println("Hey Hi");
        OverloadedDemo ovd = new OverloadedDemo();
        ovd.overload1();
        ovd.overload1(1);
        ovd.overload1("Ankur");
        ovd.overload1(1, 2);
    }   

}
