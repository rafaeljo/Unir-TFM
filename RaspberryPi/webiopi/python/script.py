import webiopi
import os
import time

#Usamos la librería de WebIOPi
GPIO = webiopi.GPIO

#definimos las salidas que utilizaremos con los relés
cpuCooler = 10
lamp = 26
relays = [cpuCooler,9,11,5,6,13,19,lamp]

#Y algunas constantes:
cpuTempMax = 50.0
cpuTempMin = 45.0

#Esta funcion es llamada para inicializar el sistema:
def setup():
    for relay in relays:
        GPIO.setup(relay, GPIO.OUT, GPIO.LOW)
        #GPIO.setFunction(relay, GPIO.OUT) #lo establecemos como salida
        #GPIO.digitalWrite(relay, GPIO.LOW) #y establecemos el nivel en bajo

#Esta función es llamada cuando paramos el servicio
def destroy():
    for relay in relays:
        GPIO.digitalWrite(relay, GPIO.HIGH)


#Esta función es llamada contínuamente por el servicio
def loop():
    compruebaTemperatura()
    #dejamos a la CPU hacer otras cosas
    webiopi.sleep(1)

def compruebaTemperatura(min = cpuTempMin, max = cpuTempMax):
        temp = getCPUtemperature()
        #webiopi.debug('Monitorizando para mantenerla entre ', min, 'y', max)
        if temp>= max:        
            webiopi.debug ('Alcanzados los ' + str(temp) + 'ºC, encendiendo el ventilador')
            GPIO.digitalWrite(cpuCooler, GPIO.HIGH)
        elif temp<=min:
            webiopi.debug('Temperatura bajada a' + str(temp) + 'paramos el ventilador')
            GPIO.digitalWrite(cpuCooler, GPIO.LOW)
        time.sleep(5)




@webiopi.macro
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace('temp=','').replace("'C\n","")))


@webiopi.macro
def testReles():
    for relay in relays:
        GPIO.digitalWrite(relay, GPIO.LOW)
        time.sleep(0.5)
        GPIO.digitalWrite(relay, GPIO.HIGH)


                        
