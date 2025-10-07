"""
Práctica 1: 

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Nicole Zoe Camacho Quezada
Número de control: 22211747
Correo institucional: L22211747@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl
import math

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N)
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1
u3 = t/tend
u4 = np.sin(m.pi/2*t)


# Componentes del circuito RLC y función de transferencia
R,L,C = 1E3, 2.2E-3, 100E-6
num = [C*L*R, C*R**2+L, R]
den = [3*C*L*R,5*C*R**2+L, 2*R]
sys = ctrl.tf(num,den)
print(f"Funcion de transferencia del sistema: {sys}")

# Componentes del controlador
kI=1599.83389309639
Cr = 1E-6
Re =1/(kI*Cr)
print(f"El valor de capacitancia del capacitor Cr es de {Cr} Faradios.\n")
print(f"El valor de resistencia del resistor Re es de {Re} Ohms.\n ")


numPID = [1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID, denPID)
print(f"Funcion de transferencia del controlador I: {PID} \n")

# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID = ctrl.feedback(X, 1, sign = -1)
print(f"Funcion de transferencia del sistema en lazo cerrado: {sysPID}")

# Estabilidad en lazo abierto
raices_den = np.roots(den)
print(f"Raices: {raices_den}")

# Respuesta del sistema en lazo abierto y en lazo cerrado
clr1 = np.array([119, 190, 240])/255
clr2 = np.array([255, 203, 97])/255
clr3 = np.array([255, 137, 79])/255
clr4 = np.array([138, 166, 36])/255
clr5 = np.array([92, 47, 194])/255
clr6 = np.array([234, 91, 111])/255

_, PAu1 = ctrl.forced_response(sys, t, u1, x0) #Respuesta en lazo abierto al escalon
_, PAu2 = ctrl.forced_response(sys, t, u2, x0) #Respuesta en lazo abierto al impulso
_, PAu3 = ctrl.forced_response(sys, t, u3, x0) #Respuesta en lazo abierto a la rampa
_, PAu4 = ctrl.forced_response(sys, t, u4, x0) #Respuesta en lazo abierto a la funcion sinusoidal

_, pidu1 = ctrl.forced_response(sysPID, t, u1, x0) #Respuesta en lazo cerrado al escalon
_, pidu2 = ctrl.forced_response(sysPID, t, u2, x0) #Respuesta en lazo cerrado al impulso
_, pidu3 = ctrl.forced_response(sysPID, t, u3, x0) #Respuesta en lazo cerrado a la rampa
_, pidu4 = ctrl.forced_response(sysPID, t, u4, x0) #Respuesta en lazo cerrado a la funcion sinusoidal

fg1 = plt.figure() #Respuesta al escalon
plt.plot(t,u1,'-', color = clr1, label = 'Ve(t)') #Entrada
plt.plot(t, PAu1,'--', color = clr2, label = 'Vs(t)') #Respuesta en lazo abierto
plt.plot(t, pidu1,':', linewidth = 4, color = clr6, label = 'PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1)) #De 0 hasta 10 en intervalos de 1
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1)) 
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show() 
fg1.savefig('step_python.pdf', bbox_inches = 'tight')

fg2 = plt.figure() #Respuesta al impulso
plt.plot(t,u2,'-', color = clr1, label = 'Ve(t)') #Entrada
plt.plot(t, PAu2,'--', color = clr2, label = 'Vs(t)') #Respuesta en lazo abierto
plt.plot(t, pidu2,':', linewidth = 4, color = clr6, label = 'PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1)) #De 0 hasta 10 en intervalos de 1
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1)) 
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show() 
fg2.savefig('impulse_python.pdf', bbox_inches = 'tight')

fg3 = plt.figure() #Respuesta a la rampa
plt.plot(t,u3,'-', color = clr1, label = 'Ve(t)') #Entrada
plt.plot(t, PAu3,'--', color = clr2, label = 'Vs(t)') #Respuesta en lazo abierto
plt.plot(t, pidu3,':', linewidth = 4, color = clr6, label = 'PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1)) #De 0 hasta 10 en intervalos de 1
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1)) 
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show() 
fg3.savefig('ramp_python.pdf', bbox_inches = 'tight')

fg4 = plt.figure() #Respuesta a la funcion sinusoidal
plt.plot(t,u4,'-', color = clr1, label = 'Ve(t)') #Entrada
plt.plot(t, PAu4,'--', color = clr2, label = 'Vs(t)') #Respuesta en lazo abierto
plt.plot(t, pidu4,':', linewidth = 4, color = clr6, label = 'PID(t)') #Respuesta en lazo cerrado
plt.xlim(0,10); plt.xticks(np.arange(0,11,1)) #De 0 hasta 10 en intervalos de 1
plt.ylim(-1.2,1.2); plt.yticks(np.arange(-1.2,1.4,0.2)) 
plt.xlabel('t [s]', fontsize = 11)
plt.ylabel('Vi(t) [V]', fontsize = 11)
plt.legend(bbox_to_anchor = (0.5, -0.2), loc = 'center', ncol = 3,
           fontsize = 9, frameon = True)
plt.show() 
fg4.savefig('sin_python.pdf', bbox_inches = 'tight')