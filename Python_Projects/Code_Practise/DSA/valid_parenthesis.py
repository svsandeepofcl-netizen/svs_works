expressions = [
    "{[()]}",
    "{[(])}",
    "()",
    "([{}])",
    "((("
]

pairs={
    '}':'{',
    ']':'[',
    ')':'('
}


stack=[]

for ch in expressions:
    # valid= True
    stack.clear()
    print(f"Calculating for {ch}")
    for symbol in ch:
        if symbol in '[({':
            stack.append(symbol)
            print("Stack", stack)
        else:
            new=stack.pop()
            if new!=pairs[symbol]:
                # valid=False
                break
    if stack:
        # valid=False
        print(f'exp {ch} is not valid')
    else:
        print(f'exp {ch} is valid')