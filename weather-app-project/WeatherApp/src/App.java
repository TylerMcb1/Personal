import java.net.http.HttpRequest;
import java.io.IOException;

import API.CurrentCall;

public class App {
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Usage: java App <API-KEY> <LOCATION>");
            System.exit(1);
        }

        String key = args[0];
        String loc = args[1];

        CurrentCall Call = new CurrentCall();
        String output = new String();

        try {
            HttpRequest req = Call.buildRequest(key, loc);
            output = Call.getResponse(req);
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println(output);
    }
}
