---
This is a super calculator that is designed to do calculations with numbers from very large numbers, or very small decimals.

---

# Functions
## Addition
*Adds 2 numbers together*

`def addition(value1 : str, value2 : str) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.addition("-1", "5")
print(equals)

Out:    "4"
```

---
## Subtraction
*Subtracts 2 numbers*

`def subtraction(value1 : str, value2 : str) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.subtraction("10", "17")
print(equals)

Out:    "-7"
```

---
## Multiplication
*Multiplies 2 numbers together*

`def multiplication(value1 : str, value2 : str) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.multiplication("4", "8")
print(equals)

Out:    "32"
```

---
## Division
*Divides 2 numbers*

`def division(value1 : str, value2 : str, precision : int = 100) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.division("6", "3")
print(equals)

Out:    "2"
```

---
## Exponential
*Multiplies a number by itself x times*

`def exponent(value : str, exp : str) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.exponent("4", "2")
print(equals)

Out:    "16"
```

---
## Factorial
*Factorial*

`def factorial(value : str) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.factorial("4")
print(equals)

Out:    "24"
```

---
## Sin
*Outputs sin of number*

`def sin(value : str, precision : int = 10) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.sin("1")
print(equals)

Out:    "0.84147098484930199201"
```

---
## Square root
*Outputs square_root of a number*

`def square_root(value : str, precision : int = 100) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.square_root("16")
print(equals)

Out:    "4"
```

---
## Round
*Rounds a number*

`def round(value : str, decimals : int = 0) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.round("16.5")
print(equals)

Out:    "17"
```
## Limits
*Find what an equation equals as x->value*

`def limit(equation, x_goes_towards : str, precision : int = 100) -> str:...`

**Example**
```
import supercalculator as calc

equals = calc.limit(equation = "(5 / (x ^ 2))", x_goes_towards = "0")
print(equals)

Out:    "infinity"
```

---
# Equation Builder

**DISCLAIMER** *Factorials do __NOT__ work in equation builder yet!!*

`def calculate(equation : str, x_val : str = None) -> str:...`

**x_val** is necessary if x is in the equation and is not defined.
- Limits define x values, **only** in the limit.

## Syntax
*Parentheses __must__ be around any operation.*

**Example**

`x - (4 * x ^2)` would be `(x - (4 *(x^2)))`

---
*X values for limits go on lower line*

**Example**

For `limit(equation = "1/x", x_goes_towards = 0)` it would be:
```
"""
lim(1 / x)
x->0
"""
```
**For multiple limits**
```
"""
(lim(1 / x) / lim(2 ^ x))
x->0.1        x->3
"""
```

---
*Functions such as sqrt(), and sin() act like parentheses*

**Example**
`"sqrt(x - 3)"`

---