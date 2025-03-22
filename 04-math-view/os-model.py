#!/Users/xosmos/opt/anaconda3/envs/os-jyy/bin/python

from pathlib import Path
import random
import sys


class OS:
    """
    A minimal executable operationg system model. Processes
    are state machines (Python generators) that can be paused
    or continued with local states being saved.
    """

    SYSCALLS = ['read', 'write', 'spawn']

    class Process:
        """
        A "freezed" state machine. The state (local variables,
        program counters, etc.) are stored in the generator
        object. 
        """

        def __init__(self, func, *args) -> None:
            # func should be a generator function. Calling
            # func(*args) returns a generator object.
            self._func = func(*args)

            # return value is set by OS's main loop
            self.retval = None

        def step(self):
            """
            Resume the process with OS-written return value,
            until the next system call is issued. 
            """
            syscalls, args, *_ = self._func.send(self.retval)
            self.retval = None
            return syscalls, args
    
    def __init__(self, src) -> None:
        # This is a hack: we directly execute the source
        # in the current python runtime--and main is thus
        # available for calling
        exec(src, globals())
        self.procs = [OS.Process(main)]
        self.buffer = ''
    
    def run(self):
        # Real operating systems wasting all CPU cycles
        # (efficiently, by putting the CPU into sleep) when
        # there is no running process at the moment. Our model
        # terminates if there is nothing to run
        while self.procs:

            # there is also a pointer to current process
            # in today's operationg system
            current = random.choice(self.procs)

            try:
                # operationg system handle interrupt and system
                # calls, and "assign" CPU to process
                match current.step():
                    case 'read', _:
                        current.retval = random.choice([0, 1])
                    case 'write', s: 
                        self.buffer += s
                    case 'spawn', (fn, *args):
                        self.procs += [OS.Process(fn, *args)]
                    case _:
                        assert 0
            
            except StopIteration:
                # The generator object terminates
                self.procs.remove(current)
        
        return self.buffer
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} file')
        exit(1)
    
    src = Path(sys.argv[1]).read_text()

    # Hack: patch sys_read(...) -> yield "sys_read", (...)
    for syscall in OS.SYSCALLS:
        src = src.replace(f'sys_{syscall}',
                          f'yield "{syscall}", ')
    
    stdout = OS(src).run()
    print(stdout)
    
