

class ParamsEstimation:
    
    # Constant arena center and position
    # Obtaining by computing average of rows
    # arena_center = [0.075, 0.46] 
    # Obtained by computing average of saccades position
    # arena_center = [0.114,  0.46]
    # obtained by guessing 
    # arena_center = [0.09, 0.5]
    
    # Obtained from calibration
    arena_center = [0.15, 0.48]
    arena_radius = 1.0 

    bin_enlarge_dist = 0.05
    bin_enlarge_angle = 10
    min_distance = 0.15
