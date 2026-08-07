enum PrinterStatus {
    IDLE,
    RUNNING,
}

class SingletonPrinter {
    private PrinterStatus state;
    private static SingletonPrinter printer = null;
    
    private SingletonPrinter() {
        this.state = PrinterStatus.IDLE;
    }

    void setRunning() {
        this.state = PrinterStatus.RUNNING;
    }

    static SingletonPrinter getInstance() {
        if(SingletonPrinter.printer == null) {
            SingletonPrinter.printer = new SingletonPrinter();
        }
        return SingletonPrinter.printer;
    }

    PrinterStatus getStatus() {
        return this.state;
    }
}

public class SingletonTest {
    public static void main(String[] args) {
        System.out.println("Singleton Demo");
        SingletonPrinter printer = new SingletonPrinter();
        // SingletonPrinter printer1 = SingletonPrinter.getInstance();
        // System.out.println(printer1.getStatus());
        // printer1.setRunning();
        // SingletonPrinter printer2 = SingletonPrinter.getInstance();
        // System.out.println(printer1.getStatus());
    }
}
