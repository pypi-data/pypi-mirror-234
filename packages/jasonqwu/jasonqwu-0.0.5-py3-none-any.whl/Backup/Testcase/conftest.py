import pytest

@pytest.fixture(scope="package", autouse=True)
def st_enptyEnv():
    print(f"\n### 初始化-目录")
    yield
    print(f"\n### 清除-目录")
