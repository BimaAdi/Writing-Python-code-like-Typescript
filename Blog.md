# Writing Python code like Typescript

I assume you guys who want to read this article know what typescript is. Javascript developer created typescript to make javascript more typesafe. Typesafe make code more readable and has less bug without writting any test. Can typesafety be achieve in python?.

## Why we need typesafety?
Imagine this innocent looking function
```python
def send_email(sender, receiver, message):
    ...
```
I intentionally hide it's code implementation. Can you guess what is function for and what parameter that we need in order to use this function by just it's function name and parameter?. We know from it's function name it's function for sending an email. What about it's parameter, what should we put in order to use this function?. 


First guess sender is str of email, receiver is str of email, message is str of body of an email. 
```python
send_email(sender="john@mail.com", receiver="doe@mail.com", message="Hello doe! How are you?")
```
Most simple guess. but it's not the only guess.


Second guess sender is int of user_id on db, receiver is int of user_id on db, message is str of body of an email. 
```python
john_user_id = 1
doe_user_id = 2
send_email(sender=1, receiver=2, message="Hello doe! How are you?")
```
Imagine working on aplication. Most aplication use some database. User usualy represent by it's id.


Third guess sender is dictionary, receiver is dictionary, message is dictionary.
```python
john = {
    "id": 1,
    "username": "john",
    "email": "john@mail.com"
}
doe = {
    "id": 2,
    "username": "doe",
    "email": "doe@mail.com"
}
message = {
    "title": "Greeting my friend doe",
    "body": "Hello doe! How are you?"
}
send_email(sender=john, receiver=doe, message=message)
```
Maybe send_email need more than email and user id. To add more data on each parameter it's used some dictionary structure. You notice that message it's not just str maybe it's need title and body.


Forth guess sender is class User, receiver is class User, message is dictionary.
```python
class User():

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

john = User(id=1, username="john", email="john@mail.com")
doe = User(id=2, username="doe", email="doe@mail.com")
message = {
    "title": "Greeting my friend doe",
    "body": "Hello doe! How are you?"
}
send_email(sender=john, receiver=doe, message=message)
```
Maybe send_email integrate with some database orm like Django ORM or Sqlalchemy. In order to make it easier for end user, it's used ORM class directly.


So which one is the correct answer? one of them can be a correct answer. Maybe the correct answer can be combination of two guess. Like sender and receiver is class User (Forth guess) but message it's str (First guess). We cannot sure unless we read it's code implementation. Which is waste of time if you an end user. As an end user who use this function we just need what function do, what parameter that it's need and what function output is.

## The Solution
### Docstring
Python has built in fuction documentation using docstring. Here docstring example.
```python
def add(x, y):
    """Add two number

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    """
    return x + y

def send_email(sender, receiver, message):
    """Send email from sender to receiver

    Parameter:\n
    sender -- email sender, class User\n
    receiver -- email receiver, class User\n
    message -- body of the email, dictionary (ex: {"title": "some title", "body": "email body"}\n

    Return: None
    """
    ...
```
What's cool about docstring it's editor compatible. In vscode it will shown docstring when you hover over a function. Most library in python use docstring to document it's function.


The problem with docstring is document syncronization. How you make sure that the docstring always sync with code implementation. You cannot put it on test right. I hear that from random person on the internet "Having outdated documentation is worse than having no documentation".


### Doctest
Btw You can test docstring using doctest kinda. Doctest testing your docstring by running example on your docstring. Doctest is already preinstalled in python so you don't need external depedencies. let's see this example create new file called my_math.py then put this code.
```python
def add(x, y):
    """Add two integer

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    >>> add(1, 2)
    3
    """
    return x + y


if __name__ == "__main__":
    import doctest

    doctest.testmod()

```
It's same code like docstring example but I add example and doctest at last line of the code. In order to test the docstring just run the file `python my_math.py`. If theres no output it's mean your example pass the test. If you want see the output run it in verbose mode `python my_math.py -v`, you'll see this output.
```bash
Trying:
    add(1, 2)
Expecting:
    3
ok
1 items had no tests:
    __main__
1 items passed all tests:
   1 tests in __main__.add
1 tests in 2 items.
1 passed and 0 failed.
Test passed
```
If you make mistake on code example it will return an error. 
```python
def add(x, y):
    """Add two integer

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    >>> add(2, 2) # <-- I change it here
    3
    """
    return x + y


if __name__ == "__main__":
    import doctest

    doctest.testmod()

```
the output:
```bash
**********************************************************************
File "~/typescript-in-python/my_math.py", line 12, in __main__.add
Failed example:
    add(2, 2) # <-- I change it here
Expected:
    3
Got:
    4
**********************************************************************
1 items had failures:
   1 of   1 in __main__.add
***Test Failed*** 1 failures.
```
Great! now I can test my docstring. But the caveats are:
1. **doctest only check the example** it doesn't check comment function parameter and return
2. **doctest need to run the code** like other testing tools in order to check it is correct or not doctest need to run the code example. If your code need some external tools like database or smtp server (like sending an email) it's hard to test using doctest.

### Python typing
Sometimes you don't need to run the code to check is code correct or not. You just need input type and output type. How? Consider this example.
```python
def add(x, y):
    """Add two integer

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    """
    return x + y

def sub(x, y):
    """Substract two integer

    Parameter:\n
    x -- int\n
    y -- int\n

    Return: int
    """
    return x - y

a = add(2, 1)
b = add(1, 1)
c = sub(a, b)
```
function add return an int and function sub need two int as input paramter. If I use two return from add function then put it on sub paramater like example above will it error? of course not because sub function need int and you put an int as well.


Since python 3.5 python have built in type called [typing](https://docs.python.org/3/library/typing.html). With typing you can add type on your function like example below.
```python
def add(x: int, y: int) -> int:
    """Add two integer"""
    return x + y

a = add(1, 2)
```
Instead put it on your docstring you put it on the function. Typing is supported on many editor. If you use vscode you can hover on variable and it will shown it's type.
![vscode show python typing](./img/vscode%20show%20python%20typing.png)


Nice now our code will have a type safety. eeehhhh not realy. If I intentionally use function incorrectlly like this.
```python
def add(x: int, y: int) -> int:
    """Add two integer"""
    return x + y

res = add(1, [])
print(res)
```
It will show error
```bash
Traceback (most recent call last):
  File "~/typescript-in-python/main.py", line 5, in <module>
    res = add(1, [])
          ^^^^^^^^^^
  File "~/typescript-in-python/main.py", line 3, in add
    return x + y
           ~~^~~
TypeError: unsupported operand type(s) for +: 'int' and 'list'
```
But it doesn't show that you put incorrect type. Even worse if you use it like this.
```python
def add(x: int, y: int) -> int:
    """Add two integer"""
    return x + y

res = add("hello", "world")
print(res)
```
It will succeed. It must be error because you put incorrect type.
```bash
helloworld
```
Why python typing doesn't have type checker by default??. Based on [pep-3107](https://peps.python.org/pep-3107/#fundamentals-of-function-annotations) it said
> Before launching into a discussion of the precise ins and outs of Python 3.0’s function annotations, let’s first talk broadly about what annotations are and are not:
>
> 1. Function annotations, both for parameters and return values, are completely optional.
> 2. Function annotations are nothing more than a way of associating arbitrary Python expressions with various parts of a function at compile-time.
> By itself, Python does not attach any particular meaning or significance to annotations. Left to its own, Python simply makes these expressions available as described in Accessing Function Annotations below.
>
> The only way that annotations take on meaning is when they are interpreted by third-party libraries. ...

So in python typing is like a decorator in typescript or java it doesn't mean anything. You need third party libraries todo type checking. Let's see some library for typechecking.

### Python typing + type checker
Here are libraries for typechecking in python. For example we will typecheck this wrong.py file
```python
def add(x: int, y: int) -> int:
    """Add two integer"""
    return x + y

res = add("hello", "world")
print(res)
```
1. [mypy](https://mypy.readthedocs.io/)
The "OG" of python type checker. To install it just using pip `pip install mypy`. Now let's use mypy to typecheck this file. Run `mypy wrong.py`. It will shown type error which is nice.
```bash
wrong.py:5: error: Argument 1 to "add" has incompatible type "str"; expected "int"  [arg-type]
wrong.py:5: error: Argument 2 to "add" has incompatible type "str"; expected "int"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```
btw you can run mypy on entire project by using `mypy .`.

2. [pyright](https://microsoft.github.io/pyright/)
Another typechecker is pyright. It created by microsoft. It's same like mypy install through pip `pip install pyright`. Then run it `pyright wrong.py`. It will shown this error.
```bash
~/typescript-in-python/wrong.py
  ~/typescript-in-python/wrong.py:5:11 - error: Argument of type "Literal['hello']" cannot be assigned to parameter "x" of type "int" in function "add"
    "Literal['hello']" is incompatible with "int" (reportArgumentType)
  ~/typescript-in-python/wrong.py:5:20 - error: Argument of type "Literal['world']" cannot be assigned to parameter "y" of type "int" in function "add"
    "Literal['world']" is incompatible with "int" (reportArgumentType)
2 errors, 0 warnings, 0 informations
```
It said that it's more faster than mypy but I found that's not much diffrent. Maybe my code base it's to small. Also pyright implement more python standard than mypy you can see on [https://microsoft.github.io/pyright/#/mypy-comparison](https://microsoft.github.io/pyright/#/mypy-comparison). Personaly I prefer mypy than pyright because the error message were more readable.

3. [pylyzer](https://github.com/mtshiba/pylyzer)
Speaking of performance and speed another new python typechecker pylyzer. It's written in rust. You can install it through pip `pip install pylyzer` or through cargo (rust package manager) `cargo install pylyzer --locked`. Then run it `pylyzer wrong.py`. It will shown this error.
```bash
Start checking: wrong.py
Found 2 errors: wrong.py
Error[#2258]: File wrong.py, line 5, <module>.res

5 | res = add("hello", "world")
  :           -------
  :                 |- expected: Int
  :                 `- but found: {"hello"}

TypeError: the type of add::x (the 1st argument) is mismatched

Error[#2258]: File wrong.py, line 5, <module>.res

5 | res = add("hello", "world")
  :                    -------
  :                          |- expected: Int
  :                          `- but found: {"world"}

TypeError: the type of add::y (the 2nd argument) is mismatched
```
So far this is the most readable and beautiful error message. It's reminds me of rust compiler error. Speed, performance and most readable error message, I think I will choose to using pylyzer if the package already stable. The problem is at the time I write this blog, pylyzer still in beta. It can only typecheck your code base, it haven't support external depedencies.

## Conclusion
Alright we successfully write python code like typescript (kinda). There is more way to using python typing module other than check simple type (str, int, bool etc). Maybe I will cover more advance type it in next blog. Maybe you guys have opinion about this, know better typechecker other then those 3, found other way to do typecheck in python or other. let me know on comment section below. As always Happy Coding.
