# Example file errors.cpp

Compile this file regularly with g++:

```
g++ errors.cpp
```

It compiles!

Now use

```
g++ -Werror=uninitialized -Werror=return-type errors.cpp
```

The mistakes are caught.
