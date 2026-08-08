interface Order {
  public void execute();
  public void undo(); 
}

class Kitchen {
    void prepare_dish(String dish)  {
        System.out.println("Preparing : [" + dish + "]");
    }

    void cancel_dish(String dish) {
        System.out.println("Cancelling : [" + dish + "]");
    }
}

class PlaceOrderCommand extends Order{
    PlaceOrderCommand(kitchen, dish) {
        this.kitchen = kitchen
        this.
    }

    void execute() {
        
    }

    void undo() {

    }

}

class CancelOrderCommand extends Order{
    void CancelOrderCommand() {

    }

    void execute() {
        
    }

    void undo() {
        
    }

}

class Waiter {

}

class FoodOrder {
    public static void main(String[] args) {
        
    }
}