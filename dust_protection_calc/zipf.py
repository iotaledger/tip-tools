# -*- coding: utf-8 -*-
import math
import plot

#===============================================================================
def zipf_distribution_scaled(addresses, zipf_coefficient, total_value):
    m = {}

    y_total = 0
    scaling_factor = math.pow(10, 10)
    for i, p in enumerate(addresses):
    	m[p] = math.pow(float(i+1), -zipf_coefficient) * scaling_factor
    	y_total += m[p]

    for i, p in enumerate(addresses):
         m[p] = (m[p] / float(y_total)) *  total_value

    return m

#===============================================================================
if __name__ == '__main__':
    total_supply = 2779530283277761
    
    zipf_coefficients = {}
    zipf_coefficients["bitcoin"]  = 0.7628
    zipf_coefficients["ethereum"] = 0.756786
    zipf_coefficients["iota"]     = 0.934275
    zipf_coefficients["obyte"]    = 1.14361
    zipf_coefficients["tether"]   = 0.815054
    zipf_coefficients["eos"]      = 0.536744
    zipf_coefficients["tron"]     = 1.02043

    identities = []
    for i in range(0, 1000, 1):
        identities.append(i)

    sub_plots  = [plot.Subplot(row_index=0, column_index=0, x_label='', y_label='balance')]
    plot_lines = []


    for zipf_coefficient_name in zipf_coefficients.keys():
        zipf_dist = zipf_distribution_scaled(identities, zipf_coefficient=zipf_coefficients[zipf_coefficient_name], total_value=total_supply)

        x = []
        y = []
        y_total = 0
        for k in zipf_dist.keys():
            x.append(k)
            y.append(zipf_dist[k])
            y_total += zipf_dist[k]

        plot_lines.append(plot.PlotLine(subplot_nr=0, x=x, y=y, name=zipf_coefficient_name))

    plot.plot(sub_plots, plot_lines)
