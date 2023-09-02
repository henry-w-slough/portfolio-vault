package reversingStrings;
import java.util.Scanner;

class reversingStrings {


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        //variables
        String givenString;
        String reversedString = "";

        
        //asking for valid string
        System.out.println("Enter a Valid String: ");
        givenString = scanner.nextLine();
          

        //making the reversed list
        for (int i = givenString.length() - 1; i >= 0; i--) {
        
            reversedString = reversedString+givenString.charAt(i);

        }


        //printing reversed string
        System.out.println(reversedString);
        
        
            scanner.close();
        }








        
    }

