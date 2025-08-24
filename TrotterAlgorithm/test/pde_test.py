from TrotterAlgorithm.core.pde import WignerPDE

pde = WignerPDE(x_points=2, p_points=2)
print("State awal amplitudo |f0⟩:")
print([amp.real for amp in pde.get_state()])

pde.evolve(dt=0.5, steps=1)
    
print("\nState setelah evolusi:")
print([amp.real for amp in pde.get_state()])