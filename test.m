clear all; close all; clc

##Theta = linspace(pi/2, pi);
##FS = []
##for i = 1:length(Theta)
##  
##FS(i) = spring_force(Theta(i))
##endfor
##plot(Theta, FS)

##TEST BREAK

##data = csvread('50_kph_data.csv');
##
##t = linspace(0,1);
##
##
##acc_out = acc_def(data,.1 );
##
##plot(data(:,1), data(:,2),'^')
##hold on
##plot(t, acc_out, '-o')

##thetas = linspace(pi/2, pi)
##for i = 1:length(thetas)
##  fs(i) = spring_force(thetas(i))
##endfor
## 
##plot(rad2deg(thetas), fs)
##hold on
##plot(rad2deg([thetas(1), thetas(end)]),[fs(1), fs(end)])
##
##xlabel('\theta [deg]')
##ylabel('Normal projected spring force [lb]')

t = linspace(0,1)
adata = 1 * rand(1,length(t)) .* sin(rand(1,length(t)) .* t + rand(1,length(t)))
x0 = [1,1,-10]

[x, v] = int2(t, adata, x0)
subplot(311)
plot(t, x)
subplot(312)
plot(t,v)
subplot(313)
plot(t,adata)