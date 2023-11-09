package org.javeriana;

import org.zeromq.ZContext;
import org.zeromq.ZMQ;
import java.util.Random;

public class CalculatorServer {
    public static void main(String[] args) {
        try (ZContext context = new ZContext()) {
            ZMQ.Socket publisher = context.createSocket(ZMQ.PUB);
            publisher.connect("tcp://localhost:5555"); // Conéctate al broker

            Random random = new Random();

            while (!Thread.currentThread().isInterrupted()) {
                int operand1 = random.nextInt(100);
                int operand2 = random.nextInt(100);
                String operation = "ADD"; // Cambia la operación según sea necesario

                // Publica la solicitud al broker
                publisher.send(String.format("%s %d %d", operation, operand1, operand2));
                Thread.sleep(1000); // Simula un retraso en la publicación
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

