clear all; close all; clc;

#I havent found how to feed functions with optional arguments when solving ODEs
#The fix for now is to just let system paramaters be global variables
global m l a f b I

m = 6.64; #lb mass of the pin assy
l = [sqrt(.3^2 + 1.22^2), 1.283]; #lengths l1, l2 in in
a = 0; #gforce of decel
b = 0; #Damping term to help troubleshoot / simulate mechanism friction
I = 29.98;

#vector of times of interest
t = linspace(0,2, 1001);

#initial condition [thetadot, theta]

#input velocity from the ramp may dominate collapse time

theta0 = [9.323340021, deg2rad(92)];
theta0 = [3.729336009, deg2rad(92)];
theta0 = [0, deg2rad(90)];


#The magic of an ODE Solver
[theta_out, istate, msg] = lsode('ode2', theta0, t);

#Break out into spatial coordinates for visualization
x = l(1)*cos(theta_out(:,2));
y = l(1)*sin(theta_out(:,2));

#plot COM in space  
subplot(131)
plot(x, y, 'o-')
xlabel('x')
ylabel('y')
axis('equal')

#plot theta and thetadot over time
subplot(1,3,[2,3])
plot(t, theta_out(:,2))
hold on 
plot(t, theta_out(:,1))
plot([0,t(end)],[pi, pi])
legend('Angular Position', 'Angular Velocity')
xlabel('t')
ylabel('\Theta')

##figure
##plot(theta_out(:,2), spring_force(theta_out(:,2)))
##title('Spring Force')
##xlabel('\Theta')

#We can find the time at which we hit 180 degrees
objective = abs(theta_out(:,2) - pi);
[d, index] = min(objective);
t_collapse = t(index);

disp('Time to Collapse:'), disp(t_collapse)

##Elis Curiosity Corner.  What typa wiggles we got? (damping seems to introduce 2nd osciliation mode)
##out = fftshift(abs(fft(theta_out(:,1))));
##plot(out,'-o')
