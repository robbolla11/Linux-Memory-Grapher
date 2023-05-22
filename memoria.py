import psutil as pst
import matplotlib.pyplot as plt

def Graph():
    #Obtenemos los procesos activos
    plt.style.use('classic')
    plt.rcParams['figure.facecolor']= '#abc8d9'
    

    procesos = list(pst.process_iter())

    nombreProcesos = []
    memoriaUsada = []
    numeroPIDS = []

    for proceso in procesos:
        try:
            #Obtenemos la info de cada prcoeso y la guardamos
            infoProcesos = proceso.as_dict(attrs=['name', 'pid', 'memory_info'])
            nombreProceso = infoProcesos['name']
            numeroPid = infoProcesos['pid']
            infoMemoria = infoProcesos['memory_info']
            usoMemoriaBytes = infoMemoria.rss  #Nos da los bytes

            nombreProcesos.append(f"{nombreProceso} (PID: {numeroPid})") #AGregamos tanto nombre como PID en caso de nombre igual
            memoriaUsada.append(usoMemoriaBytes)
            numeroPIDS.append(numeroPid)

        except (pst.NoSuchProcess, pst.AccessDenied): #para eliminar procesos que ya no existen o que no podemos acceder
            pass

    #sacamos el total de memoria y con eso vemos que porcentaje ocupa cada uno
    sumaMemoria = pst.virtual_memory().total
    percentages = [(mem_usage / sumaMemoria) * 100 for mem_usage in memoriaUsada]

    #Para poner el limite de 10 procesos mostrados
    NumProcesosGrafica = 10
    acomodarDatos = sorted(zip(nombreProcesos, numeroPIDS, memoriaUsada, percentages), key=lambda x: x[2], reverse=True)
    nombreProcesosAcomodados = [data[0] for data in acomodarDatos[:NumProcesosGrafica]]
    numeroPIDSAcomodados = [data[1] for data in acomodarDatos[:NumProcesosGrafica]]
    memoriaUsadaAcomodadas = [data[2] for data in acomodarDatos[:NumProcesosGrafica]]
    porcentajesAcomodados = [data[3] for data in acomodarDatos[:NumProcesosGrafica]]

    plt.clf()

    #Usando matplotlib creamos la grafica 
   
    
    plt.bar(nombreProcesosAcomodados, memoriaUsadaAcomodadas, color = "#c972d0", width=.9)
    plt.xticks(rotation=90)
    plt.xlabel('Nombre y numero de proceso (PID)')
    plt.ylabel('Uso de memoria') #Intervalos de 100MB
    plt.title('Uso de memoria de procesos')
    
    plt.grid(True)
    plt.rcParams['grid.alpha']= '.4'
    plt.tight_layout()

    #Para mostrar arriba de cada barrita el PID, la memoria usada y el porcentaje que ocupa de memoria
    for i in range(len(numeroPIDSAcomodados)):
        plt.text(i, memoriaUsadaAcomodadas[i]/2, f"PID: '{numeroPIDSAcomodados[i]}'\n{memoriaUsadaAcomodadas[i]/1000000:.2f}MB\n({porcentajesAcomodados[i]:.2f}%)", ha='center', va='bottom', color = 'black', fontsize = 13, fontweight = 'bold')
                                                                                        #Entre 1millon para que sea en MB
    plt.show()

    #Actualizamos cada 5 segundos la grafica
    plt.draw()
    plt.pause(5.0)

#Modo interactivo
plt.ion()

for _ in range(20):
    Graph()

plt.ioff()
plt.close()


Graph()