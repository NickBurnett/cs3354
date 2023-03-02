import java.util.Scanner;

public class FSM {
 
    // function to check the stateA
    public static void checkStateA(String n) {
       
        if(n.length() == 0) {
            System.out.println(" ");
        }
        else {
            if(n.charAt(0) == 'a') {
                System.out.print("1");
                stateB(n.substring(1));
            }
            else if(n.charAt(0) != 'b'){
                System.out.print("0");
                stateB(n.substring(1));
            }
        }
    }
 
    // function to check the stateB
    public static void stateB(String n) {
        if(n.length() == 0) {
            System.out.println(" ");
        }
        if(n.charAt(0) == 'b') {
            System.out.print("1");
            stateC(n.substring(1));
        }else if(n.charAt(0) != 'b'){
            System.out.print("0");
            stateC(n.substring(1));
        }
    }
 
    // function to check the stateC
    public static void stateC(String n) {
        if(n.length() == 0) {
            System.out.println(" ");
        }
        if(n.charAt(0) == 'c') {
            System.out.print("1");
            stateD(n.substring(1));
        }else if(n.charAt(0) != 'b'){
            System.out.print("0");
            stateD(n.substring(1));
        }
    }
 
    // function to check the stateD
    public static void stateD(String n) {
        if(n.length() == 0) {
            System.out.println(" ");
        }
        if(n.charAt(0) == 'd') {
            System.out.print("1");
            checkStateA(n.substring(1));
        }else if(n.charAt(0) != 'b'){
            System.out.print("0");
            checkStateA(n.substring(1));
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