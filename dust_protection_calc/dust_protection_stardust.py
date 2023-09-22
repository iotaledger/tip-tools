# -*- coding: utf-8 -*-
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
import outputs, plot

#===============================================================================
def getDollarFormat(value):
    return "%s$" % (locale.currency(value, symbol=False, grouping=True))

#===============================================================================
def calculateDustProtectionCostsStardust(print_summary, create_plots, show_plots):

    TOTAL_SUPPLY                = 2779530283277761
    PRICE_PER_MIOTA_DOLLAR      = 0.35

    BLOCK_SIZE_MAX              = 32768
    METADATA_LENGTH_MAX         = 8192
    NATIVE_TOKEN_COUNT_MAX      = 64
    
    WEIGHT_KEY                  = 10.0
    WEIGHT_DATA                 = 1.0

    MAXIMUM_DB_SIZES_GB         = [500.0, 1000.0, 2000.0]
    FUND_SPARSITY_PERCENTAGES   = [20.0, 50.0]
    
    payload_size_max    = outputs.getPayloadSizeMax(block_size_max=BLOCK_SIZE_MAX)
    output_size_max     = outputs.getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)

    if print_summary:    
        print("Current market cap: %s" % (getDollarFormat((TOTAL_SUPPLY / 1000000.0) * PRICE_PER_MIOTA_DOLLAR)))
        print("BlockSizeMax:        %5d" % (BLOCK_SIZE_MAX))
        print("PayloadSizeMax:      %5d" % (payload_size_max))
        print("OutputSizeMax:       %5d" % (output_size_max))
        print("MetadataLengthMax:   %5d" % (METADATA_LENGTH_MAX))
        print("NativeTokenCountMax: %5d" % (NATIVE_TOKEN_COUNT_MAX))
            
        for maximum_db_size_GB in MAXIMUM_DB_SIZES_GB:
            for fund_sparsity_percentage in FUND_SPARSITY_PERCENTAGES:
                db_size_bytes                       = maximum_db_size_GB * 1e9
                sparsity_factor                     = (fund_sparsity_percentage / 100.0)
                sparsity_db_size_increase_GB        = maximum_db_size_GB * sparsity_factor
                cost_per_byte_iota                  = (TOTAL_SUPPLY / float(db_size_bytes)) * sparsity_factor
                sparsity_distribution_costs_iota    = cost_per_byte_iota * db_size_bytes 
                sparsity_distribution_costs_dollar  = (sparsity_distribution_costs_iota / 1000000.0) * PRICE_PER_MIOTA_DOLLAR
                print()
                print("Maximum database size: %0.2fGB, fund sparsity percentage: %0.1f%%, database size increase: %0.2fGB" % (maximum_db_size_GB, fund_sparsity_percentage, maximum_db_size_GB*sparsity_factor))
                print("Costs for the fund sparsity (%0.2f GB database increase): %0.2fMi, %s (at %0.2f$/Mi price)" % (sparsity_db_size_increase_GB, sparsity_distribution_costs_iota / 1000000.0, getDollarFormat(sparsity_distribution_costs_dollar), PRICE_PER_MIOTA_DOLLAR))

    vbytes_outputs = outputs.GetExampleOutputs(output_size_max         = output_size_max,
                                               native_token_count_max  = NATIVE_TOKEN_COUNT_MAX,
                                               weight_key              = WEIGHT_KEY,
                                               weight_data             = WEIGHT_DATA,
                                               metadata_length_max     = METADATA_LENGTH_MAX,
                                              )

    for i, vbytes in enumerate(vbytes_outputs):
        if print_summary:
            print()
            vbytes.summary()

        if not create_plots:
            continue
        
        plot_lines  = []
        sub_plots   = []
    
        sub_plots.append(plot.Subplot(row_index=vbytes.plot_row_index, column_index=vbytes.plot_column_index, x_label='assumed fund sparsity percentage',   y1_label='cost per %s [MIOTA]' % (vbytes.name_plot)))
        sub_plots.append(plot.Subplot(row_index=vbytes.plot_row_index+1, column_index=vbytes.plot_column_index, x_label='assumed fund sparsity percentage', y1_label='actual max. DB size at\n 100% fund sparsity perc. [GB]', legend_y1_loc='upper right'))

        for maximum_db_size_GB in MAXIMUM_DB_SIZES_GB:
            
            x  = []
            y1 = []
            y2 = []
            for fund_sparsity_percentage in FUND_SPARSITY_PERCENTAGES:
                db_size_bytes           = maximum_db_size_GB * 1e9
                sparsity_factor         = (fund_sparsity_percentage / 100.0)
                cost_per_byte_iota      = int((TOTAL_SUPPLY / float(db_size_bytes)) * sparsity_factor)

                cost_per_output_iota    = cost_per_byte_iota * vbytes.vBytesMax()
                cost_per_output_dollar  = (cost_per_output_iota / 1000000.0) * PRICE_PER_MIOTA_DOLLAR
                
                total_outputs_size_GB   = (int(TOTAL_SUPPLY / cost_per_output_iota) * vbytes.byteSizeMax()) / 1e9

                x.append(fund_sparsity_percentage)
                y1.append(cost_per_output_iota / float(1e6))
                y2.append(total_outputs_size_GB)
                if print_summary:
                    print("Costs per %-25s     (%6s fund sparsity, Max %7sGB DB, Actual %7sGB DB): %11sMi, %11s$ (at %0.2f$/Mi price), VByteCost: %d" % (vbytes.name, "%0.1f%%" % fund_sparsity_percentage, "%0.2f" % maximum_db_size_GB, "%0.2f" % total_outputs_size_GB, "%4.6f" % (cost_per_output_iota / 1000000.0), "%4.6f" % cost_per_output_dollar, PRICE_PER_MIOTA_DOLLAR, cost_per_byte_iota))
                
            plot_lines.append(plot.PlotLine(subplot_nr=0, x=x, y=y1, name="%0.2f GB" % (maximum_db_size_GB)))
            plot_lines.append(plot.PlotLine(subplot_nr=1, x=x, y=y2, name="%0.2f GB" % (maximum_db_size_GB)))

        plot.plot(sub_plots, plot_lines, show_plot=show_plots, file_path="plots/deposit_miota_%s.jpg" % (vbytes.name.replace(" ", "_")))
    return vbytes_outputs

#===============================================================================
if __name__ == '__main__':
    calculateDustProtectionCostsStardust(print_summary=True, create_plots=True, show_plots=True)
