import random

def roll(ctx, arg):
    string = ""; total =  0
    try:
        for item in arg:

            item = prepareItem(item)

            if item[0] <= 0 or item[0] > 50:
                raise Exception
            
            list = diceResult(item[0], item[1])
            string += f"d{item[1]} " + list[0]
            total += list[1]

            string += f"final Result ==> ({total})"
        return ctx.send(string) 
    except Exception as e:
        print(e)
        return ctx.send("Wrong template, try: ([ 0 < number < 50 ]d[ 0 < number < 50 ])...")

def rollshow(ctx, arg):
    string = "";total = 0
    try:
        for item in arg:
            item = prepareItem(item)

            if item[0] <= 0 or item[0] > 50:
                raise Exception

            list = showDiceResult(item[0], item[1])
            total += list[1]; string += list[0]
     
        string += f"total ==> ({total})"
        return ctx.send(string)
    except Exception as e:
        print(e)
        return ctx.send("Wrong template, try: ([ 0 < number < 50 ]d[ 0 < number < 50 ])...")

def showDiceResult(numeroDeDados, dado):
    String = f'd{dado}:\n'; total = 0; count =1
    
    for _ in range(0, numeroDeDados):
        result = random.randint(1, dado)
        total += result
        String += f"    (dado {count}) -> {result}\n"
        count += 1
    String += f"    total (d{dado}) --> {total}\n"
    list = [String, total]
    return list

def diceResult(numeroDeDados, dado):
    String = ''; count = 1; total = 0
    
    for _ in range(0, numeroDeDados):
        result = random.randint(1, dado)
        total += result
        count += 1
    String += f"total (d{dado}) -> {total}\n"
    list = [String, total]
    return list

def prepareItem(item):
    item = item.split("d")
    
    if item[0] == '':
        item[0] = 1
    else:
        item[0] = int(item[0])
    item[1] = int(item[1])
    return item