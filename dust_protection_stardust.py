# -*- coding: utf-8 -*-
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
import outputs, plot

#===============================================================================
def getDollarFormat(value):
    return "%s$" % (locale.currency(value, symbol=False, grouping=True))

#===============================================================================
if __name__ == '__main__':

    TOTAL_SUPPLY                = 2779530283277761
    PRICE_PER_MIOTA_DOLLAR      = 1.35

    MSG_SIZE_MAX                = 32768
    
    WEIGHT_KEY                  = 10.0
    WEIGHT_DATA                 = 1.0

    MAXIMUM_DB_SIZES_GB         = [500.0, 1000.0, 2000.0]
    FUND_SPARSITY_PERCENTAGES   = [20.0, 50.0]

    print("Current market cap: %s" % (getDollarFormat((TOTAL_SUPPLY / 1000000.0) * PRICE_PER_MIOTA_DOLLAR)))
    
    payload_size_max    = outputs.getPayloadSizeMax(message_size_max=MSG_SIZE_MAX)
    output_size_max     = outputs.getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)
    
    print("MessageSizeMax: %d" % (MSG_SIZE_MAX))
    print("PayloadSizeMax: %d" % (payload_size_max))
    print("OutputSizeMax:  %d" % (output_size_max))

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

    for i, vbytes in enumerate([
        outputs.getVBytes_SigLockedSingleOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = None,
            output_size_max                         = output_size_max,
        ), 
        outputs.getVBytes_ExtendedOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "min functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = True,
            native_token_count                      = 0, 
        ),
        outputs.getVBytes_ExtendedOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "1000 byte metadata",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 0,
            dust_deposit_return_unlock_condition    = False,
            timelock_unlock_condition               = False,
            expiration_unlock_condition             = False,
            sender_block                            = False,
            tag_block                               = False,
            metadata_block                          = True,
            metadata_data_length                    = 1000,
        ),
        outputs.getVBytes_ExtendedOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "1 native token, dust return",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 1,
            dust_deposit_return_unlock_condition    = True,
            timelock_unlock_condition               = False,
            expiration_unlock_condition             = False,
            sender_block                            = False,
            tag_block                               = False,
            metadata_block                          = False,
            metadata_data_length                    = None,
        ),
        outputs.getVBytes_ExtendedOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "max functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 0,
        ),
        outputs.getVBytes_AliasOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "min functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = True,
            native_token_count                      = 0
        ),
        outputs.getVBytes_AliasOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "max functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 0,
        ),
        outputs.getVBytes_FoundryOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "min functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = True,
            native_token_count                      = 0,
        ),
        outputs.getVBytes_FoundryOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "max functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 0,
        ),
        outputs.getVBytes_NFTOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "min functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = True,
            native_token_count                      = 0,
        ),
        outputs.getVBytes_NFTOutput(
            weight_key                              = WEIGHT_KEY,
            weight_data                             = WEIGHT_DATA,
            additional_name                         = "max functionality",
            output_size_max                         = output_size_max,
            required_fields_only                    = False,
            native_token_count                      = 0
        ),
    ]):
        print()
        vbytes.summary()

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
                print("Costs per %-25s     (%6s fund sparsity, Max %7sGB DB, Actual %7sGB DB): %11sMi, %11s$ (at %0.2f$/Mi price), VByteCost: %d" % (vbytes.name, "%0.1f%%" % fund_sparsity_percentage, "%0.2f" % maximum_db_size_GB, "%0.2f" % total_outputs_size_GB, "%4.6f" % (cost_per_output_iota / 1000000.0), "%4.6f" % cost_per_output_dollar, PRICE_PER_MIOTA_DOLLAR, cost_per_byte_iota))
                
            plot_lines.append(plot.PlotLine(subplot_nr=0, x=x, y=y1, name="%0.2f GB" % (maximum_db_size_GB)))
            plot_lines.append(plot.PlotLine(subplot_nr=1, x=x, y=y2, name="%0.2f GB" % (maximum_db_size_GB)))

        plot.plot(sub_plots, plot_lines, show_plot=True, file_path="plots/deposit_miota_%s.jpg" % (vbytes.name.replace(" ", "_")))
