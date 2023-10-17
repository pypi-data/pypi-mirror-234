import json
import MetaTrader5 as mt5
from database_ex_sar_shane_forex_next3 import Database
from decimal import Decimal

class GAP:
  
  def __init__(self):
       fileObject = open("login.json", "r")
       jsonContent = fileObject.read()
       aList = json.loads(jsonContent)
       
       self.login = int (aList['login'])
       self.Server = aList['Server'] 
       self.Password = aList['Password'] 
       self.symbol_EURUSD = aList['symbol_EURUSD'] 
       self.decimal_sambol = int (aList['decimal_sambol'] )
    
  def candelstate(listOpen , listClose):
         candel_open = listOpen
         candel_close = listClose
        #  candel_open = Candel.decimal(candel_open)
        #  candel_close = Candel.decimal(candel_close)
        #  print("candel_open" , candel_open) 
        #  print("candel_close" , candel_close) 
         if candel_open > candel_close:
             candel_state = "red"
     
         elif candel_open < candel_close:
             candel_state = "green"
                 
         elif candel_open == candel_close:
             candel_state = "doji"
     
         return candel_state     
  
  
  def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  

  def gap_pip(decimal_sambol , a , b):
     
       x = 10
       for i in range(decimal_sambol):
            x = x * 10

       a = a * x
       b = b * x
      #  print("a:" , a)
      #  print("b:" , b)
       a = int (a)
       b = int (b)
       c = b - a
       c = int(c)
       c = abs(c)
       c = c / 10
       c = int(c)
      #  print("a:" , a)
      #  print("b:" , b)
      #  print("c:" , c)

       return c 

  def gap(candel_num , decimal_sambol , symbol_EURUSD):
        
        gap_point = []
        gap_amount = []
        gap_word = []
        gap_pip_amount = []
        
        # print("candel_num:" , candel_num)
        # print("decimal_sambol:" , decimal_sambol)

        lab = Database.select_table_One(candel_num)

        candel_color = lab[0][7]
        point_patern = lab[0][3]

        timepstamps = lab[0][19] 
        timepstamps = json.loads(timepstamps)
        # print("timepstamp:" , timepstamps)

        candel_color = json.loads(candel_color)
      #   print("candel_color:" , candel_color[0])
        candel_colors = ""

        for index in range(1 , 5):
              print("")
            #   print("index:" , index + 1)
              
              timepstamp_one = int (timepstamps[index])
              data_patern = mt5.copy_rates_from(symbol_EURUSD, mt5.TIMEFRAME_M15, timepstamp_one , 1)
              data_next_candel = mt5.copy_rates_from(symbol_EURUSD, mt5.TIMEFRAME_M15, timepstamp_one + 900 , 1)

            #   print("data_patern:" , data_patern)
            #   print("data_1mine:" , data_next_candel)

              can_close = data_patern[0][4]
              can_close = GAP.decimal(can_close , GAP().decimal_sambol)
              can_close = float(can_close)
              

              can_open = data_patern[0][1]
              can_open = GAP.decimal(can_open , GAP().decimal_sambol)
              can_open = float(can_open)

              candel_colors = GAP.candelstate(can_open , can_close)
            #   print("candel_colors:" , candel_colors)

              can_open_next = data_next_candel[0][1]
              can_open_next = GAP.decimal(can_open_next , GAP().decimal_sambol)
              can_open_next = float(can_open_next)
              

            #   print("can_close:" , can_close)
            #   print("can_open:" , can_open)
            #   print("can_open_next:" , can_open_next)

              if can_close != can_open_next:
                    
                    
                    if (candel_colors == "green" or candel_colors == "doji" )and can_close > can_open_next:
                          
                          if index == 2 or index == 4:
                               gap_point.append(index + 1)
                               gap_amount.append(can_open_next)
                               output_pip = GAP.gap_pip(decimal_sambol , can_open_next , can_close)
                               gap_pip_amount.append(output_pip)
                               gap_word.append("gap invers")

                          # print("gap_point:" , gap_point)
                          # print("gap_amount:" , gap_amount)
                          # print("gap_pip_amount:" , gap_pip_amount)
                          # print("gap invers")

                    elif (candel_colors == "green" or candel_colors == "doji" )and can_close < can_open_next:
                          
                          if index == 2 or index == 4:
                               gap_point.append(index + 1)
                               gap_amount.append(can_open_next)
                               output_pip = GAP.gap_pip(decimal_sambol , can_open_next , can_close)
                               gap_pip_amount.append(output_pip)
                               gap_word.append("gap")

                          # print("gap_point:" , gap_point)
                          # print("gap_amount:" , gap_amount)
                          # print("gap_pip_amount:" , gap_pip_amount)
                          # print("gap")

                    elif (candel_colors == "red" or candel_colors == "doji" )and can_close > can_open_next:
                        
                          if index == 2 or index == 4:
                            gap_point.append(index + 1)
                            gap_amount.append(can_open_next)
                            output_pip = GAP.gap_pip(decimal_sambol , can_open_next , can_close)
                            gap_pip_amount.append(output_pip)
                            gap_word.append("gap")

                          # print("gap_point:" , gap_point)
                          # print("gap_amount:" , gap_amount)
                          # print("gap_pip_amount:" , gap_pip_amount)
                          # print("gap")

                    elif (candel_colors == "red" or candel_colors == "doji") and can_close < can_open_next:
                         
                          if index == 2 or index == 4:
                              gap_point.append(index + 1)
                              gap_amount.append(can_open_next)
                              output_pip = GAP.gap_pip(decimal_sambol , can_open_next , can_close)
                              gap_pip_amount.append(output_pip)
                              gap_word.append("gap invers")
                          # print("gap_point:" , gap_point)
                          # print("gap_amount:" , gap_amount)
                          # print("gap_pip_amount:" , gap_pip_amount)
                           
                          # print("gap invers:")          
     

        gap_point = json.dumps(gap_point)
        gap_amount= json.dumps(gap_amount)
        gap_pip_amount = json.dumps(gap_pip_amount)
        gap_word = json.dumps(gap_word)

        print("gap_point:" , gap_point)
        print("gap_amount:" , gap_amount)
        print("gap_pip_amount:" , gap_pip_amount)
        print("gap_word:" , gap_word) 

        Database.update_table_gap( gap_point , gap_amount , gap_pip_amount , gap_word , candel_num)

        return True

