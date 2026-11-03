"""
问题 4 单元测试: MeetingRoom

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 MeetingRoom 对象上的多个属性
（例如 bookings 列表、total_hours_booked、free slots、utilization rate）
以验证会议室状态和冲突管理。

运行测试：
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        验证空会议室的初始状态。
        """
        # TODO: 验证 room_id、capacity、bookings、total_hours_booked、is_maintenance
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)
        pass

    def test_single_booking_multi_attributes(self):
        """
        测试创建一个有效预订。
        验证 bookings 列表、total_hours_booked、utilization rate 和 free slots。
        """
        # TODO: 预订会议 'B01'，时间为 10 到 12，参与人数为 5
        self.room.book("B01", title="Team Meeting", start_time=10, end_time=12, attendees=5)
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)  # 12 - 10 = 2 hours
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")
        self.assertEqual(self.room.bookings[0]["start_time"], 10)
        self.assertEqual(self.room.bookings[0]["end_time"], 12)
        self.assertEqual(self.room.bookings[0]["attendees"], 5)

        pass

    def test_back_to_back_meetings_allowed(self):
        """
        测试有效的连续/背靠背会议 (例如 9-10 和 10-12) 不会引发冲突错误。
        验证两个预订成功后的多属性状态。
        """
        # TODO: 预订 'B01'，时间为 9 到 10
        self.room.book("B01", title="Back-to-Back Meeting 1", start_time=9, end_time=10, attendees=5)
        # TODO: 预订 'B02'，时间为 10 到 12
        self.room.book("B02", title="Back-to-Back Meeting 2", start_time=10, end_time=12, attendees=5)
        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(self.room.total_hours_booked, 3)  # (10 - 9) + (12 - 10) = 1 + 2 = 3 hours
        pass

    def test_overlapping_booking_rejected(self):
        """
        测试重叠预订（例如 9-11 与 10-12, 或完全包含在 9-12 与 10-11 之间）
        应抛出 ValueError, 并保持会议室状态不变。
        """
        # TODO: 使用 self.assertRaises(ValueError) 实现测试
        self.room.book("B01", title="Initial Meeting", start_time=9, end_time=11, attendees=5)
        with self.assertRaises(ValueError):
            self.room.book("B02", title="Overlapping Meeting", start_time=10, end_time=12, attendees=5)
        self.assertEqual(len(self.room.bookings), 1)
        pass

    def test_cancel_booking_updates_all_attributes(self):
        """
        测试取消预订是否能正确从 bookings 中移除，
        减少 total_hours_booked, 并恢复 free slots。
        """
        # TODO: 预订两场会议，取消其中一场，并验证所有属性
        self.room.book("B01", title="Meeting 1", start_time=9, end_time=11, attendees=5)
        self.room.book("B02", title="Meeting 2", start_time=12, end_time=14, attendees=5)
        self.assertEqual(len(self.room.bookings), 2)
        self.room.cancel("B01")
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 2)  # Only B02
        self.assertEqual(self.room.bookings[0]["booking_id"], "B02")
        pass

    def test_capacity_and_validation_exceptions(self):
        """
        测试边界情况和异常：
        - 参与人数超过容量 (ValueError)
        - 开始时间 >= 结束时间 (ValueError)
        - 预订 ID 重复 (ValueError)
        - 会议室处于维护状态时预订 (RuntimeError)
        - 取消不存在的预订 (KeyError)
        """
        # TODO: 使用 self.assertRaises() 实现异常测试
        with self.assertRaises(ValueError):
            self.room.book("B01", title="Over Capacity", start_time=10, end_time=12, attendees=15)
        with self.assertRaises(ValueError):
            self.room.book("B02", title="Invalid Time", start_time=12, end_time=10, attendees=5)
        self.room.book("B03", title="Valid Meeting", start_time=10, end_time=12, attendees=5)
        with self.assertRaises(ValueError):
            self.room.book("B03", title="Duplicate ID", start_time=13, end_time=14, attendees=5)
        self.room.is_maintenance = True
        with self.assertRaises(RuntimeError):
            self.room.book("B04", title="Maintenance Booking", start_time=14, end_time=15, attendees=5)
        self.room.is_maintenance = False
        with self.assertRaises(KeyError):
            self.room.cancel("NonExistentBooking")
        pass


if __name__ == "__main__":
    unittest.main()
