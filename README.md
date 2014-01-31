CaKe
====

An interpreter for a minimal but Turing-complete stack based 'concatenative' esolang.

### About

CaKe is an extremely minimal stack-based 'concatenative' language. This tiny interpreter for it is written in Python. I put concatenative in quotes (perhaps I should have used brackets?) because I tried desparately to make the composition of two pieces of a quotation fully concatenative (meaning `[ck` would be a valid program as well as `kc]`), but it didn't quite work out.

The basic and extremely simple interpreter is entirely free of inner recursion, meaning you never have to worry about overflowing Python's stack. The nature of the language, however, means that it allocates a lot of memory, most of which it discards nearly instantaneously, so writing an infinite loop will still give Python's garbage collector a decent work out.

### Theory

I didn't come up with the combinators myself. `c` and `k` are based on an overview of the concatenative combinators `cake` and `k` by Brent Kerby in his seminal [The Theory of Concatenative Combinators](http://tunes.org/~iepos/joy.html). I have named the interpreter after his elegant contraction of `cons` and `take`. Indeed, this project started out as yet another basic SKI combinator interpreter, but I was so impressed by his work that I decided to do that instead. The notation for quotations (`[]`) is inspired by Manfred von Thun's Joy language, and just about every other concatenative language uses this same notation.

If you've studied some basic lambda caculus and combinator calculus, you probably know that the combinators S and K are equivalent to the untyped lambda calculus, forming a complete base. `k` in CaKe is the concatenative equivalent of K in SKI; however, `c` is unrelated to S. However, there are multiple complete bases for the combinator calculus, and concatenative combinators are no exception. With the added power of quotations, `c` and `k` form a complete basis, allowing the representation of more common stack combinators, as well as Church numerals and other mathy things. I have no desire to show these things here, but Kerby's site gives an overview of how they might be constructed.

In addition, I suspect that `c` and `k` are not the smallest basis that could be found for concatenative languages. Kerby describes in his paper how to translate a lambda expression into stack combinators. An intrepid programmer, or perhaps more rightly a masochistic one, might try and use his method to derived a single universal stack combinator from, say, the well known X combinator which forms a complete basis for the SKI calculus. Whoever would dare do so would one-up me and create an even more painfully minimal language. It's probably not that difficult or time consuming, but, well, I have video games to play. But please show me if you find one!

### Goodies

* Interpreter is entirely free of inner recursion, so infinite loops which do not overflow the program stack (by exhausting the Python program's memory) will run forever without crashing.
* Two input and output built-ins (`@x` pushes character x onto the stack, `.` pops the top character and prints it. This setup makes printing input back to the user somewhat tricky)
* Two combinator built-ins (`c` and `k`)
* Quotations work pretty much as they do in Joy, and can be nested infinitely
* Interactive REPL (shows the stack after running every line of code)

### Baddies

* Type safety/checking
* Robust interpreter error handling (most often, if your input is invalid, it'll just crash with no clue how to fix it)
* The ability to define and use functions besides `c`, `k`, `@`, and `.`
* No built in types besides characters and quotations
* * This means no ints, no booleans, no classes, objects, or variables
* Whitespace is not allowed unless it follows an `@` (which can only be used to push a whitespace character onto the stack)
* Debugging is extremely difficult unless one thinks in terms of more useful combinators (I've provided translations for a good number in some comments in the interpreter code)
