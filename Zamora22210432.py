"""
Práctica 3: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Zamora Chon Michelle Ariadna
Número de control: 22210432
Correo institucional: l22210432@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
import control

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import math

x0, t0, tF, dt, w, h = 0,0,10,1E-3,10,5
N = round((tF-t0)/dt)+1
t = np.linspace(t0, tF, N)
u = np.sin(2*math.pi*95/60*t) + 0.8

def cardio (Z, C, R, L):
    num =[L*R, R*Z]
    den = [C*L*R*Z, L*R+L*Z, R*Z]
    sys = control.tf(num, den)
    return sys

#Funcion de transferencia: individuo hipotenso(caso)
Z, C, R, L =  0.020, 0.250, 0.600, 0.005
sysT = cardio (Z, C, R, L)
print ('INDIVIDUO HIPOTENSO[CASO]:')
print (sysT)

#Funcion de transferencia: individuo normotenso(caso)
Z, C, R, L = 0.033, 1.500, 0.950, 0.010
sysN = cardio (Z, C, R, L)
print ('INDIVIDUO NORMOTENSO[CASO]:')
print (sysN)

#Funcion de transferencia: individuo hipertenso(caso)
Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysH = cardio (Z, C, R, L)
print ('INDIVIDUO HIPERTENSO[CASO]:')
print (sysH)

# Sistema cardiovascular
fig1 = plt.figure(); #plt.rcParams['text.usetex'] = True
ts,Ve = control.forced_response(sysT,t,u,x0)
plt.plot(t,Ve, '--', linewidth=1, color = [252/255, 199/255, 55/255], label = '$P_p(t): HIPOTENSO$')
ts,Vs = control.forced_response(sysN,t,u,x0)
plt.plot(t,Vs, '-', linewidth=1, color =  [242/255, 107/255, 15/255], label = '$P_p(t): NORMOTENSO$')
ts,Ve = control.forced_response(sysH,t,u,x0)
plt.plot(t,Ve, '-.', linewidth=1, color = [126/255, 24/255, 145/255], label = '$P_p(t): HIPERTENSO$')
plt.grid(True)
plt.xlim(0 , 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.5, 2)
plt.xlabel('$t$ $[s]$', fontsize = 11)
plt.ylabel('$V(t)$ $[V]$', fontsize = 11)
plt.title('SISTEMA CARDIOVASCULAR')
plt.legend(bbox_to_anchor=(0.5,-0.23), loc = 'center', ncol=4)
plt.show()
fig1.set_size_inches(w,h)
fig1.tight_layout()
fig1.savefig('sistema_cardiovascular.png', dpi = 600, bbox_inches='tight')
fig1.savefig('sistema_cardiovascular.pdf', dpi = 600, bbox_inches='tight')

