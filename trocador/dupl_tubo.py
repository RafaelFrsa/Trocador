# -*- coding: cp1252 -*-
# Módulo de Equações para Trocadores de Calor Duplo-Tubo

from math import *

# Fluido1 arbitrado como o tubo interno
fluido1={'Vazao':0,'T_entr':0,'T_said':0,'cp':0,'k':0,'Pr':0,'Viscos':0,
         'Densidade':0,'Diam_ext':0,'Diam_int':0,'Annulus':0,'Líquido':0,'Viscos_tw':0}

# FLuido2 arbitrado como a região anular
fluido2={'Vazao':0,'T_entr':0,'T_said':0,'cp':0,'k':0,'Pr':0,'Viscos':0,
         'Densidade':0,'Diam_ext':0,'Diam_int':0,'Annulus':0,'Líquido':0,'Viscos_tw':0}
material={'K':0,'L':1, 'Fouling factor':0,'Calor_cnste':0, 'Tw':(fluido1['T_entr']+fluido2['T_said']+fluido2['T_entr']+fluido2['T_said'])/4}


#for p in [fluido1,fluido2]:
#    for chave in p.keys():
#        p[chave]=input('Insira %s: '%chave)

def Pressure_drop_serth(fluido,material,diam_h=0):
# s --> gravidade específica, s=(densidade do fluido)/(densidade da água) ## coisa do Serth --;
# r --> Return bends, n --> nozzle losses; Serth pg. 154
    s=fluido['Densidade']/1000;G=fluido['Vazao']/fluido['Area_h']
    if fluido['Re']<4000:
        f=16/fluido['Re']
        material[u'\u0394Pn']=(15**-4)*(material['Num_gramp'])*(G**2)/s
        if fluido['Annulus']==1:
            f*=1.5 #Serth pg 113
            material[u'\u0394Pr2']=(6*10**-4)*(material['Num_gramp']*2-1)*G**2/s
        else:
            material[u'\u0394Pr1']=(7.5*10**-4)*(material['Num_gramp']*2-1)*(G**2)/s
#    elif fluido['Re']>=4000 and fluido['Re']<=10**5:
#        f=0.079*(fluido1['Re']**-0.25)
    else:
        f=0.00140+0.125*fluido['Re']**-0.32
        material[u'\u0394Pn']=(7.5*10**-4)*(material['Num_gramp'])*G**2/s
        if fluido['Annulus']==1:
            material[u'\u0394Pr2']=(6*10**-4)*(material['Num_gramp']*2-1)*G**2/s
        else:
            material[u'\u0394Pr1']=(7.5*10**-4)*(material['Num_gramp']*2-1)*(G**2)
    if fluido['Annulus']==0:
        fluido[u'\u0394P']=(4*f*2*material['L']*material['Num_gramp']*fluido['Densidade']*fluido['Vel_m']**2)/(2*fluido['Diam_int'])
        fluido[u'\u0394Ptotal']=fluido[u'\u0394P']+ material[u'\u0394Pr1']
    else:
        fluido[u'\u0394P']=(8*f*material['L']*material['Num_gramp']*fluido['Densidade']*fluido['Vel_m']**2)/(2*diam_h)
        fluido[u'\u0394Ptotal']=fluido[u'\u0394P']+ material[u'\u0394Pr2']+material[u'\u0394Pn']
    return fluido, material


def desvio(dados):
	"Retira os dados que se afastam muito da média do conjunto"
	desvio={};med=sum(dados.values())/len(dados);M=max(dados.values())
	if abs(med-M)/med>0.4:
		for d in dados.keys():
			if dados[d]==M: del dados[d]
	med=sum(dados.values())/len(dados)
	for p in dados.keys():desvio[p]=abs(med-dados[p])/med
	for p in desvio.keys():
		if desvio[p]>0.3: del dados[p]
	return dados

def calor_vazao(fluido1,fluido2):
    '''Calor Cedido igual o calor recebido pelos fluidos'''
    cp1=fluido1['cp'];cp2=fluido2['cp']
    if fluido1['Vazao']==0:
        fluido1['Vazao']=(float(fluido2['Vazao'])*cp2*abs(fluido2['T_entr']-fluido2['T_said']))/(cp1*abs(fluido1['T_entr']-fluido1['T_said']))
    elif fluido2['Vazao']==0:
        fluido2['Vazao']=(float(fluido1['Vazao'])*cp1*abs(fluido1['T_entr']-fluido1['T_said']))/(cp2*abs(fluido2['T_entr']-fluido2['T_said']))
    elif fluido1['T_said']==0:
        fluido1['T_said']=fluido1['T_entr']+(float(fluido2['Vazao'])*cp2*abs(fluido2['T_entr']-fluido2['T_said']))/(fluido1['Vazao']*cp1)
    elif fluido2['T_said']==0:
        fluido2['T_said']=fluido2['T_entr']+(float(fluido1['Vazao'])*cp1*abs(fluido1['T_entr']-fluido1['T_said']))/(fluido2['Vazao']*cp2)
    elif fluido1['T_entr']==0:
        fluido1['T_entr']=fluido1['T_said']-((float(fluido2['Vazao'])*cp2*abs(fluido2['T_said']-fluido2['T_entr']))/(fluido1['Vazao']*cp1))
    elif fluido2['T_entr']==0:
        fluido2['T_entr']=fluido2['T_said']-((float(fluido1['Vazao'])*cp1*abs(fluido1['T_said']-fluido1['T_entr']))/(fluido2['Vazao']*cp2))
    return None  

def reynolds_tube(fluido1,fluido2):
#    if fluido1['Annulus']==True:
#        A=pi*(pow(fluido1['Diam_int'],2)-pow(fluido2['Diam_ext'],2))/4
#        diam_h=fluido1['Diam_int']-fluido2['Diam_ext']
#        vel=fluido1['Vazao']/(fluido1['Densidade']*A)
#        fluido1['Re']=fluido1['Densidade']*vel*diam_h/fluido1['Viscos']
#        fluido2['Re']=4*fluido2['Vazao']/(pi*fluido2['Viscos']*fluido2['Diam_int'])
#    if fluido1['Annulus']==False:
    fluido2['Area_h']=pi*(pow(fluido2['Diam_int'],2)-pow(fluido1['Diam_ext'],2))/4;#print 'Ap-->%.12f'%A
    fluido1['Area_h']=pi*(fluido1['Diam_int']**2)/4
    diam_h=fluido2['Diam_int']-fluido1['Diam_ext'];#print 'Dh-->%.12f'%diam_h# Causa1 ==> obs.: Kern usa o diâmetro equivalente
#KAKAÇ E LIU, PG. 87, DESCRIÇÃO DO MOTIVO DE DIAMETRO HIDRÁULICO
    fluido2['Vel_m']=fluido2['Vazao']/(fluido2['Densidade']*fluido2['Area_h'])
    fluido1['Vel_m']=fluido1['Vazao']/(fluido1['Densidade']*pi*fluido1['Diam_int']**2/4)
    fluido2['Re']=fluido2['Densidade']*fluido2['Vel_m']*diam_h/fluido2['Viscos']
    fluido1['Re']=4*fluido1['Vazao']/(pi*fluido1['Viscos']*fluido1['Diam_int'])
    return fluido1['Re'],fluido2['Re']
    
def nusselt_tube(fluido1,fluido2,material):
    
#    Pr,Re,diam,L=1,fl=True,vis_tm=1,vis_tw=1,calor_cnste=False,annulus=False,do=1,D_i=1
    Pr=fluido1['Pr'];Re=fluido1['Re'];diam=fluido1['Diam_int'];L=material['L'];
    fl=fluido1['Líquido'];vis_tm=fluido1['Viscos'];vis_tw=fluido1['Viscos_tw']
    calor_cnste=material['Calor_cnste'];annulus=fluido1['Annulus']
    Pe=Re*Pr
    if annulus==True: do=fluido2['Diam_int'];D_i=fluido1['Diam_int']
#Equação 3.8
#Equação utilizada para escoamento de fluidos incompressíveis, em regime laminar,
#em um duto circular com uma condição limite de temperatura constante na parede,
#indicado pelo subscrito T, utilizada para 0.1<(Pe*diam/L)<10000"""
    if Re<=2100:
        nusselts={}
        if (Pe*diam/L)>1000 and (Pe*diam/L)<10000:
            Nu_T=(1.61)*((Pe*diam/L)**(1/3.))
            nusselts["Nu_T(Eq. 3.8)"]=Nu_T
#Equação 3.9:
#Correlação empírica desenvolvida por Hausen para as mesmas condições da equação 3.8, descrita a abaixo:
#'Equação 3.8
#Equação utilizada para escoamento de fluidos incompressíveis, em regime laminar,
#em um duto circular com uma condição limite de temperatura constante na parede,
#indicado pelo subscrito T, utilizada para 0.1<(Pe*diam/L)<10000
        if (Pe*diam/L)>0.1 and (Pe*diam/L)<10**4:
            Nu_T=3.66+(0.19*((Pe*diam/L)**0.8))/(1+0.117*((Pe*diam/L)**0.467))
            nusselts["Nu_T(Eq. 3.9)"]=Nu_T
#Equação 3.11:
#Equação utilizada considerando escoamento em regime laminar de fluidos
#incompressíveis, com a condição limite de fluxo constante de calor pela parede, subscrito H,
#geralmente realizados com as propriedades do fluido na temperatura média dos fluidos (KAKAÇ e LIU, 2002)"""
        if (Pe*diam/L)>100 and calor_cnste==True:
            Nu_H=1.953*(pow(Pe*diam/L,1/3.))
            nusselts["Nu_H(Eq. 3.11)"]=Nu_H
#Equação 3.13 - Usada para escoamento em desenvolvimento simultâneo em tubos lisos
        if (Pr)>0.5 and (Pr)<500 and (Pe*diam/L)>1000:
            Nu_T=0.664*((Pe*diam/L)**0.5)*((Pe/Re)**(-1/6.))
            nusselts["Nu_T(Eq. 3.13)"]=Nu_T
#Equação 3.24 - Utilizada para escoamento laminar de LÍQUIDOS'''
        if (((Pe*diam/L)**(1./3))*((vis_tm/vis_tw)**0.14))>=2 and (vis_tm/vis_tw)>4.4*10**-3 and (vis_tm/vis_tw)<9.75:
            Nu_T=1.86*(pow(Pe*diam/L,1/3.0))*(pow(vis_tm/vis_tw,0.14))
            nusselts["Nu_T(Eq. 3.24)"]=Nu_T
        if (Pe*diam/L)<100 and calor_cnste==True:
            Nu_H=4.36
            nusselts["Nu_H"]=Nu_H
        if annulus==True:
            d_ext=fluido2['Diam_ext']
            if calor_cnste==True:
                g=1+0.14*pow(d_ext/D_i,-1/2.);diam_h=D_i-do
                Nu_H=(1.86*pow(Pe*diam/L,1./3)*pow(vis_tm/vis_tw,0.14))+((0.19*pow(Pe*diam_h/L,0.8))/(1+(0.117*pow(Pe*diam_h/L,0.467))))*g
                nusselts['Nu_H (Eq. 3.20a)']=Nu_H
            if calor_cnste==False:
                g=1+0.14*pow(d_ext/D_i,0.1);diam_h=D_i-do
                Nu_H=(1.86*pow(Pe*diam/L,1./3)*pow(vis_tm/vis_tw,0.14))+((0.19*pow(Pe*diam_h/L,0.8))/(1+(0.117*pow(Pe*diam_h/L,0.467))))*g
                nusselts['Nu_H (Eq. 3.20b)']=Nu_H
        else:
            if (Pe*diam/L)>0.1 and (Pe*diam/L)<100:
                Nu_T=3.66
                nusselts["Nu_T(Eq. 3.7)"]=Nu_T
# Para gases, não há correção do número de Nusselt, n = 0.
    if Re>=10000:
        nusselts={}
        if fl==True:
            if Pr>0.1 and Pr<10000:
                m=0.88-0.24/(4+Pr)
                n=1/3.+0.5*pow(e,-0.6*Pr)
                Nu=5+0.015*pow(Re,m)*pow(Pr,n)
                nusselts['Nu (Eq. 3.30)']=Nu
        if fl==False:
            if Pr>0.5 and Pr<1:
                Nu=0.022*pow(Re,0.8)*(Pr,0.5)
                nusselts['Nu (Caso 7 - Tabela 3.3)']=Nu
    if Re>2100 and Re<10000:
        nusselts={}
        if  Pr>0.5 and Pr<2000:
            f=pow((1.58*log(Re,e)-3.28),-2)
            Nu=((f/2)*(Re-1000)*Pr)/(1+12.7*pow(f/2,1./2)*(pow(Pr,2/3.)-1))
            nusselts["Nu (Eq. 3.31)"]=Nu
    desvio(nusselts)
    Nu=max(nusselts.values());fluido1['Nu']=Nu
    return fluido1























    

