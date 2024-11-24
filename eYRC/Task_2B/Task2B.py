import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 
import matplotlib.animation as animation
from scipy.integrate import ode
import control as ct
import math

    
## Function : cart_pendulum_dynamics()
## ----------------------------------------------------
## Input:   y - State Vector. In case of inverted cart pendulum, the state variables
##              are position of cart x, velocity of cart x_dot, angle of pendulum
##              bob theta wrt vertical and angular velocity theta_dot of pendulum
##              bob.
##          m - Mass of pendulum bob
##          M - Mass of cart
##          L - Length of cart
##          g  - Acceleration due to gravity
##          u  - Input to the system. Input is the horizontal force acting on the cart.
##
## Output:  dy -  Derivative of State Vector.
##
## Purpose: Calculates the value of the vector dy according to the equations which 
##          govern this system.
def cart_pendulum_dynamics(y, m, M, L, g, u):
    sin_theta = np.sin(y[2])
    cos_theta = np.cos(y[2])
    
    dy = np.zeros(4)
    dy[0] = y[1]
    dy[1] = (u + m * L * sin_theta * y[3]**2 - m * g * cos_theta * sin_theta) / (M + m - m * cos_theta**2)
    dy[2] = y[3]
    dy[3] = (-u * cos_theta - m * L * cos_theta * sin_theta * y[3]**2 + (M + m) * g * sin_theta) / (L * (M + m - m * cos_theta**2))
    return dy

## Function : cart_pendulum_AB_matrix()
## ----------------------------------------------------
## Input:   m - Mass of pendulum bob
##          M - Mass of cart
##          L - Length of cart
##          g  - Acceleration due to gravity
##
## Output:  A - A matrix of system
##          B - B matrix of system
##          
## Purpose: Declare the A and B matrices in this function.
def cart_pendulum_AB_matrix(m, M, L, g):
    A = np.array([[0, 1, 0, 0],
                  [0, 0, -m*g/M, 0],
                  [0, 0, 0, 1],
                  [0, 0, (M + m)*g/(L*M), 0]])
    
    B = np.array([[0],
                  [1/M],
                  [0],
                  [-1/(L*M)]])
    
    return A, B

## Function : lqr_cart_pendulum()
## ----------------------------------------------------
## Input:   m - Mass of pendulum bob
##          M - Mass of cart
##          L - Length of cart
##          g  - Acceleration due to gravity
##          y_setpoint - Reference Point
##          y0 - Initial Condition
##
## Output:  t - Timestep
##          y - Solution array
##          
## Purpose: This function demonstrates the behavior of inverted cart pendulum with 
##          external input using the LQR controller
##          This integrates the system of differential equation from t0 = 0 to 
##          tf = 15 with initial condition y0 and input u = -Kx where K is
##          calculated using LQR Controller.
def lqr_cart_pendulum(m, M, L, g, y_setpoint, y0):
    A, B = cart_pendulum_AB_matrix(m, M, L, g)
    Q = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])
    R = 1
    K, S, E = ct.lqr(A,B,Q,R)
    
    t_span = np.arange(0, 15.1, 0.1)
    solver = ode(lambda t, y: cart_pendulum_dynamics(y, m, M, L, g, -K@(y-y_setpoint))).set_integrator('dopri5')
    solver.set_initial_value(y0, 0)
    t, y = [], []
    while solver.successful() and solver.t < t_span[-1]:
        solver.integrate(solver.t + 0.1)
        t.append(solver.t)
        y.append(solver.y)
    return np.array(t), np.array(y)

def cart_pendulum_main():
	m = 1
	M = 5
	L = 2
	g = 9.8
	y0 = np.array([0, 0, np.pi - 0.3, 0])
	y_setpoint = np.array([0, 0, np.pi, 0])
    
	t, y = lqr_cart_pendulum(m, M, L, g, y_setpoint, y0)

	def draw_cart_pendulum(ax, cartx, angle):
		# Clear the axes for the new frame
		ax.clear()
		ax.set_facecolor('black')
		# Set the limits of the plot
		ax.set_xlim(-8, 8)
		ax.set_ylim(-0.5, 10)
		# Draw the cart
		ax.add_patch( Rectangle((cartx-1, 0), 2, 2) ) 
		ax.add_patch(plt.Circle((cartx-1, 0), 0.25, color='red', fill=True))
		ax.add_patch(plt.Circle((cartx+1, 0), 0.25, color='red', fill=True))
		# find the end point
		endy = 1 + 7 * math.sin(angle-(math.pi/2))
		endx = cartx - 7 * math.cos(angle-(math.pi/2))
		# Draw the pole
		ax.plot([cartx, endx], [1, endy], color='white') 
		# Bob mass at the top of pole
		ax.add_patch(plt.Circle((endx, endy), 0.5, color='green', fill=True))
		
	# Function to update the positions of the masses for each frame
	def update(frame):
		# Draw the updated system
		draw_cart_pendulum(ax, y[frame,0], y[frame,2])
		return ax  
    
	time_interval = 0.05  # Time interval for the simulation in seconds
	
	# Create the figure and axes
	fig, ax = plt.subplots()
	
	# Draw the initial pulley system
	draw_cart_pendulum(ax, 1, 1)
	ax.set_aspect(1)
      
	# Start the animation
	ani = animation.FuncAnimation(fig, update, frames=np.arange(0,len(t)), interval=time_interval*1000, blit=False, repeat=False)
	
	plt.show()
      
if __name__ == '__main__':
	cart_pendulum_main()