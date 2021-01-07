import streamlit as st

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# setup global formatting variables
bgcolor = '#FFF'
markColor = '#27332F'

def fryetag_theme():
	# Typography
	font = "Helvetica"
	# At Urban it's the same font for all text but it's good to keep them separate in case you want to change one later.
	labelFont = "Helvetica" 
	sourceFont = "Helvetica"
	# Axes
	axisColor = "#1F77B4"
	gridColor = "#1F77B4"
	# Colors
	main_palette = ["#1696d2", 
					"#d2d2d2",
					"#000000", 
					"#fdbf11", 
					"#ec008b", 
					"#55b748", 
					"#5c5859", 
					"#db2b27", 
				   ]
	sequential_palette = ["#cfe8f3", 
						  "#a2d4ec", 
						  "#73bfe2", 
						  "#46abdb", 
						  "#1696d2", 
						  "#12719e", 
						 ]
	return {
			# width and height are configured outside the config dict because they are Chart configurations/properties not chart-elements' configurations/properties.
			#"width": 685, # from the guide
			#"height": 380, # not in the guide
            "background": bgcolor,
            "padding" : {"left": 20, "top": 20, "right": 20, "bottom": 20},
            "autosize" : "pad",
			"config": {
				"title": {
					"fontSize": 20,
					"font": font,
					"anchor": "start", # equivalent of left-aligned.
					"color": markColor,
					"dy": -20,
					"dx": 10,
					"fontWeight": "bold",
					"subtitleColor": markColor, 
					"subtitlefontWeight": "normal`"
				},
				"subtitle": {
					"fontSize": 16,
					"font": font,
                    "fontWeight": "bold",
					"anchor": "start", # equivalent of left-aligned.
					"dy": -10,
					"dx": 30,
					"fontWeight": "normal"
				},
				"axisX": {
					"domain": True,
					"domainColor": axisColor,
					"domainWidth": 1,
					"grid": False,
					"labelFont": labelFont,
					"labelColor": markColor,
					"labelFontSize": 14,
					"labelAngle": 0, 
					"tickColor": axisColor,
					#"tickSize": 5, # default, including it just to show you can change it
					"titleFont": font,
					"titleColor": markColor,
					"titleFontSize": 14,
					"titlePadding": 10, # guessing, not specified in styleguide
					#"title": "X Axis Title (units)", 
				},
				"axisY": {
					"domain": False,
					"grid": True,
					"gridColor": gridColor,
					"gridWidth": 0.1,
					"labelFont": labelFont,
					"labelFontSize": 14,
					"labelColor": markColor,
                    "labelPadding": 15,
					"labelAngle": 0, 
					"ticks": False, # even if you don't have a "domain" you need to turn these off.
					"titleFont": font,
                    "titleColor": markColor,
					"titleFontSize": 12,
					"titlePadding": 15, # guessing, not specified in styleguide
					"title": "Y Axis Title (units)", 
					# titles are by default vertical left of axis so we need to hack this 
					"titleAngle": 0, # horizontal
					"titleY": -10, # move it up
					"titleX": 30, # move it to the right so it aligns with the labels 
				},
				"range": {
					"category": main_palette,
					"diverging": sequential_palette,
				},
				"legend": {
					"labelFont": labelFont,
					"labelFontSize": 12,
					"symbolType": "square", # just 'cause
					"symbolSize": 100, # default
					"titleFont": font,
					"titleFontSize": 12,
					"title": "", # set it to no-title by default
					"orient": "top-left", # so it's right next to the y-axis
					"offset": 0, # literally right next to the y-axis.
				},
				"view": {
					"stroke": "transparent", # altair uses gridlines to box the area where the data is visualized. This takes that off.
                    "fill": bgcolor
				},
				"background": {
					"color": "white", # white rather than transparent
                    "background": "white"
				},
				### MARKS CONFIGURATIONS ###
				"area": {
				   "fill": markColor,
			   },
			   "line": {
				   "color": markColor,
				   "stroke": markColor,
				   "strokeWidth": 3,
			   },
			   "trail": {
				   "color": markColor,
				   "stroke": markColor,
				   "strokeWidth": 0,
				   "size": 1,
			   },
			   "path": {
				   "stroke": markColor,
				   "strokeWidth": 0.5,
			   },
			   "point": {
				   "filled": True,
			   },
			   "text": {
				   "font": sourceFont,
				   "color": markColor,
				   "fontSize": 11,
				   "align": "right",
				   "fontWeight": 400,
				   "size": 11,
			   }, 
			   "bar": {
					"size": 12,
					"binSpacing": 1,
					"continuousBandSize": 30,
					"discreteBandSize": 5,
					"fill": "rgb(31, 119, 180, 0.4)",
					"stroke": False,
					"opacity": 0.7,
				},
                "geoshape": {
					"size": 40,
					"stroke": False,
					"opacity": 0.7,
                    "padding": 20,
				},
	}
		}
