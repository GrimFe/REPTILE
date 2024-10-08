import pytest
from nerea.experimental import NormalizedFissionFragmentSpectrum, SpectralIndex, Traverse
from nerea.fission_fragment_spectrum import FissionFragmentSpectrum
from nerea.effective_mass import EffectiveMass
from nerea.reaction_rate import ReactionRate
from nerea.comparisons import CoverE
from nerea.calculated import CalculatedSpectralIndex, CalculatedTraverse
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


@pytest.fixture
def sample_spectrum_data():
    # Sample data for testing
    data = {
        "channel":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],
        "counts": [0, 0, 0, 0, 1, 3, 1, 4, 1, 5,  1,  3,  4,  2,  4,  1,  3,  5,  80, 65, 35, 5,  20, 25, 35, 55, 58, 60, 62, 70, 65, 50, 45, 40, 37, 34, 25, 20, 13, 5,  1,  0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_integral_data():
    data = {
        "channel": [ 6.,  8., 10., 12., 14., 16., 18., 20., 22., 24.],
        "value": [60, 80, 88, 87, 87, 88, 86, 85, 82, 78],
        "uncertainty": [.1, .2, .3, .4, .5, .6, .7, .8, .9, .1]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_power_monitor_data():
    data = {
        "Time": [datetime(2024, 5, 18, 20, 30, 15 + i) for i in range(20)],
        "value": [100, 101, 99, 98, 101, 100, 99, 98, 102, 102] * 2
    }
    return pd.DataFrame(data)

@pytest.fixture
def fission_fragment_spectrum_1(sample_spectrum_data):
    return FissionFragmentSpectrum(start_time=datetime(2024, 5, 18, 20, 30, 15),
                                   life_time=10, real_time=10,
                                   data=sample_spectrum_data, campaign_id="A", experiment_id="B",
                                   detector_id="C1", deposit_id="D1", location_id="E", measurement_id="F1")

@pytest.fixture
def fission_fragment_spectrum_2(sample_spectrum_data):
    return FissionFragmentSpectrum(start_time=datetime(2024, 5, 18, 20, 30, 15),
                                   life_time=10, real_time=10,
                                   data=sample_spectrum_data, campaign_id="A", experiment_id="B",
                                   detector_id="C2", deposit_id="D2", location_id="E", measurement_id="F2")

@pytest.fixture
def effective_mass_1(sample_integral_data):
    return EffectiveMass(deposit_id="D1", detector_id="C1", data=sample_integral_data, bins=42)

@pytest.fixture
def effective_mass_2(sample_integral_data):
    return EffectiveMass(deposit_id="D2", detector_id="C2", data=sample_integral_data, bins=42)

@pytest.fixture
def power_monitor(sample_power_monitor_data):
        return ReactionRate(experiment_id="B", data=sample_power_monitor_data, start_time=datetime(2024, 5, 29, 12, 25, 10), campaign_id='C', detector_id='M', deposit_id='dep')

@pytest.fixture
def rr_1(fission_fragment_spectrum_1, effective_mass_1, power_monitor):
    return NormalizedFissionFragmentSpectrum(fission_fragment_spectrum_1, effective_mass_1, power_monitor)

@pytest.fixture
def rr_2(fission_fragment_spectrum_2, effective_mass_2, power_monitor):
    return NormalizedFissionFragmentSpectrum(fission_fragment_spectrum_2, effective_mass_2, power_monitor)

@pytest.fixture
def sample_spectral_index(rr_1, rr_2):
    return SpectralIndex(rr_1, rr_2)

@pytest.fixture
def sample_c_si_data():
    return pd.DataFrame({'value': 1.01, 'uncertainty': .05}, index=['value'])

@pytest.fixture
def sample_c(sample_c_si_data):
    return CalculatedSpectralIndex(sample_c_si_data, 'M', ['D1', 'D2'])

@pytest.fixture
def sample_si_ce(sample_c, sample_spectral_index):
    return CoverE(sample_c, sample_spectral_index)

counts = [0,0,0,0,0,.3,.3,.4,.1,.2,.5,0,.0,1,1,1.5,2,2.5,2,3,3.5,4,4.2,3.8,4.2,3.9,3.9,4.2,4.1,4,
          0,0,0,0,0,.3,.3,.4,.1,.2,.5,0,.0,1,1,1.5,2,2.5,2,3,3.5,4,4.2,3.8,4.2,3.9,3.9,4.2,4.1,4,
          0,0,0,0,0,.3,.3,.4,.1,.2,.5,0,.0,1,1,1.5,2,2.5,2,3,3.5,4,4.2,3.8,4.2,3.9,3.9,4.2,4.1,4,
          3700,4000,4100,4200,3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800,
          3900,3900,4200,4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800, 3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700, 3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700,
          3900,3900,4200,4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800,3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700,
          3900,3900,4200,4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800,3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700,
          4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700,
          4200,3800, 3900,3900,4200,4100,3800,3700,3800,3900,4200,
          3900,3900,4200,4100,4000,3700,
          4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700,
          4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700,
          4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800,
          3900,3900,4200,4100,4000,3700, 4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800, 4100,4000,3700,4000,4100,4200,3800,3700,3800,3900,4200,3900,3900,4200,4100,
          4000,3700,4000,4100,4200,3800,
          4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700, 4200,3800, 3900,3900,4200,4100,4000,3700,
          3.7,3.8,3.9,4,4,4.2,4.1,3.5,3.2,3,2.5,2.2,2,2,1.5,1.5,1.6,1,1,1,
          .5,.6,.4,.3,.5,.3,.5,.6,.1,.3,.2,.1,0,0,0,0,0,0,0,
          0,0,0,0,0,.3,.3,.4,.1,.2,.5,0,.0,1,1,1.5,2,2.5,2,3,3.5,4,4.2,3.8,4.2,3.9,3.9,4.2,4.1,4,
          0,0,0,0,0,.3,.3,.4,.1,.2,.5,0,.0,1,1,1.5,2,2.5,2,3,3.5,4,4.2,3.8,4.2,3.9,3.9,4.2,4.1,4,
          3.7,3.8,3.9,4,4,4.2,4.1,3.5,3.2,3,2.5,2.2,2,2,1.5,1.5,1.6,1,1,1,
          .5,.6,.4,.3,.5,.3,.5,.6,.1,.3,.2,.1,0,0,0,0,0,0,0,
          3.7,3.8,3.9,4,4,4.2,4.1,3.5,3.2,3,2.5,2.2,2,2,1.5,1.5,1.6,1,1,1,
          .5,.6,.4,.3,.5,.3,.5,.6,.1,.3,.2,.1,0,0,0,0,0,0,0,]

@pytest.fixture
def rr1():
    time = [datetime(2024,5,27,13,19,20) + timedelta(seconds=i) for i in range(len(counts))]
    data =  pd.DataFrame({'Time': time, 'value': counts})
    return ReactionRate(data, data.Time.min(),
                        campaign_id='A', experiment_id='B',
                        detector_id=1, deposit_id='dep')

@pytest.fixture
def rr2():
    time = [datetime(2024,5,27,15,12,42) + timedelta(seconds=i) for i in range(len(counts))]
    data = pd.DataFrame({'Time': time, 'value': np.array(counts) / 2})
    return ReactionRate(data, data.Time.min(),
                        campaign_id='A', experiment_id='B',
                        detector_id=1, deposit_id='dep')

@pytest.fixture
def monitor1(rr1):
    data_ = rr1.data.copy()
    data_.value = data_.value.apply(lambda x: 600 if x > 1000 else 1)
    return ReactionRate(data_, data_.Time.min(),
                        campaign_id='A', experiment_id='B',
                        detector_id=2, deposit_id='dep')

@pytest.fixture
def monitor2(rr2):
    data_ = rr2.data.copy()
    data_.value = data_.value.apply(lambda x: 600 if x > 1000 else 1)
    return ReactionRate(data_, data_.Time.min(),
                        campaign_id='A', experiment_id='B',
                        detector_id=2, deposit_id='dep')

@pytest.fixture
def sample_traverse_rr(rr1, rr2):
    return Traverse({'loc A': rr1, 'loc B': rr2})

@pytest.fixture
def sample_c_traverse_data():
    return pd.DataFrame({'value': [1.01, 0.5],
                         'uncertainty': [0.01, 0.01],
                         'traverse': ['loc A', 'loc B']})

@pytest.fixture
def sample_c_traverse(sample_c_traverse_data):
    return CalculatedTraverse(sample_c_traverse_data, 'M', 'dep')

@pytest.fixture
def sample_ce_traverse(sample_c_traverse, sample_traverse_rr):
    return CoverE(sample_c_traverse, sample_traverse_rr)

def test_deposit_ids(sample_si_ce, sample_ce_traverse):
    assert sample_si_ce.deposit_ids == ['D1', 'D2']

## More tests in test_Comparison.py
