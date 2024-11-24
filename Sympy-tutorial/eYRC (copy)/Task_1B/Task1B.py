import sympy as sym

def solve_equation(x1_dot,x2_dot):
    ################ Write your code here ################
    x1, x2 = sym.symbols('x1 x2')
    equilibrium_points = sym.solve((x1_dot, x2_dot),(x1,x2))
    print(type(equilibrium_points))
    return equilibrium_points


def find_jacobian(x1,x2,x1_dot,x2_dot):
    # here x1,x2 are my two variable and x1_dot,x2_dot are the function 
    jacobs=[]
    solution = solve_equation(x1_dot,x2_dot)
    jacobs_mat = sym.Matrix([[x1_dot.diff(x1), x1_dot.diff(x2)],[x2_dot.diff(x1) ,x2_dot.diff(x2)]])
    
    for equilibrium_points in solution:
        point_ = jacobs_mat.subs(equilibrium_points)
        jacobs.append(point_)

    return jacobs

if __name__ == '__main__':
    x1,x2 = sym.symbols('x1,x2')
    x1_dot= -x1 + 3*x2
    x2_dot = -x1 -x2**2
    jacobs = find_jacobian(x1,x2,x1_dot,x2_dot)
    print('\n', 'Jacobians: \t', jacobs)
    
