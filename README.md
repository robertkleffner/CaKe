CaKe
====

An interpreter for a minimal but Turing-complete stack based 'concatenative' esolang.

### About

CaKe is an extremely minimal 'concatenative' language which performs all of its work on a stack. This tiny interpreter for it is written in Python. I put concatenative in quotes (perhaps I should have used brackets?) because I tried desparately to make the composition of two pieces of a quotation fully concatenative (meaning `[ck` would be a valid program as well as `kc]`), but it didn't quite work out.

The basic and extremely simple interpreter is entirely free of inner recursion, meaning you never have to worry about overflowing Python's stack. The nature of the language, however, means that it allocates a lot of memory in a very short amount of time, most of which it discards nearly instantaneously, so writing an infinite loop will still give Python's garbage collector a decent cardio workout.

#### Update

I have since made a second language very similar to CaKe, except it only uses the 'z' combinator and quotations, as discussed [here](http://groups.yahoo.com/neo/groups/concatenative/conversations/topics/3178), again by the lucid Brent Kerby. The interpreter for that language is in zquote.py.

### Example

```[[]cckck@\n@!@p@o@t@s@ @t@i@ @e@k@a@M..............[[]]ckk][]cckck[[]]ckk```

This little program prints 'Make it stop!' in an infinite loop (while also not overflowing the program stack).

```[[][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz@\n@!@d@l@r@o@W@ @,@o@l@l@e@H..............[[]][][][[][][]zz[][]zz]z[][]zz[][]zz][][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz[[]][][][[][][]zz[][]zz]z[][]zz[][]zz```

This program prints 'Hello, World!' in an infinite loop using the z language. Notice how exponentially worse a single combinator basis is! For further comparison, here's the `dup` command (which duplicates the top item on the stack) in CaKe:

```[]cckck```

And here's the same command implemented in zquote:

```[][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz```

For dup, CaKe uses 7 characters, but zquote uses an astonishing 77 characters! Also, every `z` present in a zquote program performs *at least* the equivalent work of both a `c` and `k` in CaKe, so its operating time and memory usage are significantly worse while making for longer programs!

### Theory

I didn't come up with the combinators myself. `c` and `k` are based on an overview of the concatenative combinators `cake` and `k` by Brent Kerby in his seminal [The Theory of Concatenative Combinators](http://tunes.org/~iepos/joy.html). I have named the interpreter after his elegant contraction of `cons` and `take`. Indeed, this project started out as yet another basic SKI combinator interpreter, but I was so impressed by his work that I decided to implement his language instead. The notation for quotations (`[]`) is inspired by Manfred von Thun's Joy language, and just about every other concatenative language uses this same notation.

If you've studied some basic lambda caculus and combinator calculus, you probably know that the combinators S and K are equivalent to the untyped lambda calculus, forming a complete base. `k` in CaKe is the concatenative equivalent of K in SKI; however, `c` is unrelated to S. However, there are multiple complete bases for the combinator calculus, and concatenative combinators are no exception. With the added power of quotations, `c` and `k` form a complete basis, allowing the representation of more common stack combinators, as well as Church numerals and other mathy things. I have no desire to show these things here, but Kerby's site gives an overview of how they might be constructed.

In addition, I suspect that `c` and `k` are not the smallest basis that could be found for concatenative languages. Kerby describes in his paper how to translate a lambda expression into stack combinators. An intrepid programmer, or perhaps more rightly a masochistic one, might try and use his method to derived a single universal stack combinator from, say, the well known X combinator which forms a complete basis for the SKI calculus. Whoever dares to do so would one-up me and create an even more painfully minimal language. It's probably not that difficult or time consuming, but, well, I have video games to play. But please show me if you find one!

#### Update

Apparently I don't have as many video games to play as I thought. However, after beating my head trying to derive a suitable single combinator basis from X, and running some hand simulations of the stack on paper and quite soon realizing I was getting nowhere, I turned to Google and found, surprise of surprises, a discussion on the [concatenative language mailing list](http://groups.yahoo.com/neo/groups/concatenative/conversations/topics/3178) in which Brent Kerby proved that deriving a single basis from X couldn't be done! I was dismayed, but Kerby, in the same message, showed a derivation of a combinator he calls `z`. This combinator, when joined with quotation, forms a complete basis for the concatenative combinator calculus. It didn't take much to whip up another interpreter, this one using only `z`, `@`, `.`, and quotation. You can find this one in the zquote.py file.

### Goodies

* Interpreter is entirely free of inner recursion, so infinite loops which do not overflow the program stack (by exhausting the Python program's memory) will run forever without crashing.
* Two input and output built-ins (`@x` pushes character x onto the stack, `.` pops the top character and prints it. This setup makes printing input back to the user somewhat tricky)
* Two combinator built-ins: `c` and `k` (for more on how to use these, see Kerby's page or the comments in the interpreter)
* Quotations work pretty much as they do in Joy, and can be nested infinitely
* Interactive REPL (shows the stack after running every line of code)
* Type 'quit' when your brain is sufficiently cooked (its not really a combinator though)

### Baddies

* No type safety/checking
* Minimal interpreter error handling (most often, if your input is invalid, it'll just crash with no clue how to fix it)
* The ability to define and use functions besides `c`, `k`, `@`, and `.`
* No built in types besides characters and quotations
* * This means no ints, no booleans, no classes, objects, or variables
* Whitespace is not allowed unless it follows an `@` (which can only be used to push a whitespace character onto the stack)
* Debugging is extremely difficult unless one thinks in terms of more useful combinators (I've provided translations for a good number in some comments in the interpreter code)
