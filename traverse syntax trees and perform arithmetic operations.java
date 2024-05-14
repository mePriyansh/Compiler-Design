import java.util.*;

class Node {
    String value;
    Node left;
    Node right;

    public Node(String value) {
        this.value = value;
        this.left = null;
        this.right = null;
    }
}

public class Main {
    static class SyntaxTree {
        Node root;

        public SyntaxTree() {
            this.root = null;
        }

        public double evaluate(Node node) {
            if (node == null)
                return 0;

            // If the node is a number, return its value
            if (node.value.matches("\\d+"))
                return Double.parseDouble(node.value);

            // Recursively evaluate left and right subtrees
            double leftValue = evaluate(node.left);
            double rightValue = evaluate(node.right);

            // Perform the operation indicated by the node's value
            switch (node.value) {
                case "+":
                    return leftValue + rightValue;
                case "-":
                    return leftValue - rightValue;
                case "*":
                    return leftValue * rightValue;
                case "/":
                    if (rightValue == 0)
                        throw new ArithmeticException("Division by zero");
                    return leftValue / rightValue;
                default:
                    throw new IllegalArgumentException("Invalid operator");
            }
        }
    }

    public static Node buildSyntaxTree(String expression) {
        String[] tokens = expression.split("\\s+");
        Stack<Node> stack = new Stack<>();

        // Iterate over each token in the postfix expression
        for (String token : tokens) {
            if (token.matches("\\d+")) {
                // If the token is a number, push it onto the stack
                Node node = new Node(token);
                stack.push(node);
            } else {
                // If the token is an operator, pop the top two elements from the stack
                if (stack.size() < 2)
                    throw new IllegalArgumentException("Invalid expression");

                Node right = stack.pop();
                Node left = stack.pop();
                Node node = new Node(token);
                node.left = left;
                node.right = right;

                // Push the new subtree back onto the stack
                stack.push(node);
            }
        }

        // The stack should contain exactly one element, the root of the syntax tree
        if (stack.size() != 1)
            throw new IllegalArgumentException("Invalid expression");

        return stack.pop();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter arithmetic expression in postfix notation (e.g., '3 4 +'): ");
        String expression = scanner.nextLine();
        scanner.close();

        Node syntaxTree = buildSyntaxTree(expression);
        SyntaxTree calculator = new SyntaxTree();
        double result = calculator.evaluate(syntaxTree);
        System.out.println("Result: " + result);
    }
}
