"""

Sorry for messy code...
This was just made as a project in my free time for fun, so my objective was just to get it working.

Will be adding as many mathimatical operators/functions as possible

"""

import copy
import collections
import math

_division_by_0_error = f"(# / 0) is not definable"
class Precision:
    limit = 100
    square_root = 100
    sin = 10
    division = 100
    

def __remove_following_0(value : str) -> str:
    if not "." in value:
        value = f"{value}."

    integer, decimal = value.split(".")[0], value.split(".")[-1]
    if len(integer) == 0:
        return "0" + value

    for i in range(1, len(integer) + 1):
        int_slice = integer[0:len(integer) - i]
        if int_slice == len(int_slice) * "0":
            return f"{integer[len(integer) - i:len(integer)]}.{decimal}"

def __remove_trailing_0(value : str) -> str:
    if not "." in value:
        return value

    integer, decimal = value.split(".")[0], value.split(".")[-1]

    for i in range(0, len(decimal)):
        dec_slice = decimal[i:-1]
        if dec_slice == len(dec_slice) * "0":
            return f"{integer}.{decimal[0:i]}"

def __guess(value1 : str, value2 : str) -> list:
    # out {operation} value2 
    # #d = definite
    #v 28 * 8 <= 259
    branches = {
        "5" : {"<" : "9", "=" : "5d", ">" : "1"},
        "1" : {"<" : "3", "=" : "1d", ">" : "0d"},
        "9" : {"<" : "9d", "=" : "9d", ">" : "7"},
        # lower branch
        "3" : {"<" : "4", "=" : "3d", ">" : "2"},
        "4" : {"<" : "4d", "=" : "4d", ">" : "3d"},
        "2" : {"<" : "2d", "=" : "2d", ">" : "1d"},
        # higher branch
        "7" : {"<" : "8", "=" : "7d", ">" : "6"},
        "6" : {"<" : "6d", "=" : "6d", ">" : "5d"},
        "8" : {"<" : "8d", "=" : "8d", ">" : "7d"}
    }
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    carry_over = "0"
    i = 0
    while True:
        i += 1
        if i == 1:
            carry_over = "5"

        if "d" in carry_over:
            carry_over = carry_over.replace("d", "")
            return carry_over, multiplication(f"{value1}{carry_over}", carry_over).replace(".", "")

        out = multiplication(f"{value1}{carry_over}", carry_over).replace(".", "")
        if int(out) < int(value2):
            carry_over = branches[carry_over]["<"]
        elif int(out) == int(value2):
            carry_over = branches[carry_over]["="]
        else:
            carry_over = branches[carry_over][">"]

def __guess_square(value : str) -> list:
    branches = [81, 64, 49, 36, 25, 16, 9, 4, 1]
    for x in range(0, 9):
        if branches[x] <= int(value):
            return str(9 - x), str(branches[x])
    return "0", "0"
        
def addition(value1 : str, value2 : str) -> str:
    """
    Adds 2 numbers together

    Parameters
    ----------
    value1 : str, required
        Number to add

    value2 : str, required
        Second number being added
    """
    # value_1 is the largest integer in terms of length or if = (>=).
    final_value = ""

    val1_sign = "-" if "-" in value1 else ""
    val2_sign = "-" if "-" in value2 else ""
    sign = ""

    if val1_sign == "-" and val2_sign == "-":
        sign = "-"
    elif val1_sign == "-" and val2_sign == "":
        return subtraction(value2, value1.replace("-",""))
    elif val1_sign == "" and val2_sign == "-":
        return subtraction(value1, value2.replace("-",""))

    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value1_int, value1_dec = value1.split(".")[0], value1.split(".")[-1]
    value2_int, value2_dec = value2.split(".")[0], value2.split(".")[-1]

    if len(value1_dec) < len(value2_dec):
        value1_dec = value1_dec + "0" * (len(value2_dec) - len(value1_dec))
    elif len(value2_dec) < len(value1_dec):
        value2_dec = value2_dec + "0" * (len(value1_dec) - len(value2_dec))

    if len(value1_int) < len(value2_int):
        value1_int = "0" * (len(value2_int) - len(value1_int)) + value1_int
    elif len(value2_int) < len(value1_int):
        value2_int = "0" * (len(value1_int) - len(value2_int)) + value2_int

    value1 = f"{value1_int}.{value1_dec}"
    value2 = f"{value2_int}.{value2_dec}"
    reg1, reg2, reg3, reg4 = 0,0,0,0

    # addition
    for x in range(1, len(value1) + 1):
        if value1[len(value1) - x] == ".":
            final_value = f".{final_value}"
            continue

        reg1 = int(value1[len(value1) - x])
        reg2 = int(value2[len(value2) - x])

        reg4 = reg1 + reg2 + reg3
        reg3 = 0
        # carry over
        if reg4 >= 10:
            reg3 = 1
            reg4 -= 10

        final_value = f"{reg4}{final_value}"
    if reg3 > 0:
        final_value = f"{reg3}{final_value}"

    if final_value[len(final_value) - 1] == ".":
        final_value = final_value.removesuffix(".")
    return f"{sign}{final_value}"

def subtraction(value1 : str, value2 : str) -> str:
    """
    Subtracts 2 number

    Parameters
    ----------
    value1 : str, required
        Base number

    value2 : str, required
        Number being subtracted
    """
    # value_1 is the largest integer in terms of length or if = (>=).
    final_value = ""

    val1_sign = "-" if "-" in value1 else ""
    val2_sign = "-" if "-" in value2 else ""

    if val1_sign == "-" and val2_sign == "":
        return "-"+addition(value1.replace("-",""), value2)
    elif val1_sign == "" and val2_sign == "-":
        return addition(value1, value2.replace("-",""))
        
    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value1_int, value1_dec = value1.split(".")[0], value1.split(".")[-1]
    value2_int, value2_dec = value2.split(".")[0], value2.split(".")[-1]

    if len(value1_dec) < len(value2_dec):
        value1_dec = value1_dec + "0" * (len(value2_dec) - len(value1_dec))
    elif len(value2_dec) < len(value1_dec):
        value2_dec = value2_dec + "0" * (len(value1_dec) - len(value2_dec))

    if len(value1_int) < len(value2_int):
        value1_int = "0" * (len(value2_int) - len(value1_int)) + value1_int
    elif len(value2_int) < len(value1_int):
        value2_int = "0" * (len(value1_int) - len(value2_int)) + value2_int

    value1 = f"{value1_int}.{value1_dec}"
    value2 = f"{value2_int}.{value2_dec}"

    sign = ""
    if int(value2.replace(".","")) > int(value1.replace(".","")):
        value1, value2 = value2, value1
        sign = "-"

    reg1, reg2, reg3, reg4 = 0,0,0,0

    # subtract
    for x in range(1, len(value1 if len(value1) > len(value2) else value2) + 1):
        if value1[len(value1) - x] == ".":
            final_value = f".{final_value}"
            continue

        reg1 = int(value1[len(value1) - x]) + reg3
        reg2 = int(value2[len(value2) - x])
        reg3 = 0

        # carry over
        if reg1 < reg2:
            reg1 += 10
            reg3 = -1
        reg4 = reg1 - reg2

        final_value = f"{reg4}{final_value}"

    if final_value[len(final_value) - 1] == ".":
        final_value = final_value.removesuffix(".")

    return f"{sign}{final_value}"

def multiplication(value1 : str, value2 : str) -> str:
    """
    Multiplies 2 numbers together

    Parameters
    ----------
    value1 : str, required
        Number to multiply

    value2 : str, required
        Second number being multiplied
    """
    final_value = "0"

    sign = "-"
    if ("-" in value1) == ("-" in value2):
        sign = ""
    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    value_dec_places = len(value1.split(".")[-1]) + len(value2.split(".")[-1])    
    
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    value1 = __remove_following_0(value1).replace(".","")
    value2 = __remove_following_0(value2).replace(".","")

    reg1, reg2, reg3, reg4 = 0,0,0,0 

    # multiply
    for x in range(1, len(value1) + 1):
        reg1 = int(value1[len(value1) - x])
        if reg1 == 0:
            continue

        for i in range(1, len(value2) + 1):
            reg2 = int(value2[len(value2) - i])

            if reg2 == 0:
                continue

            reg4 = (reg1 * reg2) + reg3
            reg3 = 0

            if reg4 >= 10 and i != len(value2):
                reg3 = int(str(reg4)[0])
                reg4 = str(reg4)[-1]
    
            final_value = addition(final_value, str(reg4) + ("0" * (x - 1 + (i - 1))))
    if reg3 > 0:
        final_value = f"{reg3}{final_value}"

    if len(final_value) >= value_dec_places:
        final_value = sign + final_value[:len(final_value) - value_dec_places] + "." + final_value[len(final_value) - value_dec_places:]
    else:
        final_value = sign + "0." + "0" * (value_dec_places - len(final_value)) + final_value
    return final_value

def division(value1 : str, value2 : str, precision : int = None) -> str:
    """
    Divides 2 numbers

    Parameters
    ----------
    value1 : str, required
        The numerator for the quotient.

    value2 : str, required
        The denominator for the quotient.

    precision : int, optional
        Number of decimal places of precision
    """
    if precision == None: precision = Precision().division if Precision().division > len(value2) + 10 else len(value2) + 10

    final_value = ""

    sign = "-"
    if ("-" in value1) == ("-" in value2):
        sign = ""

    value1, value2 = value1.replace("-", ""), value2.replace("-", "")

    if not "." in value1: value1 = f"{value1}."
    if not "." in value2: value2 = f"{value2}."

    dec_pos = len(value1.split(".")[0]) + len(value2.split(".")[-1])
    
    value1, value2 = value1.replace(".",""), value2.replace(".","")

    reg1, reg2, reg3 = "0",0,"0"

    i = -1
    l = 0
    while True:
        i += 1

        if i == dec_pos:
            final_value = f"{final_value}."
        if i >= len(value1):
            if int(reg2) != 0 or int(reg3) != 0:
                l += 1
                value1 = f"{value1}0"
            else:
                break

        reg1 = value1[i - reg2:i + 1]
        if reg3 != "0":
            reg1 = f"{reg3}{reg1}"

        if int(reg1[0:4300]) < int(value2):
            reg2 += 1
            final_value = f"{final_value}0"
            continue

        multiplace = "0"
        revolutions = 0
        # find amount of times this occures
        while True:
            _ = addition(multiplace, value2)
            if int(_) > int(reg1): break

            multiplace = _
            if multiplace == value2 and revolutions > 10:
                return _division_by_0_error
            revolutions += 1
        reg2 = 0
        reg3 = subtraction(reg1, multiplace)

        final_value = f"{final_value}{revolutions}"

        if l >= precision:
            break

    if len(final_value) < dec_pos:
        final_value = final_value + "0" * (dec_pos - len(final_value))
    return sign + __remove_following_0(final_value)

def exponent(value : str, exp : str) -> str:
    """
    Calculates value ^ exp
    Cannot have decimal exponents yet!!
    
    Parameters
    ----------
    value : str, required
        Base value that will be multiplied.

    exp : str, required
        number of times that will be multiplied
    """
    final_value = "1"

    if len(value.split(".")[-1]) == 0:
        value = value.split(".")[0]
    sign = ""
    if "-" in exp: sign = "-"

    val = int(_round(exp, 1).split(".")[0].replace("-",""))
    if (value.split(".")[0] == "1" + "0"*(len(value.split(".")[0])-1)) and (not "." in value or (value.split(".")[-1] == "0" * len(value.split(".")[-1]))):
        for x in range(0, int(multiplication(str(val), str(len(value.split('.')[0][1:]))).split(".")[0])):
            final_value = f"{final_value}0"
    else:
        for x in range(0, val):
            final_value = multiplication(final_value, value)
    
    if sign == "-": final_value = division("1", final_value)
    return final_value

def factorial(value : str) -> str:
    """
    Calculates the factorial of a number.
    Decimals and negative numbers not currently calculable.

    Parameters
    ----------
    value : str, required
        Number that will be calculated
    """
    final_value = "1"

    value = value.split(".")[0]

    for x in range(1, int(value) + 1):
        final_value = multiplication(final_value, str(x))
    return final_value

def sin(value : str, precision : int = None) -> str:
    """
    Calculates the sin() of a value
    Integer values between 0-2pi are recommended. Anything larger will reqiure precision to be higher than 10.
    
    Parameters
    ----------
    value : str, required
        Number that will be calculated

    precision : int, optional
        How precise the output value will be.
        (Recommended > 5)
    """
    if precision == None: precision = Precision().sin

    final_value = value
    # format:
    # x - x^3/3! + x^5/5! - x^7/7! + x^9/9!...
    value = value.replace("-", "")

    if not "." in value: value = f"{value}."

    num, denom = "",""

    for i in range(1, precision + 1):
        num = exponent(value, str(2*i + 1))
        denom = factorial(str(2*i + 1))

        if i % 2 == 1:
            final_value = subtraction(final_value, division(num, denom, precision))
        else:
            final_value = addition(final_value, division(num, denom, precision))
    return final_value

def square_root(value : str, precision : int = None) -> str:
    """
    Calculates the square root of a value.

    Parameters
    ----------
    value : str, required
        Number that will be square rooted.

    precision : int, optional
        Number of decimal places of precision.
    """
    if precision == None: precision = Precision().square_root

    final_value = ""
    val_sign = "-" if "-" in value else ""

    value = value.replace("-", "")

    if not "." in value: value = f"{value}."

    dec_pos = len(value.split(".")[0])

    value = value.replace(".","")

    reg1, reg2, reg3, reg4, reg5 = "0","0","0","0","0"

    i = -1
    l = 0
    # if odd then == 1
    offset = int(dec_pos % 2 == 1)
    while True:
        i += 1
        if l > precision or (int(reg3) == 0 and 2*i >= len(value)):
            break

        if 2*i >= len(value):
            l += 1
            value = f"{value}00"
        
        if 2*i == dec_pos + offset:
            final_value = f"{final_value}."

        # if i == 0 and offset then offset - 1
        reg1 = value[2*i - (offset if i > 0 else 0):2*i + 2 - offset]

        if i == 0:
            reg4, reg5 = __guess_square(reg1)

            reg2 = multiplication(reg4, "2").replace(".", "")
            reg3 = subtraction(reg1, reg5)
        else:
            reg4, reg5 = __guess(reg2, f"{reg3}{reg1}")

            reg2 = addition(reg2 + reg4, reg4)
            reg3 = subtraction(f"{reg3}{reg1}", reg5)
        
        final_value = f"{final_value}{reg4}"

    return final_value + ("i" if val_sign == "-" else "")

def _round(value : str, decimals : int = 0) -> str:
    """
    Rounds the number with the given number of decimal places.

    Parameters
    ----------
    value : str, required
        Value that will be rounded
        Ex: "23.5312"
    
    decimals : int, optional
        Number of decimal places the value will be rounded to.
        Ex: 2
        Out: "23.53"
    """
    value_dec = value.split(".")[-1]
    value_int = value.split(".")[0]
    if len(value_dec) < decimals + 1:
        value_dec = value_dec + "0" * (decimals - len(value_dec) + 1)
        value = value.split(".")[0] + "." + value_dec
    if int(value_dec[decimals]) >= 5:
        value = value[:len(value_int) + decimals + 1]
        func = None
        if value_int[0] == "-":
            func = subtraction
        else:
            func = addition
        value = func(value, "0." + "0"*(decimals - 1) + "1")
    else:
        value = value[:len(value_int) + decimals + 1]

    return value

def __calc_lim(parsed_equation : dict, x_goes_towards : str, side, precision : int = None) -> str:
    """
    Calculates limit of equation with value of X

    Parameters
    ----------
    parsed_equation : dict, required
        Parsed equation

    x_goes_towards : str, required
        Value X is reaching

    side : function, required
        Used as either addition/subtraction

    precision : int, optional
        How close the number calculated will be to X
    """
    if precision == None: precision = Precision().limit

    x_goes_towards = x_goes_towards[:-1] if (x_goes_towards[-1] == "+" or x_goes_towards[-1] == "-") else x_goes_towards
    lim = __calculate(copy.deepcopy(parsed_equation), side(x_goes_towards, "0."+"0"*precision+"1"))
    lim_mprecise = __calculate(copy.deepcopy(parsed_equation), side(x_goes_towards, "0."+"0"*(precision + 5)+"1"))

    lim_out = __remove_trailing_0(_round(lim, round(precision / 2) if (round(precision / 2) <= len(lim.split(".")[-1]) -1) else len(lim.split(".")[-1]) -1))
    lim_out_mprecise = __remove_trailing_0(_round(lim_mprecise, round(precision / 2) if (round(precision / 2) <= len(lim_mprecise.split(".")[-1]) -1) else len(lim_mprecise.split(".")[-1]) -1))
    if len(lim_out_mprecise) > len(lim_out):
        if lim_out[0] == "-": return "-∞"
        else: return "∞"
    else:
        # remove "-0."
        if lim_out[0] == "-" and lim_out.split(".")[0][1:] == "0" and len(lim_out.split(".")[-1]) == 0:
            lim_out = "0."
        return lim_out 

def limit(equation, x_goes_towards : str, precision : int = None) -> str:
    """
    Calculates the limit of an equation as x->x_goes_towards with definable precision.
    Cannot calculate x->∞ or x->-∞ yet

    Parameters
    ----------
    equation : str, required
        Equation that will be calculated. Can either be parsed or not.

    x_goes_towards : str = None, optional
        Value that X will be getting closer to.
        Ex: "54"

    precision : int, optional
        How precise the output value will be.
        Also, how many decimal places of precision
    """
    if precision == None: precision = Precision().limit

    if type(equation) == str:
        parsed_equation, lim = __parser(equation)
    else:
        parsed_equation = equation

    try:
        t_x_goes_towards = x_goes_towards[:-1] if (x_goes_towards[-1] == "+" or x_goes_towards[-1] == "-") else x_goes_towards
        out = __calculate(copy.deepcopy(parsed_equation), t_x_goes_towards)
        if out != _division_by_0_error:
            return out
    except: pass # if undefined


    if x_goes_towards[-1] == "+":
        return __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, addition, precision)
    elif x_goes_towards[-1] == "-":
        return __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, subtraction, precision)
    else:
        upper_lim = __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, addition, precision)
        lower_lim = __calc_lim(copy.deepcopy(parsed_equation), x_goes_towards, subtraction, precision)

        if upper_lim == lower_lim:
            return upper_lim
        else:
            return "DNE"

######################################## EQUATION PARSER ########################################

def __parser(expression : str):
    """
    Parses equation.

    Parameters
    ----------
    expression : str, required
        Equation that will be parsed.
    """
    expression = expression.split("\n")
    expression = [i for i in expression if i]
    lim_req = expression[-1]
    expression = expression[0]

    parsed = {}
    parentheses_queue = []
    expression = expression.replace(" ","")
    lim_req = lim_req.replace(" ","").replace("\t", "")
    lim_req = lim_req.lower().split("x->")[1:]
    current_lim = None
    just_started = False
    lim_x_vals = {}

    operators = ["+", "-", "*", "/", "^", "!"]
    functions = ["sqrt(", "sin(", "lim("]

    parentheses = 0

    read_queue = ""
    x = 0
    for char in expression:
        x += 1
        read_queue += char

        # '1': ['sqrt', dict-2], '2': ['2', '-', 'x']
        if just_started != False:
            if x - just_started >= 2:
                just_started = False
        if char == "(":
            just_started = x
            try:
                old_paren = parentheses_queue[0]
            except: old_paren = parentheses
            parentheses += 1
            parentheses_queue.insert(0, parentheses)
            try:
                if parsed[str(old_paren)][1] != None:
                    parsed[str(old_paren)][-1] = f"dict-{parentheses_queue[0]}"
                else:
                    parsed[str(old_paren)][0] = f"dict-{parentheses_queue[0]}"
            except: pass # no values in dict
            parsed.update({str(parentheses_queue[0]) : [None, None, None]})
            
            if read_queue[0] in operators:
                read_queue = read_queue[1:]
            if read_queue in functions:
                old_paren = parentheses_queue[0]
                parsed[str(parentheses_queue[0])][0] = read_queue[:-1]
                if read_queue != 'lim(':
                    parsed[str(parentheses_queue[0])].pop(-1)
                else:
                    parsed[str(parentheses_queue[0])][1] = lim_req[0]
                    current_lim = parentheses_queue[0]
                    lim_req.pop(0)

                parentheses += 1
                parentheses_queue.insert(0, parentheses)
                parsed.update({str(parentheses_queue[0]) : [None, None, None]})
                if current_lim != None:
                    lim_x_vals.update({str(parentheses_queue[0]) : str(current_lim)})
                parsed[str(old_paren)][-1] = f"dict-{parentheses_queue[0]}"

            read_queue = ""
            if current_lim != None:
                lim_x_vals.update({str(parentheses_queue[0]) : str(current_lim)})
        elif char == ")":
            try:
                right = read_queue.split(parsed.get(str(parentheses_queue[0]))[1])[-1][:-1]
                if parsed.get(str(parentheses_queue[0]))[-1] == None and right != "":
                    parsed[str(parentheses_queue[0])][-1] = right
                
                read_queue = ""
                if not None in parsed[str(parentheses_queue[0])]:
                    parentheses_queue.pop(0)
                if parsed.get(str(parentheses_queue[0]))[0] == "lim":
                    current_lim = None
                    
                if parsed[str(parentheses_queue[0])][0] in functions or (parsed[str(parentheses_queue[0])][0] == None and parsed[str(parentheses_queue[0])][-1] != None):
                    new_parsed = [i for i in parsed[str(parentheses_queue[0])] if i]
                    parsed[str(parentheses_queue[0])] = new_parsed
            except: pass

        if char in operators:
            try:
                if not just_started and parsed[str(parentheses_queue[0])][0] == None:
                    parsed[str(parentheses_queue[0])][0] = read_queue[:-1]
                if not just_started:
                    parsed[str(parentheses_queue[0])][1] = char
            except:pass
        
        for l in parentheses_queue:
            if not None in parsed[str(l)] and current_lim == None:
                parentheses_queue.remove(l)

    return parsed, lim_x_vals

def __calculate(equation : dict, x_val : str = None, lim_x_vals : dict = {}) -> str:
    """
    Parameters
    ----------
    equation : dict, required
        Parsed equation that will be calculated.

    x_val : str = None, optional
        Value that will be substituted in for X.
        Ex: "54"
    """
    operators = {'+' : addition, '-' : subtraction, '*' : multiplication, 
                 '/' : division, '^' : exponent}
    functions = {'sin' : sin, 'lim' : limit, 'sqrt' : square_root, '!' : factorial}
    current_lim_equation = {}
    current_val = []
    solved_vals = {}
    equation = collections.OrderedDict(sorted(equation.items()))
    for x in range(1, len(equation) + 1):
        current_val = list(equation.items())[len(equation) - x]
        current_key = current_val[0]
        current_val = current_val[-1]

        if current_val == None:
            current_val = list(equation.values())[len(equation) - x - 1]

        if lim_x_vals.get(current_key, None) != None:
            if current_lim_equation.get(lim_x_vals.get(current_key), None) == None:
                current_lim_equation.update({lim_x_vals.get(current_key) : {}})
            current_lim_equation[lim_x_vals.get(current_key)].update({current_key : current_val})
            continue

        if "x" in current_val:
            if x_val == None and lim_x_vals.get(current_key, None) == None:
                raise ValueError("'x_val' must be input if variable 'x' is in the equation")
        for i in range(0, len(current_val)):
            if current_val[i] == "x":
                current_val[i] = str(x_val) if (x_val != None and lim_x_vals.get(current_key, None) == None) else lim_x_vals[current_key]
            
            try:
                if 'dict' in current_val[i] and current_val[0] != "lim":
                    current_val[i] = solved_vals.get(current_val[i].replace("dict-", ""))
            except: pass

        final_val = None
        if len(current_val) == 3 and current_val[0] != "lim":
            final_val = operators.get(current_val[1])(current_val[0], current_val[-1])
        elif current_val[0] == 'lim':
            if 'dict' in current_val[-1]:
                current_val[-1] = solved_vals.get(current_val[-1].replace("dict-", ""))
            final_val = limit(current_lim_equation.get(current_key), current_val[1])
        else:
            if 'dict' in current_val[-1]:
                current_val[-1] = solved_vals.get(current_val[-1].replace("dict-", ""))
            func = functions.get(current_val[0], None)
            if func != None:
                final_val = func(current_val[-1])
            else:
                final_val = current_val[0]
        if final_val != None:
            solved_vals.update({f"{current_key}" : final_val})
    t = collections.OrderedDict(sorted(solved_vals.items()))
    t = list(t.items())[0][-1]
    return t

def calculate(equation : str, x_val : str = None) -> str:
    """
    This function is for calculation based off known values. This will not solve for variables.

    Parameters
    ----------
    equation : dict, required
        Parsed equation that will be calculated.

    x_val : str = None, optional
        Value that will be substituted in for X.
        Ex: "54"
    """
    parsed_equation, lim_x_vals = __parser(equation)
    return __calculate(parsed_equation, x_val, lim_x_vals)  
