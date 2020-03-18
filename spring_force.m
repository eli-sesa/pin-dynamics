function fs = spring_force(Theta)
  
  global m l a f b I
  
  k = 31; #spring rate lb/in  9654K637 
  f0 = 89; #Assume spring totally extended and at max force at theta=0
  ls = 2*.135 + [4.73, 6.13, 7.43];
  fs = [0, 8, 89];
 
  #lets setup some initial geometry for use in computation
  l_spring0 = 6.830; #distance from spring piviot to sheave top when locked
  
  #spring piviot arm geom
  x0 = -.083;
  y0 = -1.281;
  l_arm = sqrt(x0^2 + y0^2);
  
  #piviot to spring piviot locations
  xg = 6.485;
  yg = .463 + .130;
  
  theta_arm0  = 3*pi/2 - atan(x0/y0);

  #We only care about how much the pin has rotated each timestep
  d_Theta = Theta - pi/2;
  
  #find instantaneous locations of pin piviot
  x_arm = l_arm * cos(theta_arm0 + d_Theta);
  y_arm = l_arm * sin(theta_arm0 + d_Theta);
  #Calculate distance between piviout 
  l_calc = sqrt((xg-x_arm).^2 + (yg-y_arm).^2);
  
  #Find change in length of spring
  d_l = l_spring0 - l_calc;
  
  #angle of spring wrt horizontal
  theta_s = atan((yg-y_arm) / (xg-x_arm));
  
  #Spring Force Magnitude
  fs = f0 - k * d_l;
  
  angle = Theta - pi/2 - theta_s;
  #We project into the normal direction of the moment arm in this function
  fs = fs * cos(angle);
 
endfunction
