# filepath: c:\Users\kamat\OneDrive\Desktop\Work\UIUC\Research\maidr\maidr_streamlit\plots\multipanelplot.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from plots.utils import set_theme

def create_multipanel_plot(layout_type, color_palette, theme):
    """
    Create a multipanel plot with different subplot types arranged in a specified layout.
    
    Parameters
    ----------
    layout_type : str
        The type of layout ('Grid 2x2', 'Row', 'Column', 'Mixed')
    color_palette : str
        The color palette to use for the plots
    theme : str
        The theme to apply to the plot ('Light' or 'Dark')
        
    Returns
    -------
    plt.Figure
        The figure containing the created plot.
    """
    # Generate sample data
    # Data for line plot
    x_line = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y_line = np.array([2, 4, 1, 5, 3, 7, 6, 8])
    
    # Data for first bar plot
    categories = ["A", "B", "C", "D", "E"]
    values = np.random.rand(5) * 10
    
    # Data for scatter plot
    x_scatter = np.random.randn(50)
    y_scatter = np.random.randn(50)
    
    # Create a figure with subplots arranged according to the layout
    if layout_type == "Grid 2x2":
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        axs = axs.flatten()  # Flatten to make it easier to index
    else:  # Default to a vertical layout with 3 plots
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    # Apply theme to all subplots
    for ax in axs:
        set_theme(fig, ax, theme)
    
    # First panel: Line plot
    axs[0].plot(x_line, y_line, color="blue", linewidth=2)
    axs[0].set_title("Line Plot: Random Data")
    axs[0].set_xlabel("X-axis")
    axs[0].set_ylabel("Values")
    axs[0].grid(True, linestyle="--", alpha=0.7)
    
    # Second panel: Bar plot
    axs[1].bar(categories, values, color="green", alpha=0.7)
    axs[1].set_title("Bar Plot: Random Values")
    axs[1].set_xlabel("Categories")
    axs[1].set_ylabel("Values")
    
    # Third panel: Scatter plot
    if len(axs) > 2:  # Check if we have a third subplot (for Grid 2x2 and Column layouts)
        axs[2].scatter(x_scatter, y_scatter, color="red", alpha=0.7)
        axs[2].set_title("Scatter Plot: Random Points")
        axs[2].set_xlabel("X-axis")
        axs[2].set_ylabel("Y-axis")
    
    # Fourth panel (if Grid 2x2): Histogram
    if len(axs) > 3:  # Only for Grid 2x2 layout
        data = np.random.normal(0, 1, 1000)
        axs[3].hist(data, bins=20, color="purple", alpha=0.7)
        axs[3].set_title("Histogram: Normal Distribution")
        axs[3].set_xlabel("Values")
        axs[3].set_ylabel("Frequency")
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    return axs[0]

def create_custom_multipanel_plot(df, vars_config, layout_type, color_palette, theme):
    """
    Create a custom multipanel plot from user data.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the data to plot
    vars_config : dict
        Dictionary containing variables for each subplot
        Example: {
            'plot1': {'type': 'line', 'x': 'col1', 'y': 'col2'},
            'plot2': {'type': 'bar', 'x': 'col3', 'y': 'col4'},
            'plot3': {'type': 'scatter', 'x': 'col5', 'y': 'col6'},
            'plot4': {'type': 'hist', 'x': 'col7', 'y': None},
        }
    layout_type : str
        The type of layout ('Grid 2x2', 'Row', 'Column', 'Mixed')
    color_palette : str
        The color palette to use for the plots
    theme : str
        The theme to apply to the plot ('Light' or 'Dark')
        
    Returns
    -------
    plt.Figure
        The figure containing the created plot.
    """
    if df is None or not vars_config:
        return None
    
    # Extract configuration for each plot
    plot1_config = vars_config.get('plot1', {})
    plot2_config = vars_config.get('plot2', {})
    plot3_config = vars_config.get('plot3', {})
    plot4_config = vars_config.get('plot4', {})
    
    # Map palette names to colors
    palette_mapping = {
        "Default": ["blue", "green", "red", "purple"],
        "Colorful": ["#FF5733", "#33FF57", "#3357FF", "#F033FF"],
        "Pastel": ["#FFB6C1", "#B6FFB6", "#B6C1FF", "#FFB6FF"],
        "Dark Tones": ["#8B0000", "#006400", "#00008B", "#8B008B"],
        "Paired Colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
        "Rainbow": ["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]
    }
    
    colors = palette_mapping.get(color_palette, palette_mapping["Default"])
    
    # Create figure with appropriate layout
    if layout_type == "Grid 2x2":
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        axs = axs.flatten()  # Flatten to make it easier to index
    else:  # Default to a vertical layout with 3 plots
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        if len(axs) < 4:  # If we have fewer than 4 axes but 4 plot configs
            axs = list(axs) + [None]  # Add None to handle the 4th plot gracefully
    
    # Apply theme to all subplots
    for ax in axs:
        if ax is not None:
            set_theme(fig, ax, theme)
    
    # Function to create plot based on type
    def create_plot(ax, plot_config, color_idx):
        if ax is None or not plot_config:
            return
            
        plot_type = plot_config.get('type', 'line')
        x_var = plot_config.get('x', None)
        y_var = plot_config.get('y', None)
        
        if not x_var or (plot_type != 'hist' and not y_var):
            return
            
        color = colors[color_idx % len(colors)]
        
        if plot_type == 'line':
            sns.lineplot(data=df, x=x_var, y=y_var, ax=ax, color=color)
            ax.set_title(f"Line Plot: {y_var} vs {x_var}")
        elif plot_type == 'bar':
            if df[x_var].dtype == 'object' or df[x_var].nunique() < 15:
                # For categorical x, use count or mean
                if y_var:
                    value_counts = df.groupby(x_var)[y_var].mean()
                    value_counts.plot(kind='bar', ax=ax, color=color, alpha=0.7)
                    ax.set_title(f"Bar Plot: Mean {y_var} by {x_var}")
                else:
                    value_counts = df[x_var].value_counts()
                    value_counts.plot(kind='bar', ax=ax, color=color, alpha=0.7)
                    ax.set_title(f"Bar Plot: Counts of {x_var}")
            else:
                # For numeric x with many values, create bins
                ax.bar(df[x_var], df[y_var], color=color, alpha=0.7)
                ax.set_title(f"Bar Plot: {y_var} by {x_var}")
        elif plot_type == 'scatter':
            sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax, color=color, alpha=0.7)
            ax.set_title(f"Scatter Plot: {y_var} vs {x_var}")
        elif plot_type == 'hist':
            sns.histplot(data=df, x=x_var, ax=ax, color=color, alpha=0.7, kde=True)
            ax.set_title(f"Histogram: {x_var}")
        elif plot_type == 'multiline':
            group_var = plot_config.get('group', None)
            if group_var and group_var in df.columns:
                sns.lineplot(data=df, x=x_var, y=y_var, hue=group_var, style=group_var, 
                            markers=True, dashes=False, ax=ax)
                ax.set_title(f"Multiline Plot: {y_var} vs {x_var} by {group_var}")
            else:
                sns.lineplot(data=df, x=x_var, y=y_var, ax=ax, color=color)
                ax.set_title(f"Line Plot: {y_var} vs {x_var}")
        
        # Common labels
        ax.set_xlabel(x_var.replace("_", " ").title())
        if y_var and plot_type != 'hist':
            ax.set_ylabel(y_var.replace("_", " ").title())
    
    # Create each plot
    create_plot(axs[0], plot1_config, 0)
    create_plot(axs[1], plot2_config, 1)
    if len(axs) > 2 and axs[2] is not None:
        create_plot(axs[2], plot3_config, 2)
    if len(axs) > 3 and axs[3] is not None:
        create_plot(axs[3], plot4_config, 3)
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    return axs[0]