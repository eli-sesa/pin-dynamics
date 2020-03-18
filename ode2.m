function Thetadot = ode2(Theta, t)
  
  global m l a f b I data
  Thetadot = zeros(2,1);
  #We turn the 2nd order nonlinear ode into a coupled set of 2 1st order nonlinear odes.
  
  #ode2 is formulated using a moment of inertia I, rather than a point mass
  Thetadot(1) = (1/I) * (spring_force(Theta(2))*l(2) - 0*m*acc_def(data,t)*l(1)*sin(Theta(2))) * 0.1129848;
  Thetadot(2) = Theta(1);
  
##  if Theta(2) > pi
##    Thetadot = [0, 0];
##  endif
endfunction
