import re
import time #short pauses for visualization

#q0 -> pushes bottom marker $ onto stack, pops nothing, then goes to q1
#q1 -> reads input, expects variable(goes to q3), negation(goes to q2) or open brakcet(pushes ( onto stack, goes to q4)
#q2 -> reads input, expects variable or open bracket or negation (stays in q2)
#q3 -> reads input, expects operator(goes to q5) or closing bracket(pops ( from stackgoes to q6), or can go to q7, popping $ from stack
#q4 -> reads input, expects variable(goes to q3) pr open brakcet (pushes ( onto stack, goes to q4)
#q5 -> state where the operator has been read, goes back to q1 again
#q6 -> reads input, expects operator(goes to q5) or closing bracket(pops ( from stackgoes to q6) or can go to q7, popping $ from stack
#q7 -> final state, accepts if stack is empty (only $ remains)

#puts the automata into a class, this helps with our stack
#pushdown also because of bracket matching
class LogicalPDA:

    def __init__(self):
        #stack starts with bottom marker $
        self.stack = ['$']
        self.state = 'q0'

    def tokenize(self, expr):
        #turns input into valid tokens
        pattern = r'\s*(<->|->|~|\^|v|\(|\)|p|q)\s*'

        tokens = []
        pos = 0

        while pos < len(expr):
            match = re.match(pattern, expr[pos:]) #looks a match for each token

            #invalid tokens returns 
            if not match:
                return None

            token = match.group(1)
            tokens.append(token)

            #move to next part
            pos += match.end()

        return tokens

    def show_stack(self):
        #display stack
        print("Stack: [", ', '.join(self.stack), "]")

    def show_state(self):
        #display current state
        print("Current State:", self.state)

    def change_state(self, new_state):
        #visualize state transition
        print(f"Transition: {self.state} -> {new_state}")
        self.state = new_state


    def validate(self, expr):
        #get expression and turn into takens
        tokens = self.tokenize(expr)

        #invalid strings
        if tokens is None:
            print("\nInvalid symbols found.")
            return False

        if len(tokens) == 0:
            print("\nEmpty expression.")
            return False

        print("\nTokens:", tokens)

        #q0 -> q1
        print("\nInitial State:")
        self.show_state()
        print("Bottom marker '$' already on stack")
        self.change_state('q1')

        #True = waiting for value
        #False = waiting for operator
        expecting_value = True

        for token in tokens:

            print(f"\nRead: {token}")
            self.show_state()

            # expecting variable / negation / (
            if expecting_value:

                #variable
                if token in ['p', 'q']:

                    #q1/q2/q4 -> q3
                    if self.state in ['q1', 'q2', 'q4']:
                        self.change_state('q3')

                    print("Valid input, proceed read")
                    expecting_value = False

                #negation
                elif token == '~':

                    #q1 -> q2 or q2 stays q2
                    if self.state == 'q1':
                        self.change_state('q2')
                    elif self.state == 'q2':
                        self.change_state('q2')

                    print("Valid input, proceed read")
                    # still waiting for value

                #opening bracket
                elif token == '(':

                    #q1/q2/q4 -> q4
                    if self.state in ['q1', 'q2', 'q4']:
                        self.change_state('q4')

                    print("Push '(' onto stack")
                    self.stack.append('(')

                else:
                    # invalid token,
                    print("Syntax error: expected variable, negation or bracket but got", token)
                    return False

            #expecting operator or close bracket
            else:

                #binary operators
                if token in ['^', 'v', '->', '<->']:

                    #q3/q6 -> q5 -> q1
                    if self.state in ['q3', 'q6']:
                        self.change_state('q5')

                    print("Valid input, proceed read")
                    expecting_value = True

                    #q5 automatically returns to q1
                    time.sleep(0.5)
                    self.change_state('q1')

                # losing bracket
                elif token == ')':

                    #if only $ remains, this means no matching ( was pushed earlier
                    if self.stack[-1] == '$':
                        print("Syntax error: unmatched ')'")
                        return False

                    #q3/q6 -> q6
                    if self.state in ['q3', 'q6']:
                        self.change_state('q6')

                    print("Pop '(' from stack")
                    self.stack.pop()

                else:
                    print("Syntax error: expected operator or closing bracket but got", token)
                    return False

            self.show_stack()
            print()

            # pause for visualization
            time.sleep(0.8)

        # cannot end expecting a value
        if expecting_value:
            print("Verdict: Expression ended too early.")
            return False

        # q1 can end to q7
        if self.state in ['q3', 'q6'] and len(self.stack) == 1:
            print("Current state:", self.state)
            self.change_state('q7')

        # stack should only have $
        if len(self.stack) > 1:
            print("Verdict: Unclosed parenthesis found.")
            self.show_stack()
            return False

        # on empty (no more tokens), pop $
        print("Pop '$' from stack")
        self.stack.pop()

        self.show_stack()
        self.show_state()

        print("\nExpression accepted.")
        return True


def main():

    while True:
        print("\n=== Logical Expression Validator (PDA) ===")
        print("-"*40)
        print("\nAllowed:")
        print("Variables: p, q")
        print("Operators: ~ ^ v -> <->")
        print("Parentheses: ( )")

        print("\nExamples:")
        print("p ^ q")
        print("(p v q) -> p")
        print("~(p <-> q)")
        print("-"*40)
        expr = input("\nEnter expression: ")

        validator = LogicalPDA()
        valid = validator.validate(expr)
        time.sleep(1) #pause before showing result
        if valid:
            print("\nThe expression " + expr + " is a logical expression.")
        else:
            print("\nThe expression " + expr + " is not a logical expression.")

        again = input("\nValidate another expression? (enter Y): ").lower()

        if again != "y":
            print("PDA terminated")
            break


if __name__ == "__main__":
    main()