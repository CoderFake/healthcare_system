#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Table Component - Reusable data table with sorting and filtering
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Dict, Any, Callable, Optional

class DataTable:
    """Enhanced data table with sorting and filtering capabilities"""
    
    def __init__(self, parent, columns: List[Tuple[str, str, int]], height: int = 10):
        """
        Initialize the data table
        
        Args:
            parent: Parent widget
            columns: List of (column_id, column_text, column_width) tuples
            height: Height in rows
        """
        self.parent = parent
        self.columns = columns
        
        # Create frame for table and scrollbars
        self.frame = ttk.Frame(parent)
        
        # Create the treeview
        self._create_treeview(height)
        
        # Setup sorting
        self._setup_sorting()
        
        # Data tracking
        self.data = []
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False
    
    def _create_treeview(self, height):
        """Create the treeview with scrollbars"""
        # Extract column IDs
        column_ids = [col[0] for col in self.columns]
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.frame, 
            columns=column_ids, 
            show="headings", 
            height=height
        )
        
        # Set column headings and widths
        for col_id, col_text, col_width in self.columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width)
        
        # Add vertical scrollbar
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
    
    def _setup_sorting(self):
        """Setup column sorting"""
        for col_id, _, _ in self.columns:
            self.tree.heading(
                col_id,
                command=lambda c=col_id: self._sort_by_column(c)
            )
    
    def _sort_by_column(self, column):
        """Sort treeview data by column"""
        # Toggle sort direction if already sorting by this column
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Find column index
        col_index = [col[0] for col in self.columns].index(column)
        
        # Sort the data
        self.data.sort(
            key=lambda item: item[col_index] if item[col_index] else "",
            reverse=self.sort_reverse
        )
        
        # Reload the treeview
        self.load_data(self.data)
    
    def load_data(self, data: List[tuple]):
        """
        Load data into the table
        
        Args:
            data: List of value tuples matching column order
        """
        # Store data
        self.data = data
        
        # Clear existing items
        self.tree.delete(*self.tree.get_children())
        
        # Add data to tree
        for row in data:
            self.tree.insert("", "end", values=row)
    
    def filter_data(self, filter_func: Callable[[tuple], bool]):
        """
        Filter data based on a filter function
        
        Args:
            filter_func: Function that takes a data row and returns True if it should be displayed
        """
        # Apply filter
        self.filtered_data = [row for row in self.data if filter_func(row)]
        
        # Clear existing items
        self.tree.delete(*self.tree.get_children())
        
        # Add filtered data to tree
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)
    
    def reset_filter(self):
        """Reset filter and show all data"""
        self.filtered_data = []
        self.load_data(self.data)
    
    def get_selected_item(self) -> Optional[tuple]:
        """
        Get the currently selected item
        
        Returns:
            Selected item values as tuple or None if no selection
        """
        selected_items = self.tree.selection()
        
        if not selected_items:
            return None
        
        values = self.tree.item(selected_items[0], "values")
        return values
    
    def get_selected_items(self) -> List[tuple]:
        """
        Get all selected items
        
        Returns:
            List of selected item values as tuples
        """
        selected_items = self.tree.selection()
        
        result = []
        for item_id in selected_items:
            values = self.tree.item(item_id, "values")
            result.append(values)
        
        return result
    
    def select_item_by_value(self, column_index: int, value: Any):
        """
        Select an item by a value in a specific column
        
        Args:
            column_index: Index of column to match
            value: Value to match
        """
        for item_id in self.tree.get_children():
            item_values = self.tree.item(item_id, "values")
            if str(item_values[column_index]) == str(value):
                self.tree.selection_set(item_id)
                self.tree.see(item_id)
                return
    
    def add_row(self, values: tuple, select: bool = False):
        """
        Add a row to the table
        
        Args:
            values: Row values as tuple
            select: Whether to select the new row
        """
        # Add to data
        self.data.append(values)
        
        # Add to tree
        item_id = self.tree.insert("", "end", values=values)
        
        # Select if requested
        if select:
            self.tree.selection_set(item_id)
            self.tree.see(item_id)
    
    def update_selected_row(self, values: tuple):
        """
        Update the selected row with new values
        
        Args:
            values: New row values as tuple
        """
        selected_items = self.tree.selection()
        
        if not selected_items:
            return
        
        item_id = selected_items[0]
        
        # Update in tree
        self.tree.item(item_id, values=values)
        
        # Update in data
        old_values = self.tree.item(item_id, "values")
        for i, row in enumerate(self.data):
            if row == old_values:
                self.data[i] = values
                break
    
    def delete_selected_rows(self):
        """Delete all selected rows"""
        selected_items = self.tree.selection()
        
        if not selected_items:
            return
        
        # Collect values to remove from data
        values_to_remove = []
        for item_id in selected_items:
            values = self.tree.item(item_id, "values")
            values_to_remove.append(values)
            
            # Remove from tree
            self.tree.delete(item_id)
        
        # Remove from data
        self.data = [row for row in self.data if row not in values_to_remove]
    
    def clear(self):
        """Clear all data"""
        self.tree.delete(*self.tree.get_children())
        self.data = []
        self.filtered_data = []