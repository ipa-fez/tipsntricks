# Tips and Tricks

## useful catkin tools aliases

Custom catkin aliases can be specified in `~/.config/catkin/verb_aliases/`, some helpful ones are included in this repo.

## Enabling warnings in QtCreator

![QtCreator Warnings](/imgs/qtcreator_warnings.png)

Use at least `-Wall -Wextra`. `-pedantic` complains about a lot of extra things but may hit some stuff in ros/system includes. Individual warning categories can be disabled by using `-Wno-<warning>`, for example `-Wno-unused-parameter`.

The `-c` in CatkinTools arguments tells catkin to continue on error.

Note that you will have to do this for each build configuration (Debug, Release, etc)

## Enabling the clang-code model in QtCreator

Make sure you're on the latest version and enable the plugin (Help->About Plugins...).

![QtCreator Plugins](/imgs/qtcreator_plugins.png)

For more information, see https://doc.qt.io/qtcreator/creator-clang-codemodel.html
