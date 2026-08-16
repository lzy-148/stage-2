import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.gradient_descent import gradient

np.random.seed(0)
X = np.random.rand(100, 1)
y = 3 * X + 2 + np.random.randn(100, 1) * 0.1
X_b = np.c_[np.ones((100, 1)), X]

learning_rates = [0.0001, 0.001, 0.01, 0.1, 1]
for lr in learning_rates:
    _, loss = gradient(X_b, y, lr=lr)
    plt.plot(loss, label=str(lr))
plt.legend()
plt.xlabel("epoch")
plt.ylabel("loss")
output_path = project_root / "reports" / "learning_rate.png"
plt.savefig(output_path, dpi=200)
plt.close()
print(f"plot saved to {output_path}")