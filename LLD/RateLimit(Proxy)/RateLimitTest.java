class Request {
    String req;
    Request(String req) {
        this.req = req;
    }
}

interface RequestHandlerInterface {
    void handleRequest(Request r);
}

class RequestHandler implements RequestHandlerInterface {
    public void handleRequest(Request r) {
        System.out.println("Handled Request " + r.req);
    }
}

class RequestRateLimit implements RequestHandlerInterface {
    int requestCount;
    int maxRequstAllowed;
    RequestHandlerInterface requestHandler;
    
    RequestRateLimit(RequestHandlerInterface rq) {
        this.requestCount = 0;
        this.maxRequstAllowed = 10;
        this.requestHandler = rq;
    }
    
    public void handleRequest(Request r) {
        if(this.requestCount < this.maxRequstAllowed){
            this.requestCount += 1;
            this.requestHandler.handleRequest(r);
            return;
        }
        System.out.println("RATE LIMIT BLOCK " + r.req);
    }
}


public class RateLimitTest {
    public static void main(String[] args) {
        RequestRateLimit rrl = new RequestRateLimit(new RequestHandler());
        // RequestRateLimit rrl = new RequestRateLimit(rqh);
        rrl.handleRequest(new Request("Chiya Bhiya 1"));
        rrl.handleRequest(new Request("Chiya Bhiya 2"));
        rrl.handleRequest(new Request("Chiya Bhiya 3"));
        rrl.handleRequest(new Request("Chiya Bhiya 4"));
        rrl.handleRequest(new Request("Chiya Bhiya 5"));
        rrl.handleRequest(new Request("Chiya Bhiya 6"));
        rrl.handleRequest(new Request("Chiya Bhiya 7"));
        rrl.handleRequest(new Request("Chiya Bhiya 8"));
        rrl.handleRequest(new Request("Chiya Bhiya 9"));
        rrl.handleRequest(new Request("Chiya Bhiya 10"));
        rrl.handleRequest(new Request("Chiya Bhiya 11"));
        rrl.handleRequest(new Request("Chiya Bhiya 12"));
        rrl.handleRequest(new Request("Chiya Bhiya 13"));
        rrl.handleRequest(new Request("Chiya Bhiya 14"));
    }
}
