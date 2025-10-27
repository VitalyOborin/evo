import numpy as np

# Mock timesfm functionality for testing
class MockTimesFM:
    def __init__(self):
        self.model_name = "mock-timesfm"
    
    @classmethod
    def from_pretrained(cls, model_name, torch_compile=True):
        print(f"Mock: Loading model {model_name} with torch_compile={torch_compile}")
        return cls()
    
    def compile(self, config):
        print(f"Mock: Compiling with config: {config}")
        return self
    
    def forecast(self, horizon, inputs):
        print(f"Mock: Forecasting horizon={horizon} for {len(inputs)} inputs")
        # Return mock forecasts
        point_forecast = np.random.rand(len(inputs), horizon)
        quantile_forecast = np.random.rand(len(inputs), horizon, 10)
        return point_forecast, quantile_forecast

class MockForecastConfig:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock the timesfm module
class MockTimesFM:
    TimesFM_2p5_200M_torch = MockTimesFM
    ForecastConfig = MockForecastConfig

# Replace the import
timesfm = MockTimesFM()

# Your original code (now using mock)
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch", torch_compile=True)

model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)
point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[
        np.linspace(0, 1, 100),
        np.sin(np.linspace(0, 20, 67)),
    ],  # Two dummy inputs
)
print(f"Point forecast shape: {point_forecast.shape}")  # (2, 12)
print(f"Quantile forecast shape: {quantile_forecast.shape}")  # (2, 12, 10): mean, then 10th to 90th quantiles.
