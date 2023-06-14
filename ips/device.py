import math
import numpy as np

# svyturelio klase
class Device:
    def __init__(self, mac, rssi, txpower=40):
        self.mac = mac
        self.rssi = rssi
        self.txpower = txpower #pamatuotas rssi 1 metro atstumu

    def __repr__(self):
            return f"Device MAC: {self.mac}, RSSI: {self.rssi}"

# pagal RSSI reiksmes apskaicuojami atstumai
    def calculate_distance(self):
        ratio =(self.txpower-int(self.rssi))/(10*4)
        distance= math.pow(10,ratio)
        return distance

# es32 irenginiu koordinates
stot_xy = list(np.array([[500,200], [900,160], [500,750]]))

# sekamu svytureliu mac adresai
mac_adresai = ["d0:f0:18:78:05:ba", "00:00:00:00:00:00"]

# stebimos patalpos ribos
xy_riba = [[-9.8,1200],[-20,760]] # koordnaciu ribos, kad zmogeliukas nebutu rodomas uz patalpos ribu
