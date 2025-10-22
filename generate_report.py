import numpy as np
import math
from scipy.stats import gamma


# Variables 
tactical_operation_dict = {
    "offensive": 0, 
    "stability": -0.3832,
    "sustainment": -0.4818,
    "counterinsurgency": -0.5727,
    "defensive": -1.0436,
    "peace_operations": -3.0000
}

posture_dict = {
    "attacker": 0,
    "defender": 1.1864
}

climate_dict = {
    "temperate": 0, 
    "hot": -0.0072,
    "cold": -0.3233
}

terrain_dict = {
    "urban": 0,
    "rolling": -0.0060,
    "flat": -0.1289,
    "swamp": -0.3504,
    "rugged": -0.4060
}

enemy_capability_dict = {
    "near_peer": 0, 
    "hybrid": -0.2095,
    "failed_state": -0.7422,
    "asymmetric": -0.7422
}

tactical_action_dict = {
    # Defensive 
    "blue_counterattack_heavy_resistance": 1.651,
    "red_attack": 1.463,
    "blue_counterattack_light_resistance": 0.979,
    "patrolling": 0.603,

    # Offensive TODO 
    "amphibious_assault": 2.582,
    "blue_attack_heavy_resistance": 2.278,
    "airdrop_attack": 1.912,
    "assault_river_crossing": 1.610 
}

operational_environment_dict = {
    "close_area_near_peer": 1,
    "close_area_hybrid": 1,
    "close_area_failed_state": 1,
    "close_area_asymmetric": 1,
    
    "support_area_forward_peer": 0.188,
    "support_area_forward_hybrid": 0.209,
    "support_area_forward_failed_state": 0.257,
    "support_area_forward_asymmetric": 0.459,

    "support_area_rear_peer": 0.070,
    "support_area_rear_hybrid": 0.090,
    "support_area_rear_failed_state": 0.135,
    "support_area_rear_asymmetric": 0.310
}

combat_advantage_dict = {
    "neutral": "neutral",
    "blue_advantage_near_peer": "blue_advantage_near_peer",
    "blue_advantage_other": "blue_advantage_other",
    "red_advantage_near_peer": "red_advantage_near_peer",
    "red_advantage_other": "red_advantage_other"
}

def exponential_percentile(mean, p):
    if not (0 <= p <= 1):
        raise ValueError("p must be between 0 and 1")
    if mean <= 0:
        raise ValueError("mean must be positive")
    
    return -mean * math.log(1 - p)

def gamma_percentile(mean, p, shape=1):
    if not (0 <= p <= 1):
        raise ValueError("p must be between 0 and 1")
    if mean <= 0:
        raise ValueError("mean must be positive")
    if shape <= 0:
        raise ValueError("shape must be positive")
    
    scale = mean / shape  # because mean = shape * scale
    return gamma.ppf(p, a=shape, scale=scale)

    def get_ln_wia(par, duration_days, tactical_operation, posture, climate, terrain, enemy_capability, intercept=4.0986): 
    return intercept + (-0.1577)*np.log(par) + (-0.4630)*np.log(duration_days) + tactical_operation_dict.get(tactical_operation) 
    + posture_dict.get(posture) + climate_dict.get(climate) + terrain_dict.get(terrain) + enemy_capability_dict.get(enemy_capability)


def get_mean_wia(par, duration_days, tactical_operation, posture, climate, terrain, enemy_capability, tactical_action, operational_environment, intercept=4.0986, combat_advantage="neutral"): 
    mean = np.exp(get_ln_wia(par, duration_days, tactical_operation, posture, climate, terrain, enemy_capability, intercept)) * tactical_action_dict.get(tactical_action) * operational_environment_dict.get(operational_environment)

    match(combat_advantage_dict.get(combat_advantage)): 
        case "neutral": 
            return mean
        case "blue_advantage_near_peer":
            return exponential_percentile(mean, .5)
            
        case "blue_advantage_other":
            return gamma_percentile(mean, .5)
            
        case "red_advantage_near_peer":
            return exponential_percentile(mean, .8)

        case "red_advantage_other":
            return exponential_percentile(mean, .8)
    
   
