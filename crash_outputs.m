clear all; close all; clc;
global data
data = csvread('50_kph_data.csv');


velocity_kph = [0:20:90]; #[kph]
velocity_kph = 0;

velocity = velocity_kph * 10.9317; #convert kph to in/s

theta_start = deg2rad(92);

t_store = zeros(size(velocity));

for i = 1:length(velocity)
  [theta_model, t_collapse, params] = pin_dynamics_ode_fun(velocity(i), theta_start, PLOT=true);
  t_store(i) = t_collapse;
endfor

x_collapse = velocity .* t_store;

figure
plotyy(velocity_kph, t_store, velocity_kph, x_collapse)

xlabel('velocity [kph]')
legend('collapse time [s]', 'collapse distance [in]')


theta_data = load('pintheta.csv');
t = [0:length(theta_data)-1]' / 250;

plot(t, theta_data)

