import unittest
from simulation import BusinessSimulator

class TestBusinessSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = BusinessSimulator(
            start_cash=100000,
            monthly_revenue=10000,
            monthly_burn=5000,
            team_size=5,
            cac=50,
            arpu=100
        )

    def test_initialization(self):
        self.assertEqual(self.sim.start_cash, 100000)
        self.assertEqual(self.sim.start_revenue, 10000)

    def test_step_logic(self):
        # Test a single step with no strategy changes
        # We need to mock random to make it deterministic, or just check ranges
        # For simplicity, let's check if cash updates correctly roughly
        
        state = {
            'cash': 100000,
            'revenue': 10000,
            'burn': 5000,
            'headcount': 5,
            'alive': True
        }
        
        # Run one step
        new_state = self.sim.step(state, 'None', 'Same')
        
        # Cash should be approx 100000 + 10000 - 5000 = 105000
        # Allowing for random noise
        self.assertTrue(100000 < new_state['cash'] < 110000)
        self.assertTrue(new_state['alive'])

    def test_death_condition(self):
        state = {
            'cash': 100,
            'revenue': 0,
            'burn': 5000,
            'headcount': 5,
            'alive': True
        }
        new_state = self.sim.step(state, 'None', 'Same')
        self.assertFalse(new_state['alive'])
        self.assertEqual(new_state['cash'], 0)

    def test_hiring_impact(self):
        state = {
            'cash': 100000,
            'revenue': 10000,
            'burn': 5000,
            'headcount': 5,
            'alive': True
        }
        # Aggressive hiring adds 2 people
        new_state = self.sim.step(state, 'Aggressive', 'Same')
        self.assertEqual(new_state['headcount'], 7)
        # Burn should increase significantly (5000 + 2*8000 salary + hiring costs)
        self.assertTrue(new_state['burn'] > 5000)

if __name__ == '__main__':
    unittest.main()
