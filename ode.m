function Thetadot = ode(Theta, t)
  
  global m l a f b
  Thetadot = zeros(2,1);
  #We turn the 2nd order nonlinear ode into a coupled set of 2 1st order nonlinear odes.
  Thetadot(1) = 1/(m*l(1)^2) * (spring_force(Theta(2))*l(2) - m*a*l(1)*sin(Theta(2)) -b*Theta(1));
  Thetadot(2) = Theta(1);
  
endfunction
