"""
线性回归与梯度下降 - 完整模板
遵循五步流程：推导 → 从零实现 → 库实现 → 实验比较 → 误差分析
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("=" * 70)
print("步骤 1：数学推导 - 均方误差及其梯度")
print("=" * 70)

print("""
【均方误差 (MSE) 定义】
    MSE = (1/n) * Σ(y_i - ŷ_i)²
        = (1/n) * Σ(y_i - (w·x_i + b))²

【梯度推导】

对于单个样本 (x_i, y_i)，损失为：
    L_i = (y_i - ŷ_i)² = (y_i - w·x_i - b)²

对 w 求偏导：
    ∂L_i/∂w = -2*x_i*(y_i - w·x_i - b)

对 b 求偏导：
    ∂L_i/∂b = -2*(y_i - w·x_i - b)

对全部 n 个样本求平均：
    ∂MSE/∂w = (-2/n) * Σx_i*(y_i - ŷ_i)
    ∂MSE/∂b = (-2/n) * Σ(y_i - ŷ_i)

【向量化形式】
    ∂MSE/∂w = (-2/n) * X^T · (y - ŷ)
    ∂MSE/∂b = (-2/n) * Σ(y - ŷ)

【梯度下降更新规则】
    w := w - α * ∂MSE/∂w
    b := b - α * ∂MSE/∂b
    其中 α 为学习率
""")

print("\n" + "=" * 70)
print("步骤 2：从零实现 - NumPy 批量梯度下降")
print("=" * 70)

class LinearRegressionFromScratch:
    def __init__(self, learning_rate=0.01, n_iterations=1000, regularization=None, lambda_=0.1):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.regularization = regularization
        self.lambda_ = lambda_
        self.weights = None
        self.bias = None
        self.loss_history = []

    def _compute_gradient(self, X, y, y_pred):
        n = len(y)
        error = y - y_pred

        if self.regularization == 'l2':
            grad_w = (-2/n) * np.dot(X.T, error) + 2 * self.lambda_ * self.weights
        elif self.regularization == 'l1':
            grad_w = (-2/n) * np.dot(X.T, error) + self.lambda_ * np.sign(self.weights)
        else:
            grad_w = (-2/n) * np.dot(X.T, error)

        grad_b = (-2/n) * np.sum(error)
        return grad_w, grad_b

    def _compute_loss(self, X, y, y_pred):
        n = len(y)
        mse = np.mean((y - y_pred) ** 2)

        if self.regularization == 'l2':
            reg_term = self.lambda_ * np.sum(self.weights ** 2)
        elif self.regularization == 'l1':
            reg_term = self.lambda_ * np.sum(np.abs(self.weights))
        else:
            reg_term = 0

        return mse + reg_term

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for i in range(self.n_iterations):
            y_pred = np.dot(X, self.weights) + self.bias
            grad_w, grad_b = self._compute_gradient(X, y, y_pred)

            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b

            loss = self._compute_loss(X, y, y_pred)
            self.loss_history.append(loss)

            if i % 200 == 0:
                print(f"  迭代 {i:4d}: Loss = {loss:.6f}")

        return self

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

    def get_weights(self):
        return self.weights, self.bias


print("\n" + "=" * 70)
print("步骤 3：库实现 - sklearn")
print("=" * 70)

def sklearn_linear_regression(X_train, y_train, X_test, regularization=None, lambda_=0.1):
    if regularization == 'l2':
        model = Ridge(alpha=lambda_)
    elif regularization == 'l1':
        model = Lasso(alpha=lambda_)
    else:
        model = LinearRegression()

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return model, y_pred


print("\n" + "=" * 70)
print("步骤 4：实验比较")
print("=" * 70)

def generate_data(n_samples=200, n_features=3, noise=10):
    X = np.random.randn(n_samples, n_features)
    true_weights = np.array([2.5, -1.5, 3.0])
    true_bias = 4.0
    y = np.dot(X, true_weights) + true_bias + np.random.randn(n_samples) * noise
    return X, y, true_weights, true_bias

X, y, true_weights, true_bias = generate_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print(f"\n数据集: {len(X_train)} 训练样本, {len(X_test)} 测试样本")
print(f"真实权重: {true_weights}")
print(f"真实偏置: {true_bias:.4f}")

print("\n" + "-" * 70)
print("实验 4.1: 解析解 vs 梯度下降")
print("-" * 70)

X_mean = np.mean(X_train, axis=0)
X_std = np.std(X_train, axis=0)
X_train_norm = (X_train - X_mean) / X_std
X_test_norm = (X_test - X_mean) / X_std

analytical_weights = np.linalg.lstsq(X_train_norm, y_train, rcond=None)[0]
y_pred_analytical = np.dot(X_test_norm, analytical_weights)
mse_analytical = mean_squared_error(y_test, y_pred_analytical)
r2_analytical = r2_score(y_test, y_pred_analytical)

print(f"\n【解析解】")
print(f"  MSE: {mse_analytical:.6f}")
print(f"  R²:  {r2_analytical:.6f}")

print(f"\n【梯度下降】(学习率=0.01, 迭代=1000)")
model_gd = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=1000)
model_gd.fit(X_train_norm, y_train)
y_pred_gd = model_gd.predict(X_test_norm)
mse_gd = mean_squared_error(y_test, y_pred_gd)
r2_gd = r2_score(y_test, y_pred_gd)
print(f"  MSE: {mse_gd:.6f}")
print(f"  R²:  {r2_gd:.6f}")
print(f"  学习到的权重: {model_gd.weights}")

print("\n" + "-" * 70)
print("实验 4.2: 学习率影响分析")
print("-" * 70)

learning_rates = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0]

print("\n【学习率过大/过小的影响】")
for lr in learning_rates:
    try:
        model = LinearRegressionFromScratch(learning_rate=lr, n_iterations=200)
        model.fit(X_train_norm, y_train)
        final_loss = model.loss_history[-1]
        status = "✓ 收敛" if final_loss < 1000 else "✗ 未收敛"
        print(f"  学习率={lr:4.2f}: 最终Loss={final_loss:10.4f} {status}")
    except:
        print(f"  学习率={lr:4.2f}: ✗ 数值溢出")

print("\n" + "-" * 70)
print("实验 4.3: L1 vs L2 正则化")
print("-" * 70)

regularizations = [('无', None, 0), ('L1', 'l1', 0.1), ('L2', 'l2', 0.1)]

print("\n【正则化对比】")
for name, reg, lam in regularizations:
    model = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=500,
                                          regularization=reg, lambda_=lam)
    model.fit(X_train_norm, y_train)
    y_pred = model.predict(X_test_norm)
    mse = mean_squared_error(y_test, y_pred)
    weights_norm = np.linalg.norm(model.weights)
    weights_sparsity = np.sum(np.abs(model.weights) < 0.1) / len(model.weights)
    print(f"  {name:4s}: MSE={mse:8.4f}, 权重范数={weights_norm:8.4f}, 稀疏度={weights_sparsity:.2%}")

print("\n" + "-" * 70)
print("实验 4.4: sklearn 对比")
print("-" * 70)

sklearn_model, y_pred_sklearn = sklearn_linear_regression(X_train_norm, y_train, X_test_norm)
mse_sklearn = mean_squared_error(y_test, y_pred_sklearn)
print(f"\n【sklearn LinearRegression】")
print(f"  MSE: {mse_sklearn:.6f}")
print(f"  R²:  {r2_score(y_test, y_pred_sklearn):.6f}")

sklearn_ridge, y_pred_ridge = sklearn_linear_regression(X_train_norm, y_train, X_test_norm, 'l2', 0.1)
print(f"\n【sklearn Ridge (L2)】")
print(f"  MSE: {mean_squared_error(y_test, y_pred_ridge):.6f}")

sklearn_lasso, y_pred_lasso = sklearn_linear_regression(X_train_norm, y_train, X_test_norm, 'l1', 0.1)
print(f"\n【sklearn Lasso (L1)】")
print(f"  MSE: {mean_squared_error(y_test, y_pred_lasso):.6f}")

print("\n" + "-" * 70)
print("实验 4.5: 归一化影响")
print("-" * 70)

print("\n【归一化 vs 未归一化 梯度下降】")

print("\n  [未归一化数据]")
model_unnorm = LinearRegressionFromScratch(learning_rate=0.01, n_iterations=500)
model_unnorm.fit(X_train, y_train)
y_pred_unnorm = model_unnorm.predict(X_test)
print(f"    MSE: {mean_squared_error(y_test, y_pred_unnorm):.4f}")

print("\n  [归一化数据]")
model_norm = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=500)
model_norm.fit(X_train_norm, y_train)
y_pred_norm = model_norm.predict(X_test_norm)
print(f"    MSE: {mean_squared_error(y_test, y_pred_norm):.4f}")

print("\n" + "=" * 70)
print("步骤 5：误差分析")
print("=" * 70)

print("\n【训练误差 vs 测试误差分析】")
print("\n过拟合示例:")
X_overfit, y_overfit, _, _ = generate_data(n_samples=50, noise=5)
X_train_over, X_test_over, y_train_over, y_test_over = train_test_split(
    X_overfit, y_overfit, test_size=0.3, random_state=42)

scaler_over = StandardScaler()
X_train_over_scaled = scaler_over.fit_transform(X_train_over)
X_test_over_scaled = scaler_over.transform(X_test_over)

model_over = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=1000)
model_over.fit(X_train_over_scaled, y_train_over)
train_pred = model_over.predict(X_train_over_scaled)
test_pred = model_over.predict(X_test_over_scaled)

print(f"  训练集 MSE: {mean_squared_error(y_train_over, train_pred):.4f}")
print(f"  测试集 MSE: {mean_squared_error(y_test_over, test_pred):.4f}")
print(f"  差距: {mean_squared_error(y_test_over, test_pred) - mean_squared_error(y_train_over, train_pred):.4f}")
print(f"  过拟合风险: {'高' if abs(_) > 10 else '低'}")

print("\n" + "=" * 70)
print("问题解答")
print("=" * 70)

print("""
【问题 1: 为什么归一化会影响梯度下降速度？】

原因：特征尺度不同导致梯度下降路径呈椭圆状，收敛慢。
- 未归一化：大数值特征梯度大，小数值特征梯度小
- 优化路径：先在大梯度方向震荡，再慢慢调整小梯度方向
- 归一化后：各特征梯度相近，优化路径近似圆形，收敛更快

数学解释：
- 损失函数轮廓线由 ∇²f = H（Hessian矩阵）决定
- 未归一化时 H 的条件数大，梯度下降震荡
- 归一化后 H 条件数接近1，优化效率最大化
""")

print("""
【问题 2: L1 与 L2 正则化对参数的影响】

L2正则化 (Ridge: λ||w||²)：
- 惩罚项：λ * Σ(w_i²)
- 梯度：-2/n * Σx_i(y-ŷ) + 2λw
- 效果：所有权重缩小，趋于0但不为0
- 特点：权重平滑，不会产生稀疏解

L1正则化 (Lasso: λ||w||₁)：
- 惩罚项：λ * Σ|w_i|
- 梯度：-2/n * Σx_i(y-ŷ) + λ * sign(w)
- 效果：使部分权重 exactly 为0（稀疏解）
- 特点：可进行特征选择，适用于稀疏模型

对比：
- L2适合：多重共线性、特征关联紧密、避免过拟合
- L1适合：特征选择、高维稀疏数据
""")

print("""
【问题 3: 训练误差低是否意味着预测能力强？】

答案：不一定！需要区分以下情况：

1. 欠拟合（Underfitting）：
   - 训练误差高，测试误差也高
   - 模型太简单，无法捕捉数据模式

2. 过拟合（Overfitting）：
   - 训练误差很低
   - 测试误差很高（泛化能力差）
   - 模型记住了训练数据的噪声

3. 良好拟合（Good Fit）：
   - 训练误差低
   - 测试误差也低
   - 真正学到了数据规律

关键指标：
- 训练误差：模型在训练数据上的表现
- 测试误差：模型在新数据上的表现
- 泛化 Gap = 测试误差 - 训练误差

建议：始终使用验证集/测试集评估真实预测能力！
""")

print("\n" + "=" * 70)
print("可视化")
print("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].plot(model_gd.loss_history)
axes[0, 0].set_title('梯度下降 Loss 曲线')
axes[0, 0].set_xlabel('迭代次数')
axes[0, 0].set_ylabel('Loss')
axes[0, 0].grid(True)

for i, lr in enumerate([0.01, 0.1, 0.5]):
    model_temp = LinearRegressionFromScratch(learning_rate=lr, n_iterations=200)
    model_temp.fit(X_train_norm, y_train)
    axes[0, 1].plot(model_temp.loss_history, label=f'lr={lr}')
axes[0, 1].set_title('不同学习率的 Loss 曲线')
axes[0, 1].set_xlabel('迭代次数')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].legend()
axes[0, 1].grid(True)

methods = ['无正则化', 'L2正则化', 'L1正则化']
weights_compare = []
for reg, lam in [(None, 0), ('l2', 0.1), ('l1', 0.1)]:
    model_temp = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=500,
                                              regularization=reg, lambda_=lam)
    model_temp.fit(X_train_norm, y_train)
    weights_compare.append(model_temp.weights)

x_pos = np.arange(len(weights_compare[0]))
width = 0.25
for i, (w, label) in enumerate(zip(weights_compare, methods)):
    axes[0, 2].bar(x_pos + i*width, w, width, label=label)
axes[0, 2].set_title('正则化对权重的影响')
axes[0, 2].set_xlabel('特征')
axes[0, 2].set_ylabel('权重值')
axes[0, 2].legend()
axes[0, 2].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
axes[0, 2].grid(True, axis='y')

y_pred_all = [y_pred_analytical, y_pred_gd, y_pred_sklearn]
titles = ['解析解', '梯度下降', 'sklearn']
colors = ['blue', 'orange', 'green']

for idx, (pred, title, color) in enumerate(zip(y_pred_all, titles, colors)):
    axes[1, 0].scatter(y_test, pred, alpha=0.5, label=title, c=color)
axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1, 0].set_title('预测值 vs 真实值')
axes[1, 0].set_xlabel('真实值')
axes[1, 0].set_ylabel('预测值')
axes[1, 0].legend()
axes[1, 0].grid(True)

residuals = [y_test - pred for pred in y_pred_all]
for i, (res, title) in enumerate(zip(residuals, titles)):
    axes[1, 1].hist(res, bins=20, alpha=0.5, label=title)
axes[1, 1].set_title('残差分布')
axes[1, 1].set_xlabel('残差')
axes[1, 1].set_ylabel('频数')
axes[1, 1].legend()
axes[1, 1].grid(True)

train_mses = []
test_mses = []
for n in [20, 50, 100, 200, 500]:
    X_temp, y_temp, _, _ = generate_data(n_samples=n, noise=10)
    X_tr, X_te, y_tr, y_te = train_test_split(X_temp, y_temp, test_size=0.3, random_state=42)
    scaler_temp = StandardScaler()
    X_tr_s = scaler_temp.fit_transform(X_tr)
    X_te_s = scaler_temp.transform(X_te)

    model_temp = LinearRegressionFromScratch(learning_rate=0.1, n_iterations=500)
    model_temp.fit(X_tr_s, y_tr)
    train_mses.append(mean_squared_error(y_tr, model_temp.predict(X_tr_s)))
    test_mses.append(mean_squared_error(y_te, model_temp.predict(X_te_s)))

axes[1, 2].plot([20, 50, 100, 200, 500], train_mses, 'b-o', label='训练误差')
axes[1, 2].plot([20, 50, 100, 200, 500], test_mses, 'r-o', label='测试误差')
axes[1, 2].set_title('训练/测试误差 vs 数据量')
axes[1, 2].set_xlabel('训练样本数')
axes[1, 2].set_ylabel('MSE')
axes[1, 2].legend()
axes[1, 2].grid(True)

plt.tight_layout()
plt.savefig('linear_regression_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n可视化已保存到: linear_regression_analysis.png")
print("\n" + "=" * 70)
print("模板运行完成！")
print("=" * 70)