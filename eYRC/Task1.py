import sympy as sym
from Task_1A import Task1A
from Task_1B import Task1B
from Task_1C import Task1C

if __name__ == '__main__':
    x1,x2 = sym.symbols('x1,x2')
    x1_dot= -20*x1 +15*x2 -4*x1**2 +11*x2**2
    x2_dot = 7*x1 -9*x2 
    solution = Task1A.solve_equation(x1_dot,x2_dot)
    jacobs = Task1B.find_jacobian(x1,x2,x1_dot,x2_dot)
    eigenvalues, stability = Task1C.eigens(jacobs)

    print('\n','Equilibrium Point:','\n',solution,'\n','\n','Jacobians: ','\n',jacobs,'\n','\n','eigenvalues: ','\n',eigenvalues,'\n','\n','stability: ','\n',stability)