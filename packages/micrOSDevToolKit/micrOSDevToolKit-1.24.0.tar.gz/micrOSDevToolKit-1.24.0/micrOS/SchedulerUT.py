import unittest
import sys
from unittest.mock import patch, MagicMock

sys.path.append('source')  # Add the 'source' folder to the import paths

class SchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.scheduler_input = "1:0:0:0!task1;2:0:0:0!task2"
        self.irqperiod = 1

    @patch('Scheduler.TaskManager.micropython.schedule', MagicMock(return_value=True))
    @patch('Scheduler.TaskManager.exec_lm_core_schedule', MagicMock(return_value=True))
    def test_scheduler_with_mocked_dependencies(self):
        from source.Scheduler import scheduler

        with patch('source.Scheduler.localtime') as mock_localtime:
            with patch('source.Scheduler.suntime') as mock_suntime:
                with patch('source.Scheduler.ntp_time') as mock_ntp_time:
                    mock_localtime.return_value = (2023, 7, 13, 1, 0, 0, 2, 194)
                    mock_suntime.return_value = True
                    mock_ntp_time.return_value = False

                    result = scheduler(self.scheduler_input, self.irqperiod)

                    self.assertTrue(result)
                    mock_localtime.assert_called_once()
                    mock_suntime.assert_called_once()
                    mock_ntp_time.assert_called_once()

if __name__ == '__main__':
    unittest.main()
