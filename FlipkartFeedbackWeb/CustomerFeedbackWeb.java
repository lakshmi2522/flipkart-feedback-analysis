import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

public class CustomerFeedbackWeb {
    private static final Path WEB = Path.of("public").toAbsolutePath().normalize();

    public static void main(String[] args) throws IOException {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/api/analyze", ex -> analyze(ex));
        server.createContext("/", ex -> serve(ex));
        server.start();
        System.out.println("Server started on port " + port);
        System.out.println("Press Ctrl+C to stop.");
    }

    private static void analyze(HttpExchange ex) throws IOException {
        if (!"POST".equalsIgnoreCase(ex.getRequestMethod())) {
            send(ex, 405, "application/json", "{\"error\":\"Use POST.\"}");
            return;
        }
        String body = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        Map<String,String> data = new HashMap<>();
        for (String pair : body.split("&")) {
            String[] p = pair.split("=", 2);
            data.put(URLDecoder.decode(p[0], StandardCharsets.UTF_8),
                p.length > 1 ? URLDecoder.decode(p[1], StandardCharsets.UTF_8) : "");
        }
        String name = data.getOrDefault("customerName", "").trim();
        String feedback = data.getOrDefault("feedback", "").trim();
        String keyword = data.getOrDefault("keyword", "").trim();

        if (name.isEmpty()) { send(ex,400,"application/json","{\"error\":\"Please enter the customer name.\"}"); return; }
        if (feedback.isEmpty()) { send(ex,400,"application/json","{\"error\":\"Feedback cannot be empty.\"}"); return; }
        if (feedback.length() > 500) { send(ex,400,"application/json","{\"error\":\"Feedback cannot exceed 500 characters.\"}"); return; }

        int words = feedback.trim().split("\\s+").length;
        int occurrences = 0;
        if (!keyword.isEmpty()) {
            String text = feedback.toLowerCase();
            String target = keyword.toLowerCase();
            int at = 0;
            while ((at = text.indexOf(target, at)) != -1) { occurrences++; at += target.length(); }
        }
        String json = "{\"customerName\":\""+esc(name)+"\",\"feedback\":\""+esc(feedback)
            +"\",\"keyword\":\""+esc(keyword)+"\",\"characterCount\":"+feedback.length()
            +",\"wordCount\":"+words+",\"occurrences\":"+occurrences+"}";
        send(ex,200,"application/json; charset=UTF-8",json);
    }

    private static String esc(String s) {
        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r")
                .replace("\t", "\\t");
    }

    private static void serve(HttpExchange ex) throws IOException {
        String urlPath = ex.getRequestURI().getPath();
        if (urlPath.equals("/")) urlPath="/index.html";
        Path file = WEB.resolve(urlPath.substring(1)).normalize();
        if (!file.startsWith(WEB) || !Files.exists(file) || Files.isDirectory(file)) {
            send(ex,404,"text/plain; charset=UTF-8","Page not found."); return;
        }
        String n=file.getFileName().toString().toLowerCase();
        String type=n.endsWith(".html")?"text/html; charset=UTF-8":n.endsWith(".css")?"text/css; charset=UTF-8":n.endsWith(".js")?"application/javascript; charset=UTF-8":"text/plain; charset=UTF-8";
        send(ex,200,type,Files.readString(file,StandardCharsets.UTF_8));
    }

    private static void send(HttpExchange ex,int status,String type,String content) throws IOException {
        byte[] bytes=content.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type",type);
        ex.getResponseHeaders().set("X-Content-Type-Options","nosniff");
        ex.sendResponseHeaders(status,bytes.length);
        try(var out=ex.getResponseBody()){out.write(bytes);}
    }
}
