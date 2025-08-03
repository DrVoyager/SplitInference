import errno
import os

pipe1 = '/tmp/pipe1'  # We'll read from this pipe (sent by C++)
pipe2 = '/tmp/pipe2'  # We'll write to this pipe (to send back to C++)

# Make named pipes, ignoring "already exists" error
try:
    os.mkfifo(pipe1, mode=0o777)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

try:
    os.mkfifo(pipe2, mode=0o777)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

# Open pipes
read_pipe = open(pipe1, 'r')
write_pipe = open(pipe2, 'w')

while True:
    # Read a single line from C++ (the string)
    received_str = read_pipe.readline()
    if not received_str:
        break

    received_str = received_str.strip()
    print(f"Python: '{received_str}'")

    # Here you can process the string however you like
    # For example, let's just convert it to uppercase as a demo
    response_str = "Hello from Python to C++!"

    # Write the response string back to C++
    write_pipe.write(response_str + "\n")
    write_pipe.flush()

# Cleanup
read_pipe.close()
write_pipe.close()
