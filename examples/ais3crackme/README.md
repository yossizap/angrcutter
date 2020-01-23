### About
This is an easy crackme challenge that checks the command line arguments for a valid output.
Taken from [angr's examples](https://github.com/angr/angr-doc/blob/master/examples/ais3_crackme/).

### Solution
- Start debug with a random input
- Continue to main
- Set a breakpoint at 0x4005f9 before the call to verify and continue
- Right click 0x400602 (desired verify outcome) and select `Plugins -> Angr - set find addr`
to find a solution that will reach this address
- Right click 0x40060e (failure execution path) and select `Plugins -> Angr - set avoid addr`
to avoid symboliclly executing code in this path during exploration
- Right click `rax` in the angr widget to symbolize it since argv[1] is in it and verify is
about to check it
- Click `Start` in the angr plugin and wait for the result to be printed in the console
- Click `Apply simulation results` in the angr widget to change the value of `rax` to the
correct key
- Continue the execution
