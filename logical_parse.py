import re


class LogicalPDA:
    def __init__(self):
        # stack used for matching parentheses
        self.stack = []

    def tokenize(self, expr):
        """
        Break expression into valid logical tokens.

        Allowed:
        p, q
        ~
        ^
        v
        ->
        <->
        (
        )

        Spaces are ignored.
        """
        # remove all spaces first
        expr = expr.replace(" ", "")

        # match valid tokens only
        pattern = r'(<->|->|~|\^|v|\(|\)|p|q)'

        tokens = re.findall(pattern, expr)

        # make sure the entire expression was tokenized
        # if not, there is an invalid symbol
        if ''.join(tokens) != expr:
            return None

        return tokens

    def show_stack(self):
        """
        Display current stack state
        """
        if not self.stack:
            print("Stack: empty")
        else:
            print("Stack (top → bottom):", list(reversed(self.stack)))

    def validate(self, expr):
        """
        Main PDA validator
        """

        tokens = self.tokenize(expr)

        if tokens is None:
            print("\nInvalid symbols found.")
            return False

        if len(tokens) == 0:
            print("\nEmpty expression.")
            return False

        print("\nTokens:", tokens)

        # tracks what should come next
        # True = expecting variable, ~, or (
        # False = expecting operator or )
        expecting_value = True

        print("\nProcessing...\n")

        for i, token in enumerate(tokens):

            print(f"Read: {token}")

            # if expecting a value
            if expecting_value:

                # variables are valid values
                if token in ['p', 'q']:
                    print("Valid variable")
                    expecting_value = False

                # negation is allowed before a value
                elif token == '~':
                    print("Negation")
                    # still waiting for actual value

                # opening parenthesis
                elif token == '(':
                    print("Push '('")
                    self.stack.append('(')

                else:
                    print("Syntax error: expected variable")
                    return False

            # if expecting operator or closing parenthesis
            else:

                # binary operators
                if token in ['^', 'v', '->', '<->']:
                    print("Valid operator")
                    expecting_value = True

                # closing parenthesis
                elif token == ')':
                    if not self.stack:
                        print("Syntax error: extra ')'")
                        return False

                    print("Pop '('")
                    self.stack.pop()

                else:
                    print("Syntax error: expected operator")
                    return False

            self.show_stack()
            print()

        # final checks
        if expecting_value:
            print("Expression ended too early.")
            return False

        if self.stack:
            print("Unclosed parenthesis found.")
            self.show_stack()
            return False

        print("Expression accepted.")
        return True


def main():
    while True:
        print("\n=== Logical Expression Validator ===")
        print("Allowed:")
        print("Variables: p, q")
        print("Operators: ~ ^ v -> <->")
        print("Parentheses: ( )")
        print("\nExamples:")
        print("p ^ q")
        print("(p v q) -> p")
        print("~(p <-> q)")

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