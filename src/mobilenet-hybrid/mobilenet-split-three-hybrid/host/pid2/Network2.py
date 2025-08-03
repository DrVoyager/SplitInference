import time
import errno
import os
import numpy as np
from datetime import datetime

from layers_ds import Layers_Ds

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

class Layers_Ds:
    def __init__(self, in_channels, out_channels, size, stride, id1, id2):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.size = size
        self.stride = stride
        self.id1 = id1
        self.id2 = id2
        self.output = None

    def forward(self, input_data):
        # Dummy operation to simulate processing
        self.output = input_data  # Replace with actual computation logic

    def get_output(self):
        return self.output

class GlobalPoolLayer:
    def __init__(self, channels, size):
        self.channels = channels
        self.size = size
        self.output = None

    def forward(self, input_data):
        self.output = input_data  # Replace with actual global pooling logic

    def get_output(self):
        return self.output

class Network:
    def __init__(self):
        self.print_time("Network Init 2 Start")
        print("Initializing Network 2...\n")

        # Second Layer
        self.m_Layers_ds2_1 = Layers_Ds(8, 16, 112, 1, 211, 212)
        self.m_Layers_ds2_2 = Layers_Ds(16, 32, 112, 2, 221, 222)

        # Third Layer
        self.m_Layers_ds3_1 = Layers_Ds(32, 32, 56, 1, 311, 312)
        self.m_Layers_ds3_2 = Layers_Ds(32, 64, 56, 2, 321, 322)

        # Fourth Layer
        self.m_Layers_ds4_1 = Layers_Ds(64, 64, 28, 1, 411, 412)
        self.m_Layers_ds4_2 = Layers_Ds(64, 128, 28, 2, 421, 422)

        # Fifth Layer
        self.m_Layers_ds5_1 = Layers_Ds(128, 128, 14, 1, 511, 512)
        self.m_Layers_ds5_2 = Layers_Ds(128, 128, 14, 1, 521, 522)
        self.m_Layers_ds5_3 = Layers_Ds(128, 128, 14, 1, 531, 532)
        self.m_Layers_ds5_4 = Layers_Ds(128, 128, 14, 1, 541, 542)
        self.m_Layers_ds5_5 = Layers_Ds(128, 128, 14, 1, 551, 552)
        self.m_Layers_ds5_6 = Layers_Ds(128, 256, 14, 2, 561, 562)

        # Sixth Layer
        self.m_Layers_ds6 = Layers_Ds(256, 256, 7, 1, 61, 62)

        # Global Pooling Layer
        self.m_Poollayer6 = GlobalPoolLayer(256, 7)
        print("Initializing Network 2 Done...\n")
        self.print_time("Network Init 2 End")

    def forward(self, input_data):
        self.print_time("Inference 2 Start")
        
        self.m_Layers_ds2_1.forward(input_data)
        self.m_Layers_ds2_2.forward(self.m_Layers_ds2_1.get_output())

        self.m_Layers_ds3_1.forward(self.m_Layers_ds2_2.get_output())
        self.m_Layers_ds3_2.forward(self.m_Layers_ds3_1.get_output())

        self.m_Layers_ds4_1.forward(self.m_Layers_ds3_2.get_output())
        self.m_Layers_ds4_2.forward(self.m_Layers_ds4_1.get_output())

        self.m_Layers_ds5_1.forward(self.m_Layers_ds4_2.get_output())
        self.m_Layers_ds5_2.forward(self.m_Layers_ds5_1.get_output())
        self.m_Layers_ds5_3.forward(self.m_Layers_ds5_2.get_output())
        self.m_Layers_ds5_4.forward(self.m_Layers_ds5_3.get_output())
        self.m_Layers_ds5_5.forward(self.m_Layers_ds5_4.get_output())
        self.m_Layers_ds5_6.forward(self.m_Layers_ds5_5.get_output())

        self.m_Layers_ds6.forward(self.m_Layers_ds5_6.get_output())
        self.m_Poollayer6.forward(self.m_Layers_ds6.get_output())
        
        output = self.m_Poollayer6.get_output()
        self.print_time("Inference 2 End")
        return output

    def print_time(self, message):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"Time: {timestamp} : {message}")

# Open pipes
read_pipe = open(pipe1, 'rb')
write_pipe = open(pipe2, 'wb')

input_size = 100352  # Number of floats

while True:
    # Read a single line from C++ (the string)
    data = read_pipe.read(input_size * 4)
    if not data:
        break

    input_data = np.frombuffer(data, dtype=np.float32)

    # Here you can process the string however you like
    # For example, let's just convert it to uppercase as a demo

    # # Initialize the network
    network = Network()

    # # Feed the input data to the network and get the output
    output = network.forward(input_data)

    # # Write the response string back to C++
    # write_pipe.write(response_str + "\n")
    output_bytes = output.tobytes()
    write_pipe.write(output_bytes)
    write_pipe.flush()

# Cleanup
read_pipe.close()
write_pipe.close()