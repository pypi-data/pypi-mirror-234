function varargout = rockit_pickle_context(varargin)
  global pythoncasadiinterface
  [args,kwargs] = pythoncasadiinterface.matlab2python_arg(varargin,0,{});
  if isempty(kwargs)
    res = py.rockit.rockit_pickle_context(args{:});
  else
    res = py.rockit.rockit_pickle_context(args{:},pyargs(kwargs{:}));
  end
  varargout = pythoncasadiinterface.python2matlab_ret(res);
end
