
function acc_out = acc_def(data, t_out)
  data = data(2:end,:);
  t_in = data(:,1);
  acc_in = data(:,2);
##  if t_out(end) > t_in(end)
##    warning('Beware Runge-Kutta; t_out > t_in. However should be fixed')
##  endif  
  acc_out = spline(t_in, acc_in, t_out);
  acc_out(t_out > t_in(end)) = 0;
endfunction