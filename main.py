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
                if child not in visited:
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
    return None

# operations is a string of all of the buttons seperated by spaces
# returns all of the resulting numbers from pressing all the buttons
def press_buttons(start, operations):
    buttons = operations.split()
    results = []
    for button in buttons:
        button.lower()
        # append number
        if button.isdigit():
            results.append(float(str(start) + str(button)))
        # addition/subtraction
        if button.startswith("+") or button.startswith("-"):
            results.append(start + float(button))
        # multiplication
        if button.startswith("*") or button.startswith("x"):
            results.append(start * float(button[1:]))
        # division
        if button.startswith("/"):
            n = start / float(button[1:])
            # limit to hundreths
            if len(str(n).split('.')[1]) <= 2:
                results.append(n)
        # backspace
        if button.startswith("<<") or button.startswith("b"):
            n = str(start)[:-1]
            # n = 0 if backspace results in no numbers
            if not n:
                n = 0
            results.append(float(n))
        # swap number
        if "=>" in button:
            nums = button.split("=>")
            results.append(float(str(start).replace(str(nums[0]), str(nums[1]))))
        # reverse
        if button.startswith("r") or button.startswith("reverse"):
            results.append(float(str(start)[::-1]))

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