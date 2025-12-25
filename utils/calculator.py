# -*- coding: utf-8 -*-
"""
CALCULATOR - MATHEMATICAL AND STATISTICAL CALCULATIONS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import math
import statistics
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta

class Calculator:
    @staticmethod
    def calculate_success_rate(sent: int, verified: int) -> float:
        """Calculate success rate percentage"""
        if sent == 0:
            return 0.0
        return (verified / sent) * 100
    
    @staticmethod
    def calculate_delivery_rate(sent: int, target: int) -> float:
        """Calculate delivery rate percentage"""
        if target == 0:
            return 0.0
        return (sent / target) * 100
    
    @staticmethod
    def calculate_views_per_minute(views: int, seconds: float) -> float:
        """Calculate views per minute"""
        if seconds == 0:
            return 0.0
        return (views / seconds) * 60
    
    @staticmethod
    def calculate_efficiency_score(success_rate: float, duration: float, 
                                 views_sent: int, max_score: int = 10) -> float:
        """Calculate efficiency score (0-10)"""
        if duration <= 0 or views_sent <= 0:
            return 0.0
        
        # Normalize factors
        success_factor = success_rate / 100  # 0-1
        speed_factor = min(1.0, (views_sent / duration) / 100)  # 100 views/sec = 1
        consistency_factor = 0.8  # Could be calculated from variance
        
        # Weighted average
        score = (success_factor * 0.5) + (speed_factor * 0.3) + (consistency_factor * 0.2)
        
        # Scale to max_score
        return round(score * max_score, 2)
    
    @staticmethod
    def calculate_estimated_time(views: int, views_per_minute: float) -> float:
        """Calculate estimated completion time in minutes"""
        if views_per_minute <= 0:
            return 0.0
        return views / views_per_minute
    
    @staticmethod
    def calculate_cost(views: int, cost_per_view: float = 0.001) -> float:
        """Calculate cost for views"""
        return views * cost_per_view
    
    @staticmethod
    def calculate_profit(revenue: float, cost: float) -> float:
        """Calculate profit"""
        return revenue - cost
    
    @staticmethod
    def calculate_profit_margin(revenue: float, cost: float) -> float:
        """Calculate profit margin percentage"""
        if revenue == 0:
            return 0.0
        return ((revenue - cost) / revenue) * 100
    
    @staticmethod
    def calculate_roi(investment: float, return_amount: float) -> float:
        """Calculate Return on Investment percentage"""
        if investment == 0:
            return 0.0
        return ((return_amount - investment) / investment) * 100
    
    @staticmethod
    def calculate_growth_rate(current: float, previous: float) -> float:
        """Calculate growth rate percentage"""
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def calculate_compound_growth_rate(initial: float, final: float, 
                                      periods: int) -> float:
        """Calculate compound annual growth rate"""
        if initial == 0 or periods == 0:
            return 0.0
        
        rate = (final / initial) ** (1 / periods) - 1
        return rate * 100
    
    @staticmethod
    def calculate_average(values: List[float]) -> float:
        """Calculate average"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def calculate_weighted_average(values: List[float], weights: List[float]) -> float:
        """Calculate weighted average"""
        if not values or not weights or len(values) != len(weights):
            return 0.0
        
        weighted_sum = sum(v * w for v, w in zip(values, weights))
        total_weight = sum(weights)
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    @staticmethod
    def calculate_median(values: List[float]) -> float:
        """Calculate median"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        
        if n % 2 == 0:
            mid1 = sorted_values[n // 2 - 1]
            mid2 = sorted_values[n // 2]
            return (mid1 + mid2) / 2
        else:
            return sorted_values[n // 2]
    
    @staticmethod
    def calculate_mode(values: List[float]) -> List[float]:
        """Calculate mode(s)"""
        if not values:
            return []
        
        from collections import Counter
        counter = Counter(values)
        max_count = max(counter.values())
        
        return [value for value, count in counter.items() if count == max_count]
    
    @staticmethod
    def calculate_standard_deviation(values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.0
        
        try:
            return statistics.stdev(values)
        except:
            return 0.0
    
    @staticmethod
    def calculate_variance(values: List[float]) -> float:
        """Calculate variance"""
        if len(values) < 2:
            return 0.0
        
        try:
            return statistics.variance(values)
        except:
            return 0.0
    
    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        
        if index.is_integer():
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index % 1)
    
    @staticmethod
    def calculate_correlation(x_values: List[float], y_values: List[float]) -> float:
        """Calculate correlation coefficient"""
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        try:
            return statistics.correlation(x_values, y_values)
        except:
            # Manual calculation
            n = len(x_values)
            sum_x = sum(x_values)
            sum_y = sum(y_values)
            sum_xy = sum(x * y for x, y in zip(x_values, y_values))
            sum_x2 = sum(x * x for x in x_values)
            sum_y2 = sum(y * y for y in y_values)
            
            numerator = (n * sum_xy) - (sum_x * sum_y)
            denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
            
            if denominator == 0:
                return 0.0
            
            return numerator / denominator
    
    @staticmethod
    def calculate_linear_regression(x_values: List[float], y_values: List[float]) -> Tuple[float, float]:
        """Calculate linear regression coefficients (slope, intercept)"""
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0, 0.0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        return slope, intercept
    
    @staticmethod
    def calculate_trend(values: List[float]) -> str:
        """Calculate trend (increasing, decreasing, stable)"""
        if len(values) < 2:
            return "stable"
        
        # Simple trend detection
        increasing = 0
        decreasing = 0
        
        for i in range(1, len(values)):
            if values[i] > values[i-1]:
                increasing += 1
            elif values[i] < values[i-1]:
                decreasing += 1
        
        if increasing > decreasing * 1.5:
            return "increasing"
        elif decreasing > increasing * 1.5:
            return "decreasing"
        else:
            return "stable"
    
    @staticmethod
    def calculate_forecast(values: List[float], periods: int = 1) -> List[float]:
        """Calculate simple moving average forecast"""
        if not values or periods <= 0:
            return []
        
        forecast = []
        window_size = min(5, len(values))  # Use last 5 values or less
        
        for i in range(periods):
            last_values = values[-window_size:]
            forecast_value = sum(last_values) / len(last_values)
            forecast.append(forecast_value)
        
        return forecast
    
    @staticmethod
    def calculate_performance_index(success_rate: float, speed: float, 
                                   reliability: float, weights: Dict = None) -> float:
        """Calculate overall performance index"""
        if weights is None:
            weights = {'success': 0.4, 'speed': 0.3, 'reliability': 0.3}
        
        # Normalize values (assuming 0-100 scale)
        success_norm = success_rate / 100
        speed_norm = min(1.0, speed / 1000)  # Assuming 1000 views/min is max
        reliability_norm = reliability / 100
        
        # Calculate weighted score
        score = (success_norm * weights['success'] + 
                speed_norm * weights['speed'] + 
                reliability_norm * weights['reliability'])
        
        return round(score * 100, 2)
    
    @staticmethod
    def calculate_confidence_interval(values: List[float], confidence: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval"""
        if len(values) < 2:
            return 0.0, 0.0
        
        mean = Calculator.calculate_average(values)
        stdev = Calculator.calculate_standard_deviation(values)
        n = len(values)
        
        # Z-score for confidence level
        z_scores = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576
        }
        
        z = z_scores.get(confidence, 1.96)
        
        margin_of_error = z * (stdev / math.sqrt(n))
        
        return (mean - margin_of_error, mean + margin_of_error)
    
    @staticmethod
    def calculate_probability_distribution(values: List[float], bins: int = 10) -> Dict:
        """Calculate probability distribution"""
        if not values:
            return {}
        
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins
        
        distribution = {}
        for i in range(bins):
            bin_start = min_val + (i * bin_width)
            bin_end = bin_start + bin_width
            bin_key = f"{bin_start:.2f}-{bin_end:.2f}"
            
            count = sum(1 for v in values if bin_start <= v < bin_end)
            probability = count / len(values)
            
            distribution[bin_key] = {
                'count': count,
                'probability': probability,
                'percentage': probability * 100
            }
        
        return distribution
    
    @staticmethod
    def calculate_entropy(values: List[float]) -> float:
        """Calculate entropy (measure of uncertainty)"""
        if not values:
            return 0.0
        
        # Normalize values to probabilities
        total = sum(values)
        if total == 0:
            return 0.0
        
        probabilities = [v / total for v in values]
        
        # Calculate entropy
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        
        return entropy
    
    @staticmethod
    def calculate_break_even_point(fixed_costs: float, price_per_unit: float, 
                                  variable_cost_per_unit: float) -> float:
        """Calculate break-even point in units"""
        if price_per_unit <= variable_cost_per_unit:
            return 0.0
        
        return fixed_costs / (price_per_unit - variable_cost_per_unit)
    
    @staticmethod
    def calculate_net_present_value(cash_flows: List[float], discount_rate: float = 0.1) -> float:
        """Calculate Net Present Value"""
        npv = 0.0
        
        for t, cash_flow in enumerate(cash_flows):
            npv += cash_flow / ((1 + discount_rate) ** t)
        
        return npv
    
    @staticmethod
    def calculate_internal_rate_of_return(cash_flows: List[float], 
                                         guess: float = 0.1) -> float:
        """Calculate Internal Rate of Return"""
        # Simple IRR calculation using Newton's method
        def npv_func(rate):
            npv = 0.0
            for t, cash_flow in enumerate(cash_flows):
                npv += cash_flow / ((1 + rate) ** t)
            return npv
        
        # Use binary search for simplicity
        low, high = -0.99, 10.0
        for _ in range(100):
            mid = (low + high) / 2
            if npv_func(mid) > 0:
                low = mid
            else:
                high = mid
        
        return (low + high) / 2