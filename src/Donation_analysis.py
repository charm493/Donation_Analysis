""" Donation_analysis.py
    Yujing Li 
    02/09/2018
"""


import heapq


"""
   ParseFile: get CMTE_ID, Name, Zip, Date, and Amount information for each donation recode from file
"""
def ParseFile(file_name):

  infor = []

  with open(file_name) as openfileobject:
    for line in openfileobject:

      line = line.split('|') 

      CMTE_ID = line[0]
      Name = line[7]
      Zip = line[10]
      Date = line[13]
      Amount = line[14]
      Other_ID = line[15]
      
      # clean data 
      if (CMTE_ID != '')  and (Name != '')  and (Zip != '') and (Amount != '') and (Other_ID == ''):
        Zip = Zip[ :5]
        Date = Date[4: ]

        infor.append((CMTE_ID, Name, Zip, Date, Amount))
      
  return infor




"""
   Read_Perc: read file and get percentage to calculate percentile
"""
def Read_Perc(file_name):
  perc = int(open(file_name, 'r+').readline())
  return perc




"""
   Donation_Analysis: do analysis for all donation information
"""
def Donation_Analysis(perc, donation_list):

  repeat = {}      
  checked = {}     

  for recode in donation_list:
    CMTE_ID = recode[0]
    Name = recode[1]
    Zip = recode[2]
    Date = recode[3]
    Amount = int(recode[4])

    donor = str(Name + Zip)
    donation = [str(CMTE_ID + Zip + Date), Amount]


    if donor in checked: # check if the donor donated before 
      
      Checked_donation = checked[donor] 
      repeat.update({Checked_donation[0] : [Checked_donation[1]]})

      if donation[0] in repeat:  # check if the donation information of the repeat donor is same with other

        """
           Every time put the total money amount to the last position of the money_list
           at the second time, useing total amount plus the new amount to get the new total value
           then save the new total value and remove old total value
        """
        total = money_list[-1] 
        money_list.remove(money_list[-1])  

        money_list = repeat[donation[0]]
        money_list.append(Amount)

        total += money_list[-1]
        money_list.append(total)  
        percent_list = money_list[ :-1]
        
        p = percentile(perc, percent_list)
        l = len(percent_list)

        print CMTE_ID + '|' + Zip + '|' + Date + '|' + str(p) + '|' + str(total) + '|' + str(l)

      else:  
        repeat.update({donation[0] : [Amount]})  # put the donation information into the dict

        money_list = repeat[donation[0]]
        money_list.append(Amount) 
        percent_list = money_list[ :-1]  

        p = percentile(perc, percent_list)
        l = len(percent_list)

        print CMTE_ID + '|' + Zip + '|' + Date + '|' + str(p) + '|' + str(Amount) + '|' + str(l)
        
    else:
      checked.update({donor : donation})  # put the donor information into the dict

  

  

def percentile(perc, numbers):
  nums = heapsort(numbers)
  n_index = perc * len(nums) / 100 
  if perc % 100 == 0:
    n_index -= 1
  n = nums[n_index]

  return n



def heapsort(numbers):
  h = []
  f = []
  for value in numbers:
    heapq.heappush(h, value)
  for i in range(len(h)):
    num = heapq.heappop(h) 
    f.append(num)
  return f
 



information = ParseFile("itcont_test.txt")

perc = Read_Perc("percentile.txt")

Donation_Analysis(perc, information)

