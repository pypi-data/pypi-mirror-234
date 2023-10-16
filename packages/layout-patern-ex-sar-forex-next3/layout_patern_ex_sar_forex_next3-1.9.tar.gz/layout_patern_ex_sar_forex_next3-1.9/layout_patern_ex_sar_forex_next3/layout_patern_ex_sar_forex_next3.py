import MetaTrader5 as mt5
import pandas as pd
import json


from database_ex_forex_next3 import Database
from decimal import Decimal



class Layout:
    
    def __init__(self):

            fileObject = open("login.json", "r")
            jsonContent = fileObject.read()
            aList = json.loads(jsonContent)
            
            self.login = int (aList['login'])
            self.Server = aList['Server'] 
            self.Password = aList['Password'] 
            self.symbol_EURUSD = aList['symbol_EURUSD'] 
            self.decimal_sambol = int (aList['decimal_sambol'] )

    def decimal_mov(decimal_sambol):
        x = 10
        for i in range(decimal_sambol):
           x = x * 10
        x = x / 10
        return x    
            
    
    def decimal(num , decimal_sambol):
            telo = '0.0'
            for i in range(decimal_sambol - 2):  
              telo = telo + "0"
            telo = telo + "1" 
            telo = float (telo)
            decimal_num = Decimal(str(num))
            rounded_num = decimal_num.quantize(Decimal(f'{telo}'))
            return rounded_num  

    def cal_layout(candel_num  , factor , min , max , status):
            
            

            if status == "true":       
          
                       rec = Database.select_table_One(candel_num)
                       timepstamp = rec[0][19]
                       type = rec[0][2]
                       timepstamp = json.loads(timepstamp)
                     #   print("timepstamp:" , timepstamp)
                     #   print("type:" , type)
             
                       Result_end = 0
             
                       timestamp_point2 = int(timepstamp[1]) + 840
                       timestamp_point3 = int(timepstamp[2]) + 840
                       timestamp_point4= int(timepstamp[3]) + 840
                       timestamp_point5 = int(timepstamp[4]) + 840
                       timestamp_point6 = int(timepstamp[5]) + 840
             
                       
                    #    print("timestamp_point2:" , pd.to_datetime( timestamp_point2 , unit='s'))
                    #    print("timestamp_point3:" , pd.to_datetime( timestamp_point3 , unit='s'))
                    #    print("timestamp_point4:" , pd.to_datetime( timestamp_point4 , unit='s'))
                    #    print("timestamp_point5:" , pd.to_datetime( timestamp_point5 , unit='s'))
                    #    print("timestamp_point6:" , pd.to_datetime( timestamp_point6 , unit='s'))
             
             
                       recive2 = mt5.copy_rates_from(Layout().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point2 , 1)
                       recive3 = mt5.copy_rates_from(Layout().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point3 , 1)
                       recive4 = mt5.copy_rates_from(Layout().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point4 , 1)
                       recive5 = mt5.copy_rates_from(Layout().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point5 , 1)
                       recive6 = mt5.copy_rates_from(Layout().symbol_EURUSD , mt5.TIMEFRAME_M1 , timestamp_point6 , 1)
             
                    #    print("recive2:" , recive2)
                    #    print("recive3:" , recive3)
                    #    print("recive4:" , recive4)
                    #    print("recive5:" , recive5)
                    #    print("recive6:" , recive6)
             
                       point_close2 = recive2[0][4]
                       point_close3 = recive3[0][4]
                       point_close4 = recive4[0][4]
                       point_close5 = recive5[0][4]
                       point_close6 = recive6[0][4]
             
             
                       point_close2 = Layout.decimal(point_close2 ,Layout().decimal_sambol)
                       point_close3 = Layout.decimal(point_close3 ,Layout().decimal_sambol)
                       point_close4 = Layout.decimal(point_close4 ,Layout().decimal_sambol)
                       point_close5 = Layout.decimal(point_close5 ,Layout().decimal_sambol)
                       point_close6 = Layout.decimal(point_close6 ,Layout().decimal_sambol)
             
                       point_close2 = float(point_close2)
                       point_close3 = float(point_close3)
                       point_close4 = float(point_close4)
                       point_close5 = float(point_close5)
                       point_close6 = float(point_close6)
             
             
                    #    print("point_close2:" , point_close2)
                    #    print("point_close3:" , point_close3)
                    #    print("point_close4:" , point_close4)
                    #    print("point_close5:" , point_close5)
                    #    print("point_close6:" , point_close6)
             
             
                       if type == "Head_Shoulder":
                             
                             Result_p2 = point_close2 - point_close3
                             Result_p2 = Layout.decimal(Result_p2 ,Layout().decimal_sambol)
                             Result_p2 = abs(Result_p2) 
                             print("Result_p2:" , Result_p2)
             
                             Result_p6 = point_close6 - point_close5
                             Result_p6 = Layout.decimal(Result_p6 ,Layout().decimal_sambol)
                             Result_p6 = abs(Result_p6) 
                             print("Result_p6:" , Result_p6)

                             Result_end = 0
             
                             if Result_p6 > Result_p2:
                                   
                                   Result_end = Result_p6 / Result_p2
                                   Result_end = round(Result_end , 2)
                                   print("Result_end:" , Result_end)
             
                             elif Result_p2 > Result_p6:  
             
                                   Result_end = Result_p2 / Result_p6
                                   Result_end = round(Result_end , 2)
                                   print("Result_end:" , Result_end)   
                             
                             Result_p2 = float(Result_p2)
                             Result_p6 = float(Result_p6)
         
                             Result_p11 = int (Result_p2 * Layout.decimal_mov(Layout().decimal_sambol))
                             Result_p22 = int (Result_p6 * Layout.decimal_mov(Layout().decimal_sambol))

                             
                             if Result_end <= factor and Result_p11 >= min and Result_p11 < max and Result_p22 > min and Result_p22 < max:
                                    
                                    Database.update_table_Layout_patern( "true" , candel_num)
                                    return True

                             else:
                                    Database.update_table_Layout_patern( "false" , candel_num)
                                    return False 
             

                       elif type == "R_Head_Shoulder":
                              
                             Result_p2 = point_close2 - point_close3
                             Result_p2 = Layout.decimal(Result_p2 ,Layout().decimal_sambol)
                             Result_p2 = abs(Result_p2) 
                             print("Result_p2:" , Result_p2)
             
                             Result_p6 = point_close6 - point_close5
                             Result_p6 = Layout.decimal(Result_p6 ,Layout().decimal_sambol)
                             Result_p6 = abs(Result_p6) 
                             print("Result_p6:" , Result_p6)
                             
                             Result_end = 0
             

                             if Result_p6 > Result_p2:
                                   
                                   Result_end = Result_p6 / Result_p2
                                   Result_end = round(Result_end , 2)
                                   print("Result_end6:" , Result_end)
             
             
                             elif Result_p2 > Result_p6:  
             
                                   Result_end = Result_p2 / Result_p6
                                   Result_end = round(Result_end , 2)
                                   print("Result_end2:" , Result_end)  
                           

                             Result_p2 = float(Result_p2)
                             Result_p6 = float(Result_p6)
         
                             Result_p11 = int (Result_p2 * Layout.decimal_mov(Layout().decimal_sambol))
                             Result_p22 = int (Result_p6 * Layout.decimal_mov(Layout().decimal_sambol)) 
                             print("Result_p11:" , Result_p11)
                             print("Result_p22:" , Result_p22)
             
                             
                             if Result_end <= factor and Result_p11 >= min and Result_p11 < max and Result_p22 > min and Result_p22 < max:
                                    
                                    Database.update_table_Layout_patern("true" , candel_num)
                                    return True

                             else:
                                    Database.update_table_Layout_patern("false" , candel_num)
                                    return False 

            elif status == "false":
                   
                   Database.update_table_Layout_patern( "true" , candel_num)
                   return True
                               
