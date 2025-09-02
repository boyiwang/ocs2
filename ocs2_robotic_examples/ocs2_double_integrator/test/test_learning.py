class TestClassName(unittest.TestCase):  # 必须继承TestCase
    def setUp(self):        # 测试前准备
    def tearDown(self):     # 测试后清理  
    def test_xxx(self):     # 测试方法，必须以test_开头import unittest
from ocs2_double_integrator.test.DoubleIntegratorPyBindingTest import double_integrator_python_tests
from ocs2_double_integrator import scalar_array, vector_array
from ocs2_double_integrator import scalar_array, vector_array
from ocs2_double_integrator import scalar_array, vector_array

class TestDoubleIntegratorPyBinding(unittest.TestCase):
    """
    测试类必须继承 unittest.TestCase
    """
    
    def setUp(self):
        """
        setUp方法在每个测试方法执行前自动调用
        用于准备测试环境和初始化数据
        """
        self.test_instance = double_integrator_python_tests()
        self.test_instance.setUp()

    def test_mpc_initialization(self):
        """
        测试MPC接口初始化是否成功
        测试方法必须以 'test_' 开头
        """
        # 验证MPC对象是否正确创建
        self.assertIsNotNone(self.test_instance.mpc, "MPC interface should be initialized")
        
        # 验证维度设置是否正确
        self.assertEqual(self.test_instance.stateDim, 2, "State dimension should be 2")
        self.assertEqual(self.test_instance.inputDim, 1, "Input dimension should be 1")

    def test_mpc_solution_generation(self):
        """
        测试MPC求解过程
        """
        # 运行MPC求解
        self.test_instance.test_run_mpc()
        
        # 获取求解结果
        t_result = scalar_array()
        x_result = vector_array()
        u_result = vector_array()
        self.test_instance.mpc.getMpcSolution(t_result, x_result, u_result)
        
        # 验证解的基本属性
        self.assertGreater(len(t_result), 0, "MPC solution should have time steps")
        self.assertEqual(len(t_result), len(x_result), "Time and state arrays should have same length")
        self.assertEqual(len(t_result), len(u_result), "Time and input arrays should have same length")
        
        # 验证时间序列是递增的
        for i in range(1, len(t_result)):
            self.assertGreater(t_result[i], t_result[i-1], "Time should be increasing")

    def test_flow_map_derivatives(self):
        """
        测试流映射导数计算
        """
        # 先运行MPC获得解
        self.test_instance.test_run_mpc()
        
        # 获取第一个时间点的解
        t_result = scalar_array()
        x_result = vector_array()
        u_result = vector_array()
        self.test_instance.mpc.getMpcSolution(t_result, x_result, u_result)
        
        # 测试流映射导数
        flowMap = self.test_instance.mpc.flowMapLinearApproximation(
            t_result[0], x_result[0], u_result[0]
        )
        
        # 验证导数不为空
        self.assertIsNotNone(flowMap.f, "Flow map value should not be None")
        self.assertIsNotNone(flowMap.dfdx, "Flow map state derivative should not be None")
        self.assertIsNotNone(flowMap.dfdu, "Flow map input derivative should not be None")
        
        # 验证导数矩阵维度
        self.assertEqual(len(flowMap.f), 2, "Flow map should have 2 components (state dimension)")

    def test_cost_derivatives(self):
        """
        测试成本函数导数计算
        """
        # 先运行MPC获得解
        self.test_instance.test_run_mpc()
        
        # 获取第一个时间点的解
        t_result = scalar_array()
        x_result = vector_array()
        u_result = vector_array()
        self.test_instance.mpc.getMpcSolution(t_result, x_result, u_result)
        
        # 测试成本函数导数
        L = self.test_instance.mpc.costQuadraticApproximation(
            t_result[0], x_result[0], u_result[0]
        )
        
        # 验证成本函数值和导数
        self.assertIsNotNone(L.f, "Cost function value should not be None")
        self.assertIsNotNone(L.dfdx, "Cost state derivative should not be None")
        self.assertIsNotNone(L.dfdu, "Cost input derivative should not be None")
        self.assertGreaterEqual(L.f, 0, "Cost function should be non-negative")

    def tearDown(self):
        """
        tearDown方法在每个测试方法执行后自动调用
        用于清理测试环境
        """
        pass


if __name__ == "__main__":
    # 运行所有测试
    unittest.main()