enum NotificationType {
    EMAIL,
    SMS, 
    KABOOTER
}

interface Notification {
    public void sendNotif(String s);
} 


class Email implements Notification {
    @Override
    public void sendNotif(String s) {
        System.out.println("[EMAIL] => " + s);
    }
}

class SMS implements Notification {
    @Override
    public void sendNotif(String s) {
        System.out.println("[SMS] => " + s);
    }
}

class Kabooter implements Notification {
    @Override
    public void sendNotif( String s){
        System.out.println("[KABOOTER] => " + S)
    }
}


public class NotificationFactory {
    public static void main(String[] args) {
        System.out.println("Random");
    }    
}
