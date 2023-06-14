import pytest

if __name__ == "__main__":
    pytest.main(["-s", "-v", "--cov=./", "--cov-report=xml", "--cov-config=./.coveragerc", "unitest/"])
