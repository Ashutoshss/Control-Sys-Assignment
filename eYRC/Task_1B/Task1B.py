import sympy as sym
import Task1A 


def find_jacobian(x1,x2,x1_dot,x2_dot):
    # here x1,x2 are my two variable and x1_dot,x2_dot are the function 
    jacobs=[]
    solution = Task1A.solve_equation(x1_dot,x2_dot)
    jacobs_mat = sym.Matrix([[x1_dot.diff(x1), x1_dot.diff(x2)],[x2_dot.diff(x1) ,x2_dot.diff(x2)]])
    
    for equilibrium_points in solution:
        point_ = jacobs_mat.subs(equilibrium_points)
        jacobs.append(point_)

    return jacobs

if __name__ == '__main__':
    x1,x2 = sym.symbols('x1,x2')
    x1_dot= -x1 + 2*x1**3 + x2
    x2_dot = -x1 -x2
    jacobs = find_jacobian(x1,x2,x1_dot,x2_dot)
    # print('\n', 'Jacobians: \t', jacobs)
    
