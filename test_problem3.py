"""
问题 3 单元测试: Order

说明：
使用 Python 的 unittest 框架补全下面的单元测试方法。
你的测试方法必须断言 Order 对象上的多个属性
（例如 subtotal、discount_amount、tax_amount、shipping_fee、final_total、status）
以验证在各种条件下的状态一致性。

运行测试：
    python -m unittest test_problem3.py -v
"""
import unittest
from problem3 import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """
        在每个测试方法执行前设置测试夹具。
        """
        self.regular_order = Order("ORD100", customer_tier="regular")
        self.silver_order = Order("ORD200", customer_tier="silver")
        self.gold_order = Order("ORD300", customer_tier="gold")

    # TODO: 为 Order 类开发 5 个测试方法 develop 5 test methods for Order class
    def test1_basic_calculation(self):
        """
        TODO: 测试向订单中添加商品后的费用计算。
        断言 subtotal、discount_amount、tax_amount、shipping_fee 和 final_total。
        """
        self.regular_order.add_item("Widget", price=20.0, quantity=2)
        self.assertEqual(self.regular_order.subtotal, 40.0)
        self.assertEqual(self.regular_order.discount_amount, 0.0)
        self.assertAlmostEqual(self.regular_order.tax_amount, 3.2)  # 40 * 0.08 = 3.2
        self.assertEqual(self.regular_order.shipping_fee, 5.99)  # subtotal < 50
        self.assertAlmostEqual(self.regular_order.final_total, 49.19)  # 40 + 3.2 + 5.99 = 49.19
        self.assertEqual(self.regular_order.status, "PENDING")
        self.assertIsNone(self.regular_order.applied_coupon)

        pass


    def test2_discount_coupon_and_free_shipping(self):
        """
        TODO:测试银卡折扣、SAVE10优惠券以及免运费。
        断言 subtotal、discount_amount、tax_amount、shipping_fee 和 final_total。 
        """
        self.silver_order.add_item("Gadget", price=30.0, quantity=2)  # subtotal = 60
        self.silver_order.apply_coupon("SAVE10")  # 10% off coupon, silver_order has 5% discount.
        self.assertEqual(self.silver_order.subtotal, 60.0)
        self.assertAlmostEqual(self.silver_order.discount_amount, 8.7) # 60 * (1 - 0.05) = 57, 57 * (1-0.10) = 51.3, discount_amount = 60 - 51.3 = 8.7
        self.assertAlmostEqual(self.silver_order.tax_amount, 4.1) 
        self.assertEqual(self.silver_order.shipping_fee, 0.0)  
        self.assertAlmostEqual(self.silver_order.final_total, 55.4)  
        self.assertEqual(self.silver_order.status, "PENDING")
        self.assertEqual(self.silver_order.applied_coupon, "SAVE10")
        pass

    def test3_grocery_tax_exemption(self):
        """
        TODO:测试食品免税逻辑
        断言 subtotal、discount_amount、tax_amount、shipping_fee 和 final_total。
        """
        self.gold_order.add_item("Apple", price=10.0, quantity=5, category="grocery")  # subtotal = 50
        self.gold_order.apply_coupon("FLAT15")  # $15 off coupon, gold_order has 10% discount.
        self.assertEqual(self.gold_order.subtotal, 50.0)
        self.assertAlmostEqual(self.gold_order.discount_amount, 20.0)  # 50 * (1 - 0.10) = 45, 45 - 15 = 30, discount_amount = 50 - 30 = 20
        self.assertAlmostEqual(self.gold_order.tax_amount, 0.0)  # grocery items are tax-exempt
        self.assertEqual(self.gold_order.shipping_fee, 5.99)  # subtotal < 50 after discount
        self.assertAlmostEqual(self.gold_order.final_total, 35.99)  # 30 + 0 + 5.99 = 35.99
        self.assertEqual(self.gold_order.status, "PENDING")
        self.assertEqual(self.gold_order.applied_coupon, "FLAT15")

        pass

    def test4_status_transitions(self):
        """
        TODO:测试结账(PAID)和取消(CANCELLED)状态转换及其限制
        断言 subtotal、discount_amount、tax_amount、shipping_fee 和 final_total。
        """
        self.regular_order.add_item("Widget", price=20.0, quantity=1)
        self.regular_order.status = "PAID"
        with self.assertRaises(RuntimeError):
            self.regular_order.add_item("Gadget", price=10.0, quantity=1)
        with self.assertRaises(RuntimeError):
            self.regular_order.remove_item("Widget")
        self.assertEqual(self.regular_order.status, "PAID")
        self.silver_order.status = "CANCELLED"
        with self.assertRaises(RuntimeError):
            self.silver_order.add_item("Gadget", price=10.0, quantity=1)
        with self.assertRaises(RuntimeError):
            self.silver_order.remove_item("Gadget")
        self.assertEqual(self.silver_order.status, "CANCELLED")

        pass

    def test5_invalid_operations_and_limits(self):
        """
        TODO:测试各种异常和 FLAT15 的底线逻辑
        断言 subtotal、discount_amount、tax_amount、shipping_fee 和 final_total。
        """
        # 1. 无效的会员等级
        with self.assertRaises(ValueError):
            Order("ORD999", customer_tier="platinum")
            
        # 2. 添加负价格/零数量
        with self.assertRaises(ValueError):
            self.regular_order.add_item("Bad", price=-5.00)
        with self.assertRaises(ValueError):
            self.regular_order.add_item("Bad", price=5.00, quantity=0)
            
        # 3. 无效的优惠券
        with self.assertRaises(ValueError):
            self.regular_order.apply_coupon("INVALID")
            
        # 4. FLAT15 不能把总价减成负数（买 $10 的东西用 FLAT15，只能减 $10）
        self.regular_order.add_item("Cheap", price=10.00)
        self.regular_order.apply_coupon("FLAT15")
        self.assertEqual(self.regular_order.discount_amount, 10.00)  # discount cannot exceed subtotal
        self.assertEqual(self.regular_order.final_total, 5.99)  # subtotal - discount + tax + shipping = 10 - 10 + 0 + 5.99 = 5.99
        

        pass

if __name__ == "__main__":
    unittest.main()
