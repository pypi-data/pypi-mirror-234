import MetaTrader5 as mt5
import pandas as pd
import json


from database_ex_forex_next3 import Database
from decimal import Decimal

from line_ex_forex_next3 import LINE

class Trust_Patern_full:
        
        def __init__(self):

            fileObject = open("login.json", "r")
            jsonContent = fileObject.read()
            aList = json.loads(jsonContent)
            
            self.login = int (aList['login'])
            self.Server = aList['Server'] 
            self.Password = aList['Password'] 
            self.symbol_EURUSD = aList['symbol_EURUSD'] 
            self.decimal_sambol = int (aList['decimal_sambol'] )
             
        def decimal(num , decimal_sambol):
            telo = '0.0'
            for i in range(decimal_sambol - 2):  
              telo = telo + "0"
            telo = telo + "1" 
            telo = float (telo)
            decimal_num = Decimal(str(num))
            rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
            return rounded_num  

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
          
        def patern_true(candel_num ,  timestamp):
            
                timestamp_pulback = timestamp
              #   print("timestamp_pulback:" , pd.to_datetime( timestamp_pulback , unit='s'))
                utc_from = pd.to_datetime( timestamp_pulback , unit='s') 
                utc_to = pd.to_datetime( timestamp_pulback + 60 , unit='s')
                ticks = mt5.copy_ticks_range(Trust_Patern_full().symbol_EURUSD , utc_from, utc_to , mt5.COPY_TICKS_ALL)
              #   print("ticks:" , ticks)
                list_pullback3 = []
                for lists in ticks:
                    xx = Trust_Patern_full.decimal(lists[1] , Trust_Patern_full().decimal_sambol)
                   #  print(xx)
                    xx = float(xx)
                    list_pullback3.append(xx)
                
              #   print("list_pullback3:" , list_pullback3)
                
                cal_line_rec =  LINE.line_run(candel_num , Trust_Patern_full().symbol_EURUSD , timestamp_pulback )
                cal_line = cal_line_rec[0]
                # print("cal_line:" , cal_line)
        
                return cal_line
        
        def trust_patern(candel_num , status):
                         
                   if status == "true":      
           
                         rec = Database.select_table_One(candel_num)
                        #  print("rec:" , rec)
                         timepstamp = rec[0][19]
                         timepstamp = json.loads(timepstamp)
                         timestamp_point3 = int(timepstamp[2])
                         timestamp_point1 = int(timepstamp[0])
                         timestamp_point1 = timestamp_point1 - 900

                         # print("timestamp_point3:" , timestamp_point3)
                         
                         timecandel_patern = mt5.copy_rates_range(Trust_Patern_full().symbol_EURUSD, mt5.TIMEFRAME_M15, timestamp_point1, timestamp_point3)
                        #  print("timecandel_patern:" , timecandel_patern)
                         
                         status_trust_patern = False
                         exit = 0
            
                         list_close = []
                         list_timestamp = []
                         list_open = []
            
                    
                         for index , index_patern in enumerate(timecandel_patern): 
                               
                           #     print ("index:" , index)
            
                               timestamp_patern = index_patern[0] 
                            #    print("index_patern:" , index_patern)
                         
                               close_patern = index_patern[4]
                               close_patern = Trust_Patern_full.decimal(close_patern ,Trust_Patern_full().decimal_sambol)
                               close_patern = float(close_patern)
                         
                               open_patern = index_patern[1]
                               open_patern = Trust_Patern_full.decimal(open_patern , Trust_Patern_full().decimal_sambol)
                               open_patern = float(open_patern)
            
                               list_close.append(close_patern)
                               list_timestamp.append(timestamp_patern)
                               list_open.append(open_patern)
                               
            
                           #     print("timestamp_patern:" , timestamp_patern)
                           #     print("timestamp_patern:" , pd.to_datetime( timestamp_patern , unit='s'))
                            #    print("close_patern:" , close_patern)
                           #     print("open_patern:" , open_patern)
                         
                               color_candel = Trust_Patern_full.candelstate(open_patern , close_patern)
                           #     print("color_candel:" , color_candel)
            
                               
                               cal_line =  LINE.line_run_15mine(candel_num , Trust_Patern_full().symbol_EURUSD , timestamp_patern )
                               
                            #    print("cal_line:" , cal_line)
            
            
                         list_close.reverse()
                         list_timestamp.reverse()
                         list_open.reverse()
                        #  print ("list_close:" , list_close)
                        #  print ("list_open:" , list_open)
                        #  print ("list_timestamp:" , list_timestamp)
            
            
                         for index , point_timestamps in enumerate(list_timestamp):
            
                            
                            # print("point_timestamp:" , point_timestamp)
                            
                              
                            try:  
                                 
            
                                 point_A_close = list_close[index]
                                 point_B_close = list_close[index + 1] 
                                 point_A_open = list_open[index ]
            
                                 point_timestamp_p = list_timestamp [index + 1]
                                 point_timestamp = list_timestamp [index ]
            
                                 cal_line_p =  LINE.line_run_15mine(candel_num , Trust_Patern_full().symbol_EURUSD , point_timestamp_p )
                                 cal_line =  LINE.line_run_15mine(candel_num , Trust_Patern_full().symbol_EURUSD , point_timestamp )
                                
                                 point_line = cal_line[0]
                                 point_line = float (point_line)
            
                                 point_line_p= cal_line_p[0]
                                 point_line_p = float (point_line_p)
            
                                 print( pd.to_datetime( list_timestamp [index] , unit='s') )
            
                                 color_candel = Trust_Patern_full.candelstate(point_A_open , point_A_close)
            
                                #  print("point_A_close:" , point_A_close)
                                #  print("point_B_close:" , point_B_close)
                                #  print("point_A_open:" , point_A_open)
                                #  print("point_line_p:" , point_line_p)
                                #  print("point_line:" , point_line)
                                #  print("color_candel:" , color_candel)


                                 if color_candel == "green":
            
                                    # if point_line_p <= point_line  and point_A_close >= point_line and point_B_close <= point_line_p and index != 0 or (point_line >= point_A_open and point_line <= point_A_close and index != 0):
                                      if point_line_p <= point_line  and point_A_close >= point_line and point_B_close <= point_line_p and index != 0 or (point_line >= point_A_open and point_line <= point_A_close and index != 0) :  
                                          
                                              print("11111111111111111111111111111111111111")
                                              status_trust_patern = True
                                              break

                                      elif point_line_p >= point_line and point_A_close >= point_line and point_B_close <= point_line_p and index != 0 or (point_line >= point_A_open and point_line <= point_A_close and index != 0):   
                                        
                                              print("22222222222222222222222222222222222222")
                                              status_trust_patern = True
                                              break
                                          
                                 elif color_candel == "red":
                                      
                                    # if point_line_p <= point_line and point_B_close >= point_line_p and point_A_close <= point_line and index != 0 or (point_line <= point_A_open and point_line >= point_A_close and index != 0):
                                    if point_line_p <= point_line and point_B_close >= point_line_p and point_A_close <= point_line and index != 0 or (point_line <= point_A_open and point_line >= point_A_close and index != 0):
                                          
                                              print("11111111111111111111111111111111111111")
                                              status_trust_patern = True
                                              break

                                    if point_line_p >= point_line and point_B_close >= point_line_p and point_A_close <= point_line and index != 0 or (point_line <= point_A_open and point_line >= point_A_close and index != 0):
                                         
                                              print("2222222222222222222222222222222222222")
                                              status_trust_patern = True 
                                              break   
                
            
                                #  print("")      
            
            
                            except:
                                 print("The end")     
                              
            
                         if status_trust_patern == False:
                              print("Trust_patern fault")
                              Database.update_table_trust_patern_full("false" , candel_num) 
            
                         elif status_trust_patern == True:
                              print("Trust_patern True")
                              Database.update_table_trust_patern_full("true" , candel_num) 
                                   

                         return status_trust_patern
        
                   elif status == "false":
                        
                        Database.update_table_trust_patern_full("true" , candel_num) 
                        return True
                        