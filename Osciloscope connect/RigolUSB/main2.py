import pyvisa as visa
rm = visa.ResourceManager()
print( rm.list_resources() )
osc='USB0::0x1AB1::0x0516::DS8A234200645::INSTR'

myScope = rm.open_resource(osc)
print(myScope.query("*IDN?"))
b = "90000"
myScope.write("WGEN:FREQ " + b) #connect the wavegen to channel 1
myScope.write("WGEN:FUNC SIN")
myScope.write("WGEN:OUTP ON")
myScope.write("WGEN:VOLT 2")
myScope.write("WGEN:TIME 2")
c = "200.0E-6"
myScope.write(":TIMebase:SCALe "+c)
myScope.write(":WAVeform:SOURce CHANnel1")
myScope.write(":WAVeform:FORMat ASCII")
myScope.write(":WAVeform:POINts 1000")




data=myScope.query("WAV:DATA?")

print(data)
print(type(data))
timescale = float(myScope.query(":TIM:SCAL?"))
print("Time scale",timescale)
timeoffset = float(myScope.query(":TIM:OFFS?"))
print("Time offset =",timeoffset)
voltscale = float(myScope.query(':CHAN1:SCAL?'))
print("Volt scale =", voltscale)
voltoffset = float(myScope.query(":CHAN1:OFFS?"))
print("Volt offset =",voltoffset)
sample_rate = float(myScope.query(':ACQ:SRAT?'))
print("Sample rate =", sample_rate)
