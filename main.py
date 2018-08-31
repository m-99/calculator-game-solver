import re

def solver(start, end, max_steps, operations):
    # first find the parents
    stack = [start]
    parents = {}
    depth = {start: 0}
    visited = set([start])

    while stack:
        current = stack.pop()
        if current != end:
            # if depth will exceed limit, continue to next item in stack
            if depth[current] == max_steps:
                continue
            children = press_buttons(current, operations)
            for child in children:
                # if not visited or found more efficient way to reach here
                if child not in visited or depth[child] > depth[current] + 1:
                    visited.add(child)
                    stack.append(child)
                    parents[child] = current
                    depth[child] = depth[current] + 1
                    # end early
                    if child == end:
                        break
        # then construct the path
        else:
            path = []
            while current != start:
                path.insert(0, current)
                current = parents[current]
            return path
    # No solution
    print(parents)
    return None

# operations is a string of all of the buttons seperated by spaces
# returns all of the resulting numbers from pressing all the buttons
def press_buttons(start, operations):
    buttons = operations.split()
    # floats
    results = []
    for button in buttons:
        button.lower()

        # append number
        if button.isdigit():
            results.append(float(str(start) + str(button)))

        # invert sign
        elif button == "+/-" or button == "+-":
            results.append(float(start * -1))

        # addition/subtraction
        elif button[-1].isdigit() and (button.startswith("+") or button.startswith("-")):
            results.append(start + float(button))

        # multiplication
        elif button[-1].isdigit() and (button.startswith("*") or button.startswith("x")):
            results.append(start * float(button[1:]))

        # division
        elif button.startswith("/"):
            n = start / float(button[1:])
            # limit to hundreths
            if len(str(n).split('.')[1]) <= 2:
                results.append(n)

        # backspace
        elif button == "<<" or button == "b":
            n = str(start)[:-1]
            # n = 0 if backspace results in no numbers
            if not n:
                n = 0
            results.append(float(n))

        # swap number, only works on ints
        elif "=>" in button or "to" in button:
            if isinstance(start, int):
                nums = re.split('[^0-9]+', button)
                results.append(float(str(start).replace(str(nums[0]), str(nums[1]))))

        # reverse, only works on ints
        elif button == "r" or button == "reverse":
            start_str = str(start).replace("-", "")
            if start < 0:
                sign = -1
            else:
                sign = 1
            results.append(float(start_str[::-1]) * sign)

        # sum
        elif button == "s" or button == "sum":
            sum = 0
            if start < 0:
                sign = -1
            else:
                sign = 1
            if isinstance(start, int):
                for digit in str(start).replace("-", ""):
                    sum += int(digit)
            results.append(float(sum) * sign)

        # exponents, only works on ints
        elif "^" in button:
            if isinstance(start, int):
                exponent = re.split('[^0-9]+', button)
                results.append(float(start ** int(exponent[1])))

        # shift left, only works on ints
        elif button == "<" or button == "<shift":
            start_str = str(start).replace("-", "")
            if start < 0:
                sign = -1
            else:
                sign = 1
            if isinstance(start, int):
                results.append(float(start_str[1:] + start_str[0]))

        # shift right
        elif button == ">" or button == "shift>":
            start_str = str(start).replace("-", "")
            if start < 0:
                sign = -1
            else:
                sign = 1
            if isinstance(start, int):
                results.append(float(start_str[-1] + start_str[:-1]))

        # mirror, only works on ints
        elif button == "m" or button == "mirror":
            start_str = str(start).replace("-", "")
            if start < 0:
                sign = -1
            else:
                sign = 1
            if isinstance(start, int):
                results.append(float(start_str + start_str[::-1]))

    # cast floats to ints where applicable
    with_ints = []
    for n in results:
        if n.is_integer():
            with_ints.append(int(n))
        else:
            with_ints.append(n)
    # filter out numbers with more than six digits
    filtered = [x for x in with_ints if len(str(x)) <= 6]
    return filtered


if __name__ == '__main__':
    # solver(start, end, max_steps, operations)
    # print(solver(36, 500, 5, "1=>5 x4 /3 r")) # 83
    # print(solver(0, 196, 8, "1 +12 x13 r <<"))

    while True:
        start = int(input("start: "))
        end = int(input("goal: "))
        max_steps = int(input("moves: "))
        operations = input("buttons: ")
        print("path:")
        print(solver(start, end, max_steps, operations))
        print()
