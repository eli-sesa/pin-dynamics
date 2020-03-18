function [theta_out, t_collapse, params] = pin_dynamics_ode_fun(trigger_velocity, theta_start, PLOT=true)
  #function finds time to collapse given an assumed skate velocity [in/s],
  #and rotation after ramp contact [rad].  It then computes an input angular velocityand uses that to simulate mechanism collapse.  At this time, no acceleration field is supported'''
  
  
  #I havent found how to feed functions with optional arguments when solving ODEs
  #The fix for now is to just let system paramaters be global variables
  global m l a f b I

  m = 6.64; #lb mass of the pin assy
  l = [sqrt(.3^2 + 1.22^2), 1.283]; #lengths l1, l2 in inches
  a = 0; #gforce of decel
  #b = 0; #Damping term to help troubleshoot / simulate mechanism friction
  I = 29.98;
  I = .0087743;

  params = [m, l, a, b, I];
  
  ramp_length = 130/25.4;# ramp length in inches (assumption)
  
  if trigger_velocity == 0
    t_ramp = 0;
    theta_dot_0 = 0;
  else
    #time to traverse ramp.  Assume constant velocity over some distance
    t_ramp = ramp_length / trigger_velocity;
    #Find intial angular velocity.  IMPORTANT to find angle from 90deg.  Bug from that
    theta_dot_0 = (theta_start-pi/2)/t_ramp;
  endif
  
  #vector of times of interest
##  t = linspace(t_ramp, 1.1, 501);
  t = linspace(0, .1, 501);
  t = [0:25] / 250;
  #initial condition [thetadot, theta]
  
  theta0 = [theta_dot_0, theta_start];

  #The magic of an ODE Solver
  [theta_out, istate, msg] = lsode('ode2', theta0, t);

  #Break out into spatial coordinates for visualization
  x = l(1)*cos(theta_out(:,2));
  y = l(1)*sin(theta_out(:,2));
  
  objective = abs(theta_out(:,2) - pi);
  [d, index] = min(objective);
  t_collapse = t(index);
  
  if PLOT
    figure
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
    disp('Time to Collapse:'), disp(t_collapse)
    
  endif
  #We can find the time at which we hit 180 degrees

  ##Elis Curiosity Corner.  What typa wiggles we got? (damping seems to introduce 2nd osciliation mode)
  ##out = fftshift(abs(fft(theta_out(:,1))));
  ##plot(out,'-o')
endfunction