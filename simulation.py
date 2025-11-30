import numpy as np
import pandas as pd

class BusinessSimulator:
    def __init__(self, start_cash, monthly_revenue, monthly_burn, team_size):
        self.start_cash = start_cash
        self.start_revenue = monthly_revenue
        self.start_burn = monthly_burn
        self.start_headcount = team_size

    def step(self, current_state, strategy_hiring, strategy_marketing):
        """
        Simulates one month.
        current_state: dict with keys 'cash', 'revenue', 'burn', 'headcount'
        strategy_hiring: 'Aggressive', 'Moderate', 'None'
        strategy_marketing: 'Double', 'Same'
        """
        cash = current_state['cash']
        revenue = current_state['revenue']
        burn = current_state['burn']
        headcount = current_state['headcount']

        if cash <= 0:
            return {
                'cash': 0,
                'revenue': 0,
                'burn': 0,
                'headcount': headcount,
                'alive': False
            }

        # 1. Apply Strategy Impact
        # Hiring
        hiring_cost_per_head = 5000 # Assumption: Cost to hire + salary impact
        salary_per_head = 8000 # Assumption: Monthly salary
        
        new_hires = 0
        if strategy_hiring == 'Aggressive':
            new_hires = 2
        elif strategy_hiring == 'Moderate':
            new_hires = 1
        
        headcount += new_hires
        burn += (new_hires * salary_per_head)
        
        # Marketing
        marketing_cost = 0
        revenue_growth_base = 0.02 # 2% organic growth
        
        if strategy_marketing == 'Double':
            marketing_cost = 5000 # Assumption: Extra marketing spend
            revenue_growth_base += 0.05 # Boost growth
        
        burn += marketing_cost

        # 2. Uncertainty Models
        # Demand shock: +/- 5%
        demand_shock = np.random.uniform(-0.05, 0.05)
        
        # Bad month: 10% chance of -20% revenue
        if np.random.random() < 0.10:
            demand_shock -= 0.20
            
        # Cost spike: 5% chance of +10% burn
        cost_shock = 0
        if np.random.random() < 0.05:
            cost_shock = 0.10
            
        # 3. Update State
        revenue_growth = revenue_growth_base + demand_shock
        revenue = revenue * (1 + revenue_growth)
        
        burn = burn * (1 + cost_shock)
        
        cash = cash + revenue - burn
        
        alive = True
        if cash <= 0:
            cash = 0
            alive = False
            
        return {
            'cash': cash,
            'revenue': revenue,
            'burn': burn,
            'headcount': headcount,
            'alive': alive
        }

    def run_simulation(self, months, runs, strategy_hiring, strategy_marketing):
        results = []
        
        for _ in range(runs):
            state = {
                'cash': self.start_cash,
                'revenue': self.start_revenue,
                'burn': self.start_burn,
                'headcount': self.start_headcount,
                'alive': True
            }
            
            run_history = []
            
            for month in range(months):
                if not state['alive']:
                    # Fill remaining months with dead state
                    run_history.append(state.copy())
                    continue
                    
                state = self.step(state, strategy_hiring, strategy_marketing)
                run_history.append(state.copy())
            
            results.append(run_history)
            
        return results

    def process_results(self, results):
        """
        Aggregates results for visualization.
        """
        # Convert to 3D array: [runs, months, features] is hard because dicts
        # Let's use pandas for easier aggregation
        
        # We want:
        # 1. Median cash per month + 10th/90th percentile
        # 2. Survival rate (percentage of runs alive at end)
        # 3. Final cash distribution
        
        months = len(results[0])
        runs = len(results)
        
        cash_matrix = np.zeros((runs, months))
        alive_final = []
        final_cash = []
        
        for i, run in enumerate(results):
            for t, step in enumerate(run):
                cash_matrix[i, t] = step['cash']
            
            alive_final.append(run[-1]['alive'])
            final_cash.append(run[-1]['cash'])
            
        # Cash stats
        median_cash = np.median(cash_matrix, axis=0)
        p10_cash = np.percentile(cash_matrix, 10, axis=0)
        p90_cash = np.percentile(cash_matrix, 90, axis=0)
        
        survival_rate = sum(alive_final) / runs
        
        return {
            'median_cash': median_cash,
            'p10_cash': p10_cash,
            'p90_cash': p90_cash,
            'survival_rate': survival_rate,
            'final_cash': final_cash,
            'months': list(range(1, months + 1))
        }
