package API;

import java.net.http.HttpRequest;
import java.io.IOException;

/**
 * ApiCall provides a template for different API calls used with 
 * api.weatherapi.com. Subclasses implement the buildRequest() and 
 * getResponse() methods.
 */
abstract class ApiCall {
    /**
     * Builds an HTTP request for an API call to api.weatherapi.com
     * @param key the access key for the API
     * @param loc the location of weather retrieval
     * @return an HTTP request if successful, throws exception otherwise
     */
    public abstract HttpRequest buildRequest(String key, String loc) throws IOException;

    /**
     * Returns the JSON of API weather data as a string
     * @param req the HTTP request for the API
     * @return the JSON of the request in string form, throws exception otherwise
     */
    public abstract String getResponse(HttpRequest req) throws IOException;
}