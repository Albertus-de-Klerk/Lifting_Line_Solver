import numpy as np

# Define wing parameters
rho = 1.225
V_inf = 30
b = 10          # wing span [m]
c = 1           # chord length [m]
AR = b / c      # aspect ratio
alpha = np.deg2rad(5)   # angle of attack [rad]



# Function to read wing geometry

def GetWingData(Filename):
	with open(Filename, 'r') as infile:
		WingData = np.loadtxt(infile, dtype=float, skiprows=0, unpack=True)
		return WingData
    

WingData = GetWingData("wing.dat")
print(WingData)
print(dir(WingData))



# Define panel parameters
n_panels = 20   # number of panels
panel_span = b / n_panels   # span of each panel
x_panel = np.linspace(panel_span / 2, b - panel_span / 2, n_panels)   # x-location of panel center
S = c * panel_span   # panel area
gamma = np.zeros(n_panels)   # initialize panel vorticity

# Calculate wing lift coefficient
CL = 2 * np.pi * AR * alpha

# Define wing downwash function
def w(z):
    return -CL / (2 * AR) * (1 - (2 * z / b) ** 2)

# Calculate panel lift distribution
for i in range(n_panels):
    # Calculate y-location of panel endpoints
    y_start = -b / 2 + (i * panel_span)
    y_end = y_start + panel_span
    
    # Calculate panel mid-point location
    y_mid = (y_start + y_end) / 2
    
    # Calculate panel spanwise location
    z = np.linspace(y_start, y_end, 100)
    
    # Calculate downwash at panel mid-point
    w_mid = w(y_mid)
    
    # Calculate normal vector components
    dy = y_end - y_start
    dz = z - y_mid
    mag = np.sqrt(dy**2 + dz**2)
    n = np.array([dy/mag, dz/mag])
    
    # Calculate panel vorticity
    gamma[i] = np.sum(w_mid * S * n[1])    
    
# Calculate lift distribution
L = gamma * S * np.cos(alpha)
y = x_panel / 2   # spanwise location of panel center
CL_wing = np.sum(L) / (0.5 * rho * V_inf**2 * S)

print(CL_wing)