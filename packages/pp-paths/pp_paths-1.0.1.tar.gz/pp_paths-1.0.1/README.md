# `pp_paths`: A python script to pretty print directory structures

pass the paths of files to be printed through `stdin`. They will be printed as a tree using ascii art.

# Installation

    pip install pp_paths --user

> pp_paths [-c] [-b]

*-c* collapse directory sequences

*-b* print trees with a common base named '////'. The default is to print all the
    trees formed separated with a '*////*'

## Examples

    > find b -type f|pp_paths
    b/
    ├─a/
    │ └─b/
    │   └─c/
    │     └─d/
    │       ├─1
    │       ├─2
    │       └─3
    ├─s
    ├─b/
    │ ├─w/
    │ │ └─a
    │ ├─q
    │ └─x
    ├─r
    └─q/
      ├─e
      └─y


    > find b -type f|pp_paths -c
    b/
    ├─a/b/c/d/
    │ ├─1
    │ ├─2
    │ └─3
    ├─s
    ├─b/
    │ ├─w/a
    │ ├─q
    │ └─x
    ├─r
    └─q/
      ├─e
      └─y

    > {find b -type d; find a}|pp_paths
    b/
    ├─a/
    │ └─b/
    │   └─c/
    │     └─d
    ├─b/
    │ └─w
    ├─z
    └─q
    
    -*-*-
    a/
    └─b
    
    user@machine /dev/pts/4 /home/user/src/pp_paths
    > {find b -type d; find a}|pp_paths -b
    ////
    ├─b/
    │ ├─a/
    │ │ └─b/
    │ │   └─c/
    │ │     └─d
    │ ├─b/
    │ │ └─w
    │ │
    │ ├─z
    │ └─q
    └─a/
      └─b

You can easily integrate it with other tools which output list of files:

    > pacman -Ql tmux |awk '{print $2}'|pp_paths -c -b
    /usr/
    ├─bin/tmux
    └─share/
      ├─licenses/tmux/LICENSE
      └─man/man1/tmux.1.gz


    > bsdtar tf ~/Downloads/emacs-for-clojure-book1.zip |pp_paths -c
    emacs-for-clojure-book1/
    ├─.gitignore
    ├─README.md
    ├─customizations/
    │ ├─editing.el
    │ ├─elisp-editing.el
    │ ├─misc.el
    │ ├─navigation.el
    │ ├─setup-clojure.el
    │ ├─setup-js.el
    │ ├─shell-integration.el
    │ └─ui.el
    │
    ...
