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
        System.out.println("[KABOOTER] => " + s);
    }
}

class NotificationFactory {
    static Notification notifFactory(NotificationType nt) {
        switch (nt) {
            case NotificationType.EMAIL:
                return new Email();   
            case NotificationType.SMS:
                return new SMS();    
            case NotificationType.KABOOTER:
                return new Kabooter();
            default:
                return new Kabooter();
        }
    }
}

public class NotificationTest {
    public static void main(String[] args) {
        String s = "Meow Meow Meow";
        Notification n = NotificationFactory.notifFactory(NotificationType.KABOOTER);
        n.sendNotif(s);
    }    
}
