# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 13:18:38 2023

@author: dleon
"""
import numpy as np

def construct_envelope(f, f_prime, x_values, left_tail_log_slope, righ_tail_log_slope):
    """
    f: log_pdf
    f_prime: derivative of log_pdf"""
    
    
    #x_values should be sorted already
    assert isinstance(x_values, np.ndarray)
    
    y_values      = f(x_values)
    y_prime       = f_prime(x_values)
    
    left_tail_log_slope = y_prime[0]
    righ_tail_log_slope = y_prime[-1]
    
    assert left_tail_log_slope > 0 and righ_tail_log_slope < 0

    
    x1, x2              = x_values[:-1], x_values[1:]
    y1, y2              = y_values[:-1], y_values[1:]
    y_prime1, y_prime2  = y_prime[:-1],  y_prime[1:]
    convexity_indicator = ((y_prime2 - y_prime1)>0) * 1

    #construct convex envelopes
    #y - y1 = (y2 - y1)/(x2 - x1) × (x - x1) <-> y = (y2 - y1)/(x2 - x1) * x + y1 - (y2 - y1)/(x2 - x1) * x1
    m_convex = (y2 - y1) / (x2 - x1)
    n_convex = y1 - m_convex * x1
    area_below_secants = (np.exp(m_convex * x2 + n_convex) - np.exp(m_convex * x1 + n_convex))/m_convex
    if np.any(m_convex == 0):
        #raise ValueError('check before using')
        area_below_secants[np.where(m_convex==0)[0]] = ((x2-x1) * np.exp(y1))[np.where(m_convex==0)[0]]

    
    #construct concave envelopes
    n1                  = y1 - y_prime1 * x1
    n2                  = y2 - y_prime2 * x2
    intersection_points = (n2 - n1) / (y_prime1 - y_prime2)
    
    if np.any(y_prime1 == y_prime2 ):
        intersection_points[np.where(y_prime1 == y_prime2)[0]] = (x1/2 + x2/2)[np.where(y_prime1 == y_prime2)[0]]
    
    _area_1 = (np.exp(y_prime1 * intersection_points + n1) - np.exp(y_prime1 * x1 + n1))/y_prime1
    _area_2 = (np.exp(y_prime2 * x2 + n2) - np.exp(y_prime2 * intersection_points + n2))/y_prime2
    
    if np.any(y_prime1 == 0):
        #raise ValueError('check before using')
        _area_1[np.where(y_prime1==0)[0]] = ((intersection_points-x1) * np.exp(y1))[np.where(y_prime1==0)[0]]

    if np.any(y_prime2 == 0):
            #raise ValueError('check before using')
        _area_2[np.where(y_prime2==0)[0]] = ((x2 - intersection_points) * np.exp(y2))[np.where(y_prime2==0)[0]]

    
    area_below_tangents = _area_1 + _area_2
    
    secants_list  = list(zip(m_convex, n_convex))
    tangents_list = list(zip(intersection_points, zip(y_prime1, n1), zip(y_prime2, n2))) 
    
    all_areas    = convexity_indicator * area_below_secants + (1 - convexity_indicator) * area_below_tangents
    
    left_tail_area  =  np.exp(y_values[0])  /  left_tail_log_slope
    right_tail_area = -np.exp(y_values[-1]) /  right_tail_log_slope
    
    all_areas = np.insert(all_areas, 0, left_tail_area)
    all_areas = np.append(arr = all_areas, values = right_tail_area)
    total_area = np.sum(all_areas) # 1/ total_area is the accepantance rate
    probabilities = all_areas / total_area
    
    #only for testing purposes
    #total_convex_area  = np.sum(area_below_secants)
    #total_concave_area = np.sum(area_below_tangents)
    return secants_list, tangents_list, convexity_indicator, total_area, probabilities
    

if __name__ == '__main__':
    from ambit_stochastics.trawl import trawl
    import matplotlib.pyplot as plt
    #np.random.seed(243)
    
    nr_simulations   = 1
    tau              = 0.5
    nr_trawls        = 5
    jump_part_name   = 'norminvgauss'
    jump_part_params = (5,0,3,4.25)


    nig_trawl = trawl(nr_simulations = nr_simulations,tau = tau, nr_trawls = nr_trawls, \
                      trawl_function = lambda x : np.exp(x) * (x<=0),
                      jump_part_name = jump_part_name, jump_part_params = jump_part_params)

    nig_trawl.simulate('slice')
    values = nig_trawl.values
    
    x_1_3 = values[0,:3]
    x_1,x_2,x_3 = x_1_3
    areas_1         = nig_trawl.slice_areas_matrix[:,0]
    areas_2         = nig_trawl.slice_areas_matrix[:-1,1]
    areas_3         = nig_trawl.slice_areas_matrix[:-2,2]
    

    
    

    
    #tangents_list = list(zip()) #[(intersection_point, (m1,n1),(m2,n2))]