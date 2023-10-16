def short_word_treatment(text,add_words=False,word=None,remove_words=None,remove_all=False):
    '''

    ABOUT:
        This function takes a text input and processes it to expand commonly used short words or acronyms
        into their full forms. It also provides options to add custom short words and their corresponding full
        forms, remove existing short words, and display the most frequently used short words, you can use your 
        own short words too.

    Parameters:
        text (str): The input text to be processed.

        add_words (bool): If True, additional custom short words and their corresponding full forms
                          will be added . Default is False.

        word (dict): A dictionary containing custom short words as keys and their corresponding full
                     forms as values. This parameter is used when add_words is set to True. Default is None.

        remove_words (list): A list of short words to be removed . Default is None.
        
        remove_all (bool): If True, the function will remove all the predefine short words, by using this parameter you can
                           use your own short words only, If False then the function will use all the pre and userdefine 
                           short words during the treatment 



    Returns:
        str: The processed text with short words expanded into their full forms.

    Example:
        input_text = "OMG, BTW IRL, JK! LOL"
        expanded_text = short_word_treatment(input_text)
        print(expanded_text)
    Notes:
        If you wish to retain only a few words, you can achieve that through parameter tuning.
    Output:
        "Oh my God, By the way In real life, Just kidding! Laugh out loud" '''

    wt=[]
    try:
      
      import warnings
      warnings.filterwarnings('ignore')

      d={'LOL': 'Laugh out loud',
      'BRB': 'Be right back',
      'OMG': 'Oh my God',
      'TTYL': 'Talk to you later',
      'BTW': 'By the way',
      'SMH': 'Shaking my head',
      'IMO': 'In my opinion',
      'FYI': 'For your information',
      'JK': 'Just kidding',
      'ROFL': 'Rolling on the floor laughing',
      'NP': 'No problem',
      'TMI': 'Too much information',
      'ASAP': 'As soon as possible',
      'GTG': 'Got to go',
      'IMO': 'In my opinion',
      'AFK': 'Away from keyboard',
      'NVM': 'Never mind',
      'OP' : 'Over power',
      'ILU': 'I love you',
      'BC' : 'Because',
      'DM' : 'Direct message',
      'FTW': 'For the win',
      'IDK': "I don't know",
      'IRL': 'In real life',
      'LMK': 'Let me know',
      'NBD': 'No big deal',
      'SU' : 'Shut up',
      'THX': 'Thanks',
      'ST' : 'Stop talking',
      'YOLO':'You only live once',
      'WTH' :'What the hack',
      'GL' : 'Good luck',
      'BOL':'Best of luck',
      'OMW': 'On my way',
      'IDC': "I don't care",
      'TBH': 'To be honest',
      'IWB': 'I will be back',
      'OTW': 'On the way',
      'U'  : 'You',
      'WKLY':'Weekly',
      'COMP':'Competition',
      'R'  : 'Are',
      'TBH': 'To be honest','CAJ':'Casual','OFC':' Of course','TBF':'To be fair','IKR':'I know, right','STFU':'Shut the fuck up','TMB':'Text me back',
      'R8' : 'Right','SRY':'Sorry','GJ':'Good job','W8AM':' Wait a minute','PIC':'Picture','KK':'Okay cool','GM':'Good morning','L8R':'Later',
      'BBL':'Be back later','SEC':'Second','NC':'No comment','B4':'Before','BB':'Bye bye','XOXO':'Hugs and kisses','IMO':'In my opinion','ZZZ':'Sleeping',
      'JJ':'Just joking','F2F':'Face to face','CU':'See you','FAB':'Fabulous','TXT':'Text','M8':'Mate','DND':'Do not disturb','ILY':'I love you',
      'Q4U':'Question for you','TYT':'Take your time','LMA':'Leave me alone','5N':'Fine','Tho':'Though'}
      
      a=0
      c='Pre'
      df=0
      data=0
      df_sorted=0
      short=[]
      w=[]
      d1=[]
      
      if remove_all == True:
        d.clear()
      if add_words== True:
          #d1={f1:f2 for f1,f2 in zip(word,full_form)}
          for i,j in word.items():
              d[i]=j
      if remove_words != None:
          for k in remove_words:
              d.pop(k)

      pun=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]
      
      for i in pun:
        text=text.replace(i, ' ' + i + ' ')
        
      text1=text.upper()
      for i in text1.split():
            wt.append(i)

      for word in wt:
          if word in d:
            short.append(word)
            ind=wt.index(word)
            wt[ind]=d[word]
      #a=Counter(short)
      wt
      text1=' '.join([w for w in wt])
      
      return text1.lower()
    except ImportError as ip:
      print(ip)
    except ValueError as vs:
      print(vs)
    except TypeError as ts:
      print(ts)
    except NameError as ns:
      print(ns)
    except Exception as ex:
      print(ex)