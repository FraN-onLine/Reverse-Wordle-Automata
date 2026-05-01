import re
import time #short pauses for visualization

#puts the automata into a class, this helps with our stack
#pushdown also because of bracket matching
class LogicalPDA:

    def __init__(self):
        #stack starts with bottom marker $
        self.stack = ['$']

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

    def validate(self, expr):
        #get expression and turn into takens
        tokens = self.tokenize(expr)

        if tokens is None:
            print("\nInvalid symbols found.")
            return False

        if len(tokens) == 0:
            print("\nEmpty expression.")
            return False

        print("\nTokens:", tokens)

        # True = waiting for value
        # False = waiting for operator
        expecting_value = True

        print("\nProcessing...\n")

        for token in tokens:

            print(f"Read: {token}")

            # expecting variable / negation / (
            if expecting_value:

                # variable
                if token in ['p', 'q']:
                    print("Valid variable")
                    expecting_value = False

                # negation
                elif token == '~':
                    print("Negation")
                    # still waiting for value

                # opening bracket
                elif token == '(':
                    print("Push '(' onto stack")
                    self.stack.append('(')

                else:
                    print("Syntax error: expected variable")
                    return False

            # expecting operator / )
            else:

                # binary operators
                if token in ['^', 'v', '->', '<->']:
                    print("Valid operator")
                    expecting_value = True

                # closing bracket
                elif token == ')':

                    # if only $ remains, no matching (
                    if self.stack[-1] == '$':
                        print("Syntax error: unmatched ')'")
                        return False

                    print("Pop '(' from stack")
                    self.stack.pop()

                else:
                    print("Syntax error: expected operator")
                    return False

            self.show_stack()
            print()

            # pause for visualization
            time.sleep(0.7)

        print("\nFinal checking...")

        # cannot end expecting a value
        if expecting_value:
            print("Expression ended too early.")
            return False

        # stack should only have $
        if len(self.stack) > 1:
            print("Unclosed parenthesis found.")
            self.show_stack()
            return False

        # pop $
        print("Pop '$' (bottom marker)")
        self.stack.pop()

        self.show_stack()

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

        if valid:
            print("\nVALID")
        else:
            print("\nINVALID")

        again = input("\nTry again? (yes/no): ").lower()

        if again != "yes":
            print("Goodbye.")
            break


if __name__ == "__main__":
    main()