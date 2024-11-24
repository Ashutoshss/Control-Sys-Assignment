import sympy as sym
import Task1A
import Task1B

# def findEigenValue(matrix_):
#     '''
#     Description:    Function to calculate the Eigen value 

#     '''

#     Lambda = sym.Symbol('Lambda')
#     A = matrix_                                     # Note: the matrix should have equal row and column
#     rows, cols = A.shape
#     size = max(rows, cols)
    
#     I = sym.eye(size)                               #identity matrix

#     equation = sym.Eq(sym.det(Lambda*I - A), 0)     #characteristic equation
#     eigenvalues = sym.solve(equation, Lambda)       # so this is use to solve that quadratic equation and finding the lambda that is the eigen val

#     return eigenvalues

def eigens(jacobs):
    eigenvalues = []
    stability = []
    for jacobian in jacobs:
        eigen_value = jacobian.eigenvals()      #this is a built in function for finding the eigen value
        eigenvalues.append(eigen_value)

        isStable = all(sym.re(eigen) < 0 for eigen in eigen_value)       # because if the real part of the eigen val is negative means the system is stable 
        isUnstable = all(sym.re(eigen) > 0 for eigen in eigen_value)     # because if the real part of the eigen val is positive means the system is unstable

        if isStable:
            stability.append('Stable')
        elif isUnstable:
            stability.append('Unstable')
        else:
            stability.append('Indeterminate')
    return eigenvalues, stability


if __name__ == '__main__':
    x1,x2 = sym.symbols('x1,x2')
    x1_dot= -x1 + 2*x1**3 + x2
    x2_dot = -x1 -x2
    solution = Task1A.solve_equation(x1_dot,x2_dot)
    jacobs = Task1B.find_jacobian(x1,x2,x1_dot,x2_dot)
    eigenvalues, stability = eigens(jacobs)
    print('\n', 'eigenvalues: ', eigenvalues, '\n', 'stability: ', stability)
    