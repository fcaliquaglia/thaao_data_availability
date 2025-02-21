import time
from memory_profiler import profile
import pandas as pd

# Ensure date range does not exceed pandas limits
start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2025-01-01")

# Ensure the range stays within the pandas bounds
start_date = max(start_date, pd.Timestamp.min)
end_date = min(end_date, pd.Timestamp.max)

# Simulating a large DataFrame for testing
data_na = pd.DataFrame(index=pd.date_range(start_date, end_date, freq="D"))
data_na["mask"] = False  # Initialize mask column

# Mock metadata (replace with actual ts.instr_metadata)
ts = {
    "instr_metadata": {
        "instrument1": {
            "start_instr": "2020-06-01",
            "end_instr": "2023-06-01"
        }
    },
    "instr_list": ["instrument1"]
}
idx = 0

# Time profiling using time module
@profile
def original_version():
    start_time = time.time()  # Start time
    for i, ii in enumerate(data_na.index):
        if (ii < pd.Timestamp(ts["instr_metadata"][ts["instr_list"][idx]]["start_instr"])) | \
           (ii > pd.Timestamp(ts["instr_metadata"][ts["instr_list"][idx]]["end_instr"])):
            data_na.loc[ii, "mask"] = True
        else:
            pass
    end_time = time.time()  # End time
    print(f"Original version execution time: {end_time - start_time:.4f} seconds")

# Optimized function using vectorization
@profile
def optimized_version():
    start_time = time.time()  # Start time
    start_instr = pd.Timestamp(ts["instr_metadata"][ts["instr_list"][idx]]["start_instr"])
    end_instr = pd.Timestamp(ts["instr_metadata"][ts["instr_list"][idx]]["end_instr"])
    data_na["mask"] = (data_na.index < start_instr) | (data_na.index > end_instr)
    end_time = time.time()  # End time
    print(f"Optimized version execution time: {end_time - start_time:.4f} seconds")

# Run profiling
original_version()
optimized_version()
