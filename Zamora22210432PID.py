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
import control as ctrl

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import math

x0, t0, tF, dt, w, h = 0,0,10,1E-3,10,5
N = round((tF-t0)/dt)+1
t = np.linspace(t0, tF, N)
u = np.sin(2*math.pi*95/60*t) + 0.8

Signal = ["SISTEMA_CARDIOVASCULAR","HIPERTENSO","HIPOTENSO"]
def cardio (Z, C, R, L):
    num =[L*R, R*Z]
    den = [C*L*R*Z, L*R+L*Z, R*Z]
    sys = ctrl.tf(num, den)
    return sys

#Funcion de transferencia: individuo hipotenso(caso)
Z, C, R, L =  0.020, 0.250, 0.600, 0.005
sysT = cardio (Z, C, R, L)
print ('INDIVIDUO HIPOTENSO[CASO]:')
print (sysT)

#Funcion de transferencia: individuo normotenso(caso)
Z, C, R, L = 0.033, 1.500, 0.950, 0.010
sysN = cardio (Z, C, R, L)
print ('INDIVIDUO NORMOTENSO[CONTROL]:')
print (sysN)

#Funcion de transferencia: individuo hipertenso(caso)
Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysH = cardio (Z, C, R, L)
print ('INDIVIDUO HIPERTENSO[CASO]:')
print (sysH)  

# SISTEMA CARDIOVASCULAR
def senales(u,sysT,sysN,sysH,Signal):
    fig=plt.figure()
    
    if Signal=="SISTEMA_CARDIOVASCULAR":
        ts,Vs=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Vs, '--', color =  [252/255, 199/255, 55/255], label = '$P_p(t): HIPOTENSO$')
        ts,Ve=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [242/255, 107/255, 15/255], label = '$P_p(t): NORMOTENSO$')
        ts,Vd=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): HIPERTENSO$')
        
    elif Signal=="HIPOTENSO":
        ts,Ve=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [252/255, 199/255, 55/255], label = '$P_p(t): CONTROL$')
        ts,Vd=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): HIPOTENSO$')
        ts,pid=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,pid, ':',linewidth=3, color =  [242/255, 107/255, 15/255], label = '$Pa(t): TRATAMIENTO$')
        
    elif Signal=="HIPERTENSO":
        ts,Ve=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [252/255, 199/255, 55/255], label = '$P_p(t): CONTROL$')
        ts,Vd=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): HIPERTENSO$')
        ts,pid=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,pid, ':',linewidth=3, color =  [242/255, 107/255, 15/255], label = '$Pa(t): TRATAMIENTO$')

    plt.grid(False)
    plt.xlim(0,10)
    plt.ylim(-0.5,2)
    plt.xticks(np.arange(0,10,1))
    plt.yticks(np.arange(-0.5,2,.5))
    plt.xlabel('$t$ [s]',fontsize=11)
    plt.ylabel('$Pp(t)$ [V]',fontsize=11)
    plt.legend(bbox_to_anchor=(0.5,-0.3),loc='center',ncol=4, fontsize=8,frameon=False)
    plt.show()
    fig.set_size_inches(20,5)
    fig.tight_layout()
    namepng='PYTHON_'+Signal+ '.png'
    namepdf='PYTHON_'+Signal+ '.pdf'
    fig.savefig(namepng,dpi=600,bbox_inches='tight')
    fig.savefig(namepdf,bbox_inches='tight')
    fig.savefig('.pdf',bbox_inches='tight')

def tratamiento (sys): 
        Cr=10E-6
        Ki=1035.71406250139
        Kp=8.92851562535347e-05
        Re=1/(Ki*Cr)
        Rr=Kp*Re
        numPI=[Rr*Cr,1]
        denPI=[Re*Cr,0]
        PID=ctrl.tf(numPI,denPI)
        X = ctrl.series(PID,sysN)
        sys=ctrl.feedback(X,1,sign=-1)
        return sys
    
#Sistema de control en lazo cerrado
sysPID=tratamiento(sysH)
senales(u,sysT,sysN,sysH,"SISTEMA_CARDIOVASCULAR")
senales(u,sysN,sysT,sysPID,"HIPOTENSO")
senales(u,sysN,sysH,sysPID,"HIPERTENSO")

