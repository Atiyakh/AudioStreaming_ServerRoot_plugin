from socket import *
from threading import Thread
import sounddevice as sd
import pickle, time

# Vars:
fs = 40800
duration = 2700
packt_size = 40800

sd.default.samplerate =  fs
sd.default.channels = 1

ADDRESS = (gethostbyname(gethostname()), 8081)
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS); server.listen()

class StreamServer:
    padding = lambda _, text: ('0'*(10-len(text)))+text
    def send_packt(self):
        conn = server.accept()[0]
        starting_index = int((time.time()-self.starting_point)*packt_size)
        data = pickle.dumps(self.rec[starting_index-packt_size:starting_index])
        conn.sendall(self.padding(len(data).__str__()).encode('utf-8')+data)
    def streaming(self):
        for _ in range(int(duration*(fs/packt_size))):
            sd.sleep(int((packt_size/fs)*1000))
            Thread(target=self.send_packt, args=()).start()
    def __init__(self):
        self.rec = sd.rec(duration*fs)
        sd.sleep(100)
        self.starting_point = time.time()
        self.streaming()

if __name__ == '__main__':
    server = StreamServer()
