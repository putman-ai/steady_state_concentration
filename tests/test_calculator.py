"""
Unit tests for the steady state concentration calculator.
"""

import pytest
import numpy as np
from src.calculator import MedicationProfile, ConcentrationCalculator

def test_medication_profile_validation():
    """Test that MedicationProfile validates inputs correctly."""
    # Valid profile should not raise error
    valid_profile = MedicationProfile("Test", 1.0, 2.0, 3.0)
    
    # Test invalid parameters
    with pytest.raises(ValueError):
        MedicationProfile("Test", -1, 2.0, 3.0)  # negative dose
    with pytest.raises(ValueError):
        MedicationProfile("Test", 1.0, 0, 3.0)   # zero half-life
    with pytest.raises(ValueError):
        MedicationProfile("Test", 1.0, 2.0, -3.0) # negative interval

@pytest.mark.parametrize("time,expected", [
    (0, 0),           # Initial concentration
    (3, 0.72),        # After one dosing interval
    (6, 1.08),        # After two dosing intervals
    (-1, 0),          # Negative time should return 0
])
def test_basic_concentration_calculation(time, expected):
    """Test concentration calculations at specific time points."""
    calculator = ConcentrationCalculator()
    med = MedicationProfile("Test", dose=1.0, half_life=3.0, dosing_interval=3.0)
    
    result = calculator.calculate_concentration(med, time)
    assert np.isclose(result, expected, rtol=0.1)  # 10% tolerance for floating point

def test_timing_offset():
    """Test that timing offsets correctly shift the concentration curve."""
    calculator = ConcentrationCalculator()
    med = MedicationProfile("Test", 1.0, 3.0, 3.0)
    
    # Test that a 1-hour offset shifts the concentration curve
    regular_time = 3.0
    offset_time = 2.0  # 3.0 - 1.0
    
    regular_conc = calculator.calculate_concentration(med, regular_time)
    offset_conc = calculator.calculate_concentration(med, regular_time, timing_offset=1.0)
    
    assert regular_conc > offset_conc

def test_multiple_medications():
    """Test calculator handles multiple medications correctly."""
    calculator = ConcentrationCalculator()
    
    med1 = MedicationProfile("Med1", 1.0, 2.0, 3.0)
    med2 = MedicationProfile("Med2", 2.0, 4.0, 6.0)
    
    calculator.add_medication(med1)
    calculator.add_medication(med2)
    
    assert len(calculator.medications) == 2
    assert calculator.medications[0].name == "Med1"
    assert calculator.medications[1].name == "Med2"

def test_steady_state_approximation():
    """Test that concentration approaches steady state value."""
    calculator = ConcentrationCalculator()
    med = MedicationProfile("Test", dose=1.0, half_life=2.0, dosing_interval=4.0)
    
    # Calculate theoretical steady state
    k = np.log(2) / med.half_life
    theoretical_ss = med.dose / (k * med.dosing_interval)
    
    # Check concentration after several half-lives
    long_time = med.half_life * 10  # Should be close to steady state
    calculated_conc = calculator.calculate_concentration(med, long_time)
    
    assert np.isclose(calculated_conc, theoretical_ss, rtol=0.1)

def test_get_concentration_over_time():
    """Test calculation of concentration over multiple time points."""
    calculator = ConcentrationCalculator()
    med = MedicationProfile("Test", 1.0, 2.0, 3.0)
    
    time_points = np.array([0, 1, 2])
    concentrations = calculator.get_concentration_over_time(med, time_points)
    
    assert len(concentrations) == len(time_points)
    assert concentrations[0] == 0  # Initial concentration should be 0
    assert all(c2 > c1 for c1, c2 in zip(concentrations, concentrations[1:]))  # Should increase