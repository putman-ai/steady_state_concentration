"""
calculator.py

Core calculation module for steady state concentration analysis.
Handles medication profiles and concentration calculations.
"""

import numpy as np
from dataclasses import dataclass
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MedicationProfile:
    """Represents a medication's key characteristics for concentration calculations."""
    name: str
    dose: float  # mg
    half_life: float  # hours
    dosing_interval: float  # hours
    
    def __post_init__(self):
        """Validate medication profile parameters."""
        if any(param <= 0 for param in [self.dose, self.half_life, self.dosing_interval]):
            raise ValueError("All numerical parameters must be positive")

class ConcentrationCalculator:
    """Handles calculation of medication concentration levels."""
    
    def __init__(self):
        self.medications: List[MedicationProfile] = []
        
    def add_medication(self, medication: MedicationProfile):
        """Add a medication profile to the calculator."""
        self.medications.append(medication)
        logger.info(f"Added medication profile for {medication.name}")
        
    def calculate_concentration(self, 
                              medication: MedicationProfile, 
                              time: float,
                              timing_offset: float = 0) -> float:
        """
        Calculate medication concentration at a given time point.
        
        Args:
            medication: MedicationProfile object containing medication parameters
            time: Time point in hours
            timing_offset: Adjustment for dose timing variations (hours)
            
        Returns:
            float: Calculated concentration level
        """
        adjusted_time = time - timing_offset
        if adjusted_time < 0:
            return 0
            
        k = np.log(2) / medication.half_life
        steady_state_concentration = medication.dose / (k * medication.dosing_interval)
        concentration = steady_state_concentration * (1 - np.exp(-k * adjusted_time))
        return concentration if concentration > 0 else 0

    def get_concentration_over_time(self,
                                  medication: MedicationProfile,
                                  time_points: np.ndarray,
                                  timing_offset: float = 0) -> np.ndarray:
        """
        Calculate concentration levels over a range of time points.
        
        Args:
            medication: MedicationProfile object
            time_points: Array of time points to calculate concentrations for
            timing_offset: Optional timing adjustment in hours
            
        Returns:
            numpy.ndarray: Array of concentration levels
        """
        return np.array([
            self.calculate_concentration(medication, t, timing_offset) 
            for t in time_points
        ])