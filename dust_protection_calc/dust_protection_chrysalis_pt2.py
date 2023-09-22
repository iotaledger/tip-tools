# -*- coding: utf-8 -*-
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

#===============================================================================
def getDollarFormat(value):
    return "%s$" % (locale.currency(value, symbol=False, grouping=True))

#===============================================================================
def getDatabaseSize(price_per_miota_dollar, attack_costs_miota):
    miota_price_per_allowance   = 1.0
    dust_outputs_per_allowance  = 10
    bytes_per_output            = 236
    database_size_bytes         = (attack_costs_miota / miota_price_per_allowance) * dust_outputs_per_allowance * bytes_per_output
    database_size_gigabyte      = database_size_bytes / (1000 * 1000 * 1000)
    attack_costs_dollar         = price_per_miota_dollar * attack_costs_miota
    print("AttackCosts: %11s MIOTA (%s), Database Size: %0.2fGB" % ("%0.2f" % attack_costs_miota, getDollarFormat(attack_costs_dollar), database_size_gigabyte))

#===============================================================================
if __name__ == '__main__':
    price_per_miota_dollar      = 1.23
    
    attack_costs_miota          = 1 * 1000.0 * 1000.0               # 1 Ti
    getDatabaseSize(price_per_miota_dollar, attack_costs_miota)

    attack_costs_dollar         = 1000000
    attack_costs_miota          = (attack_costs_dollar / price_per_miota_dollar) 
    getDatabaseSize(price_per_miota_dollar, attack_costs_miota)
