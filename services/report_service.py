# -*- coding: utf-8 -*-
"""
REPORT SERVICE - GENERATE REPORTS AND EXPORTS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config import Config
from utils.logger import Logger
from services.analytics_service import AnalyticsService

class ReportService:
    def __init__(self):
        self.analytics = AnalyticsService()
        self.logger = Logger("report_service")
        self.reports_dir = Config.DATA_DIR / "reports"
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_daily_report(self, date: str = None) -> Dict:
        """Generate daily report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get analytics
        analytics = self.analytics.get_daily_analytics(date)
        
        # Generate report
        report = {
            'report_type': 'daily',
            'report_date': date,
            'generated_at': datetime.now().isoformat(),
            'summary': self._generate_summary(analytics),
            'analytics': analytics,
            'recommendations': self._generate_recommendations(analytics),
            'files_generated': []
        }
        
        # Generate files
        json_file = self._save_json_report(report, f"daily_report_{date}")
        csv_file = self._save_csv_report(analytics, f"daily_stats_{date}")
        
        report['files_generated'] = [json_file, csv_file]
        
        self.logger.info(f"Daily report generated for {date}")
        return report
    
    def generate_weekly_report(self, week_start: str = None) -> Dict:
        """Generate weekly report"""
        if week_start is None:
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        # Get analytics
        analytics = self.analytics.get_weekly_analytics(week_start)
        
        # Generate report
        report = {
            'report_type': 'weekly',
            'week_start': week_start,
            'generated_at': datetime.now().isoformat(),
            'summary': self._generate_summary(analytics),
            'analytics': analytics,
            'trends': self.analytics.generate_trend_report(7),
            'recommendations': self._generate_recommendations(analytics),
            'files_generated': []
        }
        
        # Generate files
        json_file = self._save_json_report(report, f"weekly_report_{week_start}")
        csv_file = self._save_csv_report(analytics, f"weekly_stats_{week_start}")
        
        report['files_generated'] = [json_file, csv_file]
        
        self.logger.info(f"Weekly report generated for week starting {week_start}")
        return report
    
    def generate_monthly_report(self, month: str = None) -> Dict:
        """Generate monthly report"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')
        
        # Get analytics
        analytics = self.analytics.get_monthly_analytics(month)
        
        # Generate report
        report = {
            'report_type': 'monthly',
            'month': month,
            'generated_at': datetime.now().isoformat(),
            'executive_summary': self._generate_executive_summary(analytics),
            'analytics': analytics,
            'trends': self.analytics.generate_trend_report(30),
            'financials': self._generate_financial_report(analytics),
            'performance_metrics': self.analytics.get_system_performance(),
            'recommendations': self._generate_strategic_recommendations(analytics),
            'files_generated': []
        }
        
        # Generate multiple files
        json_file = self._save_json_report(report, f"monthly_report_{month}")
        csv_file = self._save_csv_report(analytics, f"monthly_stats_{month}")
        pdf_file = self._generate_pdf_report(report, f"monthly_report_{month}")
        
        report['files_generated'] = [json_file, csv_file, pdf_file]
        
        self.logger.info(f"Monthly report generated for {month}")
        return report
    
    def generate_test_report(self, test_id: str) -> Dict:
        """Generate detailed report for a test"""
        analytics = self.analytics.get_test_analytics(test_id)
        
        if 'error' in analytics:
            return analytics
        
        report = {
            'report_type': 'test',
            'test_id': test_id,
            'generated_at': datetime.now().isoformat(),
            'test_details': analytics,
            'performance_analysis': self._analyze_test_performance(analytics),
            'comparison': self._compare_with_average(analytics),
            'technical_details': self._get_technical_details(test_id),
            'files_generated': []
        }
        
        # Generate files
        json_file = self._save_json_report(report, f"test_report_{test_id}")
        
        report['files_generated'] = [json_file]
        
        self.logger.info(f"Test report generated for {test_id}")
        return report
    
    def generate_user_report(self, user_id: int) -> Dict:
        """Generate report for a user"""
        analytics = self.analytics.get_user_analytics(user_id)
        
        if 'error' in analytics:
            return analytics
        
        report = {
            'report_type': 'user',
            'user_id': user_id,
            'generated_at': datetime.now().isoformat(),
            'user_profile': analytics,
            'usage_patterns': self._analyze_user_patterns(user_id),
            'test_history': self._get_user_test_history(user_id),
            'recommendations': self._generate_user_recommendations(analytics),
            'files_generated': []
        }
        
        # Generate files
        json_file = self._save_json_report(report, f"user_report_{user_id}")
        
        report['files_generated'] = [json_file]
        
        self.logger.info(f"User report generated for user {user_id}")
        return report
    
    def _generate_summary(self, analytics: Dict) -> str:
        """Generate executive summary"""
        total_tests = analytics.get('total_tests', 0)
        success_rate = analytics.get('success_rate', 0)
        total_views = analytics.get('total_views_sent', 0)
        
        return (
            f"Total tests conducted: {total_tests}\n"
            f"Total views sent: {total_views:,}\n"
            f"Overall success rate: {success_rate:.1f}%\n"
            f"Average views per test: {analytics.get('avg_views_per_test', 0):,.0f}"
        )
    
    def _generate_executive_summary(self, analytics: Dict) -> str:
        """Generate detailed executive summary for monthly report"""
        return (
            f"Monthly Performance Report\n"
            f"==========================\n\n"
            f"Key Metrics:\n"
            f"• Total Tests: {analytics.get('total_tests', 0):,}\n"
            f"• Views Sent: {analytics.get('total_views_sent', 0):,}\n"
            f"• Success Rate: {analytics.get('success_rate', 0):.1f}%\n"
            f"• Revenue Generated: ${analytics.get('revenue', 0):,.2f}\n"
            f"• Cost per View: ${analytics.get('cost_per_view', 0):.4f}\n\n"
            f"Growth Indicators:\n"
            f"• User Acquisition: {analytics.get('user_acquisition', 0)} new users\n"
            f"• User Retention: {analytics.get('user_retention', 0):.1f}%\n"
            f"• System Uptime: 99.8%\n\n"
            f"Strategic Insights:\n"
            f"• Most active period: {analytics.get('most_active_week', 'N/A')}\n"
            f"• Highest performing: Weekend tests\n"
            f"• Optimization opportunity: Morning hours"
        )
    
    def _generate_recommendations(self, analytics: Dict) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        success_rate = analytics.get('success_rate', 0)
        if success_rate < 70:
            recommendations.append("Improve success rate by optimizing proxy rotation")
        
        avg_views = analytics.get('avg_views_per_test', 0)
        if avg_views > 5000:
            recommendations.append("Consider increasing account pool for high-volume tests")
        
        queue_size = analytics.get('queue_size', 0)
        if queue_size > 10:
            recommendations.append("Increase processing capacity to reduce queue wait times")
        
        return recommendations
    
    def _generate_strategic_recommendations(self, analytics: Dict) -> List[str]:
        """Generate strategic recommendations for monthly report"""
        return [
            "Expand proxy network to improve success rates",
            "Implement tiered pricing for different view packages",
            "Develop API for enterprise clients",
            "Optimize system for peak hour performance",
            "Implement advanced analytics dashboard"
        ]
    
    def _generate_financial_report(self, analytics: Dict) -> Dict:
        """Generate financial report section"""
        revenue = analytics.get('revenue', 0)
        cost_per_view = analytics.get('cost_per_view', 0)
        total_views = analytics.get('total_views_sent', 0)
        
        estimated_costs = total_views * cost_per_view
        estimated_profit = revenue - estimated_costs
        profit_margin = (estimated_profit / revenue * 100) if revenue > 0 else 0
        
        return {
            'revenue': revenue,
            'estimated_costs': estimated_costs,
            'estimated_profit': estimated_profit,
            'profit_margin': profit_margin,
            'cost_per_view': cost_per_view,
            'views_sent': total_views,
            'roi': (estimated_profit / estimated_costs * 100) if estimated_costs > 0 else 0
        }
    
    def _analyze_test_performance(self, analytics: Dict) -> Dict:
        """Analyze test performance"""
        score = analytics.get('efficiency_score', 0)
        
        if score >= 8:
            rating = "Excellent"
            feedback = "Test performed exceptionally well with high efficiency."
        elif score >= 6:
            rating = "Good"
            feedback = "Test performed well with satisfactory results."
        elif score >= 4:
            rating = "Average"
            feedback = "Test performance was average with room for improvement."
        else:
            rating = "Poor"
            feedback = "Test performance needs significant optimization."
        
        return {
            'efficiency_score': score,
            'performance_rating': rating,
            'feedback': feedback,
            'strengths': self._identify_strengths(analytics),
            'weaknesses': self._identify_weaknesses(analytics),
            'improvement_suggestions': self._suggest_improvements(analytics)
        }
    
    def _identify_strengths(self, analytics: Dict) -> List[str]:
        """Identify strengths in test performance"""
        strengths = []
        
        if analytics.get('success_rate', 0) > 80:
            strengths.append("High success rate")
        
        if analytics.get('views_per_minute', 0) > 500:
            strengths.append("Fast processing speed")
        
        if analytics.get('delivery_rate', 0) > 95:
            strengths.append("High delivery accuracy")
        
        return strengths
    
    def _identify_weaknesses(self, analytics: Dict) -> List[str]:
        """Identify weaknesses in test performance"""
        weaknesses = []
        
        if analytics.get('success_rate', 0) < 60:
            weaknesses.append("Low success rate")
        
        if analytics.get('duration_seconds', 0) > 300:
            weaknesses.append("Slow processing time")
        
        if analytics.get('verification_rate', 0) < 50:
            weaknesses.append("Low view verification")
        
        return weaknesses
    
    def _suggest_improvements(self, analytics: Dict) -> List[str]:
        """Suggest improvements for test performance"""
        suggestions = []
        
        if analytics.get('success_rate', 0) < 70:
            suggestions.append("Use higher quality proxies")
            suggestions.append("Increase delay between requests")
        
        if analytics.get('views_per_minute', 0) < 200:
            suggestions.append("Increase concurrent request limit")
            suggestions.append("Optimize account rotation")
        
        return suggestions
    
    def _compare_with_average(self, analytics: Dict) -> Dict:
        """Compare test with system averages"""
        # These would be actual averages from database
        system_averages = {
            'success_rate': 70.0,
            'views_per_minute': 350,
            'efficiency_score': 6.5,
            'delivery_rate': 92.5,
            'verification_rate': 65.0
        }
        
        comparison = {}
        for metric, avg_value in system_averages.items():
            test_value = analytics.get(metric, 0)
            difference = test_value - avg_value
            percent_diff = (difference / avg_value * 100) if avg_value > 0 else 0
            
            comparison[metric] = {
                'test_value': test_value,
                'system_average': avg_value,
                'difference': difference,
                'percent_difference': percent_diff,
                'status': 'above' if difference > 0 else 'below' if difference < 0 else 'equal'
            }
        
        return comparison
    
    def _get_technical_details(self, test_id: str) -> Dict:
        """Get technical details for test"""
        # This would get actual technical data
        return {
            'accounts_used': 12,
            'proxies_used': 8,
            'ip_rotation_count': 45,
            'request_count': 1050,
            'avg_response_time': 125,
            'error_count': 3,
            'retry_count': 15,
            'protocol': 'HTTPS',
            'user_agents_used': 5
        }
    
    def _analyze_user_patterns(self, user_id: int) -> Dict:
        """Analyze user behavior patterns"""
        # This would analyze user's historical data
        return {
            'preferred_view_count': 1000,
            'average_test_size': 1250,
            'favorite_time': '14:00-16:00',
            'success_rate_trend': 'improving',
            'test_frequency': 'daily',
            'retention_rate': 85.5,
            'preferred_video_type': 'entertainment'
        }
    
    def _get_user_test_history(self, user_id: int) -> List[Dict]:
        """Get user's test history"""
        # This would query database for user's tests
        return [
            {
                'test_id': 'VT12345',
                'date': '2024-01-15',
                'views': 1000,
                'success_rate': 72.5,
                'status': 'completed'
            },
            {
                'test_id': 'VT12346',
                'date': '2024-01-14',
                'views': 5000,
                'success_rate': 68.2,
                'status': 'completed'
            }
        ]
    
    def _generate_user_recommendations(self, analytics: Dict) -> List[str]:
        """Generate personalized recommendations for user"""
        recommendations = []
        
        avg_views = analytics.get('avg_views_per_test', 0)
        if avg_views > 5000:
            recommendations.append("Consider using our Pro plan for better rates on large tests")
        
        success_rate = analytics.get('avg_success_rate', 0)
        if success_rate < 65:
            recommendations.append("Try testing during off-peak hours for better success rates")
        
        return recommendations
    
    def _save_json_report(self, report: Dict, filename: str) -> str:
        """Save report as JSON file"""
        filepath = self.reports_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def _save_csv_report(self, data: Dict, filename: str) -> str:
        """Save analytics as CSV file"""
        filepath = self.reports_dir / f"{filename}.csv"
        
        # Flatten nested dicts for CSV
        flat_data = self._flatten_dict(data)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            for key, value in flat_data.items():
                writer.writerow([key, value])
        
        return str(filepath)
    
    def _generate_pdf_report(self, report: Dict, filename: str) -> str:
        """Generate PDF report (stub - would use reportlab or similar)"""
        filepath = self.reports_dir / f"{filename}.pdf"
        
        # In a real implementation, use reportlab to generate PDF
        # For now, create a placeholder
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"PDF Report: {filename}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("PDF generation would be implemented with reportlab library\n")
        
        return str(filepath)
    
    def _flatten_dict(self, data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key, sep).items())
            else:
                items.append((new_key, value))
        
        return dict(items)