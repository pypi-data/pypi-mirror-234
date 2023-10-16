# WizLib

A collection of Python modules that might be useful across multiple projects

## ClassFamily

A class family is a set of class definitions that use single inheritance
(each subclass inherits from only one parent) and often multiple inheritance
(subclasses can inherit from subclasses). So it's a hierarchy of classes,
with one super-parent (termed the "atriarch") at the top.

We offer a way for members of the family to declare themselves simply by
living in the right package location. Then those classes can be instantiated
using keys or names, without having to be specifically called. The members
act independently of each other.

What we get, after importing everything and loading it all, is essentially a
little database of classes, where class-level properties become keys for
looking up member classes. So, for example, we can have a family of commands,
and use a command string to look up the right command.

Ultimately, the atriarch of the family -- the class at the top of the
hierarchy -- holds the database, actually a list, in the property called
"family". So that class can be queried to find appropriate family member
classes or instances thereof.

This utility provides functions for importing family members, loading the
"families" property of the super-parent, and querying the family.

In the process of loading and querying the class family, we need to *avoid*
inheritance of attributes. There might be abstract intermediary classes that
don't want to play. So we use `__dict__` to ensure we're only seeing the
atttributes that are defined on that specific class.

## SuperWrapper

Provide a decorator to wrap a method so that it's called within the inherited
version of that method.

Example of use:

```python
class Parent(SuperWrapper):
    def execute(self, method, *args, **kwargs):
        print(f"Parent execute before")
        method(self, *args, **kwargs)
        print(f"Parent execute after")

class InBetween(Parent):
    @Parent.wrap
    def execute(self, method, *args, **kwargs):
        print(f"IB execute before")
        method(self, *args, **kwargs)
        print(f"IB execute after")

class NewChild(InBetween):
    @InBetween.wrap
    def execute(self, name):
        print(f"Hello {name}")

c = NewChild()
c.execute("Jane")
```

Note that for a method to be "wrappable" it must take the form shown above, and explicitly call the method that's handed into it. So strictly, this is different from regular inheritance, where the parent class method has the same signature as the child class method.


## CommandHandler

## ConfigMachine

Enables easy configuration across multiple levels. Tries each of the following approaches in order until one finds the required config option

- First look for attributes of the instance (subclass of ConfigMachine) itself (e.g. `gitlab_host`)
- Then look for a specific env variable for that config setting in all caps, e.g. `GITLAB_HOST`
- If those both fail, then look for a YAML configuration file:
    - First identified with a `--config` / `-c` option on the command line
    - Then with a path in the `APPNAME_CONFIG` environment variable - note all caps
    - Then look in the local working directory for `.appname.yml`
    - Then look for `~/.appname.yml` in the user's home directory

Config files are in YAML, and look something like this:

```yaml
gitlab:
  host: gitlab.com
local:
  root: $HOME/git
```

Note that nested labels in the config map to hyphenated command line options.

To use the library:

```python
config = ConfigMachine('appname', args)
host = config.get('gitlab-host')
```

This assumes that `args` represents the result of `ArgumentParser` - in otherwords, a `Namespace` object.

ConfigMachine works well with CommandHandler, in which case specific config settings can be added as arguments in `add_app_args` or `add_args` and then presented on the command line.

## RLInput

Python supports the GNU readline approach, which enables tab completion, key mappings, and history with the `input()` function. But the documentation is cryptic, and the implementation differs between Linux and MacOS. RLInput makes it easy.

```python
from wizlib.rlinput import rlinput
```

It's just a function, with up to three parameters:

- `intro:str=""` - The intro or prompt, same as in the `input()` function.
- `default:str=""` - If provided, the text will be inserted into the buffer at the start, with the cursor at the end of the buffer. So that becomes the default, that must be overridden by the user if they want different input.
- `options:list=[]` - A list of options for tab completion. This assumes the options are choices for the entire entry; it's not context-dependent within the buffer.

Emacs keys are enabled by default; I'm able to use the arrow keys on my Mac so you should too. I made one change to the keyboard mappings, which is the Ctrl-A, instead of just moving the cursor to the beginning of the line, wipes the entire buffer. So to wipe out the default value and type or tab something new, just hit Ctrl-A.


---

Logo by [Freepik](https://www.freepik.com/?_gl=1*1y9rvc9*test_ga*Mjc1MTIzODYxLjE2ODA3OTczNTg.*test_ga_523JXC6VL7*MTY4MDc5NzM1OC4xLjEuMTY4MDc5NzQxNS4zLjAuMA..*fp_ga*Mjc1MTIzODYxLjE2ODA3OTczNTg.*fp_ga_1ZY8468CQB*MTY4MDc5NzM1OC4xLjEuMTY4MDc5NzQxNS4zLjAuMA..)


