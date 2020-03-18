

function [x, v] = int2(ts, as, initial_cond)
  
  x = zeros(size(ts));
  v = zeros(size(ts));
  a = zeros(size(ts));
  
  
  x(1) = initial_cond(1);
  v(1) = initial_cond(2);
  
  for i = 2:length(ts)
    dt = ts(i) - ts(i-1);
    v(i) = x(i-1) + v(i-1) * dt;
    x(i) = v(i-1) + as(i-1) * dt.^2;
  endfor
  
endfunction
