import json
import MetaTrader5 as mt5

from database_ex_forex_next3 import Database
import pandas as pd

class Candel:

    def timecandel(symbol , timestamp ):
    # def timecandel(symbol):
      try:
          timecandel = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M15, timestamp, 31)

          len_timecandel = len(timecandel)


          print ("timecandel:" , timecandel)
          print ("len_timecandel:" , len_timecandel)

        #   timecandel = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 25)
        #   timecandel = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 24)

          return timecandel
      except:
          return False
      
    def candelstate(x , listOpen , listClose):
         candel_open = listOpen[x]
         candel_close = listClose[x]
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

class Candel_pos:
    

   def candel_red (listOpen , listClose , listTimestamp):

       candel = []
       EP1 = []
       x = 0
       candel_num = 0
       original_range = range(0, 30)
       reversed_range = list(original_range)[::-1]
    #    print("reversed_range:" , reversed_range)
       for num in reversed_range:
        
                   candel_state = Candel.candelstate(num , listOpen , listClose)  
                #    print("i:" , num) 
       
                   
                #    print("candel0: " + f'{candel_state}') 
                   candel.append(candel_state)
                   if candel_state == "red": 
                        x_node = 29 - num
                        print ("x_node:" , x_node)
                        EP1.append(num + x_node)
                        EP1.append(num)
                        original_range = range(0, num)
                        reversed_range2 = list(original_range)[::-1]
                        # print("reversed_range2:" , reversed_range2)
                        for i2 in reversed_range2 :  
                            candel_state = Candel.candelstate(i2 , listOpen , listClose) 
                            # print("i2:" , i2)    
                            # print("candel1: " + f'{candel_state}')
                            candel.append(candel_state)
                            if candel_state == "green":
                              
                              print("i2:" , i2)
                              
                              EP1.append(i2)
                              
                             
                              original_range = range(0, i2)
                              reversed_range3 = list(original_range)[::-1]
                            #   print("reversed_range3:" , reversed_range3)
                              for i3 in reversed_range3:  
                                   candel_state = Candel.candelstate(i3 , listOpen , listClose)   
                                #    print("i3:" , i3)   
                                #    print("candel2: " + f'{candel_state}')
                                   candel.append(candel_state)
                                   if candel_state == "red":
                                      EP1.append(i3)

                                      print("i3:" , i3)

                                      original_range = range(0, i3)
                                      reversed_range2 = list(original_range)[::-1]

                                      for i4 in reversed_range2 :  
                                           candel_state = Candel.candelstate(i4 , listOpen , listClose) 
                                           # print("i2:" , i2)    
                                           # print("candel1: " + f'{candel_state}')
                                           candel.append(candel_state)
                                           if candel_state == "green":
                                                EP1.append(i4) 
                                                print("i4:" , i4)
                                                original_range = range(0, i4)
                                                reversed_range2 = list(original_range)[::-1]

                                                for i5 in reversed_range2 :  
                                                    candel_state = Candel.candelstate(i5 , listOpen , listClose) 
                                                    # print("i2:" , i2)    
                                                    # print("candel1: " + f'{candel_state}')
                                                    candel.append(candel_state)
                                                    if candel_state == "red":
                                                         EP1.append(i5) 
                                                         print("i5:" , i5)

                                                         print("the end")
                                                         x = 1
                                                         break
                                                    
                                           if x == 1:
                                             break         

                                   if x == 1:
                                     break    
                                      
                            if x == 1:
                                  break  
                   if x == 1:
                         break    

       prices_candel_close = []
       prices_candel_open = []
       time_candel = []
       times = []

       EP1.reverse()
        
       for index in EP1: 
            prices_candel_close.append(listClose[index])
            prices_candel_open.append(listOpen[index])
            time_candel.append(str (listTimestamp[index]))
            times.append(str (pd.to_datetime( listTimestamp[index] , unit='s'))) 


       print("EP1:" , EP1)  
    #    print("prices_candel_close:" , prices_candel_close) 
    #    print("EP_point4:" , prices_candel_close[3])
       
       x1 = prices_candel_close[3]
       x2 = prices_candel_close[1]
       x3 = prices_candel_close[5]

       print("prices_candel_close:" , prices_candel_close)

       print("x1:" , x1)
       print("x2:" , x2)
       print("x3:" , x3)
        
       list_len = len(EP1)

       try:
         select_all = Database.select_table_All()
         # print("select_all:" , select_all)
         if select_all == []:
          candel_num = 1 
         else:
              
              select_all_len = len(select_all)
              print("select_all_len:" , select_all_len)
              rec = select_all[select_all_len - 1]
            #   print("select_all:" , rec)
              candel_num = int (rec[1])
            #   print("rec:" , rec)
              candel_num = candel_num + 1
              print("candel_num:" , candel_num)

       except:
          print("erooooor select_all")

       if list_len == 6 and x == 1 and x1 > x2 and x1 > x3:
            end = EP1[0]
            point = EP1[5]
            print("end:" , end)
            time_end_patterns =  listTimestamp [end]  
            time_start_patern = listTimestamp [point]
            # print("time_end_pattern:" , time_end_pattern)
            time_end_pattern = time_end_patterns + 27000
            # print("time_end_pattern:" , time_end_pattern)
            time_start_patern = time_start_patern + 1800
            # print("time_start_pattern:" , time_start_patern)

            EP1 = json.dumps(EP1)
            candel = json.dumps(candel)
            prices_candel_close = json.dumps(prices_candel_close)
            prices_candel_open = json.dumps(prices_candel_open)
            time_candel = json.dumps(time_candel)
            times = json.dumps(times)
            value = (candel_num , "Head_Shoulder" , EP1 , "" , "" , "" , candel , prices_candel_open ,prices_candel_close , "" , "" , "" , "" , "false", "true" , "false" , time_start_patern , time_end_pattern ,time_candel , times , 0 , "0" , "false" , "" , "" , "" , "" , "")

            Database.insert_table(value)

            status = True
      
       else:
           status = False

       return status    

   def candel_green (listOpen , listClose , listTimestamp):
       
       status = None

       candel = []
       EP1 = []
       x = 0
       candel_num = 0
       original_range = range(0, 30)
       reversed_range = list(original_range)[::-1]
    #    print("reversed_range:" , reversed_range)
       for num in reversed_range:
         
                   candel_state = Candel.candelstate(num , listOpen , listClose)  
                #    print("i:" , num) 
       
                #    print("candel0: " + f'{candel_state}') 
                   candel.append(candel_state)
                   if candel_state == "green": 
                        x_node = 29 - num
                        EP1.append(num + x_node)
                        EP1.append(num)
                        original_range = range(0, num)
                        reversed_range2 = list(original_range)[::-1]
                        # print("reversed_range2:" , reversed_range2)
                        for i2 in reversed_range2 :  
                            candel_state = Candel.candelstate(i2 , listOpen , listClose) 
                            # print("i2:" , i2)    
                            # print("candel1: " + f'{candel_state}')
                            candel.append(candel_state)
                        
                            if candel_state == "red":
                              EP1.append(i2)
                              
                              original_range = range(0, i2)
                              reversed_range3 = list(original_range)[::-1]
                            #   print("reversed_range3:" , reversed_range3)
                              for i3 in reversed_range3:  
                                   candel_state = Candel.candelstate(i3 , listOpen , listClose)   
                                #    print("i3:" , i3)   
                                #    print("candel2: " + f'{candel_state}')
                                   candel.append(candel_state)
                                   if candel_state == "green":
                    
                                      EP1.append(i3)

                                      original_range = range(0, i3)
                                      reversed_range3 = list(original_range)[::-1]

                                      for i4 in reversed_range3:  
                                           candel_state = Candel.candelstate(i4 , listOpen , listClose)   
                                           # print("i3:" , i3)   
                                        #    print("candel2: " + f'{candel_state}')
                                           candel.append(candel_state)
                                           if candel_state == "red":
                                                
                                                EP1.append(i4)

                                                original_range = range(0, i4)
                                                reversed_range3 = list(original_range)[::-1]

                                                for i5 in reversed_range3:  
                                                    candel_state = Candel.candelstate(i5 , listOpen , listClose)   
                                                    # print("i3:" , i3)   
                                                    candel.append(candel_state)
                                                    if candel_state == "green":
                                                         
                                                         EP1.append(i5)

                                                         print("the end")
                                                         x = 1
                                                         break

                                           if x == 1:
                                             break
                                      
                                   if x == 1:
                                     break    
                                      
                            if x == 1:
                                  break  
                   if x == 1:
                         break   

       prices_candel_close = []
       prices_candel_open = []
       time_candel = []
       times = []

       EP1.reverse()
       candel.reverse()
        
       for index in EP1: 
            prices_candel_close.append(listClose[index])
            prices_candel_open.append(listOpen[index])
            time_candel.append(str (listTimestamp[index]))
            times.append(str (pd.to_datetime( listTimestamp[index] , unit='s')))                   
                           
 
       print("EP1:" , EP1) 

    #    print("time_candel:" , time_candel) 
       print("EP_point4:" , prices_candel_close[3])
       x1 = prices_candel_close[3]
       x2 = prices_candel_close[1]
       x3 = prices_candel_close[5]

       print("prices_candel_close:" , prices_candel_close)

       print("x1:" , x1)
       print("x2:" , x2)
       print("x3:" , x3)

       list_len = len(EP1)
       
       try:
         select_all = Database.select_table_All()
         # print("select_all:" , select_all)
         if select_all == []:
          candel_num = 1 
         else:
              
              select_all_len = len(select_all)
              print("select_all_len:" , select_all_len)
              rec = select_all[select_all_len - 1]
            #   print("select_all:" , rec)
              candel_num = int (rec[1])
            #   print("rec:" , rec)
              candel_num = candel_num + 1
              print("candel_num:" , candel_num)

       except:
          print("erooooor select_all")

       if list_len == 6 and x == 1 and x1 < x2 and x1 < x3:
            end = EP1[0]
            point = EP1[5]
            print("end:" , end)
            time_end_pattern =  listTimestamp [end]  
            time_start_patern = listTimestamp [point]
            # print("time_end_pattern:" , time_end_pattern)
            time_end_pattern = time_end_pattern + 27000
            # print("time_end_pattern:" , time_end_pattern)
            time_start_patern = time_start_patern + 1800
            # print("time_start_patern:" , time_start_patern)

            EP1 = json.dumps(EP1)
            candel = json.dumps(candel)
            prices_candel_close = json.dumps(prices_candel_close)
            prices_candel_open = json.dumps(prices_candel_open)
            time_candel = json.dumps(time_candel)
            times = json.dumps(times)
            value = (candel_num , "R_Head_Shoulder" , EP1 , "" , "" , "" , candel , prices_candel_open ,prices_candel_close , "" , "" , "" , "" , "false", "true" , "false" , time_start_patern , time_end_pattern ,time_candel , times , 0 , "0" , "false" , "" , "" , "" , "" , "")
            Database.insert_table(value)
            
            status = True
       
       else:
             status = False

       return status        

   def candel_state_color(candel_state , listOpen , listClose , listTimestamp):
       
       if candel_state == "red":
         x = Candel_pos.candel_red(listOpen , listClose , listTimestamp)
         print ("red")
         print("x:" , x)
         return x

       elif candel_state == "green":
         x = Candel_pos.candel_green(listOpen , listClose , listTimestamp)    
         print ("green")  
         print("x:" , x)
         return x  
       