import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def _ensure_venv():
    try:
        import numpy  # noqa: F401
        import sklearn  # noqa: F401
        import matplotlib  # noqa: F401
        return
    except ImportError:
        pass

    for venv_name in (".venv", "venv"):
        venv_python = PROJECT_ROOT / venv_name / "Scripts" / "python.exe"
        if venv_python.exists():
            print(f"[检测] 当前 Python 缺少依赖，自动切换到 {venv_python}\n")
            code = subprocess.call([str(venv_python), str(__file__)])
            sys.exit(code)
    else:
        print("[错误] 未找到可用的 Python 环境，请先执行：")
        print(f"        pip install -r {PROJECT_ROOT / 'requirements.txt'}")
        sys.exit(1)


_ensure_venv()

EXPERIMENTS = [
    ("任务一：线性回归 - sklearn对比", "LinearRegression_Project/experiments/sklearn_compare.py"),
    ("任务一：线性回归 - 正则化比较", "LinearRegression_Project/experiments/compare.py"),
    ("任务一：线性回归 - 学习率实验", "LinearRegression_Project/experiments/learning_rate.py"),
    ("任务二：逻辑回归 - 分类评价", "ai-learning/experiments/classification_experiment.py"),
    ("任务二：逻辑回归 - 类别不平衡", "ai-learning/experiments/logistic_regression.py"),
    ("任务三：KNN - 维度实验", "KNN/experiments/experiment.py"),
    ("任务四：K-Means 聚类", "Kmeans/test/kmeantest.py"),
    ("任务四：PCA 降维", "Kmeans/test/pcatest.py"),
    ("任务四：层次聚类与标准化", "Kmeans/test/clustertest.py"),
]


def run_experiment(name, script_path):
    full_path = PROJECT_ROOT / script_path
    print(f"\n{'='*60}")
    print(f"  运行: {name}")
    print(f"  脚本: {script_path}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, str(full_path)],
        cwd=str(full_path.parent),
    )
    if result.returncode != 0:
        print(f"[失败] {name} 退出码: {result.returncode}")
    else:
        print(f"[成功] {name}")
    return result.returncode == 0


def main():
    print("=" * 60)
    print("  机器学习实验 - 一键运行所有实验")
    print("=" * 60)

    results = []
    for name, script in EXPERIMENTS:
        ok = run_experiment(name, script)
        results.append((name, ok))

    print(f"\n{'='*60}")
    print("  运行总结")
    print(f"{'='*60}")
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        status = "✓ 通过" if ok else "✗ 失败"
        print(f"  {status}  {name}")
    print(f"\n共 {total} 个实验，{passed} 个通过，{total - passed} 个失败")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())