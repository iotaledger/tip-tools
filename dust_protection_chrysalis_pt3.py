# -*- coding: utf-8 -*-
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
import outputs, plot

#===============================================================================
def getDollarFormat(value):
    return "%s$" % (locale.currency(value, symbol=False, grouping=True))

#===============================================================================
if __name__ == '__main__':

    total_supply                = 2779530283277761
    price_per_miota_dollar      = 1.23

    msg_size_max                = 32768
    
    weight_key                  = 10.0
    weight_data                 = 1.0

    maximum_db_sizes_GB         = [50.0, 100.0, 150.0, 200.0, 400.0, 1000.0]
    fund_sparsity_percentages   = [20.0, 100.0]

    print("Current market cap: %s" % (getDollarFormat((total_supply / 1000000.0) * price_per_miota_dollar)))
    
    payload_size_max    = outputs.getPayloadSizeMax(message_size_max=msg_size_max)
    output_size_max     = outputs.getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)
    
    print("MessageSizeMax: %d" % (msg_size_max))
    print("PayloadSizeMax: %d" % (payload_size_max))
    print("OutputSizeMax:  %d" % (output_size_max))

    for maximum_db_size_GB in maximum_db_sizes_GB:
        for fund_sparsity_percentage in fund_sparsity_percentages:
            db_size_bytes                       = maximum_db_size_GB * 1e9
            sparsity_factor                     = (fund_sparsity_percentage / 100.0)
            sparsity_db_size_increase_GB        = maximum_db_size_GB * sparsity_factor
            cost_per_byte_iota                  = (total_supply / float(db_size_bytes)) * sparsity_factor
            sparsity_distribution_costs_iota    = cost_per_byte_iota * db_size_bytes
            sparsity_distribution_costs_dollar  = (sparsity_distribution_costs_iota / 1000000.0) * price_per_miota_dollar
            print()
            print("Maximum database size: %0.2fGB, fund sparsity percentage: %0.1f%%, database size increase: %0.2fGB" % (maximum_db_size_GB, fund_sparsity_percentage, maximum_db_size_GB*sparsity_factor))
            print("Costs for the fund sparsity (%0.2f GB database increase): %0.2fMi, %s (at %0.2f$/Mi price)" % (sparsity_db_size_increase_GB, sparsity_distribution_costs_iota / 1000000.0, getDollarFormat(sparsity_distribution_costs_dollar), price_per_miota_dollar))

    for i, vbytes in enumerate([
        outputs.getVBytes_Byte(),
        outputs.getVBytes_SimpleOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name=None,
            output_size_max=output_size_max,
        ), 
        outputs.getVBytes_ExtendedOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="min functionality",
            output_size_max=output_size_max,
            native_token_count=0, 
            sender_block=False,
            return_amount_block=False,
            timelock_ms_idx_block=False,
            timelock_unix_block=False,
            expiration_ms_idx_block=False,
            expiration_unix_block=False,
            indexation_block=False,
            metadata_block=False,
        ),
        outputs.getVBytes_ExtendedOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="max functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            sender_block=True,
            return_amount_block=True,
            timelock_ms_idx_block=True,
            timelock_unix_block=True,
            expiration_ms_idx_block=True,
            expiration_unix_block=True,
            indexation_block=True,
            metadata_block=True,
        ),
        outputs.getVBytes_AliasOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="min functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            metadata_block=False),
        outputs.getVBytes_AliasOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="max functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            metadata_block=True),
        outputs.getVBytes_FoundryOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="min functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            metadata_block=False),
        outputs.getVBytes_FoundryOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="max functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            metadata_block=True),
        outputs.getVBytes_NFTOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="min functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            sender_block=False,
            issuer_block=False,
            return_amount_block=False,
            timelock_ms_idx_block=False,
            timelock_unix_block=False,
            expiration_ms_idx_block=False,
            expiration_unix_block=False,
            indexation_block=False,
            metadata_block=False),
        outputs.getVBytes_NFTOutput(
            weight_key=weight_key,
            weight_data=weight_data,
            additional_name="max functionality",
            output_size_max=output_size_max,
            native_token_count=0,
            sender_block=True,
            issuer_block=True,
            return_amount_block=True,
            timelock_ms_idx_block=True,
            timelock_unix_block=True,
            expiration_ms_idx_block=True,
            expiration_unix_block=True,
            indexation_block=True,
            metadata_block=True)
    ]):
        print()
        vbytes.summary()

        plot_lines  = []
        sub_plots   = []
    
        sub_plots.append(plot.Subplot(row_index=vbytes.plot_row_index, column_index=vbytes.plot_column_index, x_label='fund sparsity percentage', y_label='cost per %s [MIOTA]' % (vbytes.name)))

        for maximum_db_size_GB in maximum_db_sizes_GB:
            
            x = []
            y = []
            for fund_sparsity_percentage in fund_sparsity_percentages:
                db_size_bytes           = maximum_db_size_GB * 1e9
                sparsity_factor         = (fund_sparsity_percentage / 100.0)
                cost_per_byte_iota      = (total_supply / float(db_size_bytes)) * sparsity_factor

                cost_per_output_iota    = cost_per_byte_iota * vbytes.vBytesMax()
                cost_per_output_dollar  = (cost_per_output_iota / 1000000.0) * price_per_miota_dollar

                x.append(fund_sparsity_percentage)
                y.append(cost_per_output_iota / float(1e6))
                print("Costs per %-25s              (%6s fund sparsity, Max %7sGB DB): %11sMi, %11s$ (at %0.2f$/Mi price)" % (vbytes.name, "%0.1f%%" % fund_sparsity_percentage, "%0.2f" % maximum_db_size_GB, "%4.6f" % (cost_per_output_iota / 1000000.0), "%4.6f" % cost_per_output_dollar,      price_per_miota_dollar))
                
            plot_lines.append(plot.PlotLine(subplot_nr=0, x=x, y=y, name="%0.2f GB" % (maximum_db_size_GB)))

        plot.plot(sub_plots, plot_lines, show_plot=True, file_path="plots/deposit_miota_%s.jpg" % (vbytes.name.replace(" ", "_")))
