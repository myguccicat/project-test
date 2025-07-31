import unittest
from modules.utils import log_app_usage

class TestUtilsModule(unittest.TestCase):

    def test_log_app_usage(self):
        # 測試不會拋錯例外（假設 log 是寫入檔案或 print，不回傳值）
        try:
            log_app_usage("Test log entry")
        except Exception as e:
            self.fail(f"log_app_usage() raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
