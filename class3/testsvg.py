''' testsvg.py '''

import pygal

fa4_in_packets = [24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24, 21]
fa4_out_packets = [21, 24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24]

# Create a Chart of type Line
line_chart = pygal.Line()

# Title
line_chart.title = 'Input/Output Packets and Bytes'

# X-axis labels (samples were every five minutes)
line_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']

# Add each one of the above lists into the graph as a line with corresponding label
line_chart.add('InPackets', fa4_in_packets)
line_chart.add('OutPackets', fa4_out_packets)

# Create an output image file from this
line_chart.render_to_file('test.svg')
