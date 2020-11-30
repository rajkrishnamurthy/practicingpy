# 
from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16 

import holoviews as hv
hv.extension('bokeh')


# Argument should be a dataframe that contains data per customer per plan
def heatmap_tab(controls):

	# the list of control domains will be colorcoded for the heat map
	controls_domains=list(set((dataFrame[dataFrame['root']==True])['control_name']))
	controls_domains.sort()
	controls_colors = Category20_16
	controls_colors.sort()

	controls_selection = CheckboxGroup(labels=controls_domains, 
									  active = [0, 1])
	range_select = RangeSlider(start = 0, end = 100, value = (80, 100),
							   step = 10, title = 'Compliance % Range')
	
	def form_controls_dataset(controls_list, range_start = 80, range_end = 100):

		# Dataframe to hold information
		heatmap_df = pd.DataFrame(columns=['impact', 'frequency', 'control'])
		range_extent = range_end - range_start

		# Iterate through all the carriers
		for i, control_name in enumerate(controls_list):

			# Add to the overall dataframe
			heatmap_df = heatmap_df.append(temp_df)

		# Overall dataframe
		heatmap_df = heatmap_df.sort_values(['impact', 'frequency'])

		return ColumnDataSource(heatmap_df)


	controls_dataset = form_controls_dataset(list(controls_domains[0]),
					   range_start = range_select.value[0],
					   range_end = range_select.value[1])

	def update(attr, old, new):
		controls_to_plot = []
		 
		for i in controls_selection.active:
			tmp_control_name=controls_selection.labels[i]
			tmp_control_id=

		
		new_controls_dataset = form_controls_dataset(controls_to_plot,
							   range_start = range_select.value[0],
							   range_end = range_select.value[1])
		
		

		controls_dataset.data.update(new_controls_dataset.data)

	controls_selection.on_change('active', update)
	range_select.on_change('value', update)


	# return tab