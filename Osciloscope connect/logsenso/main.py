import requests, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
fig= plt.figure()
ax= fig.add_subplot(1,1,1)
xdatos, ydatos= [],[]
tiempo=0;

while True:
    def animate(tiempo,xdatos,ydatos):

        response = requests.get('http://192.168.1.14/co2')
        ++tiempo
        co2 = int(response.text)
        xdatos.append(tiempo)
        ydatos.append(co2)
        ax.clear()
        ax.plot(xdatos,ydatos)
        ax.plot(xdatos,ydatos, color= 'green') #marker='o' / '^'
        ax.grid(axis='y', color='gray', linestyle='dashed')
        plt.xlabel("Tiempo[s]")
        plt.ylabel("Concentracion de CO2 [ppm]")
        plt.title("Concentración de CO2 vs Tiempo")

        print(co2)
        ani = animation.FuncAnimation(fig,animate,fargs=(xdatos,ydatos))
        plt.show()