import MetaTrader5 as mt5
import json
import pandas as pd
import time

from line_ex_sar_forex_next3 import LINE
from buy_sell_ex_forex_next3 import BUY_SELL
from database_ex_forex_next3 import Database
from decimal import Decimal


                       
class Pullback:
 
 def __init__(self , symbol_EURUSD , decimal_sambol ):
      
      self.symbol_EURUSD = symbol_EURUSD
      self.decimal_sambol = decimal_sambol

 def __str__(self):
      return f"({self.symbol_EURUSD },{self.decimal_sambol })"

 def decimal(num , decimal_sambol):
        telo = '0.0'
        for i in range(decimal_sambol - 2):  
          telo = telo + "0"
        telo = telo + "1" 
        telo = float (telo)
        decimal_num = Decimal(str(num))
        rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
        return rounded_num  


 def pullback_1_old (self , tel , status_tel  , lot):
     
   telo = '0.0'
   for i in range(self.decimal_sambol - 2):  
      telo = telo + "0"
      
   telo = telo + f"{tel}"  
   telo = float (telo)
#    print("telerance:" , telo) 

   data_all = Database.select_table_All()
   select_all_len = len(data_all)
   if select_all_len > 0:
     #  print("select_all_len:" , select_all_len)
      
      # print("rec:" , rec)

      for index in range(select_all_len - 1 , select_all_len):
      # for index in range(11 , 12):
                          
     #     print("index:" , index)
         lab = data_all[index]
     #     print("lab:" , lab)
         candel_num = lab[1]
         type = lab[2]
         point_patern = lab[3]
         timepstamp = lab[19] 
         time_start_search = lab[17]
         status = lab[15]
         chek = lab[16]
         line_POS = lab[22]
         Trust_patern = lab[25]
         Trust_patern_full = lab[26]
         Layout_patern = lab [27]
         Jump_patern = lab [28]
            
         line_POS = int(line_POS)
         candel_num = int(candel_num)
         exit = 0
         
         rec = data_all[select_all_len - 1]
        #  print("rec:" , rec)

         time_start_search = int(time_start_search)
        #  print("lab:" , lab)
        #  print("status:" , status)
        #  print("time_start_search:" , time_start_search)
        #  print("point_patern:" , point_patern)
        #  print("type:" , type)
        #  print("candel_num:" , candel_num)
        #  print("timepstamp:" , timepstamp)


         point_patern = json.loads(point_patern)
         timepstamp = json.loads(timepstamp)
         timepstamp_3 = json.loads(timepstamp[5])

     #     print("timepstamp_3:" , timepstamp_3)

         timepstamp_old = int(timepstamp_3) + 900
     #     print("timepstamp_old:" , timepstamp_old)
         

         if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
            print("Pulback_old 1111111111111111111111111111111111111111111111111111111111111111111111111111111111")
               
            inputs_candels = mt5.copy_rates_range(self.symbol_EURUSD, mt5.TIMEFRAME_M1, timepstamp_old, time_start_search)
            # print("inputs_candels:" , inputs_candels)


            for candel_recive in inputs_candels:
              #  print("candel_recive:" , candel_recive)
          
               point_open = candel_recive[1]
               point_open = Pullback.decimal(point_open , self.decimal_sambol)
               point_open = float(point_open)
              #  print ("point_open:" , point_open)

               point_close = candel_recive[4]
               point_close = Pullback.decimal(point_close , self.decimal_sambol)
               point_close = float(point_close)
              #  print ("point_close:" , point_close)
       
               point_high = candel_recive[2]
               point_high = Pullback.decimal(point_high , self.decimal_sambol)
               point_high = float(point_high)
              #  print ("point_high:" , point_high)
       
               point_low = candel_recive[3]
               point_low = Pullback.decimal(point_low , self.decimal_sambol)
               point_low = float(point_low)
              #  print ("point_low:" , point_low)

               point_timepstamp =  candel_recive[0]
               point_timepstamp = int(point_timepstamp)
              
               # print ("point_timepstamp:" , point_timepstamp)
               # print("point_timepstamp:" , pd.to_datetime( point_timepstamp , unit='s'))


               candel_statess = ''
               if point_open > point_close:
                 candel_statess = "red"
               elif point_open < point_close:
                 candel_statess = "green"
               elif point_open == point_close:
                 candel_statess = "doji"  
       
              #  print("candel_state:" , candel_statess)
       
               # cal_point = LINE.cal_point_line(1 , timestamp_pulback)
               # print("cal_point:" , cal_point)
               cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , point_timepstamp )
              #  print("cal_line_rec:" , cal_line_rec)

               cal_line = cal_line_rec[0]
              #  print("cal_line:" , cal_line)
               list_cal_line = cal_line

               cal_list_line = cal_line_rec[1]
              #  print("cal_list_line:" , cal_list_line)

               if line_POS != 0:
                                    
                   xxx = line_POS - 1
                   
                   cal_line = cal_line[xxx]
                   cal_line = [cal_line]

               # print("cal_line:" , cal_line)   

               telo_add_high = point_high + telo
               telo_sub_high = point_high - telo
               telo_add_high = Pullback.decimal(telo_add_high , self.decimal_sambol)
               telo_sub_high = Pullback.decimal(telo_sub_high , self.decimal_sambol)
               telo_add_high = float(telo_add_high)
               telo_sub_high = float(telo_sub_high)

               telo_add_low = point_low + telo
               telo_sub_low = point_low - telo
               telo_add_low = Pullback.decimal(telo_add_low , self.decimal_sambol)
               telo_sub_low = Pullback.decimal(telo_sub_low , self.decimal_sambol)
               telo_add_low = float(telo_add_low)
               telo_sub_low = float(telo_sub_low)


               # print("telo_add_high:" , telo_add_high)
               # print("telo_sub_high:" , telo_sub_high)

               # print("telo_add_low:" , telo_add_low)
               # print("telo_sub_low:" , telo_sub_low)

               a = 1
               for i in range(self.decimal_sambol + 1):
                     a = a * 10
               
               cal_price_candel = abs( int(point_open * a) - int(point_close * a) )
               cal_price_candel = int (cal_price_candel / 10)
               # print("cal_price_candel:" , cal_price_candel)


               for line , gap_point in enumerate(cal_line): 
                     
                    #  print("gap_point:" , gap_point)
                    #  print("point_low:" , point_low)
                    #  print("point_high:" , point_high)
                    #  print("point_close:" , point_close)
                    #  print("point_open:" , point_open)
                    #  print("point_timepstamp:" , pd.to_datetime( point_timepstamp , unit='s'))
                    #  print("line_POS:" , line_POS)
                    #  print("")
                     
                     cal_point = float (gap_point)

                     rec = Database.select_table_One(candel_num)
                     chek = rec[0][16]
                    #  print("rec:" , rec)

                     line_pullback = line + 1
                     

                     if (point_close != point_high and point_open != point_low and candel_statess == "green") or (point_close != point_low  and point_open != point_high and candel_statess == "red"):
                         
                         
                         # print("cal_point:" , cal_point)
                         # print("tel:" , tel)
                         
                         if point_high == cal_point and type == "Head_Shoulder" and chek == "false":
                                #  print("")
                                 print("point_high:" , point_high)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line_pullback)
                                 print("patern: up  11111111111111111111111111111111111111111111")
                                 print("pullback_MMMMMMMMMMM")
                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_high )
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     if line_POS == line_pullback or line_POS == 0:
                                          # print("shakhes: True" )
                                          rec_pos = BUY_SELL.pos_sell(point_high , shakhes , lot , self.symbol_EURUSD , commands)
                                          execution = rec_pos.comment
                                          if execution == 'Request executed':
                                                 ticket =  rec_pos.order
                                                 # print("rec_pos:" , rec_pos)
                                                 print("ticket:" , ticket)

                                     else :
                                               execution = "The line is not equal"         
 
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{point_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(High:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                
                                 if line_POS == 0 or line_POS == line_pullback:
                                           
                                        Database.update_table_chek(point_high , point_timepstamp , command , "true" , ticket , line_pullback , candel_num)               

                                 else:
                                        Database.update_table_chek(point_high , point_timepstamp , command , "false" , ticket , line_POS , candel_num)
                                                          
                                 exit = 1
                                 break

                         elif point_low == cal_point and type == "R_Head_Shoulder" and chek == "false":
                                 print("point_timepstamp:" , pd.to_datetime( point_timepstamp , unit='s'))
                                 print("point_low:" , point_low)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line_pullback)
                                 print("patern: down  11111111111111111111111111111111111111111111")
                                 print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_low)
                                 status_trade = shakhes[1]
                                #  print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                #  print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     if line_POS == line_pullback or line_POS == 0:
                                    #  print("shakhes: True" )
                                         rec_pos = BUY_SELL.pos_buy(point_low , shakhes , lot , self.symbol_EURUSD , commands)
                                         execution = rec_pos.comment
                                         if execution == 'Request executed':
                                                ticket =  rec_pos.order
                                                # print("rec_pos:" , rec_pos)
                                                # print("ticket:" , ticket)

                                 else :
                                          execution = "The line is not equal"       
                                     
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{point_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                 if line_POS == 0 or line_POS == line_pullback:
                                           
                                        Database.update_table_chek(point_low , point_timepstamp , command , "true" , ticket , line_pullback , candel_num)               
                                 else:
                                        Database.update_table_chek(point_low , point_timepstamp , command , "false" , ticket , line_POS , candel_num)
                                        
                                 exit = 1
                                 break
  
                         elif telo_add_high == cal_point and cal_price_candel > tel  and type == "Head_Shoulder" and  status_tel == True and chek == "false":
                                 print("point_high:" , point_high)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("patern: up  22222222222222222222222222222222222222222222") 
                                 print("pullback_MMMMMMMMMMM")

                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_sell(telo_add_high , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            # print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{telo_add_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_add_high:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                 Database.update_table_chek(telo_add_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                 exit = 1
                                 break
                         
                         elif telo_sub_high == cal_point and cal_price_candel > tel and type == "Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_high:" , point_high)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("patern: up  33333333333333333333333333333333333333333333")   
                                 print("pullback_MMMMMMMMMMM")     
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_sell( telo_sub_high , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            # print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{telo_sub_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_sub_high:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                 Database.update_table_chek(telo_sub_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                 exit = 1
                                 break
                    
                         elif telo_sub_low == cal_point and cal_price_candel > tel and type == "R_Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_low:" , point_low)
                                 print("telo_sub_low:" , telo_sub_low)  
                                 print("candel_color:" , candel_statess) 
                                 print ("line:" , line + 1)
                                 print("cal_price_candel:" , cal_price_candel)
                                 print("patern: down  22222222222222222222222222222222222222222222")
                                 print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_buy(telo_sub_low , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            # print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{telo_sub_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_sub_low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                 Database.update_table_chek(telo_sub_low , point_timepstamp , command , "true" , ticket , candel_num)    
                                 exit = 1
                                 break
                         
                         elif telo_add_low == cal_point and cal_price_candel > tel and type == "R_Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_low:" , point_low)
                                 print("telo_add_low:" , telo_add_low)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("cal_price_candel:" , cal_price_candel)
                                 print("patern: down  33333333333333333333333333333333333333333333")
                                 print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_buy(telo_add_low , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            # print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{1})'+ " _ " + "(Point7:" + f'{telo_add_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_add_low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                 Database.update_table_chek(telo_add_low , point_timepstamp , command , "true" , ticket , candel_num)    
                                 exit = 1
                                 break
              #  print("")

               if exit == 1:
                  break

 def pullback_1_now (self , tel , status_tel , timestamp_pulback , lot):
     
   telo = '0.0'
   for i in range(self.decimal_sambol - 2):  
      telo = telo + "0"
      
   telo = telo + f"{tel}"  
   telo = float (telo)
#    print("telerance:" , telo) 

   data_all = Database.select_table_All()
   select_all_len = len(data_all)
   if select_all_len > 0:
     #  print("select_all_len:" , select_all_len)
      rec = data_all[select_all_len - 1]
      # print("rec:" , rec)

      for index in range(select_all_len):
                          
     #     print("index:" , index)
         lab = data_all[index]
         candel_num = lab[1]
         type = lab[2]
         point_patern = lab[3]
         timepstamp = lab[19] 
         time_start_search = lab[17]
         status = lab[15]
         chek = lab[16]
         line_POS = lab[22]
         Trust_patern = lab[25]
         Trust_patern_full = lab[26]
         Layout_patern = lab [27]
         Jump_patern = lab [28]
            
         line_POS = int(line_POS)

         exit = 0


         time_start_search = int(time_start_search)
     #     print("lab:" , lab)
     #     print("status:" , status)
     #     print("time_start_search:" , time_start_search)
     #     print("point_patern:" , point_patern)
     #     print("type:" , type)
     #     print("candel_num:" , candel_num)
     #     print("timepstamp:" , timepstamp)


         point_patern = json.loads(point_patern)
         timepstamp = json.loads(timepstamp)
         timepstamp_3 = json.loads(timepstamp[3])

     #     print("timepstamp_3:" , timepstamp_3)

         timepstamp_old = int(timepstamp_3) + 900
     #     print("timepstamp_old:" , timepstamp_old)
         

         if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
            print("Pulback_now 111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
               
            inputs_candels = mt5.copy_rates_from(self.symbol_EURUSD, mt5.TIMEFRAME_M1,  timestamp_pulback , 1)

            # print("inputs_candels:" , inputs_candels)


            for candel_recive in inputs_candels:
               # print("candel_recive:" , candel_recive)
          
               point_open = candel_recive[1]
               point_open = Pullback.decimal(point_open , self.decimal_sambol)
               point_open = float(point_open)
               # print ("point_open:" , point_open)

               point_close = candel_recive[4]
               point_close = Pullback.decimal(point_close , self.decimal_sambol)
               point_close = float(point_close)
               # print ("point_close:" , point_close)
       
               point_high = candel_recive[2]
               point_high = Pullback.decimal(point_high , self.decimal_sambol)
               point_high = float(point_high)
              #  print ("point_high:" , point_high)
       
               point_low = candel_recive[3]
               point_low = Pullback.decimal(point_low , self.decimal_sambol)
               point_low = float(point_low)
              #  print ("point_low:" , point_low)

               point_timepstamp =  candel_recive[0]
               point_timepstamp = int(point_timepstamp)
               
              #  print ("point_timepstamp:" , point_timepstamp)


               candel_statess = ''
               if point_open > point_close:
                 candel_statess = "red"
               elif point_open < point_close:
                 candel_statess = "green"
               elif point_open == point_close:
                 candel_statess = "doji"  
       
              #  print("candel_state:" , candel_statess)
       
               # cal_point = LINE.cal_point_line(1 , timestamp_pulback)
               # print("cal_point:" , cal_point)
               cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , point_timepstamp )
              #  print("cal_line_rec:" , cal_line_rec)

               cal_line = cal_line_rec[0]
              #  print("cal_line:" , cal_line)

               cal_list_line = cal_line_rec[1]
              #  print("cal_list_line:" , cal_list_line)

               list_cal_line = cal_line

               if line_POS != 0:
                                    
                   xxx = line_POS - 1
                   
                   cal_line = cal_line[xxx]
                   cal_line = [cal_line]


               telo_add_high = point_high + telo
               telo_sub_high = point_high - telo
               telo_add_high = Pullback.decimal(telo_add_high , self.decimal_sambol)
               telo_sub_high = Pullback.decimal(telo_sub_high , self.decimal_sambol)
               telo_add_high = float(telo_add_high)
               telo_sub_high = float(telo_sub_high)

               telo_add_low = point_low + telo
               telo_sub_low = point_low - telo
               telo_add_low = Pullback.decimal(telo_add_low , self.decimal_sambol)
               telo_sub_low = Pullback.decimal(telo_sub_low , self.decimal_sambol)
               telo_add_low = float(telo_add_low)
               telo_sub_low = float(telo_sub_low)


               # print("telo_add_high:" , telo_add_high)
               # print("telo_sub_high:" , telo_sub_high)

               # print("telo_add_low:" , telo_add_low)
               # print("telo_sub_low:" , telo_sub_low)

               a = 1
               for i in range(self.decimal_sambol + 1):
                     a = a * 10
               
               cal_price_candel = abs( int(point_open * a) - int(point_close * a) )
               cal_price_candel = int (cal_price_candel / 10)
               # print("cal_price_candel:" , cal_price_candel)

               
               for line , gap_point in enumerate(cal_line): 
                     
                    #  print("gap_point:" , gap_point)
                     
                     cal_point = float (gap_point)

                     rec = Database.select_table_One(candel_num)
                     chek = rec[0][16]
                    #  print("chek:" , chek)

                     line_pullback = line + 1

                    #  print("gap_point:" , gap_point)
                    #  print("point_low:" , point_low)
                    #  print("point_high:" , point_high)
                    #  print("point_close:" , point_close)
                    #  print("point_open:" , point_open)
                    #  print("point_timepstamp:" , pd.to_datetime( point_timepstamp , unit='s'))
                    #  print("line_POS:" , line_POS)
                    #  print("")
                     

                     if (point_close != point_high and point_open != point_low and candel_statess == "green") or (point_close != point_low  and point_open != point_high and candel_statess == "red"):
                         
                         
                         # print("cal_point:" , cal_point)
                         # print("tel:" , tel)
                         
                         if point_high == cal_point and type == "Head_Shoulder" and chek == "false":
                                #  print("")
                                #  print("point_high:" , point_high)
                                #  print("candel_color:" , candel_statess)
                                #  print ("line:" , line_pullback)
                                #  print("patern: up  11111111111111111111111111111111111111111111")
                                #  print("pullback_MMMMMMMMMMM")
                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_high)
                                 status_trade = shakhes[1]
                                #  print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     
                                     if line_POS == line_pullback or line_POS == 0:
                                    #  print("shakhes: True" )
                                         rec_pos = BUY_SELL.pos_sell(point_high , shakhes , lot , self.symbol_EURUSD , commands)
                                         execution = rec_pos.comment
                                         if execution == 'Request executed':
                                                ticket =  rec_pos.order
                                                # print("rec_pos:" , rec_pos)
                                                # print("ticket:" , ticket)

                                     else:
                                         execution = "The line is not equal"  

                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{point_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(High:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'  
                                
                                 if line_POS == 0 or line_POS == line_pullback:
                                           
                                        Database.update_table_chek(point_high , point_timepstamp , command , "true" , ticket , line_pullback , candel_num)               
                                 else:
                                        Database.update_table_chek(point_high , point_timepstamp , command , "false" , ticket , line_POS , candel_num)
                                                                       
                                 exit = 1
                                 break

                         elif point_low == cal_point and type == "R_Head_Shoulder" and chek == "false":
                                #  print("point_low:" , point_low)
                                #  print("candel_color:" , candel_statess)
                                #  print ("line:" , line_pullback)
                                #  print("patern: down  11111111111111111111111111111111111111111111")
                                #  print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_low)
                                 status_trade = shakhes[1]
                                #  print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                #  print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     if line_POS == line_pullback or line_POS == 0:
                                    #  print("shakhes: True" )
                                         rec_pos = BUY_SELL.pos_buy(point_low , shakhes , lot , self.symbol_EURUSD , commands)
                                         execution = rec_pos.comment
                                         if execution == 'Request executed':
                                                ticket =  rec_pos.order
                                                # print("rec_pos:" , rec_pos)
                                                # print("ticket:" , ticket)
                                     else:
                                         execution = "The line is not equal"           
                                     
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{point_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                 
                                 if line_POS == 0 or line_POS == line_pullback:
                                           
                                        Database.update_table_chek(point_low , point_timepstamp , command , "true" , ticket , line_pullback , candel_num)               
                                 else:
                                        Database.update_table_chek(point_low , point_timepstamp , command , "false" , ticket , line_POS , candel_num)
                                        
                                 exit = 1
                                 break

                         elif telo_add_high == cal_point and cal_price_candel > tel  and type == "Head_Shoulder" and  status_tel == True and chek == "false":
                                 print("point_high:" , point_high)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("patern: up  22222222222222222222222222222222222222222222") 
                                 print("pullback_MMMMMMMMMMM")

                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_sell(telo_add_high , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            # print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{telo_add_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_add_high:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                 Database.update_table_chek(telo_add_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                 exit = 1
                                 break
                         
                         elif telo_sub_high == cal_point and cal_price_candel > tel and type == "Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_high:" , point_high)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("patern: up  33333333333333333333333333333333333333333333")   
                                 print("pullback_MMMMMMMMMMM")     
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_sell( telo_sub_high , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{telo_sub_high})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_sub_high:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                 Database.update_table_chek(telo_sub_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                 exit = 1
                                 break
                         
                         elif telo_sub_low == cal_point and cal_price_candel > tel and type == "R_Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_low:" , point_low)
                                 print("telo_sub_low:" , telo_sub_low)  
                                 print("candel_color:" , candel_statess) 
                                 print ("line:" , line + 1)
                                 print("cal_price_candel:" , cal_price_candel)
                                 print("patern: down  22222222222222222222222222222222222222222222")
                                 print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_buy(telo_sub_low , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{telo_sub_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_sub_low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                 Database.update_table_chek(telo_sub_low , point_timepstamp , command , "true" , ticket , candel_num)    
                                 exit = 1
                                 break
                         
                         elif telo_add_low == cal_point and cal_price_candel > tel and type == "R_Head_Shoulder" and status_tel == True and chek == "false":
                                 print("point_low:" , point_low)
                                 print("telo_add_low:" , telo_add_low)
                                 print("candel_color:" , candel_statess)
                                 print ("line:" , line + 1)
                                 print("cal_price_candel:" , cal_price_candel)
                                 print("patern: down  33333333333333333333333333333333333333333333")
                                 print("pullback_HHHHHHHHHH")
                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                 status_trade = shakhes[1]
                                 print("status_trade:" , status_trade)
                                 shakhes = int (shakhes[0])
                                 print("shakhes:" , shakhes)
                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{1}'
                                 ticket = 0
                                 execution = 0
                                 if status_trade == True:
                                     print("shakhes: True" )
                                     rec_pos = BUY_SELL.pos_buy(telo_add_low , shakhes , lot , self.symbol_EURUSD , commands)
                                     execution = rec_pos.comment
                                     if execution == 'Request executed':
                                            ticket =  rec_pos.order
                                            print("rec_pos:" , rec_pos)
                                            print("ticket:" , ticket)
                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{1})'+ " _ " + "(Point7:" + f'{telo_add_low})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(telo_add_low:" + f'{tel})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                 Database.update_table_chek(telo_add_low , point_timepstamp , command , "true" , ticket , candel_num)    
                                 exit = 1
                                 break
            
               if exit == 1:
                  break



 def pullback_2_old (self , tel , status_tel  , lot):
       
       telo = '0.0'
       for i in range(self.decimal_sambol - 2):  
          telo = telo + "0"
          
       telo = telo + f"{tel}"  
       telo = float (telo)
     #   print("telerance:" , telo) 
      
       data_all = Database.select_table_All()
       select_all_len = len(data_all)
       if select_all_len > 0:
          # print("select_all_len:" , select_all_len)
          # rec = data_all[select_all_len - 1]
          
          # print("rec:" , rec)


          for index in range(select_all_len - 1 , select_all_len):          
                                     
                    # print("index:" , index)
                    lab = data_all[index]
                    candel_num = lab[1]
                    type = lab[2]
                    point_patern = lab[3]
                    timepstamp = lab[19] 
                    time_start_search = lab[17]
                    status = lab[15]
                    chek = lab[16]
                    line_POS = lab[22]
                    Trust_patern = lab[25]
                    Trust_patern_full = lab[26]
                    Layout_patern = lab [27]
                    Jump_patern = lab [28]
                       
                    line_POS = int(line_POS)
                    candel_num = int(candel_num)

                    timepstamp_ticks = []

                    
                    time_start_search = int(time_start_search)
                    # print("lab:" , lab)
                    # print("status:" , status)
                    # print("time_start_search:" , time_start_search)
                    # print("point_patern:" , point_patern)
                    # print("type:" , type)
                    # print("candel_num:" , candel_num)
              
                    point_patern = json.loads(point_patern)
                    timepstamp = json.loads(timepstamp)
                    timepstamp_3 = json.loads(timepstamp[5])

                    # print("timepstamp_3:" , timepstamp_3)
                    timepstamp_old = int(timepstamp_3) + 900
                    # print("timepstamp_old:" , timepstamp_old)
                    

                    if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                        print("Pullback_old 222222222222222222222222222222222222222222222222222222222222222222222222222222222")
                        
                        
                        inputs_candels = mt5.copy_rates_range(self.symbol_EURUSD, mt5.TIMEFRAME_M1, timepstamp_old, time_start_search)
                        # print("inputs_candels:" , inputs_candels)

                        for candel_recive in inputs_candels:
                            
                            point_close = candel_recive[4]
                            point_close = Pullback.decimal(point_close , self.decimal_sambol)
                            point_close = float(point_close)
                            # print("point_close:" , point_close)

                            point_open = candel_recive[1]
                            point_open = Pullback.decimal(point_open , self.decimal_sambol)
                            point_open = float(point_open)
                            # print("point_open:" , point_open)

                            point_timepstamp =  candel_recive[0]
                            point_timepstamp = int(point_timepstamp)
                            # print("point_timepstamp:" , point_timepstamp)

                            timestamp_pulback_p = point_timepstamp - 60
                            timestamp_pullback_n = point_timepstamp + 60 


                            point_close_p = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pulback_p  , 1)
                            point_close_p = point_close_p[0][4]
                            point_close_p = Pullback.decimal(point_close_p , self.decimal_sambol)
                            point_close_p = float(point_close_p)
                            # print ("point_close_p:" , point_close_p)
  
                            point_close_n = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pullback_n , 1)
                            point_close_n = point_close_n[0][4]
                            point_close_n = Pullback.decimal(point_close_n , self.decimal_sambol)
                            point_close_n = float(point_close_n)
                            # print ("point_close_n:" , point_close_n)

                            
                            utc_to = pd.to_datetime( point_timepstamp + 60 , unit='s')
                            utc_from = pd.to_datetime( point_timepstamp , unit='s')    
                            ticks = mt5.copy_ticks_range(self.symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                         #    print("ticks:" , ticks)

                            for i in range(100):
                                 print("i:" , i)
                                 ticks = mt5.copy_ticks_range(self.symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                                #  print("ticks:" , ticks)
                                 for indexxxx , xx in enumerate(ticks):       
                                     timepstamp_ticks.append(xx[0])
                                 len_ticks = len(ticks)
                                 print(len_ticks)
                                 if len_ticks >= 1:
                                     break
                                 time.sleep(0.1)
                          
                            
                            print("timepstamp_ticks:" , timepstamp_ticks)       

                            timepstamp_ticks_end = timepstamp_ticks[-1]   
                            

                         #    timepstamp_ticks_end = timepstamp_ticks[i]
                            timepstamp_ticks_end = int (timepstamp_ticks_end)
                            print("timepstamp_ticks_end:" , timepstamp_ticks_end)
                            # print("timepstamp_ticks_end:" , pd.to_datetime( timepstamp_ticks_end , unit='s'))

                            candel_statess = ''
                            if point_open > point_close:
                              candel_statess = "red"
                            elif point_open < point_close:
                              candel_statess = "green"
                            elif point_open == point_close:
                              candel_statess = "doji"

                       

                            # print("candel_statess:" , candel_statess)  

                            cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , timepstamp_ticks_end )
                            # print("cal_line_rec:" , cal_line_rec)
              
                            cal_line = cal_line_rec[0]
                            # print("cal_line:" , cal_line)

              
                            cal_list_line = cal_line_rec[1]
                            #  print("cal_list_line:" , cal_list_line)  

                            list_cal_line = cal_line

                            if line_POS != 0:
                                    
                                 xxx = line_POS - 1
                                 cal_line = cal_line[xxx]
                                 cal_line = [cal_line]

                            a = 1
                            for i in range(self.decimal_sambol + 1):
                                  a = a * 10
                            
                            cal_price_candel = abs( int(point_open * a) - int(point_close * a) )
                            cal_price_candel = int (cal_price_candel / 10)
                            # print("cal_price_candel:" , cal_price_candel)

                            telo_add_close_high = point_close + telo
                            telo_sub_close_low = point_close - telo
                            telo_add_close_high = Pullback.decimal(telo_add_close_high , self.decimal_sambol)
                            telo_sub_close_low = Pullback.decimal(telo_sub_close_low , self.decimal_sambol)
                            telo_sub_close_low = float(telo_sub_close_low)
                            telo_add_close_high = float(telo_add_close_high)

                        #    try:            
                            
                            line = 0   
                            exit = 0 
                            run = True
    
                            if run == True:
                                  
                                for line , gap_point in enumerate(cal_line):       
                                                 
                                                 
                                      cal_point = float (gap_point)
                                      # print("cal_point:" , cal_point)
                                      line_pullback = line + 1
                                       
                                      if point_close == cal_point and (candel_statess == "green" or  candel_statess == "doji") and cal_point > point_close_p and cal_point > point_close_n and type == "Head_Shoulder":
                                                 print("UP  1111111111111111111111111111111111111111111111")
                                                #  print("pullback_MMMMMMMMMM")
                                                #  print ("line:" , line_pullback)
                                                 time_command = pd.to_datetime(timepstamp_ticks_end , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close)
                                                 status_trade = shakhes[1]
                                                #  print("status_trade:" , status_trade)
                                                 
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      # print("shakhes: True" )
                                                      if line_POS == line_pullback or line_POS == 0:
                                                           rec_pos = BUY_SELL.pos_sell(point_close , shakhes , lot , self.symbol_EURUSD , commands)
                                                           execution = rec_pos.comment
                                                           if execution == 'Request executed':
                                                                  ticket =  rec_pos.order
                                                           #        print("rec_pos:" , rec_pos)
                                                                 #  print("ticket:" , ticket)
                                                      else :
                                                           execution = "The line is not equal"   

                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{cal_point})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'  
                                                
                                                 if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "true" , ticket , line_pullback , candel_num)
                                                 else:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "false" , ticket , line_POS , candel_num)
                                                        
                                                 exit = 1
                                                 break
              
                                      elif point_close == cal_point and (candel_statess == "red" or  candel_statess == "doji") and cal_point < point_close_p and cal_point < point_close_n and type == "R_Head_Shoulder":
                                                 print("DOWN 2222222222222222222222222222222222222222222222")
                                                 print("pullback_HHHHHHHHHH")
                                                 print ("line:" , line + 1) 
                                                 time_command = pd.to_datetime(timepstamp_ticks_end , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close)
                                                 status_trade = shakhes[1]
                                                #  print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      # print("shakhes: True" )
                                                      if line_POS == line_pullback or line_POS == 0:
                                                           rec_pos = BUY_SELL.pos_buy(point_close , shakhes , lot , self.symbol_EURUSD , commands)
                                                           execution = rec_pos.comment
                                                           if execution == 'Request executed':
                                                                  ticket =  rec_pos.order
                                                           #        print("rec_pos:" , rec_pos)
                                                                 #  print("ticket:" , ticket)
                                                      else :
                                                           execution = "The line is not equal"           


                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{cal_point})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 

                                                 if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "true" , ticket , line_pullback , candel_num)
                                                 else:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "false" , ticket , line_POS , candel_num)
                                                 exit = 1
                                                 break
                                                 
                                      elif cal_point == telo_add_close_high and (candel_statess == "green" or  candel_statess == "doji") and cal_point > point_close_p and cal_point > point_close_n and type == "Head_Shoulder" and  status_tel == True:
                                                 print("UP TEL 11111111111111111111111111111111111111111111")
                                                 print("pullback_MMMMMMMMMM")
                                                 print ("line:" , line + 1) 
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_sell(telo_add_close_high , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_add_close_high})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(telo_high:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_add_close_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                                 
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_sub_close_low and (candel_statess == "red" or  candel_statess == "doji") and cal_point < point_close_p and cal_point < point_close_n and type == "R_Head_Shoulder" and  status_tel == True:
                                                 print("DOWN TEL 222222222222222222222222222222222222222222")
                                                 print("pullback_HHHHHHHHHH")
                                                 print ("line:" , line + 1)    
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_buy(telo_sub_close_low , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_sub_close_low})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(telo_low:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_sub_close_low , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_sub_close_low and (candel_statess == "green" or  candel_statess == "doji") and cal_point > point_close_p and cal_point > point_close_n and type == "Head_Shoulder" and  status_tel == True:
                                                 print("UP TEL 11111111111111111111122222222222222222222222")
                                                 print("pullback_MMMMMMMMMM")
                                                 print ("line:" , line + 1) 
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_sell(telo_sub_close_low , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_sub_close_low})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(Telo_high-1-2:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_sub_close_low , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_add_close_high and (candel_statess == "red" or  candel_statess == "doji") and cal_point < point_close_p and cal_point < point_close_n and type == "R_Head_Shoulder" and  status_tel == True:
                                                 print("DOWN TEL 222222222222222222221111111111111111111111")
                                                 print("pullback_HHHHHHHHHH")
                                                 print ("line:" , line + 1)
                                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_buy(telo_add_close_high , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_add_close_high})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(Telo_high-2-1:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_add_close_high , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
                                      
                                      else :
                                           exit = 0
                          
                                # print("")
                                if (exit == 1):
                                  break
                        #    except:
                        #     print("error plan2")  

 def pullback_2_now (self , tel , status_tel , timestamp_pulback , lot):
       
       telo = '0.0'
       for i in range(self.decimal_sambol - 2):  
          telo = telo + "0"
          
       telo = telo + f"{tel}"  
       telo = float (telo)
     #   print("telerance:" , telo) 
      
       data_all = Database.select_table_All()
       select_all_len = len(data_all)
       if select_all_len > 0:
          # print("select_all_len:" , select_all_len)
          # rec = data_all[select_all_len - 1]
          # print("rec:" , rec)
          


          for index in range(select_all_len):
                                     
                    # print("index:" , index)
                    lab = data_all[index]
                    candel_num = lab[1]
                    type = lab[2]
                    point_patern = lab[3]
                    timepstamp = lab[19] 
                    time_start_search = lab[17]
                    status = lab[15]
                    chek = lab[16]

                    line_POS = lab[22]
                    Trust_patern = lab[25]
                    Trust_patern_full = lab[26]
                    Layout_patern = lab [27]
                    Jump_patern = lab [28]
                    
                       
                    line_POS = int(line_POS)
                    candel_num = int(candel_num)
             
             
                    time_start_search = int(time_start_search)

                    timepstamp_ticks = []

                    
                    # print("lab:" , lab)
                    # print("status:" , status)
                    # print("time_start_search:" , time_start_search)
                    # print("point_patern:" , point_patern)
                    # print("type:" , type)
                    # print("candel_num:" , candel_num)
              
                    point_patern = json.loads(point_patern)
                    timepstamp = json.loads(timepstamp)
                    timepstamp_3 = json.loads(timepstamp[3])

                    # print("timepstamp_3:" , timepstamp_3)
                    timepstamp_p = int(timestamp_pulback) - 60
                    # print("timepstamp_old:" , timepstamp_old)


                    if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                        print("Pullback_now 222222222222222222222222222222222222222222222222222222222222222222222222222222222")
                        
                        
                        inputs_candels = mt5.copy_rates_from(self.symbol_EURUSD, mt5.TIMEFRAME_M1,  timepstamp_p , 1)
                        # print("inputs_candels:" , inputs_candels)

                        for candel_recive in inputs_candels:
                            
                            point_close = candel_recive[4]
                            point_close = Pullback.decimal(point_close , self.decimal_sambol)
                            point_close = float(point_close)
                            # print("point_close:" , point_close)

                            point_open = candel_recive[1]
                            point_open = Pullback.decimal(point_open , self.decimal_sambol)
                            point_open = float(point_open)
                            # print("point_open:" , point_open)

                            point_timepstamp =  candel_recive[0]
                            point_timepstamp = int(point_timepstamp)
                            # print("point_timepstamp:" , point_timepstamp)

                            timestamp_pulback_p = point_timepstamp - 60
                            timestamp_pullback_n = point_timepstamp + 60 

                            # print ("timestamp_pulback_p:" , timestamp_pulback_p)
                            # print ("timestamp_pullback_n:" , timestamp_pullback_n)

                            point_close_p = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pulback_p  , 1)
                            point_close_p = point_close_p[0][4]
                            point_close_p = Pullback.decimal(point_close_p , self.decimal_sambol)
                            point_close_p = float(point_close_p)
                            # print ("point_close_p:" , point_close_p)
  
                            point_close_n = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pullback_n , 1)
                            point_close_n = point_close_n[0][4]
                            point_close_n = Pullback.decimal(point_close_n , self.decimal_sambol)
                            point_close_n = float(point_close_n)
                            # print ("point_close_n:" , point_close_n)

                            print("timestamp_pulback:" , pd.to_datetime( point_timepstamp , unit='s'))
                            utc_to = pd.to_datetime( point_timepstamp + 60 , unit='s')
                            utc_from = pd.to_datetime( point_timepstamp , unit='s')    
                            
                         #    print("ticks:" , ticks)
                         
                            for i in range(100):
                                 print("i:" , i)
                                 ticks = mt5.copy_ticks_range(self.symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                                #  print("ticks:" , ticks)
                                 for indexxxx , xx in enumerate(ticks):       
                                     timepstamp_ticks.append(xx[0])
                                 len_ticks = len(ticks)
                                 print(len_ticks)
                                 if len_ticks >= 1:
                                     break
                                 time.sleep(0.1)

   
                            print("timepstamp_ticks:" , timepstamp_ticks)   
                         #    print("timepstamp_ticks:" , timepstamp_ticks[i])    

                            timepstamp_ticks_end = timepstamp_ticks[-1]
                         #    print("timepstamp_ticks:" , timepstamp_ticks) 
                            timepstamp_ticks_end = int (timepstamp_ticks_end)
                            print("timepstamp_ticks_end:" , timepstamp_ticks_end)


                            candel_statess = ''
                            if point_open > point_close:
                              candel_statess = "red"
                            elif point_open < point_close:
                              candel_statess = "green"
                            elif point_open == point_close:
                              candel_statess = "doji"

                            # print("candel_statess:" , candel_statess)  
                            

                            cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , timepstamp_ticks_end )
                            # print("cal_line_rec:" , cal_line_rec)
              
                            cal_line = cal_line_rec[0]
                            # print("cal_line:" , cal_line)
              
                            cal_list_line = cal_line_rec[1]
                            #  print("cal_list_line:" , cal_list_line)  

                            list_cal_line = cal_line

                            if line_POS != 0:
                                    
                                 xxx = line_POS - 1
                                 cal_line = cal_line[xxx]
                                 cal_line = [cal_line]

                            a = 1
                            for i in range(self.decimal_sambol + 1):
                                  a = a * 10
                            
                            cal_price_candel = abs( int(point_open * a) - int(point_close * a) )
                            cal_price_candel = int (cal_price_candel / 10)
                            # print("cal_price_candel:" , cal_price_candel)

                            telo_add_close_high = point_close + telo
                            telo_sub_close_low = point_close - telo
                            telo_add_close_high = Pullback.decimal(telo_add_close_high , self.decimal_sambol)
                            telo_sub_close_low = Pullback.decimal(telo_sub_close_low , self.decimal_sambol)
                            telo_sub_close_low = float(telo_sub_close_low)
                            telo_add_close_high = float(telo_add_close_high)


                        #    try:  
                        #   
                            
                            line = 0   
                            exit = 0 
                            run = True
    
                            if run == True:
                                  
                                for line , gap_point in enumerate(cal_line):       
                                                 
                                                 
                                      cal_point = float (gap_point)
                                      # print("cal_point:" , cal_point)
                                      line_pullback = line + 1
                                       
                                      if point_close == cal_point and (candel_statess == "green" or  candel_statess == "doji") and point_close > point_close_p and point_close > point_close_n and type == "Head_Shoulder":
                                                #  print("UP  1111111111111111111111111111111111111111111111")
                                                #  print("pullback_MMMMMMMMMM")
                                                #  print ("line:" , line + 1)
                                                 time_command = pd.to_datetime( timepstamp_ticks_end , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close)
                                                 status_trade = shakhes[1]
                                                #  print("status_trade:" , status_trade)
                                                 
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      # print("shakhes: True" )
                                                      if line_POS == line_pullback or line_POS == 0:
                                                           rec_pos = BUY_SELL.pos_sell(point_close , shakhes , lot , self.symbol_EURUSD , commands)
                                                           execution = rec_pos.comment
                                                           if execution == 'Request executed':
                                                                  ticket =  rec_pos.order
                                                                 #  print("rec_pos:" , rec_pos)
                                                                 #  print("ticket:" , ticket)
                                                      else :
                                                           execution = "The line is not equal"            


                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{2})'+ " _ " + "(Point7:" + f'{cal_point})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'  
                                                 if line_POS == 0 or line_POS == line_pullback: 
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "true" , ticket , line_pullback , candel_num)
                                                 else:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "false" , ticket , line_POS , candel_num)
                                                        
                                                 exit = 1
                                                 break
              
                                      elif point_close == cal_point and (candel_statess == "red" or  candel_statess == "doji") and point_close < point_close_p and point_close < point_close_n and type == "R_Head_Shoulder":
                                                #  print("DOWN 2222222222222222222222222222222222222222222222")
                                                #  print("pullback_HHHHHHHHHH")
                                                #  print ("line:" , line_pullback) 
                                                 time_command = pd.to_datetime( timepstamp_ticks_end , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close)
                                                 status_trade = shakhes[1]
                                                #  print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      # print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_buy(point_close , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                            #  print("rec_pos:" , rec_pos)
                                                            #  print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{2})'+ " _ " + "(Point7:" + f'{cal_point})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                
                                                 if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "true" , ticket , line_pullback , candel_num)
                                                 else:
                                                        Database.update_table_chek(point_close , timepstamp_ticks_end , command , "false" , ticket , line_POS , candel_num)
                                                        
                                                 exit = 1
                                                 break
                                                 
                                      elif cal_point == telo_add_close_high and (candel_statess == "green" or  candel_statess == "doji") and cal_point > point_close_p and cal_point > point_close_n and type == "Head_Shoulder" and  status_tel == True:
                                                #  print("UP TEL 11111111111111111111111111111111111111111111")
                                                #  print("pullback_MMMMMMMMMM")
                                                #  print ("line:" , line + 1) 
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                #  print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      # print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_sell(telo_add_close_high , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                            #  print("rec_pos:" , rec_pos)
                                                            #  print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_add_close_high})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(telo_high:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_add_close_high , point_timepstamp , command , "true" , ticket , candel_num)     
                                                 
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_sub_close_low and (candel_statess == "red" or  candel_statess == "doji") and cal_point < point_close_p and cal_point < point_close_n and type == "R_Head_Shoulder" and  status_tel == True:
                                                 print("DOWN TEL 222222222222222222222222222222222222222222")
                                                 print("pullback_HHHHHHHHHH")
                                                 print ("line:" , line + 1)    
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_buy(telo_sub_close_low , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_sub_close_low})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(telo_low:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_sub_close_low , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_sub_close_low and (candel_statess == "green" or  candel_statess == "doji") and cal_point > point_close_p and cal_point > point_close_n and type == "Head_Shoulder" and  status_tel == True:
                                                 print("UP TEL 11111111111111111111122222222222222222222222")
                                                 print("pullback_MMMMMMMMMM")
                                                 print ("line:" , line + 1) 
                                                 time_command = pd.to_datetime( point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_sell(telo_sub_close_low , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_sub_close_low})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(Telo_high-1-2:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_sub_close_low , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
              
                                      elif cal_point == telo_add_close_high and (candel_statess == "red" or  candel_statess == "doji") and cal_point < point_close_p and cal_point < point_close_n and type == "R_Head_Shoulder" and  status_tel == True:
                                                 print("DOWN TEL 222222222222222222221111111111111111111111")
                                                 print("pullback_HHHHHHHHHH")
                                                 print ("line:" , line + 1)
                                                 time_command = pd.to_datetime(point_timepstamp , unit='s')
                                                 shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol)
                                                 status_trade = shakhes[1]
                                                 print("status_trade:" , status_trade)
                                                 shakhes = int (shakhes[0])
                                                 commands = f'{candel_num}' + "_" + f'B' + "_" + f'{line + 1}' + '_' + f'{shakhes}' + "_" + f'{2}'
                                                 ticket = 0
                                                 execution = 0
                                                 if status_trade == True:
                                                      print("shakhes: True" )
                                                      rec_pos = BUY_SELL.pos_buy(telo_add_close_high , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                             ticket =  rec_pos.order
                                                             print("rec_pos:" , rec_pos)
                                                             print("ticket:" , ticket)
                                                 command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line + 1})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{2})'+ " _ " + "(Point7:" + f'{telo_add_close_high})' + " _ " + "(Time:" + f'{time_command})'+ " _ " + "(Telo_high-2-1:" + f'{tel})' + "_" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                                 Database.update_table_chek(telo_add_close_high , point_timepstamp , command , "true" , ticket , candel_num)
                                                 exit = 1
                                                 break
                                      
                                      else :
                                           exit = 0
                          
                                # print("")
                                if (exit == 1):
                                  break
                        #    except:
                        #     print("error plan2")
                    
         

 def pullback_3_old (self , lot):
               
      data_all = Database.select_table_All()
      select_all_len = len(data_all)
      print("select_all_len:" , select_all_len)

      if select_all_len > 0:
               
         for index in range(select_all_len - 1 , select_all_len ):
        #  for index in range(11 , 12 ):
                             
          #   print("indexs:" , index)
            lab = data_all[index]
          #   print ("lab:" , lab)
            candel_num = lab[1]
            type = lab[2]
            point_patern = lab[3]
            status = lab[15]
            chek = lab[16]
            time_start_search = lab[17]
            timepstamp = lab[19] 
            line_POS = lab[22]
            Trust_patern = lab[25]
            Trust_patern_full = lab[26]
            Layout_patern = lab [27]
            Jump_patern = lab [28]
            
            

            line_POS = int(line_POS)

            # print("line_POS:" , line_POS)
            exit = 0
            line = []
            list_timpstamp_sec = []
            list_pullback3 = []
            
          #   print("select_all_len:" , select_all_len)
            rec = data_all[select_all_len - 1]
            # print("rec:" , rec)

            time_start_search = int(time_start_search)
            point_patern = json.loads(point_patern)
            timepstamp = json.loads(timepstamp)
            timepstamp_3 = json.loads(timepstamp[5])

            # print("line_POS:" , line_POS)

            timepstamp_old = int(timepstamp_3) + 900
            

            if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                     
                print("pullback_old 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")
                    
                list_point = []
                list_point_left_right = []
                list_point_group = []
                inputs_candels = mt5.copy_rates_range(self.symbol_EURUSD, mt5.TIMEFRAME_M1, timepstamp_old, time_start_search)
                # print("inputs_candels:" , inputs_candels)
               #  print("point_patern:" , point_patern)
                
               #  print("cal_line:" , cal_line)
               #  print ("list_pullback3:" , list_pullback3) 
               #  print ("timestamp_pulback:" , timestamp_pulback) 


                for indexs , candel_recive in enumerate(inputs_candels):       
                  # if indexs == 9:
                    #  print("candel_recive:" , candel_recive)
                    #  print("indexs:" , indexs)

                    #  if indexs == 10 :
                    #       quit()
                     

            #    try:
                     point_timepstamp =  candel_recive[0]
                     point_timepstamp = int (point_timepstamp)
                    #  print("point_timepstamp:" , point_timepstamp)

                    #  print("timestamp_pulback:" , pd.to_datetime( point_timepstamp , unit='s'))
                     utc_from = pd.to_datetime( point_timepstamp , unit='s') 
                     utc_to = pd.to_datetime( point_timepstamp + 60 , unit='s')
                        
                     ticks = mt5.copy_ticks_range(self.symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                    #  print("ticks:" , ticks)
                     

                     for lists in ticks:
                         xx = Pullback.decimal(lists[1] , self.decimal_sambol)
                        #  print(xx)
                         xx = float(xx)
                         list_pullback3.append(xx)
                    #  print("list_pullback3:" , list_pullback3)    

                     for indexxxx in ticks:
                         list_timpstamp_sec.append(indexxxx[0])

                    #  print("")    


                    #  list_timpstamp_sec = [1694581740 , 1694581752 ]
                    #  print ("list_pullback3" , list_pullback3[0])
                    #  list_pullback3 = [1.07557, 1.07558, 1.07559, 1.07558, 1.07557, 1.07555, 1.07554, 1.07551, 1.07546, 1.07549, 1.07545, 1.07544]
                     for indexxx , index_ticks_times in enumerate(list_timpstamp_sec): 
                                #  print("indexxx:" , indexxx)             
                                #  print("list_pullback3:" , list_pullback3)  
                                 index_tick_time = int(index_ticks_times)
                                #  print("candel_num:" , candel_num)
                                #  print("index_tick_time:" , index_tick_time)
                                #  print (pd.to_datetime( index_tick_time , unit='s'))

                                #  print("line_POS:" , line_POS)

                                 cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , index_tick_time )
                                 cal_line = cal_line_rec[0]
                                 cal_list_line = cal_line_rec[1]
                                 list_cal_line = cal_line

                                 if line_POS != 0:

                                    cal_line = cal_line[line_POS - 1]
                                    cal_line = [cal_line]


                                 list_pullback3_time_1s = list_pullback3[indexxx]
                                #  print("list_pullback3_time_1s:" , list_pullback3_time_1s)
            
            
                                 try:
                                     for indexxxx , index_point_close in enumerate([list_pullback3_time_1s]):  
                                            # print("indexxxx:" , indexxxx)  
                                            # print("index_point_close:" , index_point_close)       
                                           
                                            # for line_point in cal_line:  
                                            for linee , line_point in enumerate(cal_line): 

                                              #  print ("linee:" , linee ) 

                                               line_point = float (line_point)
                                               index_point_close = float (index_point_close)

                                              #  print("line_point:" , line_point) 
                                              #  print("index_point_close:" , index_point_close) 
            
                                               if line_point ==  index_point_close:
                                                   line.append(linee)
                                                  #  print("indexxx:" , indexs)
                                                   list_point.append(index_point_close)
                                                   list_point_left_right.append(list_pullback3[indexxx - 1])
                                                   list_point_left_right.append(list_pullback3[indexxx])
                                                   list_point_left_right.append(list_pullback3[indexxx + 1])
                                                  #  print("list_point_left_right:" , list_point_left_right)
            
                                               if list_point_left_right != []:
                                                          
                                                           list_point_group.append(list_point_left_right)
                                                           list_point_left_right = []
                                     
                                 except:
                                     print("error list_pullback3[indexs + 1]")
                                    # print("")
            
                                #  print("list_pullback3:" , list_pullback3)                
                                #  print("list_point_group:" , list_point_group) 
                                #  print("line:" , line)  

                                 
                                 if list_point_group != []:
                                         
                                        #  print("point_timepstamp:" , point_timepstamp)
                                        #  print("list_point_group:" , list_point_group)   
                                         
                                    # try:
                                        
                                      for index_list , list in enumerate(list_point_group):    
                      
                                            list_point_left_right = list
                                            if len(list) == 3:
            
                                              # print("list_point_left_right:" , list_point_left_right)
                                              # print("cal_line:" , cal_line)
                                                  

                                              left_candel = list_point_left_right[0]
                                              right_candel = list_point_left_right[2]
                                              point_close_3 = list_point_left_right[1]
                                              
                                              left_candel = float(left_candel)
                                              right_candel = float(right_candel)
                                              point_close_3 = float(point_close_3)
                  
                                              rec = Database.select_table_One(candel_num)
                                              chek = rec[0][16]
                                               #    print("chek:" , chek)
                                              line_pullback =  line[index_list] + 1
                                                  
                                              # print("left_candel:" , left_candel)
                                              # print("right_candel:" , right_candel)
                                              # print("point_close_3:" , point_close_3)
                                              # print("line_pullback:" , line_pullback)


                                                  
                      
                                              if point_close_3 == point_close_3 and point_close_3 > left_candel and point_close_3 > right_candel and type == "Head_Shoulder" and chek == "false":
                                                       print("1111111111111111111111111111111111111111111111")
                                                      #  print("point_timepstamp:" , point_timepstamp)
                                                      #  print("list_pullback3:" , list_pullback3)
                                                      #  print("point_close_3:" , point_close_3)
                                                      #  print("left_candel:" , left_candel)
                                                      #  print("right_candel:" , right_candel)
                                                      #  print ("line_pullback:" , line_pullback)
                                                       time_command = pd.to_datetime(index_tick_time , unit='s')
                                                       shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close_3)
                                                       status_trade = shakhes[1]
                                                      #  print("status_trade:" , status_trade)
                                                       shakhes = int (shakhes[0])
                                                       commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'
                                                       ticket = 0
                                                       execution = 0
                                                       if status_trade == True:
                                                            # print("shakhes: True" )
                                                            # print("line_POS_true:" , line_POS)
                                                            if line_POS == line_pullback or line_POS == 0:
                                                                 rec_pos = BUY_SELL.pos_sell(point_close_3 , shakhes , lot , self.symbol_EURUSD , commands)
                                                                 # print("rec_pos:" , rec_pos)
                                                                 execution = rec_pos.comment
                                                                 if execution == 'Request executed':
                                                                    ticket =  rec_pos.order
                                                                   #  print("rec_pos:" , rec_pos)
                                                                   #  print("ticket:" , ticket)
                                                            else:
                                                                 execution = "The line is not equal"
                                                                        
                                                       command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{3})'+ " _ " + "(Point7:" + f'{point_close_3})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                                       if line_POS == 0 or line_POS == line_pullback:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "true" , ticket , line_pullback , candel_num)     
                                                       else:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "false" , ticket , line_POS , candel_num)
                                                          
                                                       exit = 1
                                                       break
                      
                                              elif point_close_3 == point_close_3 and point_close_3 < left_candel and point_close_3 < right_candel and type == "R_Head_Shoulder" and chek == "false":
                                                       print("22222222222222222222222222222222222222222222222")
                                                      #  print("point_close_3:" , point_close_3)
                                                      #  print("left_candel:" , left_candel)
                                                      #  print("right_candel:" , right_candel)
                                                      #  print ("line_pullback:" , line_pullback)
                                                       time_command = pd.to_datetime( index_tick_time , unit='s')
                                                       shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close_3)
                                                       status_trade = shakhes[1]
                                                      #  print("status_trade:" , status_trade)
                                                       shakhes = int (shakhes[0])
                                                       commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'
                                                       ticket = 0
                                                       execution = 0
                                                       if status_trade == True:
                                                            # print("shakhes: True" )
                                                            # print("line_POS_true:" , line_POS)
                                                            if line_POS == line_pullback or line_POS == 0:    
                                                                rec_pos = BUY_SELL.pos_buy( point_close_3 , shakhes , lot , self.symbol_EURUSD , commands)
                                                                execution = rec_pos.comment
                                                                if execution == 'Request executed':
                                                                   ticket =  rec_pos.order
                                                                  #  print("rec_pos:" , rec_pos)
                                                                  #  print("ticket:" , ticket)
                                                            else:
                                                                 execution = "The line is not equal"

                                                       command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{3})'+ " _ " + "(Point7:" + f'{point_close_3})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})'  + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                                      
                                                       if line_POS == 0 or line_POS == line_pullback:
                                                            Database.update_table_chek(point_close_3 , index_tick_time , command , "true" , ticket , line_pullback , candel_num)     
                                                       else:
                                                            Database.update_table_chek(point_close_3 , index_tick_time , command , "false" , ticket , line_POS , candel_num)
                                                       
                                                       exit = 1
                                                       break    
                                                  
                                                 
                                              # print("")  
            
                                              if exit== 1:
                                                   break
                                              
                                      if exit== 1:
                                              break   
                                 list_point_group = [] 
                                 list_point_left_right = []    
                                 line = []   

                                #  print("")

                        # except:
                        #        print("the end")     
                     
                     if exit== 1:
                            break 
            #    except:
            #        print("error plan 33333333333") 

 def pullback_3_now (self , timestamp_pulback , list_pullback3 , lot):
               
      data_all = Database.select_table_All()
      select_all_len = len(data_all)
      print("select_all_len:" , select_all_len)

      if select_all_len > 0:
               
         for index in range(select_all_len):
                          
            # print("indexs:" , index)
            lab = data_all[index]
            candel_num = lab[1]
            type = lab[2]
            point_patern = lab[3]
            status = lab[15]
            chek = lab[16]
            time_start_search = lab[17]
            timepstamp = lab[19] 
            line_POS = lab[22]
            Trust_patern = lab[25]
            Trust_patern_full = lab[26]
            Layout_patern = lab [27]
            Jump_patern = lab [28]
            
            line_POS = int(line_POS)

            exit = 0
            line = []
            list_timpstamp_sec = []
            list_pullback3 = []
            
          #   print("select_all_len:" , select_all_len)
            rec = data_all[select_all_len - 1]
            # print("rec:" , rec)

            time_start_search = int(time_start_search)
            point_patern = json.loads(point_patern)
            timepstamp = json.loads(timepstamp)
            timepstamp_3 = json.loads(timepstamp[3])

     #     print("timepstamp_3:" , timepstamp_3)

          
            

            if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                     
                print("pullback_now 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")
                    
                list_point = []
                list_point_left_right = []
                list_point_group = []
                
                inputs_candels = mt5.copy_rates_from(self.symbol_EURUSD, mt5.TIMEFRAME_M1,  timestamp_pulback , 1)

                # print("inputs_candels:" , inputs_candels)
               #  print("point_patern:" , point_patern)
                
               #  print("cal_line:" , cal_line)
               #  print ("list_pullback3:" , list_pullback3) 
               #  print ("timestamp_pulback:" , timestamp_pulback) 


                for indexs , candel_recive in enumerate(inputs_candels):       
                  # if indexs == 9:
                    #  print("candel_recive:" , candel_recive)
                    #  print("indexs:" , indexs)

                    #  if indexs == 10 :
                    #       quit()
                     

            #    try:
                     point_timepstamp =  candel_recive[0]
                     point_timepstamp = int (point_timepstamp)
                    #  print("point_timepstamp:" , point_timepstamp)

                     utc_from = pd.to_datetime( point_timepstamp , unit='s') 
                     utc_to = pd.to_datetime( point_timepstamp + 60 , unit='s')
                        
                     ticks = mt5.copy_ticks_range(self.symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
                    #  print("ticks:" , ticks)
                    #  time.sleep(1)
    
                     for lists in ticks:
                         xx = Pullback.decimal(lists[1] , self.decimal_sambol)
                        #  print(xx)
                         xx = float(xx)
                         list_pullback3.append(xx)
                    #  print("list_pullback3:" , list_pullback3)    

                     for indexx in ticks:
                         list_timpstamp_sec.append(indexx[0])

                    #  print("")    


                    #  list_timpstamp_sec = [1694581740 , 1694581752 ]
                    #  print ("list_pullback3" , list_pullback3[0])
                    #  list_pullback3 = [1.07557, 1.07558, 1.07559, 1.07558, 1.07557, 1.07555, 1.07554, 1.07551, 1.07546, 1.07549, 1.07545, 1.07544]
                     for indexxx , index_ticks_times in enumerate(list_timpstamp_sec): 
                                #  print("indexxx:" , indexxx)             
                                #  print("list_pullback3:" , list_pullback3)  
                                 index_tick_time = int(index_ticks_times)
                                #  print("candel_num:" , candel_num)
                                #  print("index_tick_time:" , index_tick_time)
                                #  print (pd.to_datetime( index_tick_time , unit='s'))
                                 cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , index_tick_time )
                                 cal_line = cal_line_rec[0]
                                 cal_list_line = cal_line_rec[1]

                                #  print("line_POS:" , line_POS)
                                #  print("cal_line:" , cal_line)

                                 if line_POS != 0:
                                    
                                    xxx = line_POS - 1
                                    
                                    cal_line = cal_line[xxx]
                                    cal_line = [cal_line]

                                #  print("cal_line_pos:" , cal_line)
            
                                #  print("cal_line:" , cal_line)
                                 
                                #  print("cal_line:" , cal_line)

                                 list_pullback3_time_1s = list_pullback3[indexxx]
                                #  print("list_pullback3_time_1s:" , list_pullback3_time_1s)
            
            
                                 try:
                                    for indexxxx , index_point_close in enumerate([list_pullback3_time_1s]):  
                                            # print("indexxxx:" , indexxxx)  
                                            # print("index_point_close:" , index_point_close)       
                                           
                                            # for line_point in cal_line:  
                                            for linee , line_point in enumerate(cal_line): 

                                              #  print ("linee:" , linee ) 

                                               line_point = float (line_point)
                                               index_point_close = float (index_point_close)

                                              #  print("line_point:" , line_point) 
                                              #  print("index_point_close:" , index_point_close) 
            
                                               if line_point ==  index_point_close:
                                                   line.append(linee)
                                                  #  print("indexxx:" , indexs)
                                                   list_point.append(index_point_close)
                                                   list_point_left_right.append(list_pullback3[indexxx - 1])
                                                   list_point_left_right.append(list_pullback3[indexxx])
                                                   list_point_left_right.append(list_pullback3[indexxx + 1])
                                                  #  print("list_point_left_right:" , list_point_left_right)
            
                                               if list_point_left_right != []:
                                                          
                                                           list_point_group.append(list_point_left_right)
                                                           list_point_left_right = []
                                     
                                 except:
                                     print("error list_pullback3[indexs + 1]")
                                    # print("")
            
                                #  print("list_pullback3:" , list_pullback3)                
                                #  print("list_point_group:" , list_point_group) 
                                #  print("line:" , line)  

                                 
                                 if list_point_group != []:
                                         
                                        #  print("point_timepstamp:" , point_timepstamp)
                                        #  print("list_point_group:" , list_point_group)   
                                         
                                    # try:
                                        
                                      for index_list , list in enumerate(list_point_group):    
                      
                                            list_point_left_right = list
                                            if len(list) == 3:
            
                                              # print("list_point_left_right:" , list_point_left_right)
                                              # print("cal_line:" , cal_line)
                                                  

                                              left_candel = list_point_left_right[0]
                                              right_candel = list_point_left_right[2]
                                              point_close_3 = list_point_left_right[1]
                                              left_candel = float(left_candel)
                                              right_candel = float(right_candel)
                                              point_close_3 = float(point_close_3)
                  
                                              # rec = Database.select_table_One(candel_num)
                                              # chek = rec[0][16]
                                               #    print("chek:" , chek)
                                              line_pullback =  line[index_list] + 1
                                                  
                                              # print("left_candel:" , left_candel)
                                              # print("right_candel:" , right_candel)
                                              # print("point_close_3:" , point_close_3)
                                              # print("line_pullback:" , line_pullback)

                      
                                              if point_close_3 == point_close_3 and point_close_3 > left_candel and point_close_3 > right_candel and type == "Head_Shoulder" and chek == "false":
                                                       print("1111111111111111111111111111111111111111111111")
                                                      #  print("point_timepstamp:" , point_timepstamp)
                                                      #  print("list_pullback3:" , list_pullback3)
                                                      #  print("point_close_3:" , point_close_3)
                                                      #  print("left_candel:" , left_candel)
                                                      #  print("right_candel:" , right_candel)
                                                      #  print ("line_pullback:" , line_pullback)
                                                       time_command = pd.to_datetime(index_tick_time , unit='s')
                                                       shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close_3)
                                                       status_trade = shakhes[1]
                                                      #  print("status_trade:" , status_trade)
                                                       shakhes = int (shakhes[0])
                                                       commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'
                                                       ticket = 0
                                                       execution = 0
                                                       if status_trade == True:
                                                            # print("shakhes: True" )
                                                          if line_POS == line_pullback or line_POS == 0:
                                                              rec_pos = BUY_SELL.pos_sell(point_close_3 , shakhes , lot , self.symbol_EURUSD , commands)
                                                              # print("rec_pos:" , rec_pos)
                                                              execution = rec_pos.comment
                                                              if execution == 'Request executed':
                                                                 ticket =  rec_pos.order
                                                                #  print("rec_pos:" , rec_pos)
                                                                #  print("ticket:" , ticket)
                                                          else:
                                                               execution = "The line is not equal"      


                                                       command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{3})'+ " _ " + "(Point7:" + f'{point_close_3})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})' + " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                                       if line_POS == 0 or line_POS == line_pullback:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "true" , ticket , line_pullback , candel_num)     
                                                       
                                                       else:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "false" , ticket , line_POS , candel_num)
                                                          
                                                       exit = 1
                                                       break
                      
                                              elif point_close_3 == point_close_3 and point_close_3 < left_candel and point_close_3 < right_candel and type == "R_Head_Shoulder" and chek == "false":
                                                       print("22222222222222222222222222222222222222222222222")
                                                      #  print("point_close_3:" , point_close_3)
                                                      #  print("left_candel:" , left_candel)
                                                      #  print("right_candel:" , right_candel)
                                                      #  print ("line_pullback:" , line_pullback)
                                                       time_command = pd.to_datetime( index_tick_time , unit='s')
                                                       shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_close_3)
                                                       status_trade = shakhes[1]
                                                      #  print("status_trade:" , status_trade)
                                                       shakhes = int (shakhes[0])
                                                       commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{3}'
                                                       ticket = 0
                                                       execution = 0
                                                       if status_trade == True:
                                                            # print("shakhes: True" )
                                                           if line_POS == line_pullback or line_POS == 0:   
                                                               rec_pos = BUY_SELL.pos_buy( point_close_3 , shakhes , lot , self.symbol_EURUSD , commands)
                                                               execution = rec_pos.comment
                                                               if execution == 'Request executed':
                                                                  ticket =  rec_pos.order
                                                                 #  print("rec_pos:" , rec_pos)
                                                                 #  print("ticket:" , ticket)
                                                           else:
                                                                execution = "The line is not equal"       

                                                       command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_now:" f'{3})'+ " _ " + "(Point7:" + f'{point_close_3})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(Status_trade:" + f'{status_trade})'  + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})'
                                                       if line_POS == 0 or line_POS == line_pullback:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "true" , ticket , line_pullback , candel_num)     
                                                       else:
                                                           Database.update_table_chek(point_close_3 , index_tick_time , command , "false" , ticket , line_POS , candel_num)
                                                          
                                                       exit = 1
                                                       break    
                                                  
                                                 
                                              # print("")  
            
                                              if exit== 1:
                                                   break
                                              
                                      if exit== 1:
                                              break   
                                 list_point_group = [] 
                                 list_point_left_right = []    
                                 line = []   

                                #  print("")

                        # except:
                        #        print("the end")     
                     
                     if exit== 1:
                            break 
            #    except:
            #        print("error plan 33333333333") 



 def pullback_4_old(self , tel , status_tel , lot):
           
           telo = '0.0'
           for i in range(self.decimal_sambol - 2):  
              telo = telo + "0"
              
           telo = telo + f"{tel}"  
           telo = float (telo)
          #  print("telerance:" , telo) 
        
           data_all = Database.select_table_All()
           select_all_len = len(data_all)
           if select_all_len > 0:
          #     print("select_all_len:" , select_all_len)
              # rec = data_all[select_all_len - 1]
              # print("rec:" , rec)
              
              for index in range(select_all_len - 1 , select_all_len):  
               #   print("")
                                  
               #   print("index:" , index)
                 lab = data_all[index]
                 candel_num = lab[1]
                 type = lab[2]
                 point_patern = lab[3]
                 timepstamp = lab[19] 
                 time_start_search = lab[17]
                 status = lab[15]
                 chek = lab[16]
                 line_POS = lab[22]
                 Trust_patern = lab[25]
                 Trust_patern_full = lab[26]
                 Layout_patern = lab [27]
                 Jump_patern = lab [28]
                    
                 line_POS = int(line_POS)
                 candel_num = int(candel_num)

                 exit = 0
                 
                 time_start_search = int(time_start_search)
               #   print("lab:" , lab)
               #   print("status:" , status)
               #   print("time_start_search:" , time_start_search)
               #   print("point_patern:" , point_patern)
               #   print("type:" , type)
               #   print("candel_num:" , candel_num)
           
                 point_patern = json.loads(point_patern)
                 timepstamp = json.loads(timepstamp)
                 timepstamp_3 = json.loads(timepstamp[5])

               #   print("timepstamp_3:" , timepstamp_3)

                 timepstamp_old = int(timepstamp_3) + 900
                #  print("timepstamp_old:" , timepstamp_old)

                 
                 if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                     print("Pullback_old 4444444444444444444444444444444444444444444444444444444444444444444444444444")

                     inputs_candels = mt5.copy_rates_range(self.symbol_EURUSD, mt5.TIMEFRAME_M1, timepstamp_old, time_start_search)
                     
                    #  print("inputs_candels:" , inputs_candels)

                     for candel_recive in inputs_candels:
                         # print("candel_recive:" , candel_recive)  


                         timestamp_pulback4 = candel_recive[0]
                         timestamp_pulback4 = int(timestamp_pulback4)
                         # print("timestamp_pulback4:" , timestamp_pulback4)  

                         timestamp_pulback_p = timestamp_pulback4 - 60
                         timestamp_pullback_n = timestamp_pulback4 + 60

                         # print("timestamp_pulback_p:" , timestamp_pulback_p)
                         # print( pd.to_datetime( timestamp_pulback_p , unit='s'))
                         # print("timestamp_pullback_n:" , timestamp_pullback_n)
                         # print( pd.to_datetime( timestamp_pullback_n , unit='s'))  
                         
                         
                         point_open = candel_recive[1]
                         point_open = Pullback.decimal(point_open , self.decimal_sambol)
                         point_open = float(point_open)
                        #  print ("point_open:" , point_open)

                         point_close = candel_recive[4]
                         point_close = Pullback.decimal(point_close , self.decimal_sambol)
                         point_close = float(point_close)
                        #  print ("point_close:" , point_close)
          
                         point_close_p = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pulback_p  , 1)
                         point_close_p = point_close_p[0][4]
                         point_close_p = Pullback.decimal(point_close_p , self.decimal_sambol)
                         point_close_p = float(point_close_p)
                        #  print ("point_close_p:" , point_close_p)

                         point_open_n = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pullback_n , 1)
                         point_open_n = point_open_n[0][1]
                         point_open_n = Pullback.decimal(point_open_n , self.decimal_sambol)
                         point_open_n = float(point_open_n)
                        #  print ("point_open_n:" , point_open_n)
                 
                 
                         candel_state = ''
                         if point_open > point_close:
                           candel_state = "red"
                         elif point_open < point_close:
                           candel_state = "green"
                         elif point_open == point_close:
                           candel_state = "doji"  
                 
                        #  print("candel_state:" , candel_state)
                 
                         # cal_point = LINE.cal_point_line(1 , timestamp_pulback)
                         # print("cal_point:" , cal_point)
                         cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , timestamp_pulback4 )
                        #  print("cal_line_rec:" , cal_line_rec)

                         cal_line = cal_line_rec[0]
                        #  print("cal_line:" , cal_line)

          
                         cal_list_line = cal_line_rec[1]
                        #  print("cal_list_line:" , cal_list_line)
                         # print("cal_line:" , cal_line)
                         list_cal_line = cal_line

                         if line_POS != 0:
                                    
                               xxx = line_POS - 1
                               cal_line = cal_line[xxx]
                               cal_line = [cal_line]


                         if (candel_state == "red" and point_open > point_close_p and type == "Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                          #  print("1111111111111111111111111111111111111111111111")
                                          #  print("point_open:" , point_open)
                                          #  print ("line:" , line_pullback)
                                          #  print("pullback MMMMMMMMMMMMMMMM")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                          #  print("status_trade:" , status_trade)
                                           
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_sell(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                       #  print("rec_pos:" , rec_pos)
                                                       #  print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"       

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: red)" + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         elif (candel_state == "green" and point_open < point_close_p and type == "R_Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                          #  print("2222222222222222222222222222222222222222222222")
                                          #  print("point_open:" , point_open)
                                          #  print ("line:" , line_pullback)
                                          #  print("pullback HHHHHHHHHHHHHHHH")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                          #  print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_buy(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                       #  print("rec_pos:" , rec_pos)
                                                       #  print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"        

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: green)" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break    
                                               
                         if (candel_state == 'doji' and point_open > point_close_p and point_open > point_open_n and type == "Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                           print("1111111111111111111111111111111111111111111111")
                                           print("point_open:" , point_open)
                                           print ("line_pullback:" , line_pullback)
                                           print("pullback MMMMMMMMMMMMMMMM") 
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                           print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_sell(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                        print("rec_pos:" , rec_pos)
                                                        print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: doji)"  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         elif (candel_state == "doji" and point_open < point_close_p and point_open < point_open_n and type == "R_Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                           print("22222222222222222222222222222222222222222")
                                           print("point_open:" , point_open)
                                           print ("line_pullback:" , line_pullback)
                                           print("pullback HHHHHHHHHHHHHHHHHH")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                           print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_buy( point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                        print("rec_pos:" , rec_pos)
                                                        print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pulback_old:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: doji)"  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         if exit == 1:
                             break
                        #  print("")

 def pullback_4_now (self , tel , status_tel , timestamp_pulback , lot):
           
           telo = '0.0'
           for i in range(self.decimal_sambol - 2):  
              telo = telo + "0"
              
           telo = telo + f"{tel}"  
           telo = float (telo)
          #  print("telerance:" , telo) 
        
           data_all = Database.select_table_All()
           select_all_len = len(data_all)
           if select_all_len > 0:
          #     print("select_all_len:" , select_all_len)
              rec = data_all[select_all_len - 1]
              # print("rec:" , rec)
              
              for index in range(select_all_len):
               #   print("")
                                  
               #   print("index:" , index)
                 lab = data_all[index]
                 candel_num = lab[1]
                 type = lab[2]
                 point_patern = lab[3]
                 timepstamp = lab[19] 
                 time_start_search = lab[17]
                 status = lab[15]
                 chek = lab[16]

                 line_POS = lab[22]
                 Trust_patern = lab[25]
                 Trust_patern_full = lab[26]
                 Layout_patern = lab [27]
                 Jump_patern = lab [28]
                    
                 line_POS = int(line_POS)
                 candel_num = int(candel_num)
                 
                 exit = 0
        
                 time_start_search = int(time_start_search)
               #   print("lab:" , lab)
               #   print("status:" , status)
               #   print("time_start_search:" , time_start_search)
               #   print("point_patern:" , point_patern)
               #   print("type:" , type)
               #   print("candel_num:" , candel_num)
           
                 point_patern = json.loads(point_patern)
                 timepstamp = json.loads(timepstamp)
                 timepstamp_3 = json.loads(timepstamp[3])

               #   print("timepstamp_3:" , timepstamp_3)

                 timepstamp_old = int(timepstamp_3) + 900
                #  print("timepstamp_old:" , timepstamp_old)

                 
                 if status == "true" and chek == "false" and Trust_patern_full == "true" and Layout_patern == "true" and Jump_patern == "true":
                     print("Pullback_now 4444444444444444444444444444444444444444444444444444444444444444444444444444")

                     inputs_candels = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 ,  timestamp_pulback , 1)
                    #  print("inputs_candels:" , inputs_candels)

                     for candel_recive in inputs_candels:
                         # print("candel_recive:" , candel_recive)  


                         timestamp_pulback4 = candel_recive[0]
                         timestamp_pulback4 = int(timestamp_pulback4)
                         # print("timestamp_pulback4:" , timestamp_pulback4)  

                         timestamp_pulback_p = timestamp_pulback4 - 60
                         timestamp_pullback_n = timestamp_pulback4 + 60
                         # print("timestamp_pulback_p:" , timestamp_pulback_p)
                         # print( pd.to_datetime( timestamp_pulback_p , unit='s'))
                         # print("timestamp_pullback_n:" , timestamp_pullback_n)
                         # print( pd.to_datetime( timestamp_pullback_n , unit='s'))  
                         
                         
                         point_open = candel_recive[1]
                         point_open = Pullback.decimal(point_open , self.decimal_sambol)
                         point_open = float(point_open)
                        #  print ("point_open:" , point_open)

                         point_close = candel_recive[4]
                         point_close = Pullback.decimal(point_close , self.decimal_sambol)
                         point_close = float(point_close)
                        #  print ("point_close:" , point_close)
          
                         point_close_p = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pulback_p  , 1)
                         point_close_p = point_close_p[0][4]
                         point_close_p = Pullback.decimal(point_close_p , self.decimal_sambol)
                         point_close_p = float(point_close_p)
                        #  print ("point_close_p:" , point_close_p)

                         point_open_n = mt5.copy_rates_from(self.symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_pullback_n , 1)
                         point_open_n = point_open_n[0][1]
                         point_open_n = Pullback.decimal(point_open_n , self.decimal_sambol)
                         point_open_n = float(point_open_n)
                        #  print ("point_open:" , point_open_n)
                 
                 
                         candel_state = ''
                         if point_open > point_close:
                           candel_state = "red"
                         elif point_open < point_close:
                           candel_state = "green"
                         elif point_open == point_close:
                           candel_state = "doji"  
                 
                        #  print("candel_state:" , candel_state)
                 
                         # cal_point = LINE.cal_point_line(1 , timestamp_pulback)
                         # print("cal_point:" , cal_point)
                         cal_line_rec =  LINE.line_run(candel_num , self.symbol_EURUSD , timestamp_pulback4 )
                        #  print("cal_line:" , cal_line)
                         cal_line = cal_line_rec[0]
                        #  print("cal_line:" , cal_line)

                         cal_list_line = cal_line_rec[1]

                         list_cal_line = cal_line

                         if line_POS != 0:
                                    
                               xxx = line_POS - 1
                               cal_line = cal_line[xxx]
                               cal_line = [cal_line]

                         if (candel_state == "red" and point_open > point_close_p and type == "Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    # print("gap_point:" , gap_point)
                                    cal_point = float(gap_point)
                                    line_pullback = line + 1
                                   #  

                                    if point_open == cal_point:
                                          #  print("1111111111111111111111111111111111111111111111")
                                          #  print("point_open:" , point_open)
                                          #  print ("line:" , line + 1)
                                          #  print("pullback MMMMMMMMMMMMMMMM")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                          #  print("status_trade:" , status_trade)
                                           
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_sell(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                       #  print("rec_pos:" , rec_pos)
                                                       #  print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"       

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pullback_now:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: red)" + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         elif (candel_state == "green" and point_open < point_close_p and type == "R_Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    # print("gap_point:" , gap_point)
                                    cal_point = float(gap_point)
                                    line_pullback = line + 1
                                   

                                    if point_open == cal_point:
                                          #  print("2222222222222222222222222222222222222222222222")
                                          #  print("point_open:" , point_open)
                                          #  print ("line:" , line + 1)
                                          #  print("pullback HHHHHHHHHHHHHHHH")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                          #  print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_buy(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                       #  print("rec_pos:" , rec_pos)
                                                       #  print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pullback_now:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: green)" + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break    
                                               
                         if (candel_state == 'doji' and point_open > point_close_p and point_open > point_open_n and type == "Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    print("gap_point:" , gap_point)
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                           print("1111111111111111111111111111111111111111111111")
                                           print("point_open:" , point_open)
                                           print ("line:" , line + 1)
                                           print("pullback MMMMMMMMMMMMMMMM") 
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                           print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                     rec_pos = BUY_SELL.pos_sell(point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                     execution = rec_pos.comment
                                                     if execution == 'Request executed':
                                                        ticket =  rec_pos.order
                                                        print("rec_pos:" , rec_pos)
                                                        print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"

                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pullback_now:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: doji)"  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         elif (candel_state == "doji" and point_open < point_close_p and point_open < point_open_n and type == "R_Head_Shoulder"):

                              for line , gap_point in enumerate(cal_line):
                                    print("gap_point:" , gap_point)
                                    cal_point = float(gap_point)
                                   #  print("cal_point:" , cal_point)
                                    line_pullback = line + 1

                                    if point_open == cal_point:
                                           print("22222222222222222222222222222222222222222")
                                           print("point_open:" , point_open)
                                           print ("line:" , line + 1)
                                           print("pullback HHHHHHHHHHHHHHHHHH")
                                           time_command = pd.to_datetime( timestamp_pulback4 , unit='s')
                                           shakhes = LINE.line_shakhes(candel_num , self.symbol_EURUSD , self.decimal_sambol , point_open)
                                           status_trade = shakhes[1]
                                           print("status_trade:" , status_trade)
                                           shakhes = int (shakhes[0])
                                           commands = f'{candel_num}' + "_" + f'R_H' + "_" + f'{line_pullback}' + '_' + f'{shakhes}' + "_" + f'{4}'
                                           ticket = 0
                                           execution = 0
                                           if status_trade == True:
                                                # print("shakhes: True" )
                                                if line_POS == line_pullback or line_POS == 0:
                                                      rec_pos = BUY_SELL.pos_buy( point_open , shakhes , lot , self.symbol_EURUSD , commands)
                                                      execution = rec_pos.comment
                                                      if execution == 'Request executed':
                                                         ticket =  rec_pos.order
                                                         print("rec_pos:" , rec_pos)
                                                         print("ticket:" , ticket)
                                                else :
                                                      execution = "The line is not equal"
         
                                           command = "(Patern:" + f'{candel_num})' + " _ " + "(Type:" + f'{type})' + " _ " + "(Line:" + f'{line_pullback})' + ' _ ' + "(Shakhes:" + f'{shakhes})' + " _ " + "(Pullback_now:" f'{4})'+ " _ " + "(Point7:" + f'{point_open})' + " _ " + "(Time:" + f'{time_command})' + " _ " + "(candel_state: doji)"  + " _ " + "(Status_trade:" + f'{status_trade})' + " _ " + "(ticket:" + f'{ticket})'+ " _ " + "(execution:" + f'{execution})' + " _ " + "(list_line:" + f'{list_cal_line})' + " _ " + "(list_line:" + f'{cal_list_line})' 
                                           if line_POS == 0 or line_POS == line_pullback:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "true" , ticket , line_pullback , candel_num)
                                           else:
                                                        Database.update_table_chek(point_open , timestamp_pulback4 , command , "false" , ticket , line_POS , candel_num)
                                                
                                           exit = 1
                                           break
                                    
                         if exit == 1:
                             break
                       
                    
   