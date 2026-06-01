import numpy as np

def get_trench_escape_data():
    """
    1. The Deep Ocean Trench Escape
    Math: Rosenbrock (Banana) Function.
    Characteristics: Steep, intimidating canyon walls with a long, curved, 
    nearly flat valley floor. Perfect stress-test for Momentum.
    """
    x = np.linspace(-2.0, 2.0, 100)
    y = np.linspace(-1.0, 3.0, 100)
    X, Y = np.meshgrid(x, y)
    # Equation: f(x,y) = (1-x)^2 + 100*(y-x^2)^2
    Z = (1 - X)**2 + 100 * (Y - X**2)**2
    return X, Y, Z

def get_cyberpunk_matrix_data():
    """
    2. The Cyberpunk Signal Jam
    Math: Beale Function.
    Characteristics: A highly asymmetrical grid featuring flat plateaus running 
    in one direction, bordered by sudden, sharp, chaotic cliffs. Ideal for Adam's adaptive sizing.
    """
    x = np.linspace(-4.5, 4.5, 100)
    y = np.linspace(-4.5, 4.5, 100)
    X, Y = np.meshgrid(x, y)
    # Equation: Beale's Function
    Z = (1.5 - X + X*Y)**2 + (2.25 - X + X*Y**2)**2 + (2.625 - X + X*Y**3)**2
    return X, Y, Z

def get_desert_swarm_data():
    """
    3. The Sonoran Desert Swarm Rescue
    Math: Rastrigin Function.
    Characteristics: An egg-carton topological nightmare. Hundreds of symmetrical 
    local minima traps surrounding one deep global minimum. Ideal for AGWO swarm tactics.
    """
    x = np.linspace(-4.0, 4.0, 100)
    y = np.linspace(-4.0, 4.0, 100)
    X, Y = np.meshgrid(x, y)
    # Equation: f(x,y) = 20 + (x^2 - 10*cos(2*pi*x)) + (y^2 - 10*cos(2*pi*y))
    Z = 20 + (X**2 - 10 * np.cos(2 * np.pi * X)) + (Y**2 - 10 * np.cos(2 * np.pi * Y))
    return X, Y, Z