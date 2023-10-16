# Nested bars
from tqdm import trange
for i in trange(10):
    for j in trange(int(1e7), leave=False, unit_scale=True):
        pass
    
