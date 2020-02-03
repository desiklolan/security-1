# Command Execution

If you look at how the command line works, you can find that there is multiple way to add more commands:

- `command1 && command2` that will run `command2` if `command1` succeeds.
- `command1 || command2` that will run `command2` if `command1` fails.
- `command1 ; command2` that will run `command1` then `command2`.
- `command1 | command2` that will run `command1` and send the output of `command1` to `command2`.

You can use `` `command` `` to run a command.

You can use `$(command)` to run a command.

