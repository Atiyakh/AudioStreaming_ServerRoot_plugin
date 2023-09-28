from socket import *
from threading import Thread
import sounddevice as sd
import pickle, time, numpy
import traceback

# Vars:
fs = 40800
duration = 2700
packt_size = 40800

sd.default.samplerate =  fs
sd.default.channels = 1

class StreamConnection:
    def recv_full_packt(self, conn):
        buffer = int(conn.recv(10).decode('utf-8'))
        data = b''
        while True:
            if len(data) == buffer: break
            data += conn.recv(10_000)
        return data
    def recv_packt(self):
        connection = socket(AF_INET, SOCK_STREAM)
        connection.connect(("85.114.123.229", 8081))
        data = pickle.loads(self.recv_full_packt(connection))
        starting_index = int((time.time()-self.starting_point)*packt_size)
        try:self.rec[starting_index:(starting_index+packt_size)] = data
        except: traceback.print_exc()
    def streaming(self):
        for _ in range(int(duration*(fs/packt_size))):
            sd.sleep(int((packt_size/fs)*1000))
            Thread(target=self.recv_packt, args=()).start()
    def __init__(self):
        self.rec = numpy.zeros((packt_size*duration, 1))
        sd.play(self.rec)
        self.starting_point = time.time()
        self.streaming()

if __name__ == '__main__':
    stream = StreamConnection()
