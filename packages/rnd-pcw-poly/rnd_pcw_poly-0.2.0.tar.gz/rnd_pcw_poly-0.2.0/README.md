# rnd-pcw-poly

Generates random piecewise polynomial functions (for example for testing CPD-algorithms).

## Example

```python
import numpy as np
import matplotlib.pyplot as plt
from rnd_pcw_poly import rnd_pcw_poly

# generate a piecewise polynomial function with 5 "jumps" / 6 segments;
# no more than 200 degrees of freedom in total and locally no more than
# 6 degrees of freedom. 
p = rnd_pcw_poly(5, 200, 6)

# plot it
xs = np.linspace(0,1,5000)
ys = p(xs)
plt.scatter(xs, ys)
plt.show()
```

The algorithm has seperately seedable and idependent core characteristics like jump locations, dof distribution, realization etc.
