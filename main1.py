from z3 import *

u_a_1 = Bool("u_a_1")
v_a_1 = Bool('v_a_1')
u_a_2 = Bool("u_a_2")
v_a_2 = Bool('v_a_2')

u_b_1 = Bool("u_b_1")
v_b_1 = Bool('v_b_1')
u_b_2 = Bool("u_b_2")
v_b_2 = Bool('v_b_2')

u_c_1 = Bool("u_c_1")
v_c_1 = Bool('v_c_1')
u_c_2 = Bool("u_c_2")
v_c_2 = Bool('v_c_2')

u_d_1 = Bool("u_d_1")
v_d_1 = Bool('v_d_1')
u_d_2 = Bool("u_d_2")
v_d_2 = Bool('v_d_2')

u_e_1 = Bool("u_e_1")
v_e_1 = Bool('v_e_1')
u_e_2 = Bool("u_e_2")
v_e_2 = Bool('v_e_2')

s = Solver()
s.add(Or([And([u_a_1, u_b_1, u_c_1]), And([v_a_1, v_b_1, v_c_1])]))
s.add(Or([And([u_a_2, u_b_2, u_c_2]), And([v_a_2, v_b_2, v_c_2])]))

s.add(Or([And([u_d_1, u_e_1]), And([v_d_1, v_e_1])]))
s.add(Or([And([u_d_2, u_e_2]), And([v_d_2, v_e_2])]))

s.add(Or([And([u_d_1, u_c_1]), And([v_d_1, v_c_1])]))
s.add(Or([And([u_d_2, u_c_2]), And([v_d_2, v_c_2])]))

s.add(Or([Not(Or([And([u_a_1, u_d_1]), And([v_a_1, v_d_1])])), Not(Or([And([u_a_2, u_d_2]), And([v_a_2, v_d_2])]))]))

s.add(Or([Not(Or([And([u_c_1, u_e_1]), And([v_c_1, v_e_1])])), Not(Or([And([u_c_2, u_e_2]), And([v_c_2, v_e_2])]))]))

s.check()
model = s.model()
# print model[1]



def getBit(u, v):
    if u == False and v == True:
        return '0'
    elif u == True and v == False:
        return '1'
    elif u == True and v == True:
        return '*'
    else:
        return 'z'


def get(u1, v1, u2, v2):
    return getBit(u1, v1) + getBit(u2, v2)


print 'a:' + get(u_a_1, v_a_1, u_a_2, v_a_2)
print 'b:' + get(u_b_1, v_b_1, u_b_2, v_b_2)
print 'c:' + get(u_c_1, v_c_1, u_c_2, v_c_2)
print 'd:' + get(u_d_1, v_d_1, u_d_2, v_d_2)
print 'e:' + get(u_e_1, v_e_1, u_e_2, v_e_2)