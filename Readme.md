# Tips and Tricks

## General

In order to improve the quality of our codebase, avoid bugs, and save time during reviews, it is very important to look at compiler warnings. Some easy mistakes like a missing return or an uninitialised variable can be caught by those warnings.

Everyone should at least build their code with warnings before submitting a pull request. It is however highly recommended to _always_ build your code with warnings. This will help spot mistakes early, allowing for corrections during the normal workflow instead of a bulk refactoring at the end.

Warnings are generally enabled with arguments passed to the compiler. How these arguments are specified, depends on the tools that are used. Below are some examples of how to do this.

## catkin tools

To enable warnings with catkin tools, pass these arguments to it when you build:

```
catkin build --cmake-args -DCMAKE_CXX_FLAGS=-Wall -Wextra
```

If it gets confused, you might have to use `--` to separate catkin args from paths like so:

```
catkin build --cmake-args -DCMAKE_CXX_FLAGS=-Wall -Wextra --
```

These flags _should_ be cached until you delete your build folder, but it doesn't hurt to specify them every time. To save time, you can specify custom catkin aliases.

Custom catkin aliases can be specified in `~/.config/catkin/verb_aliases/`, some helpful ones are included in this repo. Since this config file doesn't seem to like quotes/escapes much, you might have to append a space after the alias when you use it on the command line.

Other helpful catkin tools arguments are

`-c` continue on error: this will build packages that don't depend on ones that failed to build instead of abandoning everything.

`--summary` will print a nice summary of which packages were built and which ones errored out at the end of the build.

## Enabling warnings in QtCreator

It's a good idea to enable warnings in QtCreator. They will be shown in a list that lets you jump to the relevant line in the code as well as being hilighted in the code itself with exclamation marks.

![QtCreator Warnings](/imgs/qtcreator_warnings.png)

Use at least `-Wall -Wextra`. `-pedantic` complains about a lot of extra things but may hit some stuff in ros/system includes. Individual warning categories can be disabled by using `-Wno-<warning>`, for example `-Wno-unused-parameter`.

The `-c` in CatkinTools arguments tells catkin to continue on error.

## Enabling the Clang Code Model in QtCreator

The clang code model can show a bunch of extra warnings. It parses the code continuously and can therefore show warnings without having to start a compile first.

Make sure you're on the latest version and enable the plugin (Help->About Plugins...).

![QtCreator Plugins](/imgs/qtcreator_plugins.png)

For more information, see https://doc.qt.io/qtcreator/creator-clang-codemodel.html

Since the code model parses the current file and includes in the background it can be a bit slower than the regular built in code model.
