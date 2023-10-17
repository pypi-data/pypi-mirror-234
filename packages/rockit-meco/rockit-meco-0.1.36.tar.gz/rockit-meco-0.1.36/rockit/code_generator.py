


from os import stat
import casadi as cs
import os

class CodeVariable:
    def __init__(self, name, dtype,
            comment=""):
        self.name = name
        self.dtype = dtype
        self.comment = comment

class LocalVariable(CodeVariable):
    pass

class MemoryField(CodeVariable):
    def __init__(self, name, dtype,
            comment=""):
        CodeVariable.__init__(self, name, dtype, comment=comment)

class BaseCodeGenerator:
    def __init__(self,
            ocp,
            name=None,
            use_codegen=False,
            casadi_fun_name=None,
            build_dir_abs=None,
            prefix=None):
        self.ocp = ocp
        self.name = name
        self.use_codegen = use_codegen
        self.casadi_fun_name = casadi_fun_name
        self.build_dir_abs = build_dir_abs
        self.prefix = prefix

    @staticmethod
    def escape(e):
      return e.replace('\\','/')

class CasadiWrapperCodeGenerator(BaseCodeGenerator):
    def __init__(self,*args,**kwargs):
        BaseCodeGenerator.__init__(self,*args,**kwargs)


        [_,states] = self.ocp.sample(self.ocp.x,grid='control')
        [_,algebraics] = self.ocp.sample(self.ocp.z,grid='control')
        [_,controls] = self.ocp.sample(self.ocp.u,grid='control-')
        parameters_symbols = self.ocp.parameters['']+self.ocp.parameters['control']
        parameters = []
        for p in self.ocp.parameters['']:
            parameters.append(self.ocp.value(p))
        for p in self.ocp.parameters['control']:
            parameters.append(self.ocp.sample(p,grid='control-')[1])
        casadi_fun_name = 'ocpfun'
        is_coll = False
        if hasattr(self.ocp._method, "Xc"):
            is_coll = True

        variables = self.ocp.value(cs.vvcat(self.ocp.variables['']))
        [_,variables_control] = self.ocp.sample(cs.vvcat(self.ocp.variables['control']),grid='control-')
        [_,variables_states] = self.ocp.sample(cs.vvcat(self.ocp.variables['states']),grid='control')
        lam_g = self.ocp._method.opti.lam_g

        hotstart_symbol = cs.veccat(variables,variables_control,variables_states,lam_g)

        ocpfun = self.ocp.to_function(casadi_fun_name,
            [states]+(["z"] if is_coll else [cs.MX()])+[controls]+parameters+[hotstart_symbol],
            [states,algebraics,controls,hotstart_symbol],
            ['x0','z0','u0'] + [p.name() for p in self.ocp.parameters['']] + [p.name() for p in self.ocp.parameters['control']] + ['hotstart_in'],
            ['x','z','u','hotstart_out'])

        casadi_codegen_file_name_base = cs.name+"_codegen.c"
        casadi_codegen_file_name = os.path.join(cs.build_dir_abs,casadi_codegen_file_name_base)




    def casadi_call(self,funname,*args):
        method = f"casadi_c_{funname}_id"
        if self.use_codegen:
            if funname=="eval":
                method = f"{self.casadi_fun_name}"
            else:
                method = f"{self.casadi_fun_name}_{funname}"
        if not self.use_codegen:
            args = ("m->id",) + args
        return method + "(" + ",".join(args) + ")"

    def str_includes(self):
        for e in self.includes():
            return '#include "' + e + '"' + "\n"

    def includes(self):
        ret = []
        if self.use_codegen:
            ret.append(self.name + "_codegen.h")
        else:
            ret.append("casadi/casadi_c.h")
        return ret

    def setup_deps(self):
        if not self.use_codegen:
            yield MemoryField("id", "int")
            yield MemoryField("pop", "int"," Need to pop when destroyed?")
            yield LocalVariable("flag", "int")
        yield MemoryField("mem", "int")

    def str_setup(self):
        s = ""
        if not self.use_codegen:
            s+= f"""
            if (casadi_c_n_loaded()) {{ 
              m->id = casadi_c_id("{self.casadi_fun_name}");
              m->pop = 0;
            }}
            if (m->id<0) {{
              if (build_dir==0) {{
                strcpy(casadi_file, "{self.escape(self.build_dir_abs)}");
              }} else {{
                strcpy(casadi_file, build_dir);
              }}
              strcat(casadi_file, "/{self.name}.casadi");
              flag = casadi_c_push_file(casadi_file);
              m->pop = 1;
              if (flag) {{
                m->fatal(m, "initialize", "Could not load file '%s'.\\n", casadi_file);
                return 0;
              }}
              m->id = casadi_c_id("{self.casadi_fun_name}");
              if (m->id<0) {{
                m->fatal(m, "initialize", "Could not locate function with name '{self.casadi_fun_name}'.\\n");
                {self.call_destroy()}
                return 0;
              }}
            }}"""
        s += f"""/* Allocate memory (thread-safe) */
            {self.casadi_call("incref")};
            /* Checkout thread-local memory (not thread-safe) */
            m->mem = {self.casadi_call("checkout")};
            """
        return s
    def str_work(self):
        return self.casadi_call("work","sz_arg", "sz_res", "sz_iw", "sz_w")+";\n"

    def str_destroy(self):
        return f"""
               /* Free memory (thread-safe) */
              {self.casadi_call("decref")};
              /* Release thread-local (not thread-safe) */
              {self.casadi_call("release","m->mem")};
              {"" if self.use_codegen else "if (m->pop) casadi_c_pop();"}
              """

    def call_destroy(self):
        return f"{self.prefix}destroy(m);"

    def str_solve(self,args,rets):
        s= ""
        for i,e in enumerate(args):
            s+= f"m->arg_casadi[{i}] = {e};\n"
        for i,e in enumerate(rets):
            s+= f"m->res_casadi[{i}] = {e};\n"
        s += f"""
            return {self.casadi_call("eval","m->arg_casadi","m->res_casadi","m->iw_casadi","m->w_casadi","m->mem")};
        """
        return s

    def str_get_stats(self):
        return f"""return {self.casadi_call("stats") if self.use_codegen else 0};"""
