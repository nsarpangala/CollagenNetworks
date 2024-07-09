def calculate_spring_length(spring):
    """Calculate the length of a spring based on the positions of its balls."""
    dx = spring.ball1.position[0] - spring.ball2.position[0]
    dy = spring.ball1.position[1] - spring.ball2.position[1]
    return (dx**2 + dy**2)**0.5

def calculate_fiber_end_end(filament):
    """Calculate the end end distance on the positions of its balls."""
    springs = filament.springs
    dx = springs[0].ball1.position[0] - springs[-1].ball2.position[0]
    dy = springs[0].ball1.position[1] - springs[-1].ball2.position[1]
    return (dx**2 + dy**2)**0.5

def calculate_fiber_length(filament):
    """Calculate the total length of a filament (a list of springs)."""
    return sum(calculate_spring_length(spring) for spring in filament.springs)

def calculate_strain(original_length, deformed_length):
    """Calculate strain based on original and deformed lengths."""
    return (deformed_length - original_length) / original_length