"""
Responsive design utilities for mobile-friendly interface.
"""

import streamlit as st
from typing import Dict, Tuple, Optional


class ResponsiveDesign:
    """Utilities for responsive design and mobile detection."""
    
    @staticmethod
    def get_device_type() -> str:
        """
        Detect device type based on user agent or viewport.
        Returns: 'mobile', 'tablet', or 'desktop'
        """
        # Check if we can get viewport info from browser
        try:
            # This is a simplified detection - in a real app you might use JavaScript
            # For now, we'll rely on CSS media queries and assume mobile-first
            return "mobile"  # Default to mobile-first approach
        except:
            return "mobile"
    
    @staticmethod
    def get_mobile_css() -> str:
        """Get mobile-optimized CSS styles."""
        return """
        <style>
        /* Mobile-first responsive CSS injection */
        @import url('styles/mobile.css');
        
        /* JavaScript for viewport detection */
        <script>
        function detectViewport() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            const isMobile = width < 768;
            const isTablet = width >= 768 && width <= 1024;
            
            document.body.setAttribute('data-device', 
                isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop'
            );
            
            // Store in session state
            window.streamlit?.setComponentValue({
                'viewport_width': width,
                'viewport_height': height,
                'device_type': isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop'
            });
        }
        
        // Run on load and resize
        window.addEventListener('load', detectViewport);
        window.addEventListener('resize', detectViewport);
        
        // Initial detection
        detectViewport();
        </script>
        </style>
        """
    
    @staticmethod
    def create_mobile_layout(content_func, sidebar_func=None):
        """
        Create a mobile-optimized layout.
        
        Args:
            content_func: Function that renders main content
            sidebar_func: Optional function that renders sidebar content
        """
        # Mobile-first approach
        if sidebar_func:
            # On mobile, sidebar content goes to top
            with st.container():
                st.markdown('<div class="mobile-sidebar">', unsafe_allow_html=True)
                sidebar_func()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Main content
        with st.container():
            st.markdown('<div class="mobile-content">', unsafe_allow_html=True)
            content_func()
            st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def mobile_columns(*ratios) -> Tuple:
        """
        Create responsive columns that stack on mobile.
        
        Args:
            *ratios: Column ratios for desktop view
            
        Returns:
            Tuple of column objects
        """
        # On mobile, we'll stack columns vertically using CSS
        cols = st.columns(ratios)
        
        # Add mobile-responsive classes
        for i, col in enumerate(cols):
            col.markdown(f'<div class="responsive-col responsive-col-{i}">', 
                        unsafe_allow_html=True)
        
        return cols
    
    @staticmethod
    def mobile_button(label: str, key: Optional[str] = None, **kwargs) -> bool:
        """
        Create a mobile-optimized button.
        
        Args:
            label: Button text
            key: Unique key for the button
            **kwargs: Additional arguments for st.button
            
        Returns:
            Boolean indicating if button was clicked
        """
        # Add mobile-specific styling
        st.markdown(
            f"""
            <style>
            div[data-testid="stButton"] > button[kind="primary"] {{
                width: 100%;
                height: 44px;
                font-size: 16px;
                border-radius: 8px;
                margin: 8px 0;
                touch-action: manipulation;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        
        return st.button(label, key=key, **kwargs)
    
    @staticmethod
    def mobile_file_uploader(label: str, **kwargs):
        """
        Create a mobile-optimized file uploader.
        
        Args:
            label: Uploader label
            **kwargs: Additional arguments for st.file_uploader
        """
        # Add mobile-specific styling
        st.markdown(
            """
            <style>
            .stFileUploader {
                margin: 16px 0;
            }
            .stFileUploader > div {
                padding: 16px;
                border: 2px dashed #ccc;
                border-radius: 8px;
                text-align: center;
                min-height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        return st.file_uploader(label, **kwargs)
    
    @staticmethod
    def mobile_selectbox(label: str, options, **kwargs):
        """
        Create a mobile-optimized selectbox.
        
        Args:
            label: Selectbox label
            options: List of options
            **kwargs: Additional arguments for st.selectbox
        """
        # Add mobile-specific styling
        st.markdown(
            """
            <style>
            .stSelectbox > div > div > select {
                font-size: 16px !important;
                height: 44px;
                padding: 8px 12px;
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        return st.selectbox(label, options, **kwargs)
    
    @staticmethod
    def mobile_text_input(label: str, **kwargs):
        """
        Create a mobile-optimized text input.
        
        Args:
            label: Input label
            **kwargs: Additional arguments for st.text_input
        """
        # Add mobile-specific styling
        st.markdown(
            """
            <style>
            .stTextInput > div > div > input {
                font-size: 16px !important;
                height: 44px;
                padding: 8px 12px;
                border-radius: 8px;
                border: 2px solid #ddd;
            }
            .stTextInput > div > div > input:focus {
                border-color: #007bff;
                outline: none;
                box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        return st.text_input(label, **kwargs)
    
    @staticmethod
    def mobile_metric(label: str, value: str, delta: Optional[str] = None):
        """
        Create a mobile-optimized metric display.
        
        Args:
            label: Metric label
            value: Metric value
            delta: Optional delta value
        """
        # Create mobile-friendly metric layout
        st.markdown(
            f"""
            <div class="mobile-metric">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                {f'<div class="metric-delta">{delta}</div>' if delta else ''}
            </div>
            <style>
            .mobile-metric {{
                background: #f8f9fa;
                padding: 16px;
                border-radius: 8px;
                margin: 8px 0;
                text-align: center;
                border: 1px solid #e9ecef;
            }}
            .metric-label {{
                font-size: 14px;
                color: #6c757d;
                margin-bottom: 8px;
                font-weight: 500;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: #212529;
                margin-bottom: 4px;
            }}
            .metric-delta {{
                font-size: 12px;
                color: #28a745;
                font-weight: 500;
            }}
            @media (max-width: 767px) {{
                .mobile-metric {{
                    padding: 12px;
                    margin: 6px 0;
                }}
                .metric-value {{
                    font-size: 20px;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def mobile_chart_container():
        """
        Create a mobile-optimized container for charts.
        """
        return st.container()
    
    @staticmethod
    def get_responsive_chart_config() -> Dict:
        """
        Get responsive configuration for Plotly charts.
        
        Returns:
            Dictionary with responsive chart configuration
        """
        return {
            'displayModeBar': False,  # Hide toolbar on mobile
            'responsive': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': [
                'pan2d', 'lasso2d', 'select2d', 'autoScale2d',
                'hoverClosestCartesian', 'hoverCompareCartesian'
            ],
            'layout': {
                'margin': {'l': 20, 'r': 20, 't': 40, 'b': 40},
                'font': {'size': 12},
                'showlegend': True,
                'legend': {
                    'orientation': 'h',
                    'y': -0.2,
                    'x': 0.5,
                    'xanchor': 'center'
                }
            }
        }
    
    @staticmethod
    def mobile_navigation_menu(options: Dict[str, str]) -> str:
        """
        Create a mobile-friendly navigation menu.
        
        Args:
            options: Dictionary of {label: value} for menu options
            
        Returns:
            Selected option value
        """
        st.markdown(
            """
            <style>
            .mobile-nav {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                padding: 16px 0;
                justify-content: center;
            }
            .mobile-nav-item {
                padding: 8px 16px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 20px;
                text-decoration: none;
                color: #495057;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.2s;
                cursor: pointer;
                min-height: 40px;
                display: flex;
                align-items: center;
            }
            .mobile-nav-item:hover,
            .mobile-nav-item.active {
                background: #007bff;
                color: white;
                border-color: #007bff;
            }
            @media (max-width: 767px) {
                .mobile-nav-item {
                    flex: 1 1 calc(50% - 4px);
                    text-align: center;
                    justify-content: center;
                    min-width: 120px;
                }}
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Use selectbox for mobile navigation
        return st.selectbox(
            "Navigate to:",
            options=list(options.keys()),
            format_func=lambda x: options.get(x, x),
            key="mobile_nav"
        )