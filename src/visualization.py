"""
visualization.py

Visualization module for steady state concentration analysis.
Handles plotting of concentration levels and timing variations.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from .calculator import MedicationProfile, ConcentrationCalculator

class ConcentrationVisualizer:
    """Handles visualization of medication concentration levels."""
    
    def __init__(self, calculator: ConcentrationCalculator):
        self.calculator = calculator
        
    def plot_concentrations(self, 
                          time_range: Tuple[float, float] = (0, 24),
                          time_step: float = 0.1,
                          title: str = 'Medication Concentration Levels Over Time',
                          figsize: Tuple[int, int] = (10, 6)):
        """
        Plot concentration levels over time for all medications in the calculator.
        
        Args:
            time_range: Tuple of (start_time, end_time) in hours
            time_step: Time increment for calculations
            title: Title for the plot
            figsize: Figure dimensions (width, height)
        """
        if not self.calculator.medications:
            logger.warning("No medications to plot")
            return
            
        time_points = np.arange(time_range[0], time_range[1], time_step)
        plt.figure(figsize=figsize)
        
        for med in self.calculator.medications:
            concentrations = self.calculator.get_concentration_over_time(
                med, time_points
            )
            label = f'{med.name} ({med.dosing_interval}hr interval)'
            plt.plot(time_points, concentrations, label=label)
        
        plt.xlabel('Time (hours)')
        plt.ylabel('Concentration (mg)')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_timing_variations(self,
                             medication: MedicationProfile,
                             time_range: Tuple[float, float] = (0, 72),
                             time_step: float = 0.1,
                             figsize: Tuple[int, int] = (10, 6)):
        """
        Plot concentration levels with timing variations for a single medication.
        
        Args:
            medication: MedicationProfile to analyze
            time_range: Tuple of (start_time, end_time) in hours
            time_step: Time increment for calculations
            figsize: Figure dimensions (width, height)
        """
        time_points = np.arange(time_range[0], time_range[1], time_step)
        plt.figure(figsize=figsize)
        
        # Calculate concentrations with different timing offsets
        variations = [
            ('On time', 0),
            ('One hour early', -1),
            ('One hour late', 1)
        ]
        
        for label, offset in variations:
            concentrations = self.calculator.get_concentration_over_time(
                medication, time_points, offset
            )
            plt.plot(time_points, concentrations, label=label)
        
        plt.xlabel('Time (hours)')
        plt.ylabel('Concentration (mg)')
        plt.title(f'Effect of Timing on {medication.name} Concentration')
        plt.legend()
        plt.grid(True)
        plt.show()