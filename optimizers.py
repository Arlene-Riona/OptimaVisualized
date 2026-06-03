import numpy as np

def simulate_momentum(initial_x, initial_y, gradient_func, steps=30, lr=0.01, beta=0.9):
    """
    Computes a trajectory path using Gradient Descent with Momentum.
    Formula:
        v_t = beta * v_{t-1} + lr * grad(w_t)
        w_{t+1} = w_t - v_t
    Perfect for building kinetic inertia to glide through flat valley floors.
    """
    path = [[initial_x, initial_y]]
    
    # Initialize velocity vectors for both parameters to zero
    v_x, v_y = 0.0, 0.0
    
    x, y = initial_x, initial_y
    
    for _ in range(steps):
        # Calculate the localized gradients using numerical approximation or specific landscape equations
        grad_x, grad_y = gradient_func(x, y)
        
        # Compute historical kinetic velocity updates
        v_x = beta * v_x + lr * grad_x
        v_y = beta * v_y + lr * grad_y
        
        # Apply step update to parameters
        x = x - v_x
        y = y - v_y
        
        path.append([x, y])
        
    return np.array(path)

def simulate_adam(initial_x, initial_y, gradient_func, steps=30, lr=0.1, beta1=0.9, beta2=0.999, eps=1e-8):
    """
    Computes a trajectory path using the Adam (Adaptive Moment Estimation) Core.
    Formulas:
        m_t = beta1 * m_{t-1} + (1 - beta1) * grad
        v_t = beta2 * v_{t-1} + (1 - beta2) * grad^2
        m_hat = m_t / (1 - beta1^t),  v_hat = v_t / (1 - beta2^t)
        w_{t+1} = w_t - (lr / (sqrt(v_hat) + eps)) * m_hat
    Adapts learning scales independently for steep cliffs vs flat plateaus.
    """
    path = [[initial_x, initial_y]]
    
    # m = 1st moment vector (mean), v = 2nd moment vector (uncentered variance)
    m_x, m_y = 0.0, 0.0
    v_x, v_y = 0.0, 0.0
    
    x, y = initial_x, initial_y
    
    for t in range(1, steps + 1):
        grad_x, grad_y = gradient_func(x, y)
        
        # 1. Update biased first moment estimate
        m_x = beta1 * m_x + (1 - beta1) * grad_x
        m_y = beta1 * m_y + (1 - beta1) * grad_y
        
        # 2. Update biased second raw moment estimate
        v_x = beta2 * v_x + (1 - beta2) * (grad_x ** 2)
        v_y = beta2 * v_y + (1 - beta2) * (grad_y ** 2)
        
        # 3. Compute bias-corrected first moment estimate
        m_x_hat = m_x / (1 - beta1 ** t)
        m_y_hat = m_y / (1 - beta1 ** t)
        
        # 4. Compute bias-corrected second raw moment estimate
        v_x_hat = v_x / (1 - beta2 ** t)
        v_y_hat = v_y / (1 - beta2 ** t)
        
        # 5. Apply adaptive parameter update sequence
        x = x - (lr / (np.sqrt(v_x_hat) + eps)) * m_x_hat
        y = y - (lr / (np.sqrt(v_y_hat) + eps)) * m_y_hat
        
        path.append([x, y])
        
    return np.array(path)

def simulate_agwo(initial_x, initial_y, fitness_func, steps=30, num_wolves=8):
    """
    Computes a swarm tracking path using an Adaptive Grey Wolf Optimizer (AGWO).
    
    Instead of following a single point, a swarm of candidate vectors encircles 
    the best positions discovered so far: Alpha (best), Beta (second), and Delta (third).
    
    Returns:
        A list of coordinate frames, where each frame contains the positions of all wolves
        at that specific time step. This structure allows Plotly to animate the full pack 
        converging on the global minimum!
    """
    # 1. Initialize a pack of wolves randomly distributed near the starting point
    # We create a small variance so the pack starts scattered as a swarm
    np.random.seed(42)
    wolves = np.zeros((num_wolves, 2))
    for i in range(num_wolves):
        wolves[i, 0] = initial_x + np.random.uniform(-1.0, 1.0)
        wolves[i, 1] = initial_y + np.random.uniform(-1.0, 1.0)
        
    # Track the collective history of the entire pack across all time steps
    swarm_history = [wolves.copy()]
    
    for step in range(steps):
        # 2. Evaluate the fitness (elevation/loss) of each wolf in the pack
        fitness = np.array([fitness_func(w[0], w[1]) for w in wolves])
        
        # 3. Identify the current social hierarchy leaders (Alpha, Beta, Delta)
        # We look for the lowest values since we are minimizing our loss landscapes
        sorted_indices = np.argsort(fitness)
        
        alpha_pos = wolves[sorted_indices[0]].copy()
        beta_pos = wolves[sorted_indices[1]].copy()
        delta_pos = wolves[sorted_indices[2]].copy()
        
        # 4. Compute the adaptive convergence factor 'a'
        # 'a' decreases linearly from 2 down to 0 over the course of the hunt, 
        # transitioning the pack from exploration (searching) to exploitation (attacking)
        a = 2.0 - step * (2.0 / steps)
        
        # 5. Update the position of every wolf in the pack
        for i in range(num_wolves):
            # Each wolf updates its position based on the Alpha, Beta, and Delta vectors
            new_pos = np.zeros(2)
            
            # Encircling calculation loops for Alpha, Beta, and Delta influences
            for leader_pos in [alpha_pos, beta_pos, delta_pos]:
                r1 = np.random.rand()
                r2 = np.random.rand()
                
                # Compute coefficient vectors A and C
                A = 2.0 * a * r1 - a
                C = 2.0 * r2
                
                # Calculate distance vector to the leader
                D = np.abs(C * leader_pos - wolves[i])
                
                # Compute the step component toward this leader
                X_step = leader_pos - A * D
                new_pos += X_step
                
            # Average the component positions to settle the wolf's new coordinate
            wolves[i] = new_pos / 3.0
            
        swarm_history.append(wolves.copy())
        
    return swarm_history