import numpy as np
import pandas as pd

class BusinessSimulator:
    def __init__(self, start_cash, monthly_revenue, monthly_burn, team_size, cac, arpu):
        self.start_cash = start_cash
        self.start_revenue = monthly_revenue
        self.start_burn = monthly_burn
        self.start_headcount = team_size
        self.cac = cac
        self.arpu = arpu

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
        
        # Marketing & Growth (Unit Economics Model)
        marketing_budget = 0
        organic_growth_rate = 0.02 # 2% organic word-of-mouth
        
        if strategy_marketing == 'Double':
            marketing_budget = 5000 # Extra marketing spend
        
        burn += marketing_budget

        # Calculate new customers from marketing
        # Avoid division by zero if CAC is 0 (unlikely but safe)
        cac = max(self.cac, 1.0) 
        paid_customers = marketing_budget / cac
        
        # Calculate current customers
        current_customers = revenue / max(self.arpu, 1.0)
        
        # Organic growth
        organic_customers = current_customers * organic_growth_rate
        
        # Total new customers
        total_new_customers = paid_customers + organic_customers

        # 2. Uncertainty Models
        # Demand shock: +/- 5% on new customer acquisition
        demand_shock = np.random.uniform(-0.05, 0.05)
        total_new_customers = total_new_customers * (1 + demand_shock)
        
        # Bad month: 10% chance of churn spike (losing customers)
        churn_rate = 0.05 # 5% base churn
        if np.random.random() < 0.10:
            churn_rate += 0.10 # Spike to 15% churn
            
        # Update customer count
        churned_customers = current_customers * churn_rate
        next_customers = current_customers + total_new_customers - churned_customers
        
        # Cost spike: 5% chance of +10% burn
        cost_shock = 0
        if np.random.random() < 0.05:
            cost_shock = 0.10
            
        # 3. Update State
        revenue = next_customers * self.arpu
        
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
