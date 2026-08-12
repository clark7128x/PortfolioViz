"""
PortfolioViz - A Desktop Portfolio Visualization Application
Author: Python Developer
Description: A modern GUI application for managing and visualizing investment portfolios
"""

import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from tkinter import messagebox

# =============================================================================
# Configure CustomTkinter appearance
# =============================================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class PortfolioVizApp(ctk.CTk):
    """Main application class for PortfolioViz"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("PortfolioViz - Portfolio Visualization Dashboard")
        self.geometry("1300x800")
        self.minsize(1100, 700)
        
        # CSV file path
        self.csv_file = "portfolio.csv"
        
        # Load existing data or create new DataFrame
        self.df = self.load_data()
        
        # Build the GUI
        self.create_layout()
        self.create_sidebar()
        self.create_main_area()
        
        # Initial dashboard update
        self.update_dashboard()
        
    def load_data(self):
        """
        Load portfolio data from CSV file.
        Creates a new file with headers if it doesn't exist.
        """
        columns = ['Asset Name', 'Type', 'Quantity', 'Buy Price', 'Current Price']
        
        if os.path.exists(self.csv_file):
            try:
                df = pd.read_csv(self.csv_file)
                # Validate columns
                if list(df.columns) != columns:
                    print("Warning: CSV columns mismatch. Creating backup and new file.")
                    os.rename(self.csv_file, self.csv_file + ".backup")
                    df = pd.DataFrame(columns=columns)
                    df.to_csv(self.csv_file, index=False)
            except Exception as e:
                print(f"Error loading CSV: {e}")
                df = pd.DataFrame(columns=columns)
        else:
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.csv_file, index=False)
            print(f"Created new portfolio file: {self.csv_file}")
        
        return df
    
    def save_data(self):
        """Save current DataFrame to CSV file"""
        try:
            self.df.to_csv(self.csv_file, index=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
            return False
    
    def create_layout(self):
        """Configure the main grid layout"""
        self.grid_columnconfigure(0, weight=0)  # Sidebar - fixed width
        self.grid_columnconfigure(1, weight=1)  # Main area - expandable
        self.grid_rowconfigure(0, weight=1)
    
    def create_sidebar(self):
        """Create the left sidebar with input form"""
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        # App Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="💼 PortfolioViz",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.pack(pady=(25, 5), padx=20)
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Investment Portfolio Manager",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 20), padx=20)
        
        # Separator
        self.separator1 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30")
        self.separator1.pack(fill="x", padx=20, pady=10)
        
        # Form Title
        self.form_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="Add New Asset",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.form_title.pack(pady=(10, 15), padx=20)
        
        # Asset Name Input
        self.name_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Asset Name:",
            font=ctk.CTkFont(size=13)
        )
        self.name_label.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.name_entry = ctk.CTkEntry(
            self.sidebar_frame,
            width=270,
            height=35,
            placeholder_text="e.g., Apple Inc., Bitcoin"
        )
        self.name_entry.pack(pady=(0, 10), padx=25)
        
        # Asset Type Dropdown
        self.type_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Asset Type:",
            font=ctk.CTkFont(size=13)
        )
        self.type_label.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.type_var = ctk.StringVar(value="Stock")
        self.type_dropdown = ctk.CTkOptionMenu(
            self.sidebar_frame,
            width=270,
            height=35,
            values=["Stock", "Crypto", "Cash"],
            variable=self.type_var,
            dynamic_resizing=False
        )
        self.type_dropdown.pack(pady=(0, 10), padx=25)
        
        # Quantity Input
        self.quantity_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Quantity:",
            font=ctk.CTkFont(size=13)
        )
        self.quantity_label.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.quantity_entry = ctk.CTkEntry(
            self.sidebar_frame,
            width=270,
            height=35,
            placeholder_text="e.g., 10, 0.5"
        )
        self.quantity_entry.pack(pady=(0, 10), padx=25)
        
        # Buy Price Input
        self.buy_price_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Buy Price ($):",
            font=ctk.CTkFont(size=13)
        )
        self.buy_price_label.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.buy_price_entry = ctk.CTkEntry(
            self.sidebar_frame,
            width=270,
            height=35,
            placeholder_text="e.g., 150.00"
        )
        self.buy_price_entry.pack(pady=(0, 10), padx=25)
        
        # Current Price Input
        self.current_price_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Current Price ($):",
            font=ctk.CTkFont(size=13)
        )
        self.current_price_label.pack(pady=(5, 2), padx=25, anchor="w")
        
        self.current_price_entry = ctk.CTkEntry(
            self.sidebar_frame,
            width=270,
            height=35,
            placeholder_text="e.g., 175.00"
        )
        self.current_price_entry.pack(pady=(0, 15), padx=25)
        
        # Add Asset Button
        self.add_button = ctk.CTkButton(
            self.sidebar_frame,
            text="➕ Add Asset",
            width=270,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.add_asset
        )
        self.add_button.pack(pady=(10, 5), padx=25)
        
        # Clear Form Button
        self.clear_button = ctk.CTkButton(
            self.sidebar_frame,
            text="🗑️ Clear Form",
            width=270,
            height=35,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            border_width=2,
            command=self.clear_form
        )
        self.clear_button.pack(pady=(5, 10), padx=25)
        
        # Status Message Label
        self.status_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=260
        )
        self.status_label.pack(pady=10, padx=25)
        
        # Separator
        self.separator2 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray30")
        self.separator2.pack(fill="x", padx=20, pady=15, side="bottom")
        
        # Asset Count Label (at bottom)
        self.asset_count_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Total Assets: 0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.asset_count_label.pack(pady=(0, 20), padx=20, side="bottom")
        
        # Delete Asset Section
        self.delete_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.delete_frame.pack(fill="x", padx=25, pady=5, side="bottom")
        
        self.delete_label = ctk.CTkLabel(
            self.delete_frame,
            text="Delete Asset:",
            font=ctk.CTkFont(size=11)
        )
        self.delete_label.pack(anchor="w")
        
        self.delete_entry = ctk.CTkEntry(
            self.delete_frame,
            width=180,
            height=30,
            placeholder_text="Asset name to delete"
        )
        self.delete_entry.pack(side="left", pady=5)
        
        self.delete_button = ctk.CTkButton(
            self.delete_frame,
            text="Delete",
            width=80,
            height=30,
            fg_color="#8B0000",
            hover_color="#A52A2A",
            command=self.delete_asset
        )
        self.delete_button.pack(side="right", pady=5)
    
    def create_main_area(self):
        """Create the right main area with dashboard and chart"""
        # Main Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_rowconfigure(0, weight=0)  # Dashboard
        self.main_frame.grid_rowconfigure(1, weight=1)  # Chart
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # =====================================================================
        # Dashboard Section
        # =====================================================================
        self.dashboard_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.dashboard_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        # Dashboard Title
        self.dashboard_title = ctk.CTkLabel(
            self.dashboard_frame,
            text="📊 Portfolio Summary",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.dashboard_title.pack(pady=(20, 15))
        
        # Summary Cards Container
        self.cards_container = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.cards_container.pack(fill="x", padx=30, pady=(0, 20))
        self.cards_container.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card 1: Total Portfolio Value
        self.value_card = ctk.CTkFrame(self.cards_container, corner_radius=15)
        self.value_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.value_icon = ctk.CTkLabel(
            self.value_card,
            text="💰",
            font=ctk.CTkFont(size=30)
        )
        self.value_icon.pack(pady=(20, 5))
        
        self.value_title = ctk.CTkLabel(
            self.value_card,
            text="Total Portfolio Value",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.value_title.pack(pady=2)
        
        self.value_amount = ctk.CTkLabel(
            self.value_card,
            text="$0.00",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00D4FF"
        )
        self.value_amount.pack(pady=(5, 20))
        
        # Card 2: Total Profit/Loss
        self.pnl_card = ctk.CTkFrame(self.cards_container, corner_radius=15)
        self.pnl_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.pnl_icon = ctk.CTkLabel(
            self.pnl_card,
            text="📈",
            font=ctk.CTkFont(size=30)
        )
        self.pnl_icon.pack(pady=(20, 5))
        
        self.pnl_title = ctk.CTkLabel(
            self.pnl_card,
            text="Total Profit/Loss",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.pnl_title.pack(pady=2)
        
        self.pnl_amount = ctk.CTkLabel(
            self.pnl_card,
            text="$0.00",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00FF00"
        )
        self.pnl_amount.pack(pady=(5, 20))
        
        # Card 3: Return Percentage
        self.return_card = ctk.CTkFrame(self.cards_container, corner_radius=15)
        self.return_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.return_icon = ctk.CTkLabel(
            self.return_card,
            text="📊",
            font=ctk.CTkFont(size=30)
        )
        self.return_icon.pack(pady=(20, 5))
        
        self.return_title = ctk.CTkLabel(
            self.return_card,
            text="Return (%)",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.return_title.pack(pady=2)
        
        self.return_amount = ctk.CTkLabel(
            self.return_card,
            text="0.00%",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00FF00"
        )
        self.return_amount.pack(pady=(5, 20))
        
        # =====================================================================
        # Chart Section
        # =====================================================================
        self.chart_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Chart Title
        self.chart_title = ctk.CTkLabel(
            self.chart_frame,
            text="🥧 Asset Allocation by Type",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.chart_title.pack(pady=(15, 10))
        
        # Matplotlib Figure Setup
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.fig.patch.set_facecolor('#2B2B2B')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2B2B2B')
        
        # Canvas for embedding matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def add_asset(self):
        """Add a new asset to the portfolio"""
        # Get input values
        name = self.name_entry.get().strip()
        asset_type = self.type_var.get()
        quantity_str = self.quantity_entry.get().strip()
        buy_price_str = self.buy_price_entry.get().strip()
        current_price_str = self.current_price_entry.get().strip()
        
        # Validate: Check for empty fields
        if not all([name, quantity_str, buy_price_str, current_price_str]):
            self.show_status("⚠️ Please fill in all fields.", "#FFD700")
            return
        
        # Validate: Check numeric values
        try:
            quantity = float(quantity_str)
            buy_price = float(buy_price_str)
            current_price = float(current_price_str)
        except ValueError:
            self.show_status("❌ Invalid numbers. Please enter valid numeric values.", "#FF6B6B")
            return
        
        # Validate: Check for positive values
        if quantity <= 0:
            self.show_status("❌ Quantity must be greater than 0.", "#FF6B6B")
            return
        
        if buy_price < 0 or current_price < 0:
            self.show_status("❌ Prices cannot be negative.", "#FF6B6B")
            return
        
        # Check for duplicate asset name
        if name.lower() in self.df['Asset Name'].str.lower().values:
            self.show_status(f"⚠️ Asset '{name}' already exists.", "#FFD700")
            return
        
        # Create new row and add to DataFrame
        new_asset = pd.DataFrame({
            'Asset Name': [name],
            'Type': [asset_type],
            'Quantity': [quantity],
            'Buy Price': [buy_price],
            'Current Price': [current_price]
        })
        
        self.df = pd.concat([self.df, new_asset], ignore_index=True)
        
        # Save to CSV
        if self.save_data():
            self.show_status(f"✅ Successfully added '{name}'!", "#00FF00")
            self.clear_form()
            self.update_dashboard()
        else:
            # Rollback if save failed
            self.df = self.df.iloc[:-1]
    
    def delete_asset(self):
        """Delete an asset from the portfolio"""
        name = self.delete_entry.get().strip()
        
        if not name:
            self.show_status("⚠️ Enter asset name to delete.", "#FFD700")
            return
        
        # Find the asset (case-insensitive)
        mask = self.df['Asset Name'].str.lower() == name.lower()
        
        if not mask.any():
            self.show_status(f"❌ Asset '{name}' not found.", "#FF6B6B")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            self.df = self.df[~mask].reset_index(drop=True)
            
            if self.save_data():
                self.show_status(f"🗑️ Deleted '{name}'.", "#00FF00")
                self.delete_entry.delete(0, 'end')
                self.update_dashboard()
    
    def clear_form(self):
        """Clear all input fields"""
        self.name_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.buy_price_entry.delete(0, 'end')
        self.current_price_entry.delete(0, 'end')
        self.type_var.set("Stock")
    
    def show_status(self, message, color):
        """Display a status message that fades after 4 seconds"""
        self.status_label.configure(text=message, text_color=color)
        # Clear message after 4 seconds
        self.after(4000, lambda: self.status_label.configure(text=""))
    
    def update_dashboard(self):
        """Recalculate all values and update the dashboard display"""
        # Update asset count
        asset_count = len(self.df)
        self.asset_count_label.configure(text=f"Total Assets: {asset_count}")
        
        if self.df.empty:
            # No data - show zeros
            self.value_amount.configure(text="$0.00")
            self.pnl_amount.configure(text="$0.00", text_color="#00FF00")
            self.return_amount.configure(text="0.00%", text_color="#00FF00")
            self.pnl_icon.configure(text="📈")
            self.update_pie_chart()
            return
        
        # Calculate Current Value for each asset
        self.df['Current Value'] = self.df['Quantity'] * self.df['Current Price']
        
        # Calculate Cost Basis for each asset
        self.df['Cost Basis'] = self.df['Quantity'] * self.df['Buy Price']
        
        # Calculate totals
        total_value = self.df['Current Value'].sum()
        total_cost = self.df['Cost Basis'].sum()
        profit_loss = total_value - total_cost
        
        # Calculate return percentage
        if total_cost > 0:
            return_pct = (profit_loss / total_cost) * 100
        else:
            return_pct = 0.0
        
        # Update Total Portfolio Value
        self.value_amount.configure(text=f"${total_value:,.2f}")
        
        # Update Profit/Loss with color coding
        if profit_loss >= 0:
            self.pnl_amount.configure(
                text=f"+${profit_loss:,.2f}",
                text_color="#00FF00"
            )
            self.pnl_icon.configure(text="📈")
        else:
            self.pnl_amount.configure(
                text=f"-${abs(profit_loss):,.2f}",
                text_color="#FF6B6B"
            )
            self.pnl_icon.configure(text="📉")
        
        # Update Return Percentage
        if return_pct >= 0:
            self.return_amount.configure(
                text=f"+{return_pct:.2f}%",
                text_color="#00FF00"
            )
        else:
            self.return_amount.configure(
                text=f"{return_pct:.2f}%",
                text_color="#FF6B6B"
            )
        
        # Update pie chart
        self.update_pie_chart()
    
    def update_pie_chart(self):
        """Generate and display the pie chart for asset allocation"""
        self.ax.clear()
        
        if self.df.empty:
            # No data - display message
            self.ax.text(
                0.5, 0.5,
                'No assets in portfolio\n\nAdd your first asset using the form',
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.ax.transAxes,
                fontsize=14,
                color='white',
                style='italic'
            )
            self.ax.set_facecolor('#2B2B2B')
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Group by Type and sum current values
        allocation = self.df.groupby('Type')['Current Value'].sum()
        
        # Filter out zero values
        allocation = allocation[allocation > 0]
        
        if allocation.empty:
            self.ax.text(
                0.5, 0.5,
                'All assets have zero value',
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.ax.transAxes,
                fontsize=14,
                color='white'
            )
            self.ax.set_facecolor('#2B2B2B')
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Define colors for each asset type
        color_map = {
            'Stock': '#4CAF50',   # Green
            'Crypto': '#FF9800',  # Orange
            'Cash': '#2196F3'     # Blue
        }
        
        colors = [color_map.get(t, '#9E9E9E') for t in allocation.index]
        
        # Create explode effect
        explode = [0.03] * len(allocation)
        
        # Create pie chart
        wedges, texts, autotexts = self.ax.pie(
            allocation.values,
            labels=None,
            autopct='%1.1f%%',
            colors=colors,
            explode=explode,
            shadow=True,
            startangle=90,
            pctdistance=0.75
        )
        
        # Style the percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        # Create legend with values
        legend_labels = [
            f'{t}: ${v:,.2f}' 
            for t, v in zip(allocation.index, allocation.values)
        ]
        
        self.ax.legend(
            wedges,
            legend_labels,
            title="Asset Types",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=10,
            title_fontsize=12,
            facecolor='#2B2B2B',
            edgecolor='gray',
            labelcolor='white'
        )
        
        # Style the plot
        self.ax.set_facecolor('#2B2B2B')
        
        # Adjust layout
        self.fig.tight_layout()
        
        # Redraw canvas
        self.canvas.draw()


# =============================================================================
# Application Entry Point
# =============================================================================
def main():
    """Main function to run the application"""
    print("=" * 50)
    print("  PortfolioViz - Portfolio Visualization App")
    print("=" * 50)
    print("\nStarting application...")
    
    app = PortfolioVizApp()
    app.mainloop()


if __name__ == "__main__":
    main()