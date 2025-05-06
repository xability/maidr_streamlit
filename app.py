import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import maidr

# Import plot modules
from plots.utils import set_theme, color_palettes
from plots.histogram import create_histogram, create_custom_histogram
from plots.boxplot import create_boxplot, create_custom_boxplot
from plots.scatterplot import create_scatterplot, create_custom_scatterplot
from plots.barplot import create_barplot, create_custom_barplot
from plots.lineplot import create_lineplot, create_custom_lineplot
from plots.heatmap import create_heatmap, create_custom_heatmap
from plots.multilineplot import generate_multiline_data, create_multiline_plot, create_custom_multiline_plot
from plots.multilayerplot import create_multilayer_plot, create_custom_multilayer_plot
from plots.multipanelplot import create_multipanel_plot, create_custom_multipanel_plot

# Set random seed
np.random.seed(1000)

# Set page config
st.set_page_config(
    page_title="Learning Data Visualization with MAIDR",
    page_icon="📊",
    layout="wide"
)

# Define functions to render MAIDR plots
def render_maidr_plot(ax):
    """Renders a matplotlib plot with MAIDR accessibility features"""
    # Apply figure size from sliders
    fig_width = st.session_state.get('fig_width', 10)
    fig_height = st.session_state.get('fig_height', 6)
    
    # Resize the figure
    ax.figure.set_size_inches(fig_width, fig_height)
    
    # Only display the MAIDR accessible output (which includes the plot)
    try:
        components.html(
            maidr.render(ax).get_html_string(),
            scrolling=False,  # Disable scrolling
            height=fig_height * 110,  # Slightly larger height to prevent scrolling
            width=fig_width * 110,    # Slightly larger width to prevent scrolling
        )
    except Exception as e:
        # If MAIDR rendering fails, fall back to standard matplotlib rendering
        st.error(f"Error rendering MAIDR accessibility features: {str(e)}")
        st.warning("Falling back to standard matplotlib plot without accessibility features.")
        st.pyplot(ax.figure)

# Function to render custom plot based on uploaded data
def render_custom_plot(df, plot_type, color, theme, **kwargs):
    """Render a custom plot based on user data and selections"""
    if plot_type == "Histogram":
        var = kwargs.get('var')
        if var:
            ax = create_custom_histogram(df, var, color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Box Plot":
        var_x = kwargs.get('var_x')
        var_y = kwargs.get('var_y')
        if var_x:
            ax = create_custom_boxplot(df, var_x, var_y, color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Scatter Plot":
        var_x = kwargs.get('var_x')
        var_y = kwargs.get('var_y')
        if var_x and var_y:
            ax = create_custom_scatterplot(df, var_x, var_y, color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Bar Plot":
        var = kwargs.get('var')
        if var:
            ax = create_custom_barplot(df, var, color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Line Plot":
        var_x = kwargs.get('var_x')
        var_y = kwargs.get('var_y')
        if var_x and var_y:
            ax = create_custom_lineplot(df, var_x, var_y, color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Heatmap":
        var_x = kwargs.get('var_x')
        var_y = kwargs.get('var_y')
        var_value = kwargs.get('var_value')
        colorscale = kwargs.get('colorscale', 'YlGnBu')
        if var_x and var_y:
            ax = create_custom_heatmap(df, var_x, var_y, var_value, colorscale, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Multiline Plot":
        var_x = kwargs.get('var_x')
        var_y = kwargs.get('var_y')
        var_group = kwargs.get('var_group')
        palette = kwargs.get('palette', 'Default')
        if var_x and var_y and var_group:
            ax = create_custom_multiline_plot(df, var_x, var_y, var_group, palette, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Multilayer Plot":
        var_x = kwargs.get('var_x')
        var_background = kwargs.get('var_background')
        var_line = kwargs.get('var_line')
        background_type = kwargs.get('background_type', 'Bar Plot')
        background_color = kwargs.get('background_color', 'Default')
        line_color = kwargs.get('line_color', 'Default')
        if var_x and var_background and var_line:
            ax = create_custom_multilayer_plot(df, var_x, var_background, var_line, 
                                          background_type, background_color, line_color, theme)
            if ax:
                render_maidr_plot(ax)
    
    elif plot_type == "Multipanel Plot":
        vars_config = kwargs.get('vars_config', {})
        layout_type = kwargs.get('layout_type', 'Grid 2x2')
        palette = kwargs.get('palette', 'Default')
        if vars_config:
            ax = create_custom_multipanel_plot(df, vars_config, layout_type, palette, theme)
            if ax:
                render_maidr_plot(ax)

# Sidebar for theme and figure settings
with st.sidebar:
    st.title("Settings")
    theme = st.radio("Select Theme:", ["Light", "Dark"])
    st.session_state['theme'] = theme
    
    # Store the slider values directly in session state with keys
    fig_width = st.slider("Figure Width", min_value=6, max_value=15, value=10, key="fig_width")
    fig_height = st.slider("Figure Height", min_value=4, max_value=10, value=6, key="fig_height")

# Main content
st.title("Learning Data Visualization with MAIDR")

# Tabs for different plots
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "Practice", "Histogram", "Box Plot", "Scatter Plot", "Bar Plot", "Line Plot", "Heatmap",
    "Multilayer Plot", "Multipanel Plot", "Multiline Plot"
])

# Practice tab
with tab1:
    st.header("Create your own Custom Plot")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Show data preview
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Show data types
        st.subheader("Data Types")
        st.dataframe(pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes,
            'Unique Values': [df[col].nunique() for col in df.columns]
        }))
        
        # Plot selection
        st.subheader("Create Plot")
        col1, col2 = st.columns(2)
        
        with col1:
            plot_type = st.selectbox(
                "Select Plot Type:",
                ["", "Histogram", "Box Plot", "Scatter Plot", "Bar Plot", "Line Plot", 
                 "Heatmap", "Multiline Plot", "Multilayer Plot", "Multipanel Plot"]
            )
            
            # Get numeric and categorical columns
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Plot specific inputs
            if plot_type == "Histogram":
                var = st.selectbox("Select Variable for Histogram:", numeric_cols)
                plot_color = st.selectbox("Select Color:", list(color_palettes.keys()), key="histogram_color")
                
                if st.button("Generate Histogram"):
                    with col2:
                        render_custom_plot(df, plot_type, color_palettes[plot_color], theme, var=var)
            
            elif plot_type == "Box Plot":
                var_x = st.selectbox("Select Numerical Variable:", numeric_cols)
                var_y = st.selectbox("Select Categorical Variable (optional):", [""] + categorical_cols)
                plot_color = st.selectbox("Select Color:", list(color_palettes.keys()), key="boxplot_color")
                
                if st.button("Generate Box Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, color_palettes[plot_color], theme, 
                                          var_x=var_x, var_y=var_y if var_y else None)
            
            elif plot_type == "Scatter Plot":
                var_x = st.selectbox("Select X Variable:", numeric_cols, key="scatter_x")
                var_y = st.selectbox("Select Y Variable:", [col for col in numeric_cols if col != var_x], key="scatter_y")
                plot_color = st.selectbox("Select Color:", list(color_palettes.keys()), key="scatter_color")
                
                if st.button("Generate Scatter Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, color_palettes[plot_color], theme, 
                                          var_x=var_x, var_y=var_y)
            
            elif plot_type == "Bar Plot":
                var = st.selectbox("Select Categorical Variable:", categorical_cols)
                plot_color = st.selectbox("Select Color:", list(color_palettes.keys()), key="barplot_color")
                
                if st.button("Generate Bar Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, color_palettes[plot_color], theme, var=var)
            
            elif plot_type == "Line Plot":
                var_x = st.selectbox("Select X Variable:", numeric_cols, key="line_x")
                var_y = st.selectbox("Select Y Variable:", [col for col in numeric_cols if col != var_x], key="line_y")
                plot_color = st.selectbox("Select Color:", list(color_palettes.keys()), key="line_color")
                
                if st.button("Generate Line Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, color_palettes[plot_color], theme, 
                                          var_x=var_x, var_y=var_y)
            
            elif plot_type == "Heatmap":
                var_x = st.selectbox("Select X Variable (categorical):", categorical_cols, key="heatmap_x")
                var_y = st.selectbox("Select Y Variable (categorical):", 
                                     [col for col in categorical_cols if col != var_x], key="heatmap_y")
                var_value = st.selectbox("Select Value Variable (numeric, optional):", 
                                         [""] + numeric_cols, key="heatmap_value")
                colorscale = st.selectbox("Select Color Scale:", 
                                         ["YlGnBu", "viridis", "plasma", "inferno", "RdBu_r", "coolwarm"])
                
                if st.button("Generate Heatmap"):
                    with col2:
                        render_custom_plot(df, plot_type, None, theme, 
                                          var_x=var_x, var_y=var_y, 
                                          var_value=var_value if var_value else None,
                                          colorscale=colorscale)
            
            elif plot_type == "Multiline Plot":
                var_x = st.selectbox("Select X Variable:", numeric_cols, key="multiline_x")
                var_y = st.selectbox("Select Y Variable:", 
                                     [col for col in numeric_cols if col != var_x], key="multiline_y")
                var_group = st.selectbox("Select Group Variable (categorical):", 
                                        categorical_cols, key="multiline_group")
                palette = st.selectbox("Select Color Palette:", 
                                      ["Default", "Colorful", "Pastel", "Dark Tones", "Paired Colors", "Rainbow"])
                
                if st.button("Generate Multiline Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, None, theme, 
                                          var_x=var_x, var_y=var_y, var_group=var_group,
                                          palette=palette)
            
            elif plot_type == "Multilayer Plot":
                var_x = st.selectbox("Select X Variable:", df.columns.tolist(), key="multilayer_x")
                var_background = st.selectbox("Select Background Variable (numeric):", 
                                            numeric_cols, key="multilayer_bg")
                var_line = st.selectbox("Select Line Variable (numeric):", 
                                       [col for col in numeric_cols if col != var_background], key="multilayer_line")
                background_type = st.selectbox("Select Background Plot Type:", 
                                             ["Bar Plot", "Histogram", "Scatter Plot"])
                background_color = st.selectbox("Select Background Color:", 
                                               list(color_palettes.keys()), key="multilayer_bg_color")
                line_color = st.selectbox("Select Line Color:", 
                                          list(color_palettes.keys()), key="multilayer_line_color")
                
                if st.button("Generate Multilayer Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, None, theme, 
                                          var_x=var_x, var_background=var_background, var_line=var_line,
                                          background_type=background_type, 
                                          background_color=background_color, line_color=line_color)
            
            elif plot_type == "Multipanel Plot":
                st.subheader("Panel 1")
                plot1_type = st.selectbox("Plot Type:", ["line", "bar", "scatter", "hist"], key="panel1_type")
                plot1_x = st.selectbox("X Variable:", df.columns.tolist(), key="panel1_x")
                plot1_y = st.selectbox("Y Variable (if applicable):", 
                                       [""] + numeric_cols, key="panel1_y")
                
                st.subheader("Panel 2")
                plot2_type = st.selectbox("Plot Type:", ["line", "bar", "scatter", "hist"], key="panel2_type")
                plot2_x = st.selectbox("X Variable:", df.columns.tolist(), key="panel2_x")
                plot2_y = st.selectbox("Y Variable (if applicable):", 
                                       [""] + numeric_cols, key="panel2_y")
                
                st.subheader("Panel 3")
                plot3_type = st.selectbox("Plot Type:", ["line", "bar", "scatter", "hist"], key="panel3_type")
                plot3_x = st.selectbox("X Variable:", df.columns.tolist(), key="panel3_x")
                plot3_y = st.selectbox("Y Variable (if applicable):", 
                                       [""] + numeric_cols, key="panel3_y")
                
                layout_type = st.selectbox("Select Layout Type:", 
                                          ["Grid 2x2", "Column", "Row"], key="multi_layout")
                palette = st.selectbox("Select Color Palette:", 
                                      ["Default", "Colorful", "Pastel", "Dark Tones", "Paired Colors", "Rainbow"],
                                      key="multi_palette")
                
                # Create vars_config dictionary
                vars_config = {
                    'plot1': {'type': plot1_type, 'x': plot1_x, 'y': plot1_y if plot1_y else None},
                    'plot2': {'type': plot2_type, 'x': plot2_x, 'y': plot2_y if plot2_y else None},
                    'plot3': {'type': plot3_type, 'x': plot3_x, 'y': plot3_y if plot3_y else None}
                }
                
                if st.button("Generate Multipanel Plot"):
                    with col2:
                        render_custom_plot(df, plot_type, None, theme, 
                                          vars_config=vars_config, layout_type=layout_type, palette=palette)
    
    else:
        st.info("Please upload a CSV file to practice creating visualizations with your own data.")
        
        # Sample data option
        if st.button("Use Sample Data"):
            # Load the sample data included with the app
            try:
                df = pd.read_csv("dummy_data_for_practice.csv")
                st.session_state['sample_data'] = df
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {e}")

# Histogram tab
with tab2:
    st.header("Histogram")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        distribution_type = st.selectbox(
            "Select histogram distribution type:",
            [
                "Normal Distribution",
                "Positively Skewed",
                "Negatively Skewed",
                "Unimodal Distribution",
                "Bimodal Distribution",
                "Multimodal Distribution",
            ],
            key='hist_dist'
        )
        hist_color = st.selectbox(
            "Select histogram color:",
            list(color_palettes.keys()),
            key='hist_color'
        )
    
    with col2:
        # Create and render the histogram
        ax = create_histogram(distribution_type, hist_color, theme)
        render_maidr_plot(ax)

# Box Plot tab
with tab3:
    st.header("Box Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        boxplot_type = st.selectbox(
            "Select box plot type:",
            [
                "Positively Skewed with Outliers",
                "Negatively Skewed with Outliers",
                "Symmetric with Outliers",
                "Symmetric without Outliers",
            ],
            key='box_type'
        )
        boxplot_color = st.selectbox(
            "Select box plot color:",
            list(color_palettes.keys()),
            key='box_color'
        )
    
    with col2:
        # Create and render the box plot
        ax = create_boxplot(boxplot_type, boxplot_color, theme)
        render_maidr_plot(ax)

# Scatter Plot tab
with tab4:
    st.header("Scatter Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        scatterplot_type = st.selectbox(
            "Select scatter plot type:",
            [
                "No Correlation",
                "Weak Positive Correlation",
                "Strong Positive Correlation",
                "Weak Negative Correlation",
                "Strong Negative Correlation",
            ],
            key='scatter_type'
        )
        scatter_color = st.selectbox(
            "Select scatter plot color:",
            list(color_palettes.keys()),
            key='scatter_color_main'
        )
    
    with col2:
        # Create and render the scatter plot
        ax = create_scatterplot(scatterplot_type, scatter_color, theme)
        render_maidr_plot(ax)

# Bar Plot tab
with tab5:
    st.header("Bar Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        barplot_color = st.selectbox(
            "Select bar plot color:",
            list(color_palettes.keys()),
            key='bar_color'
        )
    
    with col2:
        # Create and render the bar plot
        ax = create_barplot(barplot_color, theme)
        render_maidr_plot(ax)

# Line Plot tab
with tab6:
    st.header("Line Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        lineplot_type = st.selectbox(
            "Select line plot type:",
            [
                "Linear Trend",
                "Exponential Growth",
                "Sinusoidal Pattern",
                "Random Walk",
            ],
            key='line_type'
        )
        lineplot_color = st.selectbox(
            "Select line plot color:",
            list(color_palettes.keys()),
            key='line_color_main'
        )
    
    with col2:
        # Create and render the line plot
        ax = create_lineplot(lineplot_type, lineplot_color, theme)
        render_maidr_plot(ax)

# Heatmap tab
with tab7:
    st.header("Heatmap")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        heatmap_type = st.selectbox(
            "Select heatmap type:",
            [
                "Random",
                "Correlated",
                "Checkerboard",
            ],
            key='heatmap_type'
        )
    
    with col2:
        # Create and render the heatmap
        ax = create_heatmap(heatmap_type, theme)
        render_maidr_plot(ax)

# Multilayer Plot tab
with tab8:
    st.header("Multilayer Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        multilayer_background_type = st.selectbox(
            "Select background plot type:",
            [
                "Bar Plot",
                "Histogram",
                "Scatter Plot"
            ],
            key='multilayer_bg_type'
        )
        multilayer_background_color = st.selectbox(
            "Select background color:",
            list(color_palettes.keys()),
            key='multilayer_bg_color_main'
        )
        multilayer_line_color = st.selectbox(
            "Select line color:",
            list(color_palettes.keys()),
            key='multilayer_line_color_main'
        )
    
    with col2:
        # Create and render the multilayer plot
        ax = create_multilayer_plot(
            multilayer_background_type, 
            multilayer_background_color, 
            multilayer_line_color, 
            theme
        )
        render_maidr_plot(ax)

# Multipanel Plot tab
with tab9:
    st.header("Multipanel Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        # Removed the layout dropdown
        multipanel_color = st.selectbox(
            "Select color palette:",
            [
                "Default",
                "Colorful", 
                "Pastel", 
                "Dark Tones", 
                "Paired Colors", 
                "Rainbow"
            ],
            key='multipanel_color'
        )
    
    with col2:
        # Create and render the multipanel plot with fixed layout (removed layout parameter)
        ax = create_multipanel_plot("Grid 2x2", multipanel_color, theme)
        render_maidr_plot(ax)

# Multiline Plot tab
with tab10:
    st.header("Multiline Plot")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        multiline_type = st.selectbox(
            "Select multiline plot type:",
            [
                "Simple Trends",
                "Seasonal Patterns",
                "Growth Comparison",
                "Random Series",
            ],
            key='multiline_type'
        )
        multiline_color = st.selectbox(
            "Select color palette:",
            [
                "Default",
                "Colorful", 
                "Pastel", 
                "Dark Tones", 
                "Paired Colors", 
                "Rainbow"
            ],
            key='multiline_color'
        )
    
    with col2:
        # Generate data and create the multiline plot
        data = generate_multiline_data(multiline_type)
        ax = create_multiline_plot(data, multiline_type, multiline_color, theme)
        render_maidr_plot(ax)

# Footer
st.markdown("---")
st.markdown("Learning Data Visualization with MAIDR - Explore different visualization types and make them accessible")
