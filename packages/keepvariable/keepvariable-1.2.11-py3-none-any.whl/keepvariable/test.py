

import keepvariable.keepvariable_core as kv


a="2022-01-01"
b="blabla"
c=1000
d={"test":123}

a=kv.Var(a)
b=kv.Var(b)
c=kv.Var(c)
d=kv.Var(d)


kv.save_variables(kv.kept_variables,filename="testing_vars.kpv")


b=kv.load_variable("testing_vars.kpv")
a=kv.load_variable("testing_vars.kpv")
c=kv.load_variable("testing_vars.kpv")
print(a)
print(b)
print(c)

a=kv.load_variable("testing_vars.kpv")


