package API;

import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.net.http.HttpClient;
import java.io.IOException;

public class CurrentCall extends ApiCall {

    public HttpRequest buildRequest(String key, String loc) throws IOException {
        String baseURL = "http://api.weatherapi.com/v1/current.json";
        String finalURL = String.format("%s?key=%s&q=%s", baseURL, key, loc);

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(finalURL))
            .method("GET", HttpRequest.BodyPublishers.noBody())
            .build();

        return request;
    }
    
    public String getResponse(HttpRequest req) throws IOException {
        HttpResponse <String> response = null;

        try {
            response = HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());
        } catch (Exception e) {
            throw new IOException(e);
        }

        return response.body();
    }
}
