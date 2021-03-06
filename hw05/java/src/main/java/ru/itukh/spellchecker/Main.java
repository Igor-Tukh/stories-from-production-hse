package ru.itukh.spellchecker;

import org.apache.commons.codec.EncoderException;

import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        SpellChecker checker = new SpellChecker();
        System.out.println("Type text to apply the spell checker or type 'exit' to exit.");
        while(true) {
            System.out.print("> ");
            String text = in.nextLine();
            if (text.equals("exit")) {
                break;
            }
            try {
                checker.check(text);
            } catch (IOException | EncoderException e) {
                System.out.println("Error occurred during spell checking: " + e.getMessage() + ".");
                System.exit(1);
            }
        }
    }
}
