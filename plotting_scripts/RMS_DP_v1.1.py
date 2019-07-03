#!/usr/bin/python  

## RMS.py  AUG 2011 Bryan Putnam

## Program finds the RMS innovation and spread for the background 
## forecast and analysis of EnKF cycles for a given radar and given
## number of cycles. 

import os,sys,string,time,dircache,shutil,stat,pty,popen2 
import matplotlib.pyplot as plt 

from operator import *


#select the directory to work in
homedir = './'

#select the radar to get the results for:
radar = 'KOUN'

#does this file contain dual-pol variables?
dp = 'False'

#give the experiment name (files are placed in this folder in the working directory) 
exp_list = ['dbz_15min'] 

#number of experiments
n_exps = len(exp_list) 


#list the times to get the results for:

#may 10 case 
#times = ['021870','022140','022410','022680','022950','023220','023490','023760','024300','024570','024840','025110','025380','025650','025920','026190','026460','026730','027000']

#utc_times = ['210430','211800','213130','214500','215830','221200','222530','223900']

#time_dist = 270

#may 10 case OU_prime 
#times = ['025380','025650','025920','026190','026460','026730','027000']
#utc_times = ['220300','221630','223000']
#time_dist = 270

#may 20 case
#output times 
times = ['002200','002205','002210','002215','002220','002225','002230','002235','002240','002245','002250','002255']

#times for x axis 
utc_times = ['2200','2215','2230','2245']

time_dist = 15

#whether addtiive noise or multiplicative inflation method is used (i.e. these produce 'bfinf' files)
inf = 0


#duplicate time array for sawtooth plots
int_times = []
saw_tooth_times = []
for t in range(0,len(times),1):
  int_times.append(int(times[t])) 
  saw_tooth_times.append(int(times[t]))
  saw_tooth_times.append(int(times[t])) 


#Initialize arrays

bginvZ = [[] for i in range(n_exps)] #RMS innovation of background forecast for Z
bginvV = [[] for i in range(n_exps)] #RMS innovation of background forecast for Vr
bginvZdr = [[] for i in range(n_exps)] #RMS innovation of background forecast for Zdr
bginvKdp = [[] for i in range(n_exps)] #RMS innovation of background forecast for Kdp

anainvZ = [[] for i in range(n_exps)] #RMS innovation of analysis for Z
anainvV = [[] for i in range(n_exps)] #RMS innovation of analysis for Vr
anainvZdr = [[] for i in range(n_exps)] #RMS innovation of analysis for Zdr
anainvKdp =[[] for i in range(n_exps)] #RMS innovation of analysis for Kdp 

bganaZ = [[] for i in range(n_exps)] #RMS background and analysis for Z
bganaV = [[] for i in range(n_exps)] #RMS background and analysis for Vr
bganaZdr = [[] for i in range(n_exps)] #RMS background and analysis for Zdr
bganaKdp = [[] for i in range(n_exps)] #RMS background and analysis for Kdp 

bgsprdZ = [[] for i in range(n_exps)] #RMS spread of background forecast for Z
bgsprdV = [[] for i in range(n_exps)] #RMS spread of background forecast for Vr
bgsprdZdr = [[] for i in range(n_exps)] #RMS spread of background forecast for Zdr
bgsprdKdp = [[] for i in range(n_exps)] #RMS spread of background forecast for Kdp

anasprdZ = [[] for i in range(n_exps)] #RMS spread of analysis for Z
anasprdV = [[] for i in range(n_exps)] #RMS spread of analysis for Vr
anasprdZdr = [[] for i in range(n_exps)] #RMS spread of analysis for Zdr
anasprdKdp = [[] for i in range(n_exps)] #RMS spread of analysis for Kdp 

bganasprdZ = [[] for i in range(n_exps)] #background and analysis spread for Z

bganasprdV = [[] for i in range(n_exps)] #background and analysis spread for V

bganasprdZdr = [[] for i in range(n_exps)] #background and analysis spread for Zdr 
bganasprdKdp = [[] for i in range(n_exps)] #background and analysis spread for Kdp 

Z_consist = [[] for i in range(n_exps)]  #consistency ratios for Z
V_consist = [[] for i in range(n_exps)]  #consistency ratios for V
Zdr_consist = [[] for i in range(n_exps)] #consistency ratios for Zdr
Kdp_consist = [[] for i in range(n_exps)] #consistency ratios for Kdp 


#get the stat data

for exp in range(0,n_exps,1): 
  for t in times:

    exp_name = exp_list[exp] 

    #analysis innovation file
    anainvZfile = homedir + exp_name + '/' + radar + 'rmsdan' + t

    #analysis spread file
    anasprdZfile = homedir + exp_name + '/' + radar + 'spreadana' + t

    if inf == 0:    #ENKF without inflation (i.e. using relaxation method) 
      #background innovation file
      bginvZfile = homedir + exp_name + '/' + radar + 'rmsdbg' + t
      #background spread file
      bgsprdZfile = homedir + exp_name + '/' + radar + 'spreadfcs' + t
      #consistency 
      consistfile = homedir + exp_name + '/' + radar + 'innov' + t 
    else:
      #background innovation file
      bginvZfile = homedir + exp_name + '/' + radar + 'rmsdbg_bfinf' + t
      #background spread file 
      bgsprdZfile = homedir + exp_name + '/' + radar + 'spread_bfinf' + t
      #consistency 
      consistfile = homedir + exp_name + '/' + radar + 'innov_bfinf' + t  
 
    thisFile = open(bginvZfile, 'r')
    thisFile.seek(16)
    bginvZ_in = thisFile.read(16)
    bginvZ[exp].append(float(bginvZ_in.strip())) 
    thisFile.seek(0)
    bginvV_in = thisFile.read(16)
    bginvV[exp].append(float(bginvV_in.strip()))
    if(dp == 'True'):
      thisFile.seek(45)
      bginvZdr_in = thisFile.read(16)
      bginvZdr[exp].append(float(bginvZdr_in.strip()))
      #thisFile.next() 
      #bginvKdp_in = thisFile.read(16) 
      #bginvKdp[exp].append(float(bginvKdp_in.strip())) 
    thisFile.close() 

    

    thisFile = open(anainvZfile,'r')
    thisFile.seek(16)
    anainvZ_in = thisFile.read(16)
    anainvZ[exp].append(float(anainvZ_in.strip()))
    thisFile.seek(0)
    anainvV_in = thisFile.read(16)
    anainvV[exp].append(float(anainvV_in.strip()))
    if(dp == 'True'):
      thisFile.seek(45)
      anainvZdr_in = thisFile.read(16)
      anainvZdr[exp].append(float(anainvZdr_in.strip()))
      #thisfile.next()
      #anainvKdp_in = thisFile.read(16)
      #anainvKdp[exp].append(float(anainvKdp_in.strip()))
    thisFile.close()

    #create duplicate lists for sawtooth plots 
    bganaZ[exp].append(float(bginvZ_in.strip()))
    bganaZ[exp].append(float(anainvZ_in.strip()))

    bganaV[exp].append(float(bginvV_in.strip()))
    bganaV[exp].append(float(anainvV_in.strip()))
  

    if(dp == 'True'):
      bganaZdr[exp].append(float(bginvZdr_in.strip()))
      bganaZdr[exp].append(float(anainvZdr_in.strip()))

      #bganaKdp[exp].append(float(bginvKdp_in.strip()))
      #bganaKdp[exp].append(float(anainvKdp_in.strip()))



    thisFile = open(bgsprdZfile,'r')
    thisFile.seek(16)
    bgsprdZ_in = thisFile.read(16)
    bgsprdZ[exp].append(float(bgsprdZ_in.strip()))
    thisFile.seek(0)
    bgsprdV_in = thisFile.read(16)
    bgsprdV[exp].append(float(bgsprdV_in.strip()))
    if(dp == 'True'):
      thisFile.seek(45)
      bgsprdZdr_in = thisFile.read(16)
      bgsprdZdr[exp].append(float(bgsprdZdr_in.strip()))
      #next(thisFile)
      #bgsprdKdp_in = thisFile.read(16)
      #bgsprdKdp[exp].append(float(bgsprdKdp_in.strip()))
    thisFile.close()
 
    thisFile = open(anasprdZfile,'r')
    thisFile.seek(16)
    anasprdZ_in = thisFile.read(16)
    anasprdZ[exp].append(float(anasprdZ_in.strip()))
    thisFile.seek(0)
    anasprdV_in = thisFile.read(16)
    anasprdV[exp].append(float(anasprdV_in.strip()))
    if(dp == 'True'):
      thisFile.seek(45)
      anasprdZdr_in = thisFile.read(16)
      anasprdZdr[exp].append(float(anasprdZdr_in.strip()))
      #next(thisFile)
      #anasprdKdp_in = thisFile.read(16)
      #anasprdKdp[exp].append(float(anasprdKdp_in.strip()))
    thisFile.close()

    bganasprdZ[exp].append(float(bgsprdZ_in.strip()))
    bganasprdZ[exp].append(float(anasprdZ_in.strip()))

    bganasprdV[exp].append(float(bgsprdV_in.strip()))
    bganasprdV[exp].append(float(anasprdV_in.strip()))

    if(dp == 'True'):
      bganasprdZdr[exp].append(float(bgsprdZdr_in.strip()))
      bganasprdZdr[exp].append(float(anasprdZdr_in.strip()))

      #bganasprdKdp[exp].append(float(bgsprdKdp_in.strip()))
      #bganasprdKdp[exp].append(float(anasprdKdp_in.strip()))

    thisFile = open(consistfile,'r')
    thisFile.seek(16)
    Z_consist_in = thisFile.read(16)
    Z_consist[exp].append(float(Z_consist_in.strip()))
    thisFile.seek(0)
    V_consist_in = thisFile.read(16)
    V_consist[exp].append(float(V_consist_in.strip()))
    if(dp == 'True'):
      thisFile.seek(45)
      Zdr_consist_in = thisFile.read(16)
      Zdr_consist[exp].append(float(Zdr_consist_in.strip()))
      #next(thisFile)
      #Kdp_consist_in = thisFile.read(16)
      #Kdp_consist[exp].append(float(Kdp_consist_in.strip())) 
    thisFile.close()
 
#end time loop

#get value range for plotting
for exp in range(0,n_exps,1): 

  sprdzmin = min(bganasprdZ[exp]) - 1.0
  sprdzmax = max(bganasprdZ[exp]) + 1.0
  sprdvmin = min(bganasprdV[exp]) - 1.0
  sprdvmax = max(bganasprdV[exp]) + 1.0 

  ylimminZ = min(bganaZ[exp]) - 1.0
  ylimminV = min(bganaV[exp]) - 1.0
  ylimmincZ = min(Z_consist[exp]) - 1.0
  ylimmincV = min(V_consist[exp]) - 1.0
  ylimmaxZ = max(bganaZ[exp]) + 1.0
  ylimmaxV = max(bganaV[exp]) + 1.0
  ylimmaxcZ = max(Z_consist[exp]) + 1.0
  ylimmaxcV = max(V_consist[exp]) + 1.0
  
  ylimminZ = min(ylimminZ,sprdzmin)
  ylimmaxZ = max(ylimmaxZ,sprdzmax)

  ylimminV = min(ylimminV,sprdvmin)
  ylimmaxV = max(ylimmaxV,sprdvmax)
   


  if(dp == 'True'):
 
    sprdzdrmin = min(bganasprdZdr[exp]) - 1.0
    sprdzdrmax = max(bganasprdZdr[exp]) + 1.0
    #sprdkdpmin = min(bganasprdKdp[exp]) - 1.0
    #sprdkdpmax = max(bganasprdKdp[exp]) + 1.0

    ylimminZdr = min(bganaZdr[exp]) - 1.0
    #ylimminKdp = min(bganaKdp[exp]) - 1.0
    ylimmincZdr = min(Zdr_consist[exp]) - 1.0
    #ylimmincKdp = min(Kdp_consist[exp]) - 1.0
    ylimmaxZdr = max(bganaZdr[exp]) + 1.0
    #ylimmaxKdp = max(bganaKdp[exp]) + 1.0
    ylimmaxcZdr = max(Zdr_consist[exp]) + 1.0
    #ylimmaxcKdp = max(Kdp_consist[exp]) + 1.0


    ylimminZdr = min(ylimminZdr,sprdzdrmin)
    ylimmaxZdr = max(ylimmaxZdr,sprdzdrmax)
    #ylimminKdp = min(ylimminKdp,sprdkdpmin)
    #ylimmaxKdp = max(ylimmaxKdp,sprdkdpmax) 

int_time_length = len(int_times) 
time_length = len(saw_tooth_times) 


#plot the RMSI and spread sawtooth plots

#create a list of 1s to plot optimal consistency ratio
one_list = []
for t in times:
  one_list.append(1.0) 

#create a list of several colors for each experiment 
color_list = ['#000000','#FF0000','#0000CD','#008000','#FFA500','#800080']
fig1 = plt.figure(1)
for exp in range(0,n_exps,1): 
  plt.plot(saw_tooth_times,bganaZ[exp],color = color_list[exp],linewidth = 3.0,label = exp_list[exp])
  plt.plot(saw_tooth_times,bganasprdZ[exp],'--',color = color_list[exp],linewidth = 3.0)
plt.xlim(saw_tooth_times[0],saw_tooth_times[time_length-1])
plt.xticks(range(saw_tooth_times[0],saw_tooth_times[time_length-1]+time_dist,time_dist*2),utc_times) 
plt.ylim(ylimminZ,ylimmaxZ) 
#plt.legend(loc = 'upper right')
plt.xlabel('Time (UTC)')
plt.ylabel('RMSI')
plt.title('Z (dBZ)')

plt.savefig('Z RMSI', figsize = (13, 13), dpi=300)
plt.show()

fig2 = plt.figure(2)
for exp in range(0,n_exps,1):
  plt.plot(int_times,Z_consist[exp],color = color_list[exp],linewidth = 3.0,label = exp_list[exp])
plt.plot(int_times,one_list,color = '#8b8989',linewidth = 3.0)
plt.xlim(int_times[0],int_times[int_time_length-1])
plt.xticks(range(int_times[0],int_times[int_time_length-1]+time_dist,time_dist*2),utc_times)
plt.ylim(ylimmincZ,ylimmaxcZ)
#plt.legend(loc = 'upper right')
plt.xlabel('Time (UTC)')
plt.ylabel('Consistency Ratio')
plt.title('Z (dBZ)')

plt.savefig('Z Consistency Ratio', figsize = (13, 13), dpi=300)
plt.show()


fig3 = plt.figure(3)
for exp in range(0,n_exps,1):
  plt.plot(saw_tooth_times,bganaV[exp],color = color_list[exp],linewidth = 3.0, label = exp_list[exp])
  plt.plot(saw_tooth_times,bganasprdV[exp],'--',color = color_list[exp],linewidth = 3.0)
plt.xlim(saw_tooth_times[0],saw_tooth_times[time_length-1])
plt.xticks(range(saw_tooth_times[0],saw_tooth_times[time_length-1]+time_dist,time_dist*2),utc_times)
plt.ylim(ylimminV,ylimmaxV)
#plt.legend(loc = 'upper right')
plt.xlabel('Time (UTC)')
plt.ylabel(radar)
plt.title('V (m/s)')

plt.savefig('Vr RMSI', figsize = (13, 13), dpi=300)
plt.show()

fig4 = plt.figure(4)
for exp in range(0,n_exps,1):
  plt.plot(int_times,V_consist[exp],color = color_list[exp],linewidth = 3.0, label = exp_list[exp])
plt.plot(int_times,one_list,color = '#8b8989',linewidth = 3.0)
plt.xlim(int_times[0],int_times[int_time_length-1])
plt.xticks(range(int_times[0],int_times[int_time_length-1]+time_dist,time_dist*2),utc_times)
plt.ylim(ylimmincV,ylimmaxcV)
#plt.legend(loc = 'upper right')
plt.xlabel('Time (UTC)')
plt.ylabel('Consistency Ratio')
plt.title('V (m/s)')

plt.savefig('Vr Consistency Ratio', figsize = (13, 13), dpi=300)
plt.show()


if(dp == 'True'):
  fig5 = plt.figure(5)
  for exp in range(0,n_exps,1):
    plt.plot(saw_tooth_times,bganaZdr[exp],color_list[exp],linewidth = 3.0, label = exp_list[exp])
    plt.plot(saw_tooth_times,bganasprdZdr[exp],'--',color = color_list[exp],linewidth = 3.0)
  plt.xlim(saw_tooth_times[0],saw_tooth_times[time_length-1])
  plt.xticks(range(saw_tooth_times[0],saw_tooth_times[time_length-1]+time_dist,time_dist*2),utc_times)
  plt.ylim(ylimminZdr,ylimmaxZdr)
  #plt.legend(loc = 'upper right')
  plt.xlabel('Time (UTC)')
  plt.ylabel('RMSI')
  plt.title('ZDR (dB)')

  plt.show() 

  fig6 = plt.figure(6)
  for exp in range(0,n_exps,1):
    plt.plot(int_times,Zdr_consist[exp],color_list[exp],linewidth = 3.0, label = exp_list[exp])
  plt.plot(int_times,one_list,color = '#000000',linewidth = 3.0)
  plt.xlim(int_times[0],int_times[int_time_length-1])
  plt.xticks(range(int_times[0],int_times[int_time_length-1]+time_dist,time_dist*2),utc_times)
  plt.ylim(ylimmincZdr,ylimmaxcZdr)
 # plt.legend(loc = 'upper right')
  plt.xlabel('Time (UTC)')
  plt.ylabel('Consistency Ratio')
  plt.title('ZDR (dB)')

  plt.show()

#  fig7 = plt.figure(7)
#  for exp in range(0,n_exps,1):
#    plt.plot(saw_tooth_times,bganaKdp[exp],color_list[exp],linewidth = 3.0, label = exp_list[exp])
#    plt.plot(saw_tooth_times,bganasprdKdp[exp],'--',color = color_list[exp],linewidth = 3.0)
#  plt.xlim(saw_tooth_times[0],saw_tooth_times[time_length-1]) 
#  plt.xticks(range(saw_tooth_times[0],saw_tooth_times[time_length-1]+time_dist,time_dist*3),utc_times)
#  plt.ylim(ylimminKdp,ylimmaxKdp)
#  plt.legend(loc = 'upper right') 
#  plt.xlabel('Time')
#  plt.ylabel('RMSI')
#  plt.title('KDP (deg/km)')

#  plt.show() 

#  fig8 = plt.figure(8)
#  for exp in range(0,n_exps,1):
#    plt.plot(int_times,bganaKdp[exp],color_list[exp],linewidth = 3.0, label = exp_list[exp])
#  plt.plot(int_times,one_list,color = '#000000',linewidth = 3.0)
#  plt.xlim(int_times[0],int_times[int_time_length-1])
#  plt.xticks(range(int_times[0],int_times[int_length-1]+time_dist,time_dist*3),utc_times)
#  plt.ylim(0,2)
#  plt.legend(loc = 'upper right')
#  plt.xlabel('Time')
#  plt.ylabel('Consistency Ratio')
#  plt.title('KDP (deg/km)')
#
#  plt.show()

