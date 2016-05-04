package src.PolishNotation;

import src.Calculator;
import src.DivisionByZeroException;
import src.OperationNotSupportedException;
import src.ParseValueException;

import java.util.EmptyStackException;
import java.util.HashMap;
import java.util.Stack;

public class PolishNotationParser {
    public String polishCompute(String rawStr, Calculator calc) throws ParseValueException, DivisionByZeroException, OperationNotSupportedException {
        Stack<String> stack = new Stack<String>();
        String[] raw = rawStr.split(" ");
        String[] operations = new String[]{"+", "-", "*", "/"};
        for (int i = 0; i < raw.length; i++) {
            boolean operation = false;
            for (String e : operations)
                if (raw[i].equals(e))
                    operation = true;
            if (!operation)
                stack.push(raw[i]);
            else {
                try {
                    String arg2 = stack.pop();
                    String arg1 = stack.pop();
                    stack.push(calc.calculate(arg1, raw[i], arg2));
                } catch (EmptyStackException exception) {
                    throw new ParseValueException();
                }

            }
        }
        return stack.peek().trim();
    }


    public String convertToPolish(String rawStr) throws ParseValueException {
        Stack<String> opStack = new Stack<String>();
        StringBuilder answer = new StringBuilder();
        String[] raw = rawStr.split(" ");
        HashMap<String, Integer> operations = new HashMap<>();
        operations.put("(", 1);
        operations.put("+", 2);
        operations.put("-", 2);
        operations.put("/", 3);
        operations.put("*", 3);
        operations.put(")", 4);
        for (int i = 0; i < raw.length; i++) {
            boolean operation = false;
            if (operations.containsKey(raw[i]))
                operation = true;
            if (!operation)
                answer.append(raw[i] + " ");
            else {
                if (raw[i].equals("("))
                    opStack.push("(");
                else if (raw[i].equals(")")) {
                    try {
                        String topOp = opStack.pop();
                        while (!topOp.equals("(")) {
                            answer.append(topOp + " ");
                            topOp = opStack.pop();
                        }
                    } catch (EmptyStackException ex) {
                        throw new ParseValueException();
                    }
                } else {

                    while (!opStack.isEmpty() && operations.get(opStack.peek()) >= operations.get(raw[i]))
                        answer.append(opStack.pop() + " ");
                    opStack.push(raw[i]);
                }
            }
        }
        while (!opStack.isEmpty())
            answer.append(opStack.pop() + " ");
        return answer.toString().trim();

    }
}
