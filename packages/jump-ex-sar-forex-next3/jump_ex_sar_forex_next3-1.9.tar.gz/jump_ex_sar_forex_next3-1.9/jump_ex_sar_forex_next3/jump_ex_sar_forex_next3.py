import MetaTrader5 as mt5
import json

from decimal import Decimal

from database_ex_forex_next3 import Database


class Jump:

    def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        rounded_num = float(rounded_num)
        return rounded_num  

    def decimal_mov(decimal_sambol):
        x = 1
        for i in range(decimal_sambol):
           x = x * 10

        return x    
    
    def avg_close_open(symbol_EURUSD , decimal_sambol , factor):
     
     
     
     timecandel_1mine = mt5.copy_rates_from_pos(symbol_EURUSD, mt5.TIMEFRAME_M15, 0, 1000)

     difference_candels = []
     for candel_difference in timecandel_1mine:
            
           point_close = candel_difference[4]
           point_close = Jump.decimal(point_close , decimal_sambol)

           point_open = candel_difference[1]
           point_open = Jump.decimal(point_open , decimal_sambol)

           difference = abs(point_close - point_open)
           difference = difference * Jump.decimal_mov(decimal_sambol)
           difference = int(difference)
           difference_candels.append(difference)
     
     avg = sum(difference_candels)/len(difference_candels)
     avg = factor * avg
     avg = round(avg , 1)
     return avg
   
    def avg_jump_patern (candel_num , symbol_EURUSD , decimal_sambol , factor ):
       
       lab = Database.select_table_One(candel_num)

       timepstamp = lab[0][19] 
       timepstamp = json.loads(timepstamp)

       out_jump = True

    #    print("timepstamp:" , timepstamp)

       timestamp_start = int( timepstamp[0] )
       timestamp_end = int( timepstamp[5] )
    #    print("timepstamp:" , timepstamp)

       racive_15mine = mt5.copy_rates_range(symbol_EURUSD, mt5.TIMEFRAME_M15, timestamp_start, timestamp_end)

    #    print("racive:" , racive_15mine)

       difference_candels = []
       for candel_difference in racive_15mine:
            
           point_close = candel_difference[4]
           point_close = Jump.decimal(point_close , decimal_sambol)

           point_open = candel_difference[1]
           point_open = Jump.decimal(point_open , decimal_sambol)

           difference = abs(point_close - point_open)

        #    print("difference:" , difference)  

           difference = difference * Jump.decimal_mov(decimal_sambol)
           difference = round(difference , 2)
            
           difference = int(difference)
           difference_candels.append(difference)

    #    print("difference_candels:" , difference_candels)   

       jump_factor = Jump.avg_close_open(symbol_EURUSD , decimal_sambol , factor)


       for index in difference_candels:
          
          if index > jump_factor:
            #  print("11111111111111111111")
             out_jump = False
             Database.update_jump_patern( "false" , candel_num)
             break

    #    print("jump_factor:" , jump_factor)
    #    print("out_jump:" , out_jump)

       if out_jump == True:
          Database.update_jump_patern("true" , candel_num)

       return out_jump   
    