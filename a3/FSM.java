import java.util.Scanner;

public class FSM {
 
    // function to check the stateA
    public static void checkStateA(String n) {
       
        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {
            if(n.charAt(0) == 'a') {
                stateB(n.substring(1));
            }
            else {
                stateF(n.substring(1));
            }
        }
    }
 
    // function to check the stateB
    public static void stateB(String n) {
       
        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {
           
            if(n.charAt(0) == 'a') {
                stateC(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateC
    public static void stateC(String n) {
       
        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {
            if(n.charAt(0) == 'a') {
                stateD(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateD
    public static void stateD(String n) {
       
        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {
           
            if(n.charAt(0) == 'a') {
                stateE(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateE
    public static void stateE(String n) {
       
        if(n.length() == 0) {
            System.out.println("String accepted");
        }
 
        else if(n.charAt(0) == 'a') {
            stateE(n.substring(1));
        }
        else if(n.charAt(0) == 'b') {
            stateF(n.substring(1));
        }
    }
 
    // function to check the stateF
    public static void stateF(String n) {

        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {

            if(n.charAt(0) == 'b') {
                stateG(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateG
    public static void stateG(String n) {

        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {

            if(n.charAt(0) == 'b') {
                stateH(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateH
    public static void stateH(String n) {

        if(n.length() == 0) {
            System.out.println("String not accepted");
        }
        else {

            if(n.charAt(0) == 'b') {
                stateQ(n.substring(1));
            }
            else {
                System.out.println("String not accepted");
            }
        }
    }
 
    // function to check the stateQ
    public static void stateQ(String n) {

        if(n.length() == 0) {
            System.out.println("String accepted");
        }
        else {

            if(n.charAt(0) == 'b') {
                stateQ(n.substring(1));
            }
            else if(n.charAt(0) == 'a') {
                stateB(n.substring(1));
            }
        }
    }
 
    // Driver code
    public static void main(String[] args) {
       
        // input string 1
        Scanner in = new Scanner(System.in);
        String input = in.nextLine();
 
        // function call to check the string
        checkStateA(input);

        in.close();
    }
}