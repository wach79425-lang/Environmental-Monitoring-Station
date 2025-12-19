"""
Advanced Visualization for Environmental Data
Author: [Your Name]
Purpose: Create advanced visualizations and dashboards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class EnvironmentalVisualizer:
    """Advanced visualization class for environmental data"""
    
    def __init__(self, data):
        self.data = data
        self.setup_styles()
    
    def setup_styles(self):
        """Setup visualization styles"""
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        self.colors = {
            'NORMAL': '#3498db',      # Blue
            'OBJECT_DETECTED': '#2ecc71',  # Green
            'ALERT_CLOSE': '#e74c3c'  # Red
        }
    
    def create_comprehensive_dashboard(self, output_file="environmental_dashboard.png"):
        """Create a comprehensive dashboard of all metrics"""
        fig = plt.figure(figsize=(20, 15))
        gs = GridSpec(4, 4, figure=fig)
        
        # 1. Time Series - Distance
        ax1 = fig.add_subplot(gs[0, :2])
        self.plot_distance_time_series(ax1)
        
        # 2. Time Series - Reflectance
        ax2 = fig.add_subplot(gs[0, 2:])
        self.plot_reflectance_time_series(ax2)
        
        # 3. Histogram - Distance
        ax3 = fig.add_subplot(gs[1, :2])
        self.plot_distance_histogram(ax3)
        
        # 4. Histogram - Reflectance
        ax4 = fig.add_subplot(gs[1, 2:])
        self.plot_reflectance_histogram(ax4)
        
        # 5. Scatter Plot
        ax5 = fig.add_subplot(gs[2, :2])
        self.plot_correlation_scatter(ax5)
        
        # 6. State Timeline
        ax6 = fig.add_subplot(gs[2, 2:])
        self.plot_state_timeline(ax6)
        
        # 7. Box Plot - Distance by State
        ax7 = fig.add_subplot(gs[3, :2])
        self.plot_distance_by_state(ax7)
        
        # 8. Box Plot - Reflectance by State
        ax8 = fig.add_subplot(gs[3, 2:])
        self.plot_reflectance_by_state(ax8)
        
        plt.suptitle('Environmental Monitoring Station - Comprehensive Dashboard', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Dashboard saved: {output_file}")
        
        return fig
    
    def plot_distance_time_series(self, ax):
        """Plot distance measurements over time"""
        time_seconds = self.data['Tempo(ms)'] / 1000
        ax.plot(time_seconds, self.data['Distancia(cm)'], 'b-', alpha=0.7, linewidth=0.5)
        ax.set_title('Distance Measurements Over Time', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Distance (cm)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=10, color='r', linestyle='--', alpha=0.5, label='Alert Threshold')
        ax.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Ideal Boundary')
        ax.legend(fontsize=9)
        
        # Add statistical annotations
        valid_distances = self.data[self.data['Distancia(cm)'] < 999]['Distancia(cm)']
        if len(valid_distances) > 0:
            ax.text(0.02, 0.98, f'Mean: {valid_distances.mean():.1f} cm\nStd: {valid_distances.std():.1f} cm',
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    def plot_reflectance_time_series(self, ax):
        """Plot reflectance measurements over time"""
        time_seconds = self.data['Tempo(ms)'] / 1000
        ax.plot(time_seconds, self.data['Luminosidade(IR)'], 'g-', alpha=0.7, linewidth=0.5)
        ax.set_title('IR Reflectance Over Time', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Reflectance (0-1023)')
        ax.grid(True, alpha=0.3)
        
        # Add statistical annotations
        ax.text(0.02, 0.98, f'Mean: {self.data["Luminosidade(IR)"].mean():.0f}\nStd: {self.data["Luminosidade(IR)"].std():.0f}',
               transform=ax.transAxes, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    def plot_distance_histogram(self, ax):
        """Plot histogram of distance measurements"""
        valid_distances = self.data[self.data['Distancia(cm)'] < 999]['Distancia(cm)']
        if len(valid_distances) > 0:
            ax.hist(valid_distances, bins=30, alpha=0.7, color='blue', edgecolor='black')
            ax.set_title('Distance Distribution', fontsize=12, fontweight='bold')
            ax.set_xlabel('Distance (cm)')
            ax.set_ylabel('Frequency')
            ax.axvline(x=10, color='r', linestyle='--', alpha=0.7)
            ax.axvline(x=30, color='g', linestyle='--', alpha=0.7)
            
            # Add distribution curve
            from scipy.stats import gaussian_kde
            kde = gaussian_kde(valid_distances)
            x_range = np.linspace(valid_distances.min(), valid_distances.max(), 100)
            ax.plot(x_range, kde(x_range) * len(valid_distances) * (x_range[1]-x_range[0]),
                   'r-', linewidth=2, alpha=0.8, label='Density')
            ax.legend()
    
    def plot_reflectance_histogram(self, ax):
        """Plot histogram of reflectance measurements"""
        ax.hist(self.data['Luminosidade(IR)'], bins=30, alpha=0.7, color='green', edgecolor='black')
        ax.set_title('Reflectance Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('Reflectance')
        ax.set_ylabel('Frequency')
        
        # Add distribution curve
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(self.data['Luminosidade(IR)'])
        x_range = np.linspace(self.data['Luminosidade(IR)'].min(), 
                             self.data['Luminosidade(IR)'].max(), 100)
        ax.plot(x_range, kde(x_range) * len(self.data) * (x_range[1]-x_range[0]),
               'b-', linewidth=2, alpha=0.8, label='Density')
        ax.legend()
    
    def plot_correlation_scatter(self, ax):
        """Plot correlation between distance and reflectance"""
        valid_data = self.data[self.data['Distancia(cm)'] < 999]
        if len(valid_data) > 0:
            scatter = ax.scatter(valid_data['Distancia(cm)'],
                               valid_data['Luminosidade(IR)'],
                               c=pd.Categorical(valid_data['Estado']).map(self.colors),
                               alpha=0.6, s=30)
            ax.set_title('Distance vs Reflectance Correlation', fontsize=12, fontweight='bold')
            ax.set_xlabel('Distance (cm)')
            ax.set_ylabel('Reflectance')
            
            # Add correlation coefficient
            correlation = valid_data['Distancia(cm)'].corr(valid_data['Luminosidade(IR)'])
            ax.text(0.02, 0.98, f'Correlation: {correlation:.3f}',
                   transform=ax.transAxes, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
            
            # Add legend for colors
            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor=self.colors[state], label=state)
                             for state in valid_data['Estado'].unique()]
            ax.legend(handles=legend_elements, fontsize=9)
    
    def plot_state_timeline(self, ax):
        """Plot state changes over time"""
        time_seconds = self.data['Tempo(ms)'] / 1000
        
        # Create color segments based on state
        for i in range(len(self.data)-1):
            state = self.data.iloc[i]['Estado']
            color = self.colors.get(state, 'gray')
            ax.axvspan(time_seconds.iloc[i], time_seconds.iloc[i+1],
                      alpha=0.3, color=color)
        
        ax.set_title('System State Timeline', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time (seconds)')
        ax.set_yticks([])
        
        # Add state labels
        state_changes = self.data['Estado'] != self.data['Estado'].shift()
        for idx in self.data[state_changes].index:
            ax.text(time_seconds.iloc[idx], 0.5, self.data.iloc[idx]['Estado'],
                   rotation=90, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def plot_distance_by_state(self, ax):
        """Plot box plot of distance by state"""
        valid_data = self.data[self.data['Distancia(cm)'] < 999]
        if len(valid_data) > 0:
            states = []
            distances = []
            colors = []
            
            for state in valid_data['Estado'].unique():
                state_data = valid_data[valid_data['Estado'] == state]
                states.append(state)
                distances.append(state_data['Distancia(cm)'].values)
                colors.append(self.colors.get(state, 'gray'))
            
            bp = ax.boxplot(distances, labels=states, patch_artist=True)
            
            # Color the boxes
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.6)
            
            ax.set_title('Distance Distribution by State', fontsize=12, fontweight='bold')
            ax.set_ylabel('Distance (cm)')
            ax.grid(True, alpha=0.3)
    
    def plot_reflectance_by_state(self, ax):
        """Plot box plot of reflectance by state"""
        states = []
        reflectances = []
        colors = []
        
        for state in self.data['Estado'].unique():
            state_data = self.data[self.data['Estado'] == state]
            states.append(state)
            reflectances.append(state_data['Luminosidade(IR)'].values)
            colors.append(self.colors.get(state, 'gray'))
        
        bp = ax.boxplot(reflectances, labels=states, patch_artist=True)
        
        # Color the boxes
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        
        ax.set_title('Reflectance Distribution by State', fontsize=12, fontweight='bold')
        ax.set_ylabel('Reflectance')
        ax.grid(True, alpha=0.3)

def create_interactive_dashboard(data, output_file="interactive_dashboard.html"):
    """Create interactive Plotly dashboard"""
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Distance Over Time', 'Reflectance Over Time',
                       'Distance Distribution', 'Reflectance Distribution',
                       'Correlation Scatter', 'System States'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'histogram'}, {'type': 'histogram'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]]
    )
    
    # 1. Distance over time
    fig.add_trace(
        go.Scatter(
            x=data['Tempo(ms)']/1000,
            y=data['Distancia(cm)'],
            mode='lines',
            name='Distance',
            line=dict(color='blue', width=1),
            hovertemplate='Time: %{x:.1f}s<br>Distance: %{y:.1f}cm'
        ),
        row=1, col=1
    )
    
    # Add threshold lines
    fig.add_hline(y=10, line_dash="dash", line_color="red", 
                  annotation_text="Alert", row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Ideal", row=1, col=1)
    
    # 2. Reflectance over time
    fig.add_trace(
        go.Scatter(
            x=data['Tempo(ms)']/1000,
            y=data['Luminosidade(IR)'],
            mode='lines',
            name='Reflectance',
            line=dict(color='green', width=1),
            hovertemplate='Time: %{x:.1f}s<br>Reflectance: %{y:.0f}'
        ),
        row=1, col=2
    )
    
    # 3. Distance histogram
    valid_distances = data[data['Distancia(cm)'] < 999]['Distancia(cm)']
    fig.add_trace(
        go.Histogram(
            x=valid_distances,
            name='Distance Distribution',
            marker_color='blue',
            opacity=0.7,
            nbinsx=30
        ),
        row=2, col=1
    )
    
    # 4. Reflectance histogram
    fig.add_trace(
        go.Histogram(
            x=data['Luminosidade(IR)'],
            name='Reflectance Distribution',
            marker_color='green',
            opacity=0.7,
            nbinsx=30
        ),
        row=2, col=2
    )
    
    # 5. Correlation scatter
    valid_data = data[data['Distancia(cm)'] < 999]
    color_map = {'NORMAL': 'blue', 'OBJECT_DETECTED': 'green', 'ALERT_CLOSE': 'red'}
    colors = valid_data['Estado'].map(color_map)
    
    fig.add_trace(
        go.Scatter(
            x=valid_data['Distancia(cm)'],
            y=valid_data['Luminosidade(IR)'],
            mode='markers',
            name='Correlation',
            marker=dict(
                color=colors,
                size=8,
                opacity=0.6
            ),
            text=valid_data['Estado'],
            hovertemplate='Distance: %{x:.1f}cm<br>Reflectance: %{y:.0f}<br>State: %{text}'
        ),
        row=3, col=1
    )
    
    # 6. State timeline
    for state, color in color_map.items():
        state_data = data[data['Estado'] == state]
        if len(state_data) > 0:
            fig.add_trace(
                go.Scatter(
                    x=state_data['Tempo(ms)']/1000,
                    y=[state] * len(state_data),
                    mode='markers',
                    name=state,
                    marker=dict(color=color, size=10),
                    showlegend=True
                ),
                row=3, col=2
            )
    
    # Update layout
    fig.update_layout(
        title_text="Environmental Monitoring Station - Interactive Dashboard",
        height=900,
        showlegend=True,
        template="plotly_white"
    )
    
    # Update axis labels
    fig.update_xaxes(title_text="Time (seconds)", row=1, col=1)
    fig.update_yaxes(title_text="Distance (cm)", row=1, col=1)
    fig.update_xaxes(title_text="Time (seconds)", row=1, col=2)
    fig.update_yaxes(title_text="Reflectance", row=1, col=2)
    fig.update_xaxes(title_text="Distance (cm)", row=2, col=1)
    fig.update_yaxes(title_text="Frequency", row=2, col=1)
    fig.update_xaxes(title_text="Reflectance", row=2, col=2)
    fig.update_yaxes(title_text="Frequency", row=2, col=2)
    fig.update_xaxes(title_text="Distance (cm)", row=3, col=1)
    fig.update_yaxes(title_text="Reflectance", row=3, col=1)
    fig.update_xaxes(title_text="Time (seconds)", row=3, col=2)
    fig.update_yaxes(title_text="State", row=3, col=2)
    
    fig.write_html(output_file)
    print(f"✓ Interactive dashboard saved: {output_file}")
    return fig

def main():
    """Main function to run visualizations"""
    print("="*60)
    print("ENVIRONMENTAL DATA VISUALIZATION")
    print("="*60)
    
    # Load sample data
    try:
        data = pd.read_csv("sample_readings.csv")
        print(f"Loaded {len(data)} records for visualization")
        
        # Create visualizer instance
        visualizer = EnvironmentalVisualizer(data)
        
        # Create comprehensive dashboard
        visualizer.create_comprehensive_dashboard()
        
        # Create interactive dashboard
        create_interactive_dashboard(data)
        
        print("\n" + "="*60)
        print("VISUALIZATION COMPLETE")
        print("="*60)
        print("\nGenerated Files:")
        print("✓ environmental_dashboard.png - Static comprehensive dashboard")
        print("✓ interactive_dashboard.html - Interactive web dashboard")
        print("\nThe visualizations provide insights into:")
        print("1. Temporal patterns in distance and reflectance")
        print("2. Statistical distributions of measurements")
        print("3. Correlations between different parameters")
        print("4. System state transitions and patterns")
        
    except FileNotFoundError:
        print("Error: sample_readings.csv not found.")
        print("Please ensure you have data to visualize.")
    except Exception as e:
        print(f"Error during visualization: {e}")

if __name__ == "__main__":
    main()
