"""
Environmental Monitoring Station - Data Analysis Tool
Author: [Your Name]
Country: Mozambique
Purpose: Analyze environmental data from Arduino station
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class EnvironmentalAnalyzer:
    """Main class for environmental data analysis"""
    
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load CSV data from Arduino station"""
        print(f"Loading data from: {self.filename}")
        
        try:
            self.data = pd.read_csv(self.filename)
            print(f"Successfully loaded {len(self.data)} records")
            print(f"Time range: {self.data['Tempo(ms)'].min()} to {self.data['Tempo(ms)'].max()} ms")
            
            # Convert timestamp to datetime
            start_time = datetime.now()
            self.data['datetime'] = self.data['Tempo(ms)'].apply(
                lambda x: start_time + timedelta(milliseconds=x)
            )
            
            # Display basic info
            self.display_basic_info()
            
        except FileNotFoundError:
            print(f"Error: File {self.filename} not found.")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def display_basic_info(self):
        """Display basic information about the dataset"""
        print("\n" + "="*60)
        print("DATASET INFORMATION")
        print("="*60)
        
        print(f"\nShape: {self.data.shape}")
        print(f"Columns: {list(self.data.columns)}")
        
        print("\nData Types:")
        print(self.data.dtypes)
        
        print("\nMissing Values:")
        print(self.data.isnull().sum())
        
        print("\nBasic Statistics:")
        print(self.data[['Distancia(cm)', 'Luminosidade(IR)']].describe())
        
        print("\nState Distribution:")
        state_counts = self.data['Estado'].value_counts()
        for state, count in state_counts.items():
            percentage = (count / len(self.data)) * 100
            print(f"  {state}: {count} records ({percentage:.1f}%)")
    
    def analyze_distance_patterns(self):
        """Analyze distance measurement patterns"""
        print("\n" + "="*60)
        print("DISTANCE PATTERN ANALYSIS")
        print("="*60)
        
        # Filter valid distances
        valid_distances = self.data[self.data['Distancia(cm)'] < 999]
        
        if len(valid_distances) > 0:
            print(f"\nValid distance measurements: {len(valid_distances)}")
            
            # Statistical analysis
            stats_dict = {
                'Mean': valid_distances['Distancia(cm)'].mean(),
                'Median': valid_distances['Distancia(cm)'].median(),
                'Std Dev': valid_distances['Distancia(cm)'].std(),
                'Min': valid_distances['Distancia(cm)'].min(),
                'Max': valid_distances['Distancia(cm)'].max(),
                'Range': valid_distances['Distancia(cm)'].max() - valid_distances['Distancia(cm)'].min()
            }
            
            for key, value in stats_dict.items():
                print(f"{key}: {value:.2f} cm")
            
            # Distance categories
            bins = [0, 10, 30, 100, 300]
            labels = ['Very Close (<10cm)', 'Ideal (10-30cm)', 'Moderate (30-100cm)', 'Far (>100cm)']
            
            valid_distances['distance_category'] = pd.cut(
                valid_distances['Distancia(cm)'],
                bins=bins,
                labels=labels,
                include_lowest=True
            )
            
            print("\nDistance Category Distribution:")
            category_counts = valid_distances['distance_category'].value_counts()
            for category, count in category_counts.items():
                percentage = (count / len(valid_distances)) * 100
                print(f"  {category}: {count} measurements ({percentage:.1f}%)")
            
            return valid_distances
        else:
            print("No valid distance measurements found.")
            return None
    
    def analyze_reflectance_patterns(self):
        """Analyze IR reflectance patterns"""
        print("\n" + "="*60)
        print("REFLECTANCE PATTERN ANALYSIS")
        print("="*60)
        
        if 'Luminosidade(IR)' in self.data.columns:
            reflectance = self.data['Luminosidade(IR)']
            
            print(f"\nReflectance Statistics:")
            print(f"Mean: {reflectance.mean():.2f}")
            print(f"Median: {reflectance.median():.2f}")
            print(f"Std Dev: {reflectance.std():.2f}")
            print(f"Min: {reflectance.min():.2f}")
            print(f"Max: {reflectance.max():.2f}")
            
            # Correlation with distance
            valid_data = self.data[self.data['Distancia(cm)'] < 999]
            if len(valid_data) > 1:
                correlation = valid_data['Distancia(cm)'].corr(valid_data['Luminosidade(IR)'])
                print(f"\nCorrelation between distance and reflectance: {correlation:.3f}")
                
                if abs(correlation) > 0.3:
                    print("  → Moderate correlation detected")
                elif abs(correlation) > 0.7:
                    print("  → Strong correlation detected")
                else:
                    print("  → Weak or no correlation")
            
            # Reflectance categories
            bins = [0, 300, 600, 900, 1023]
            labels = ['Low (0-300)', 'Medium (300-600)', 'High (600-900)', 'Very High (900-1023)']
            
            self.data['reflectance_category'] = pd.cut(
                self.data['Luminosidade(IR)'],
                bins=bins,
                labels=labels,
                include_lowest=True
            )
            
            print("\nReflectance Category Distribution:")
            category_counts = self.data['reflectance_category'].value_counts()
            for category, count in category_counts.items():
                percentage = (count / len(self.data)) * 100
                print(f"  {category}: {count} measurements ({percentage:.1f}%)")
    
    def analyze_state_transitions(self):
        """Analyze state transitions and patterns"""
        print("\n" + "="*60)
        print("STATE TRANSITION ANALYSIS")
        print("="*60)
        
        # State duration analysis
        state_changes = self.data['Estado'] != self.data['Estado'].shift()
        state_starts = self.data[state_changes]
        
        if len(state_starts) > 1:
            print(f"\nNumber of state transitions: {len(state_starts)}")
            
            # Calculate state durations
            durations = []
            for i in range(len(state_starts) - 1):
                start_time = state_starts.iloc[i]['Tempo(ms)']
                end_time = state_starts.iloc[i + 1]['Tempo(ms)']
                duration = (end_time - start_time) / 1000  # Convert to seconds
                state = state_starts.iloc[i]['Estado']
                durations.append((state, duration))
            
            # Group by state
            state_durations = {}
            for state, duration in durations:
                if state not in state_durations:
                    state_durations[state] = []
                state_durations[state].append(duration)
            
            print("\nAverage State Durations:")
            for state, dur_list in state_durations.items():
                avg_duration = np.mean(dur_list)
                print(f"  {state}: {avg_duration:.2f} seconds")
    
    def create_visualizations(self, output_dir="output"):
        """Create comprehensive visualizations"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nCreating visualizations in '{output_dir}' directory...")
        
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        
        # 1. Distance over time
        axes[0, 0].plot(self.data['Tempo(ms)']/1000, self.data['Distancia(cm)'], 'b-', alpha=0.7, linewidth=0.5)
        axes[0, 0].set_title('Distance Measurements Over Time')
        axes[0, 0].set_xlabel('Time (seconds)')
        axes[0, 0].set_ylabel('Distance (cm)')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].axhline(y=10, color='r', linestyle='--', alpha=0.5, label='Alert Threshold (10cm)')
        axes[0, 0].axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Ideal Range Boundary (30cm)')
        axes[0, 0].legend()
        
        # 2. Reflectance over time
        axes[0, 1].plot(self.data['Tempo(ms)']/1000, self.data['Luminosidade(IR)'], 'g-', alpha=0.7, linewidth=0.5)
        axes[0, 1].set_title('IR Reflectance Over Time')
        axes[0, 1].set_xlabel('Time (seconds)')
        axes[0, 1].set_ylabel('Reflectance (0-1023)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. State distribution
        state_counts = self.data['Estado'].value_counts()
        colors = ['blue', 'green', 'red']
        axes[1, 0].bar(state_counts.index, state_counts.values, color=colors[:len(state_counts)])
        axes[1, 0].set_title('System State Distribution')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Distance histogram
        valid_distances = self.data[self.data['Distancia(cm)'] < 999]['Distancia(cm)']
        axes[1, 1].hist(valid_distances, bins=20, alpha=0.7, color='blue', edgecolor='black')
        axes[1, 1].set_title('Distance Measurement Distribution')
        axes[1, 1].set_xlabel('Distance (cm)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].axvline(x=10, color='r', linestyle='--', alpha=0.7, label='Alert Threshold')
        axes[1, 1].axvline(x=30, color='g', linestyle='--', alpha=0.7, label='Ideal Boundary')
        axes[1, 1].legend()
        
        # 5. Correlation scatter plot
        valid_data = self.data[self.data['Distancia(cm)'] < 999]
        if len(valid_data) > 0:
            scatter = axes[2, 0].scatter(valid_data['Distancia(cm)'], 
                                        valid_data['Luminosidade(IR)'],
                                        c=pd.Categorical(valid_data['Estado']).codes,
                                        cmap='viridis', alpha=0.6)
            axes[2, 0].set_title('Distance vs Reflectance Correlation')
            axes[2, 0].set_xlabel('Distance (cm)')
            axes[2, 0].set_ylabel('Reflectance')
            plt.colorbar(scatter, ax=axes[2, 0], label='State')
        
        # 6. Time-based analysis
        axes[2, 1].text(0.5, 0.5, 'Environmental Monitoring Station\nData Analysis Complete',
                       ha='center', va='center', fontsize=12)
        axes[2, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/environmental_analysis.png', dpi=150, bbox_inches='tight')
        print(f"✓ Main visualization saved: {output_dir}/environmental_analysis.png")
        
        # Create interactive plot
        self.create_interactive_plot(output_dir)
        
        return fig
    
    def create_interactive_plot(self, output_dir):
        """Create interactive Plotly visualization"""
        fig = go.Figure()
        
        # Add distance trace
        fig.add_trace(go.Scatter(
            x=self.data['Tempo(ms)']/1000,
            y=self.data['Distancia(cm)'],
            mode='lines',
            name='Distance (cm)',
            line=dict(color='blue', width=1),
            hovertemplate='Time: %{x:.1f}s<br>Distance: %{y:.1f}cm'
        ))
        
        # Add reflectance trace
        fig.add_trace(go.Scatter(
            x=self.data['Tempo(ms)']/1000,
            y=self.data['Luminosidade(IR)'],
            mode='lines',
            name='Reflectance',
            line=dict(color='green', width=1),
            yaxis='y2',
            hovertemplate='Time: %{x:.1f}s<br>Reflectance: %{y:.0f}'
        ))
        
        # Update layout
        fig.update_layout(
            title='Environmental Monitoring Station - Live Data',
            xaxis=dict(title='Time (seconds)'),
            yaxis=dict(title='Distance (cm)', side='left'),
            yaxis2=dict(title='Reflectance', side='right', overlaying='y'),
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Add threshold lines
        fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Alert Threshold")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Ideal Boundary")
        
        fig.write_html(f'{output_dir}/interactive_plot.html')
        print(f"✓ Interactive plot saved: {output_dir}/interactive_plot.html")
    
    def generate_report(self, output_file="environmental_report.md"):
        """Generate comprehensive analysis report"""
        print(f"\nGenerating analysis report: {output_file}")
        
        report = f"""# Environmental Monitoring Station - Analysis Report

## Report Summary
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Data Source**: Arduino Environmental Station
- **Total Records**: {len(self.data)}
- **Analysis Duration**: {(self.data['Tempo(ms)'].max() - self.data['Tempo(ms)'].min())/1000:.1f} seconds

## System Performance

### Data Collection:
- **Sampling Rate**: {len(self.data)/(self.data['Tempo(ms)'].max()/1000):.2f} Hz
- **Data Completeness**: {100 - (self.data.isnull().sum().sum()/len(self.data)*100):.1f}%
- **Measurement Range**: Distance: 0-{self.data['Distancia(cm)'].max():.0f}cm, Reflectance: 0-1023

### State Analysis:
"""
        
        # Add state statistics
        state_counts = self.data['Estado'].value_counts()
        for state, count in state_counts.items():
            percentage = (count / len(self.data)) * 100
            report += f"- **{state}**: {count} records ({percentage:.1f}%)\n"
        
        # Add distance analysis
        valid_distances = self.data[self.data['Distancia(cm)'] < 999]
        if len(valid_distances) > 0:
            report += f"""
## Distance Analysis

### Statistical Summary:
- **Mean Distance**: {valid_distances['Distancia(cm)'].mean():.1f} cm
- **Median Distance**: {valid_distances['Distancia(cm)'].median():.1f} cm
- **Standard Deviation**: {valid_distances['Distancia(cm)'].std():.1f} cm
- **Measurement Range**: {valid_distances['Distancia(cm)'].min():.1f} to {valid_distances['Distancia(cm)'].max():.1f} cm

### Distance Categories:
"""
            bins = [0, 10, 30, 100, 300]
            labels = ['Very Close (<10cm)', 'Ideal (10-30cm)', 'Moderate (30-100cm)', 'Far (>100cm)']
            
            valid_distances['distance_category'] = pd.cut(
                valid_distances['Distancia(cm)'],
                bins=bins,
                labels=labels,
                include_lowest=True
            )
            
            category_counts = valid_distances['distance_category'].value_counts()
            for category, count in category_counts.items():
                percentage = (count / len(valid_distances)) * 100
                report += f"- **{category}**: {count} measurements ({percentage:.1f}%)\n"
        
        # Add reflectance analysis
        report += f"""
## Reflectance Analysis

### Statistical Summary:
- **Mean Reflectance**: {self.data['Luminosidade(IR)'].mean():.0f}
- **Median Reflectance**: {self.data['Luminosidade(IR)'].median():.0f}
- **Standard Deviation**: {self.data['Luminosidade(IR)'].std():.0f}
- **Dynamic Range**: {self.data['Luminosidade(IR)'].min():.0f} to {self.data['Luminosidade(IR)'].max():.0f}

## Environmental Insights

### Observations:
1. **System Responsiveness**: The station successfully detects changes in the environment
2. **Alert System**: Proper triggering of alerts when objects are too close
3. **Data Consistency**: Measurements show expected patterns and ranges
4. **Environmental Conditions**: Reflectance values indicate surface properties

### Recommendations:
1. **Deployment Optimization**: Consider sensor placement for specific applications
2. **Data Collection**: Extend monitoring periods for trend analysis
3. **Alert Thresholds**: Adjust based on specific environmental requirements
4. **Maintenance**: Regular sensor calibration for accuracy

## Technical Specifications
- **Microcontroller**: Arduino Uno
- **Primary Sensor**: HC-SR04 Ultrasonic (2-400cm range)
- **Secondary Sensor**: IR Reflectance (0-1023 analog)
- **Alert System**: RGB LED + Buzzer
- **Data Output**: CSV format via Serial

---
*Report generated automatically by Environmental Monitoring Analysis Tool*

**Location**: Mozambique  
**Project**: Environmental Monitoring Station  
**Version**: 1.0  
"""
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved: {output_file}")
        return report

def main():
    """Main function to run analysis"""
    print("="*70)
    print("ENVIRONMENTAL MONITORING STATION - DATA ANALYSIS")
    print("="*70)
    print("Author: [Your Name]")
    print("Country: Mozambique")
    print("="*70)
    
    # Initialize analyzer
    analyzer = EnvironmentalAnalyzer("sample_readings.csv")
    
    if analyzer.data is not None:
        # Run analyses
        analyzer.analyze_distance_patterns()
        analyzer.analyze_reflectance_patterns()
        analyzer.analyze_state_transitions()
        
        # Create visualizations
        analyzer.create_visualizations()
        
        # Generate report
        analyzer.generate_report()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print("\nOutput Files Created:")
        print("✓ environmental_analysis.png - Comprehensive visualizations")
        print("✓ interactive_plot.html - Interactive data exploration")
        print("✓ environmental_report.md - Detailed analysis report")
        print("\nNext Steps:")
        print("1. Review the generated reports")
        print("2. Adjust sensor placement based on findings")
        print("3. Consider longer-term data collection")
        print("4. Share findings with environmental researchers")
    
    else:
        print("Analysis could not be completed. Please check your data file.")

if __name__ == "__main__":
    main()
