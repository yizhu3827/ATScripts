import pytest
if __name__ == '__main__':
    command_line = ["-s", "./scripts/test_*.py", "--alluredir", "./report/allure_json"]
    pytest.main(command_line)