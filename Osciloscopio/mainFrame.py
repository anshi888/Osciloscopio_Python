from tkinter import StringVar, Tk, Frame, Button, Label, ttk, PhotoImage
from urllib import response
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#AUDIO ESPECTRO
import matplotlib
import pyaudio as pa 
import struct 
import scipy.fftpack as fourier
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
#API REQUEST
from requests import post
#Pyvisa Osciloscopio
import pyvisa as visa
import numpy


class MainFrame(Frame): #Clase principal llamada de las funciones secundarias
    def __init__(self, master,*args):
        super().__init__(master,*args)  # Especif.Ventana
        #Variables de entrada 
        self.var_ton= StringVar()
        self.var_toff=StringVar()
        self.var_pulsos=StringVar()
        self.Layaout() 
        self.electroporador()
        self.Camara()
        self.Config_graph()
        self.Config_osci()
        
    
    def Layaout(self):
        global frame4 #PARAMETROS ELECTROPORADOR
        global frame  #CAMARA
        global frame3 #GRAFICO VOZ
        global frame1 #Osciloscopio
        #Separo el layaout
 ########Seccion 1########################################
        frame = Frame(self.master,bg='black',bd=2)
        frame.grid(column=0,row=1,sticky='nsew')
########Seccion2########################################### 
        frame1 = Frame(self.master,bg='black',bd=2)
        frame1.grid(column=2,row=0, sticky='nsew')
########Seccion3###########################################
        frame3 = Frame(self.master,bg='black',bd=2)
        frame3.grid(column=2,row=1,sticky='nsew')
########Seccion4########################################### 
        frame4=Frame(self.master,bg='black',bd=2) 
        frame4.grid(column=0,columnspan=2,row=0,sticky='nsew')
########Configuro columnas y filas del layout################
        self.master.columnconfigure(0,weight=3)
        self.master.columnconfigure(2,weight=2)
        self.master.rowconfigure(0,weight=2)
        self.master.rowconfigure(1,weight=8)
####### PARAMETROS DEL ELECTROPORADOR ##############################
    def electroporador(self):
        global frame4 #Enlazo por medio variable global layout seccion4
        #TITULO
        self.titulo=Label(frame4, text="Multi-control software",bg='black',font=('Arial',25,'bold'),fg="white")
        self.titulo.place(x=180,y=20)
        #TON
        self.ton=Label(frame4, text="Ton [ns] : ",bg='black',font=('Arial',15,'bold'),fg="white")
        self.ton.place(x=40+100,y=100)

        self.ingresoton = ttk.Entry(frame4,textvariable=self.var_ton)
        self.ingresoton.place(x=160+100,y=22+80,height=30,width=250)
        #Toff
        self.toff=Label(frame4, text="Toff [us] : ",bg='black',font=('Arial',15,'bold'),fg="white")
        self.toff.place(x=40+100,y=180)

        self.ingresotoff = ttk.Entry(frame4,textvariable=self.var_toff)
        self.ingresotoff.place(x=160+100,y=98+80,height=30,width=250)
        #Pulsos
        self.pulsos=Label(frame4, text="Pulsos : ",bg='black',font=('Arial',15,'bold'),fg="white")
        self.pulsos.place(x=40+100,y=180+80)
        #Relaciono Entry var_pulsos=StringVar() para extraccion
        self.ingresopulsos = ttk.Entry(frame4,textvariable=self.var_pulsos)
        self.ingresopulsos.place(x=160+100,y=178+80,height=30,width=250)
        #BOTONES
        self.bt_enviar= Button(frame4,text='Enviar',font=('Arial',12,'bold'),
             width=12,bg='green',fg='white',command=self.send)
        self.bt_enviar.place(x=40+40+160,y=320+40)

        self.bt_stop= Button(frame4,text='Stop',font=('Arial',12,'bold'),
             width=12,bg='green',fg='white')
        self.bt_stop.place(x=190+40+160,y=320+40)
    def send(self): #Funcion para extraer parametros Entry y enviar por medio request
        pulsos_v=self.var_pulsos.get()
        toff_v=self.var_toff.get()
        ton_v=self.var_ton.get()
        #peticion post envia pulsos
        foo=post('http://192.168.1.209/get', data = {'ton':ton_v,'toff':toff_v,'pulsos':pulsos_v})
        #print(pulsos_v)
        #print(toff_v)
        #print(ton_v)
    def stop(self):
        print("Stop")
        foo=post('http://192.168.1.209/get', data = {'ton':'100','toff':'100','pulsos':'-1'})

###################FUNCION CAMARA########################################
    def Camara(self):
        global frame #Layou seccion2
        #BOTONES#################333
        self.init_video= Button(frame,text='Iniciar',font=('Arial',12,'bold'),
        width=10,bg='green',fg='white',command=self.iniciar)
        self.init_video.place(x=60,y=0)

        self.stop_video= Button(frame,text='stop',font=('Arial',12,'bold'),
        width=10,bg='green',fg='white',command=self.finalizar)
        self.stop_video.place(x=140+40,y=0)

        self.gray= Button(frame,text='Gray',font=('Arial',12,'bold'),
        width=10,bg='green',fg='white',command=self.grayf)
        self.gray.place(x=260+40,y=0)

        self.hsv= Button(frame,text='HSV',font=('Arial',12,'bold'),
        width=10,bg='green',fg='white',command=self.hsvf)
        self.hsv.place(x=380+40,y=0)

        self.rgb= Button(frame,text='RGB',font=('Arial',12,'bold'),
        width=10,bg='green',fg='white',command=self.rgbf)
        self.rgb.place(x=500+40,y=0)
        #VENTANA CAMARA
        self.lblVideo = Label(frame,width=640,bg="black")
        self.lblVideo.place(x = 50, y = 50,height=400)
    # Funcion Visualizar CAMARA
    def visualizar(self):
        global frame, cap,rgb, hsv, gray
        if cap is not None:
            ret, frame = cap.read()
        # Si es correcta
            if ret == True:

                if (rgb == 1 and hsv == 0 and gray == 0):
                    
                # Color BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif (rgb == 0 and hsv == 0 and gray == 1):
                # Color GRAY
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                elif rgb == 0 and hsv == 1 and gray == 0:
                # Color HSV
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Rendimensionamos el video
                frame = imutils.resize(frame, width=640)

                # Convertimos el video
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)

                # Mostramos en el GUI
                self.lblVideo.configure(image=img)
                self.lblVideo.image = img
           
                self.lblVideo.after(1, self.visualizar)

            else:
                 cap.release()
    #INICIAR / FINALIZAR CAMARA        
    def iniciar(self):
        global cap,hsv,rgb,gray
        
        rgb=1
        hsv=0
        gray=0  
        cap= cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.visualizar()
    def finalizar(self):
        cap.release()
        print("FIN")
    # Conversion de color
    def hsvf(self):
        global hsv, rgb, gray
        rgb = 0
        hsv = 1
        gray = 0
    def rgbf(self):
        global hsv, rgb, gray
        rgb = 1
        hsv = 0
        gray = 0
    def grayf(self):
        global hsv,rgb,gray
        rgb=0
        hsv=0
        gray=1
################################GRAFICOS ESPECTRAL##################################################
    def Config_graph(self):
        global FRAMES,ax1
        self.fig,(ax,ax1) = plt.subplots(2)
        #Color de fondo
        self.fig.patch.set_facecolor('black')
        #Contorno de grafico
        ax.set_title('Espectro de Frecuencia',color="green")

        ax.spines['bottom'].set_color('green')
        ax.spines['top'].set_color('green')
        ax.spines['left'].set_color('green')
        ax.spines['right'].set_color('green')
        ax1.spines['bottom'].set_color('green')
        ax1.spines['top'].set_color('green')
        ax1.spines['left'].set_color('green')
        ax1.spines['right'].set_color('green')
        #Color de ejes
        ax.tick_params(axis='x', colors='green')
        ax.tick_params(axis='y', colors='green')
        ax1.tick_params(axis='x', colors='green')
        ax1.tick_params(axis='y', colors='green')
        #Parametros
        FRAMES = 1024*8                                   # Tamaño del paquete a procesar
        FORMAT = pa.paInt16                               # Formato de lectura INT 16 bits
        CHANNELS = 1
        Fs = 44100                                        # Frecuencia de muestreo típica para audio

        p = pa.PyAudio()

        self.stream = p.open(                                  # Abrimos el canal de audio con los parámeteros de configuración
            format = FORMAT,
            channels = CHANNELS,
            rate = Fs,
            input=True,
            output=True,
            frames_per_buffer=FRAMES
        )
        x_audio = np.arange(0,FRAMES,1)
        x_fft = np.linspace(0, Fs, FRAMES)

        self.line, = ax.plot(x_audio, np.random.rand(FRAMES),'g')
        self.line_fft, = ax1.semilogx(x_fft, np.random.rand(FRAMES), 'b')

        ax.set_ylim(-1500,1500)
        ax.ser_xlim = (0,FRAMES)
        Fmin = 1
        Fmax = 5000
        ax1.set_xlim(Fmin,Fmax)
        self.F = (Fs/FRAMES)*np.arange(0,FRAMES//2)                 # Creamos el vector de frecuencia para encontrar la frecuencia dominante
        global frame3 #llamo al layoyt 3
        #muestro figura
       
        self.canvas= FigureCanvasTkAgg(self.fig,master=frame3)
        self.canvas.get_tk_widget().pack(padx=0,pady=0,expand=True,fill='x',side='bottom')
        
    def animete(self): #REPLICO EL WHILE ACTUALIZACION CON FUNCION AFTER MAIN.PY
        FRAMES = 1024*8  
        data=self.stream.read(FRAMES)
        dataInt = struct.unpack(str(FRAMES) + 'h', data)   # Convertimos los datos que se encuentran empaquetados en bytes
        self.line.set_ydata(dataInt)                            # Asignamos los datos a la curva de la variación temporal
        M_gk = abs(fourier.fft(dataInt)/FRAMES)            # Calculamos la FFT y la Magnitud de la FFT del paqute de datos
        ax1.set_ylim(0,np.max(M_gk+10)) 
        self.line_fft.set_ydata(M_gk)
        M_gk = M_gk[0:FRAMES//2]                           # Tomamos la mitad del espectro para encontrar la Frecuencia Dominante
        Posm = np.where(M_gk == np.max(M_gk))
        F_fund = self.F[Posm]                                   # Encontramos la frecuencia que corresponde con el máximo de M_gk
        #print(int(F_fund),np.max(M_gk+10))
        #funcion ANIMATION ACTUALIZAR EN EL GRAFICO
        animation.FuncAnimation(self.fig,self.animete,interval=10,blit=False)
        self.canvas.draw()
    
#################GRAFICO OSCIOLOSCOPIO##################################################
    def Config_osci(self):
        global frame1,myScope
        self.fig2,ax2 = plt.subplots()
        #Color de fondo
        ax2.set_ylim(-30,30)
        ax2.set_xlim(0,500e-09)
        self.fig2.patch.set_facecolor('black')
        #Contorno de grafico
        ax2.spines['bottom'].set_color('green')
        ax2.spines['top'].set_color('green')
        ax2.spines['left'].set_color('green')
        ax2.spines['right'].set_color('green')
        #Color de ejes
        ax2.tick_params(axis='x', colors='green')
        ax2.tick_params(axis='y', colors='green')
        plt.title("Osciloscopio",color= 'green',size=18,family="Arial")
        
        self.line2, = ax2.plot([],[],color='g')
        #Abre comuncicacion con osciloscopio 
        rm=visa.ResourceManager()
        #Direccionamiento osciloscopio
        osc='USB0::0x1AB1::0x0516::DS8A234200645::INSTR'
        #Abrir intrumento
        myScope = rm.open_resource(osc)
        self.canvas2= FigureCanvasTkAgg(self.fig2,master=frame1)
        self.canvas2.get_tk_widget().pack(padx=0,pady=0,expand=False,fill='x',side='top')
    def animate_osc(self):
        global myScope
        #Peticion de datos osciloscopio
        data=myScope.query("WAV:DATA?")#Datos extraidos
        data=data.split(',') #Datos array separación
        data= list(data) #Datos del osciloscopio 
        print(data)
        data=data[10:len(data)-1]
        muestra=np.array(data)
        lista_sample=[]
        for k in range(len(muestra)-1):
            lista_sample.append(float(muestra[k]))
        #Parametros Y graficar limpiar - Voltage
        y= [float(x) for x in lista_sample]
        #Parametros de tiempo
        timeoffset = float(myScope.query(":TIM:OFFS?")[0])
        timescale = float(myScope.query(":TIM:SCAL?"))
        time = numpy.linspace(timeoffset  * timescale, 0.0000005+50e-09 * timescale, num=len(y))
        self.line2.set_data(time,y)
        animation.FuncAnimation(self.fig2,self.animate_osc,interval=10,blit=False)
        self.canvas2.draw()