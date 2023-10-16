def EmoTextHandeler(text,process_on='both',process_type='remove',add=None,add_em=None,remove=None,remove_em=None,remove_all=None,case='same'):
    """
    About:

        This function deals with emojis and emoticons and contains a lot of predefined emojis and emoticons within itself.

    
    Parameters:
        * text (str) : The input text to be processed.
        
        * process_on (str) --> ['emj','emt','both'] : if 'emj', then function will deal with emojis only,
                                                    if 'emt', then function will works on emoticons only,
                                                    if 'both', function would be able to deal with emojis as well as 
                                                            emoticons, Default is 'both'
                                                            
        * process_type (str) --> ['remove','replace'] : The function will remove emojis and emoticons if the value is set to 'remove,' 
                                                      and it will replace emojis or emoticons with text if the value is set to 'replace
        
        * add (str) --> ['emj'/'emoji' or 'emt'/'emoticon']: To add more emojis or emoticons, use the 'add_em' parameter. If the value is set to 'emj,'
                                                            you can add more emojis by the help of add_em parameter,
                                                            and if it's set to 'emt',
                                                            you can add more emoticons by the help of
                                                            add_em parameter. Default is None
                                                           
        * add_em (dict) : Provide emojis or emoticons and their meanings in the form of a dictionary. Default is None
        
        
        * remove (str) --> ['emj'/'emoji' or 'emt'/'emoticon']: To remove emojis or emoticons, use the 'remove_em' parameter. 
                                                              If the value is set to 'emj,' you can remove any emoji from a predefined set of emojis, 
                                                              and if the value is set to 'emt,' 
                                                              you can remove any emoticon from a predefined set of emoticons. Default is None
                                                              
        * remove_em (list) : List of emojis or emoticons that you want to remove from the predefined set of emojis or emoticons. Default is None
        
        
        * remove_all (str) --> ['emj','emt','both'] : This parameter is used to remove the predefined set of emojis, emoticons, or both. 
                                                    If the value is set to 'emj,' then all the predefined emojis will be removed.
                                                    If the value is set to 'emt,' the function will remove all predefined emoticons. 
                                                    To remove both predefined emojis and emoticons, set the value to 'both.' 
                                                    The default setting is 'both.
                                         
        * case (str) --> ['same','lower','upper']: A string specifying the desired letter case for the output text.
        
            - 'same': Keep the original letter case (default).
            - 'lower': Convert all letters to lowercase.
            - 'upper': Convert all letters to uppercase.
        
        
    Returns:
        str: The processed text based on the specified conditions.

    
    Usage:
        # processed_text = EmoTextHandeler(text=text,process_on='emj',process_type='replace',case='lower')
          print(processed_text)
        # processed_text = EmoTextHandeler(text=text,remove_all='emt',add='emt',add_em={"( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses"},remove='emj',
                                            remove_em=["👿","🤩"])
          print(processed_text)    
          
    Note:
        - This module allows you to remove, or replace words in the input text based on specified conditions.
        - You can customize the processing behavior by adjusting the function parameters.
        - This function provides the freedom to add or remove any emojis or emoticons.
        - It gives you the freedom to make it work with your specifically chosen emojis and emoticons also.
    """
    
    d = {
    "😀": "Grinning","😃": "Grinning with Big Eyes","😄": "Grinning with Smiling Eyes","😁": "Beaming with Smiling Eyes",
    "😆": "Grinning Squinting","😅": "Grinning with Sweat","🤣": "Rolling on the Floor Laughing","😂": "Face with Tears of Joy",
    "😊": "Smiling with Smiling Eyes","😇": "Smiling with Halo","🙂": "Slightly Smiling","🙃": "Upside-Down","😉": "Winking",
    "😌": "Relieved","😍": "Heart Eyes","😎": "Smiling with Sunglasses","🤩": "Star-Struck","😏": "Smirking","😐": "Neutral",
    "😑": "Expressionless","😒": "Unamused","😕": "Confused","🙁": "Slightly Frowning","😮": "Open Mouth","😯": "Hushed","😲": "Astonished",
    "😳": "Flushed","😦": "Frowning with Open Mouth","😧": "Anguished","😨": "Fearful","😰": "Anxious with Sweat","😥": "Sad but Relieved",
    "😢": "Crying","😭": "Loudly Crying","😱": "Screaming in Fear","😖": "Confounded","😣": "Persevering","😞": "Disappointed",
    "😓": "Downcast with Sweat","😩": "Weary","😫": "Tired","😤": "with Steam From Nose","😡": "Pouting","😠": "Angry","🤬": "with Symbols on Mouth",
    "😈": "Smiling with Horns","👿": "Angry with Horns","💀": "Skull","☠️": "Skull and Crossbones","💩": "Pile of Poo","🤡": "Clown",
    "👹": "Ogre","👺": "Goblin","👻": "Ghost","👽": "Alien","👾": "Alien Monster","🤖": "Robot","💋": "Kiss Mark","❤️": "Red Heart",
    "💔": "Broken Heart","❣️": "Heart Exclamation","💕": "Two Hearts","💞": "Revolving Hearts","💓": "Beating Heart","💗": "Growing Heart",
    "💖": "Sparkling Heart","💘": "Heart with Arrow","💝": "Heart with Ribbon","💙": "Blue Heart","💚": "Green Heart","💛": "Yellow Heart",
    "🧡": "Orange Heart","💜": "Purple Heart","🖤": "Black Heart","🤍": "White Heart","💯": "Hundred Points","🔥": "Fire","🌟": "Glowing Star",
    "✨": "Sparkles","🌈": "Rainbow","⭐": "Star","🌞": "Sun with Face","🌝": "Full Moon with Face","🌚": "New Moon with Face","🌍": "Earth Globe Europe-Africa",
    "🌎": "Earth Globe Americas","🌏": "Earth Globe Asia-Australia","🌱": "Seedling","🌼": "Blossom","🍁": "Maple Leaf","🍂": "Fallen Leaf",
    "🍃": "Leaf Fluttering in Wind","🌸": "Cherry Blossom","🌺": "Hibiscus","🌻": "Sunflower","🌴": "Palm Tree","🌵": "Cactus","🌾": "Sheaf of Rice","🌿": "Herb",
    "🍀": "Four Leaf Clover","🍁": "Maple Leaf","🍂": "Fallen Leaf","🍃": "Leaf Fluttering in Wind","🍇": "Grapes","🍈": "Melon",
    "🍉": "Watermelon","🍊": "Tangerine","🍋": "Lemon","🍌": "Banana","🍍": "Pineapple","🍎": "Red Apple","🍏": "Green Apple",
    "🍐": "Pear","🍑": "Peach","🍒": "Cherries","🍓": "Strawberry","🥝": "Kiwi Fruit","🍅": "Tomato","🍆": "Eggplant","🥑": "Avocado",
    "🥒": "Cucumber","🥕": "Carrot","🌽": "Ear of Corn","🌶️": "Hot Pepper","🥦": "Broccoli","🍄": "Mushroom","🥜": "Peanuts",
    "🌰": "Chestnut","🍞": "Bread","🥐": "Croissant","🥖": "Baguette Bread","🥨": "Pretzel","🥯": "Bagel","🥞": "Pancakes",
    "🧀": "Cheese Wedge","🍖": "Meat on Bone","🍗": "Poultry Leg","🥩": "Cut of Meat","🥓": "Bacon","🍔": "Hamburger","🍟": "French Fries",
    "🍕": "Pizza","🌭": "Hot Dog","🥪": "Sandwich","🍱": "Bento Box","🍲": "Pot of Food","🍛": "Curry Rice","🍜": "Steaming Bowl",
    "🍝": "Spaghetti","🍠": "Roasted Sweet Potato","🍢": "Oden","🍣": "Sushi","🍤": "Fried Shrimp","🍥": "Fish Cake with Swirl",
    "🍡": "Dango","🍦": "Soft Ice Cream","🍧": "Shaved Ice","🍨": "Ice Cream","🍩": "Doughnut","🍪": "Cookie","🎂": "Birthday Cake",
    "🍰": "Shortcake","🧁": "Cupcake","🥧": "Pie","🍫": "Chocolate Bar","🍬": "Candy","🍭": "Lollipop","🍮": "Custard","🍯": "Honey Pot",
    "🍼": "Baby Bottle","🥤": "Cup with Straw","🍺": "Beer Mug","🍻": "Clinking Beer Mugs","🥂": "Clinking Glasses","🥃": "Tumbler Glass","🍸": "Cocktail Glass",
    "🍹": "Tropical Drink","🍾": "Bottle with Popping Cork","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🍴": "Fork and Knife",
    "☕": "Hot Beverage","🍵": "Teacup without Handle","🍶": "Sake","🥢": "Chopsticks","🥄": "Spoon","🔪": "Kitchen Knife",
    "🏺": "Amphora","🍽️": "Fork and Knife with Plate","🧊": "Ice Cube","🥤": "Cup with Straw","🥢": "Chopsticks","🍽️": "Fork and Knife with Plate",
    "🧂": "Salt","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🧇": "Waffle","🧆": "Falafel","🥙": "Stuffed Flatbread","🌮": "Taco",
    "🌯": "Burrito","🍔": "Hamburger","🍟": "French Fries","🍕": "Pizza","🥪": "Sandwich","🍱": "Bento Box","🥗": "Green Salad",
    "🌞": "Sun","🌝": "Full Moon","🌚": "New Moon","🌛": "First Quarter Moon","🌜": "Last Quarter Moon","🌙": "Crescent Moon",
    "🌎": "Earth Globe Americas","🌍": "Earth Globe Europe-Africa","🌏": "Earth Globe Asia-Australia","🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain",
    "🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud","🌤️": "Sun Behind Small Cloud",
    "❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away","🌪️": "Tornado","🌫️": "Fog",
    "🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain","🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud",
    "🌤️": "Sun Behind Small Cloud","🌫️": "Fog","❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away",
    "🌪️": "Tornado","🌊": "Water Wave","🏄‍♂️": "Man Surfing","🏄‍♀️": "Woman Surfing","🏊‍♂️": "Man Swimming","🏊‍♀️": "Woman Swimming","🚣‍♂️": "Man Rowing Boat",
    "🚣‍♀️": "Woman Rowing Boat","🏆": "Trophy","🥇": "1st Place Medal","🥈": "2nd Place Medal","🥉": "3rd Place Medal","🏅": "Sports Medal",
    "🎖️": "Military Medal","🏵️": "Rosette","🎗️": "Reminder Ribbon","🎫": "Ticket","🎟️": "Admission Tickets","🎪": "Circus Tent",
    "🤹‍♀️": "Woman Juggling","🤹‍♂️": "Man Juggling","🎭": "Performing Arts","🎨": "Artist Palette","🎰": "Slot Machine","🎲": "Game Die",
    "🎯": "Direct Hit","🎳": "Bowling","🎮": "Video Game","🎰": "Slot Machine","🎲": "Game Die","🎳": "Bowling",
    "🥁": "Drum","🎷": "Saxophone","🎸": "Guitar","🎻": "Violin","🎺": "Trumpet","🎹": "Musical Keyboard","🎼": "Sheet Music",
    "🎧": "Headphone","🎤": "Microphone","🎬": "Clapper Board","🎥": "Movie Camera","📷": "Camera","📸": "Camera with Flash",
    "📽️": "Film Projector","📺": "Television","📻": "Radio","🎙️": "Studio Microphone","🎚️": "Level Slider","🎛️": "Control Knobs",
    "⏸️": "Pause Button","⏹️": "Stop Button","⏺️": "Record Button","📀": "DVD","💿": "Optical Disc","📼": "Videocassette",
    "🔊": "Loudspeaker","🔉": "Speaker Medium Volume","🔈": "Speaker Low Volume","🔇": "Muted Speaker","🔔": "Bell","🕭": "Bell with Slash",
    "📢": "Loudspeaker","📣": "Megaphone","🕯️": "Candle","💡": "Light Bulb","🔦": "Flashlight","🏮": "Red Paper Lantern","🪔": "Candle",
    "🧯": "Fire Extinguisher","🗑️": "Wastebasket","🧹": "Broom","🧺": "Basket","🧻": "Roll of Paper","🧼": "Soap","🧽": "Sponge",
    "🧴": "Lotion Bottle","🛁": "Bathtub","🚿": "Shower","🪒": "Razor","🧻": "Roll of Paper","🚽": "Toilet","🚪": "Door",
    "🪑": "Chair","🛋️": "Couch and Lamp","🪓": "Axe","🪔": "Diya Lamp","🪕": "Banjo","🪁": "Kite","🥎": "Softball","🥏": "Flying Disc",
    "🥍": "Lacrosse","🧿": "Nazar Amulet","🧩": "Puzzle Piece","🧸": "Teddy Bear","🧺": "Basket","💢":"Anger or Frustration",
    "💤":"Sleeping","💦":"Sweat droplets or spelling water","☮":"Peace","🕉":"Om","🕳":"Hole","🆚":"versus","♾":"Infinity",
    "⚛":"Atom","☢":"Radioactive","🚭":"No smoking","⚠":"Warning","♻":"Recycling","▶":"Play","⏸":"Pause","📈":"Increasing",
    "📉":"Decreasing","📕":"Red book","📒":"Yellow book","📗":"Green book","📊":"Bar chart","🐶":"Dog","🐱":"Cat","👀":"Eyes","🦊":"Fox","🦄":"Unicorn","🐔":"Chicken","🐲":"Dragon","🦓":"Zebra","🐨":"Koala",
    "🐼":"Panda","🐸":"Frog","🦝":"Raccoon","🐮":"Cow","🐷":"Pig","🐗":"Boar","🐭":"Mouse","🐹":"Hamster","🦒":"Giraffe",
    "🐟":"Fish","🦀":"Crab","🦠":"Microbe","🕷":"Spider","🕸":"Spider web","🦷":"Tooth","🦴":"Bone","🧠":"Brain","👣":"Footprints",
    "👅":"Tongue","👄":"Mouth","👸":"Princess","🤴":"Prince","👵":"Old woman","👼":"Baby angel","👮":"Female police officer","👮":"Male police officer",
    "🕵":"Detective","🕵":"Detective","👷":"Construction worker","👷🏻‍♀️":"Construction worker","👨🏻‍🏫":"Teacher","👰":"Bride",
    "🤰":"Preagnant","🛀":"Taking bath","🤝":"Handshake","👌🏻":"Perfect","🔑":"Key","🧬":"DNA","💊":"Pill","💣":"Bomb",
    "🔬":"Microscope","🖨":"Printer","💻":"Laptop","🔗":"Link","🚬":"Cigarette","🔋":"Battery","🔌":"Electric plug",
    "✂":"Scissiors","📌":"Pushpin","⌚":"Watch","⚰":"Coffin","📺":"TV"}
    
    d1 = {
    ":-)": "Smile",":-(": "Frown",":-D": "Big Grin",":-P": "Sticking Out Tongue",";-)": "Wink",":-|": "Indifferent",":-/": "Skeptical",
    ":-*": "Kiss",":-O": "Surprised",":-X": "Sealed Lips","<3": "Heart","^_^": "Happy","T_T": "Crying",":-]": "Happy",":-[": "Sad",
    ":-||": "Angry",":')": "Tears of Joy",":-B": "Nerd",":3": "Cute Face",":|]": "Robot",":-#": "Braces",":-&": "Sick",":-%": "Confused",":->": "Sarcastic",":-\\": "Shrug",
    ":')-<": "Crying with a Mustache",":-o)": "Clown","(^_^)": "Joyful","(-_-)": "Disapproval","(*_*)": "Amazement","(-.-)": "Sigh",
    "(@_@)": "Dazed","(/_\)": "Distressed","(\*_\*)": "Excited","(\^.^)": "Happy","(;_;)": "Tearful","(+_+)": "Agitated","(-.-;)": "Worried",
    "(o_o)": "Surprised","(>_>)": "Shifty Eyes","(-'_'-)": "Nervous","(*^_^*)": "Blushing","(^o^)": "Cheerful","(#^.^#)": "Pleased",
    "(;^_^)/": "Joy","(/o\\)": "Tension","(^_-)": "Wink","(T_T)/": "Bowing","(@.@)": "Staring","(~o~)": "Drooling","(-_-)zzz": "Sleeping",
    "(>_>)<": "Evil Grin","(*_*)>": "Hypnotized","d[-_-]b": "Listening to Music","(^0^)/": "Excited","(*_*;)": "Embarrassed","(o^^)o": "Applause",
    "(@_@;": "Dizzy","(^o^;)": "Sweating","(-_-)/": "Salute","(@o@)/": "Cheers",":-Oo": "Surprised","(^_-)b": "Thumbs Up","O_O": "Wide-Eyed",
    "(o_o)": "Staring","(=_=)": "Bored","(>_<)": "Angry","(o_0)": "Confused","(-.-')": "Annoyance","(-_-)ゞ": "Sigh","(^,^)": "Giggling",
    "(-_-メ)": "Dissatisfied","(^_~)": "Winking","(-_-)凸": "Flipping the Bird","(o_ _)o": "Apology","(°ロ°)": "Disapproval","(◠‿◠✿)": "Cuteness Overload","( ͡° ͜ʖ ͡°)": "Lenny Face",
    "( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses","(ง •̀_•́)ง": "Ready to Fight","¯_(ツ)_/¯": "Shrugging","( •_•)>⌐■-■": "Deal With It",
    "ಠ_ಠ": "Disapproval or Disbelief","(¬‿¬)": "Smirking","(¬_¬)": "Sarcasm","(☞ﾟヮﾟ)☞": "Finger Guns","(つ◕_◕)つ": "Sending a Hug",
    "( ͡~ ͜ʖ ͡°)": "Lenny Face with a Wink","(ง'̀-'́)ง": "Getting Ready for a Challenge","(¬‿¬) ": "Flirting","¯_(⊙_ʖ⊙)_/¯": "Confused Lenny Face",
    "(´・ω・)っ": "Kawaii Face","(••) ( ••)>⌐■-■ (⌐■_■)": "Sunglasses Deal With It","(¬‿¬) ": "Smirking with Style","(つ•̀ω•́)つ*:･ﾟ✧": "Sending Positive Vibes"}
    
    d2 = {
    "😀": "Grinning","😃": "Grinning with Big Eyes","😄": "Grinning with Smiling Eyes","😁": "Beaming with Smiling Eyes",
    "😆": "Grinning Squinting","😅": "Grinning with Sweat","🤣": "Rolling on the Floor Laughing","😂": "Face with Tears of Joy",
    "😊": "Smiling with Smiling Eyes","😇": "Smiling with Halo","🙂": "Slightly Smiling","🙃": "Upside-Down","😉": "Winking",
    "😌": "Relieved","😍": "Heart Eyes","😎": "Smiling with Sunglasses","🤩": "Star-Struck","😏": "Smirking","😐": "Neutral",
    "😑": "Expressionless","😒": "Unamused","😕": "Confused","🙁": "Slightly Frowning","😮": "Open Mouth","😯": "Hushed","😲": "Astonished",
    "😳": "Flushed","😦": "Frowning with Open Mouth","😧": "Anguished","😨": "Fearful","😰": "Anxious with Sweat","😥": "Sad but Relieved",
    "😢": "Crying","😭": "Loudly Crying","😱": "Screaming in Fear","😖": "Confounded","😣": "Persevering","😞": "Disappointed",
    "😓": "Downcast with Sweat","😩": "Weary","😫": "Tired","😤": "with Steam From Nose","😡": "Pouting","😠": "Angry","🤬": "with Symbols on Mouth",
    "😈": "Smiling with Horns","👿": "Angry with Horns","💀": "Skull","☠️": "Skull and Crossbones","💩": "Pile of Poo","🤡": "Clown",
    "👹": "Ogre","👺": "Goblin","👻": "Ghost","👽": "Alien","👾": "Alien Monster","🤖": "Robot","💋": "Kiss Mark","❤️": "Red Heart",
    "💔": "Broken Heart","❣️": "Heart Exclamation","💕": "Two Hearts","💞": "Revolving Hearts","💓": "Beating Heart","💗": "Growing Heart",
    "💖": "Sparkling Heart","💘": "Heart with Arrow","💝": "Heart with Ribbon","💙": "Blue Heart","💚": "Green Heart","💛": "Yellow Heart",
    "🧡": "Orange Heart","💜": "Purple Heart","🖤": "Black Heart","🤍": "White Heart","💯": "Hundred Points","🔥": "Fire","🌟": "Glowing Star",
    "✨": "Sparkles","🌈": "Rainbow","⭐": "Star","🌞": "Sun with Face","🌝": "Full Moon with Face","🌚": "New Moon with Face","🌍": "Earth Globe Europe-Africa",
    "🌎": "Earth Globe Americas","🌏": "Earth Globe Asia-Australia","🌱": "Seedling","🌼": "Blossom","🍁": "Maple Leaf","🍂": "Fallen Leaf",
    "🍃": "Leaf Fluttering in Wind","🌸": "Cherry Blossom","🌺": "Hibiscus","🌻": "Sunflower","🌴": "Palm Tree","🌵": "Cactus","🌾": "Sheaf of Rice","🌿": "Herb",
    "🍀": "Four Leaf Clover","🍁": "Maple Leaf","🍂": "Fallen Leaf","🍃": "Leaf Fluttering in Wind","🍇": "Grapes","🍈": "Melon",
    "🍉": "Watermelon","🍊": "Tangerine","🍋": "Lemon","🍌": "Banana","🍍": "Pineapple","🍎": "Red Apple","🍏": "Green Apple",
    "🍐": "Pear","🍑": "Peach","🍒": "Cherries","🍓": "Strawberry","🥝": "Kiwi Fruit","🍅": "Tomato","🍆": "Eggplant","🥑": "Avocado",
    "🥒": "Cucumber","🥕": "Carrot","🌽": "Ear of Corn","🌶️": "Hot Pepper","🥦": "Broccoli","🍄": "Mushroom","🥜": "Peanuts",
    "🌰": "Chestnut","🍞": "Bread","🥐": "Croissant","🥖": "Baguette Bread","🥨": "Pretzel","🥯": "Bagel","🥞": "Pancakes",
    "🧀": "Cheese Wedge","🍖": "Meat on Bone","🍗": "Poultry Leg","🥩": "Cut of Meat","🥓": "Bacon","🍔": "Hamburger","🍟": "French Fries",
    "🍕": "Pizza","🌭": "Hot Dog","🥪": "Sandwich","🍱": "Bento Box","🍲": "Pot of Food","🍛": "Curry Rice","🍜": "Steaming Bowl",
    "🍝": "Spaghetti","🍠": "Roasted Sweet Potato","🍢": "Oden","🍣": "Sushi","🍤": "Fried Shrimp","🍥": "Fish Cake with Swirl",
    "🍡": "Dango","🍦": "Soft Ice Cream","🍧": "Shaved Ice","🍨": "Ice Cream","🍩": "Doughnut","🍪": "Cookie","🎂": "Birthday Cake",
    "🍰": "Shortcake","🧁": "Cupcake","🥧": "Pie","🍫": "Chocolate Bar","🍬": "Candy","🍭": "Lollipop","🍮": "Custard","🍯": "Honey Pot",
    "🍼": "Baby Bottle","🥤": "Cup with Straw","🍺": "Beer Mug","🍻": "Clinking Beer Mugs","🥂": "Clinking Glasses","🥃": "Tumbler Glass","🍸": "Cocktail Glass",
    "🍹": "Tropical Drink","🍾": "Bottle with Popping Cork","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🍴": "Fork and Knife",
    "☕": "Hot Beverage","🍵": "Teacup without Handle","🍶": "Sake","🥢": "Chopsticks","🥄": "Spoon","🔪": "Kitchen Knife",
    "🏺": "Amphora","🍽️": "Fork and Knife with Plate","🧊": "Ice Cube","🥤": "Cup with Straw","🥢": "Chopsticks","🍽️": "Fork and Knife with Plate",
    "🧂": "Salt","🥄": "Spoon","🍽️": "Fork and Knife with Plate","🧇": "Waffle","🧆": "Falafel","🥙": "Stuffed Flatbread","🌮": "Taco",
    "🌯": "Burrito","🍔": "Hamburger","🍟": "French Fries","🍕": "Pizza","🥪": "Sandwich","🍱": "Bento Box","🥗": "Green Salad",
    "🌞": "Sun","🌝": "Full Moon","🌚": "New Moon","🌛": "First Quarter Moon","🌜": "Last Quarter Moon","🌙": "Crescent Moon",
    "🌎": "Earth Globe Americas","🌍": "Earth Globe Europe-Africa","🌏": "Earth Globe Asia-Australia","🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain",
    "🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud","🌤️": "Sun Behind Small Cloud",
    "❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away","🌪️": "Tornado","🌫️": "Fog",
    "🌧️": "Rain Cloud","⛈️": "Cloud with Lightning and Rain","🌩️": "Cloud with Lightning","🌦️": "Sun Behind Rain Cloud","🌥️": "Sun Behind Large Cloud",
    "🌤️": "Sun Behind Small Cloud","🌫️": "Fog","❄️": "Snowflake","🌨️": "Cloud with Snow","☃️": "Snowman","🌬️": "Wind Face","💨": "Dashing Away",
    "🌪️": "Tornado","🌊": "Water Wave","🏄‍♂️": "Man Surfing","🏄‍♀️": "Woman Surfing","🏊‍♂️": "Man Swimming","🏊‍♀️": "Woman Swimming","🚣‍♂️": "Man Rowing Boat",
    "🚣‍♀️": "Woman Rowing Boat","🏆": "Trophy","🥇": "1st Place Medal","🥈": "2nd Place Medal","🥉": "3rd Place Medal","🏅": "Sports Medal",
    "🎖️": "Military Medal","🏵️": "Rosette","🎗️": "Reminder Ribbon","🎫": "Ticket","🎟️": "Admission Tickets","🎪": "Circus Tent",
    "🤹‍♀️": "Woman Juggling","🤹‍♂️": "Man Juggling","🎭": "Performing Arts","🎨": "Artist Palette","🎰": "Slot Machine","🎲": "Game Die",
    "🎯": "Direct Hit","🎳": "Bowling","🎮": "Video Game","🎰": "Slot Machine","🎲": "Game Die","🎳": "Bowling",
    "🥁": "Drum","🎷": "Saxophone","🎸": "Guitar","🎻": "Violin","🎺": "Trumpet","🎹": "Musical Keyboard","🎼": "Sheet Music",
    "🎧": "Headphone","🎤": "Microphone","🎬": "Clapper Board","🎥": "Movie Camera","📷": "Camera","📸": "Camera with Flash",
    "📽️": "Film Projector","📺": "Television","📻": "Radio","🎙️": "Studio Microphone","🎚️": "Level Slider","🎛️": "Control Knobs",
    "⏸️": "Pause Button","⏹️": "Stop Button","⏺️": "Record Button","📀": "DVD","💿": "Optical Disc","📼": "Videocassette",
    "🔊": "Loudspeaker","🔉": "Speaker Medium Volume","🔈": "Speaker Low Volume","🔇": "Muted Speaker","🔔": "Bell","🕭": "Bell with Slash",
    "📢": "Loudspeaker","📣": "Megaphone","🕯️": "Candle","💡": "Light Bulb","🔦": "Flashlight","🏮": "Red Paper Lantern","🪔": "Candle",
    "🧯": "Fire Extinguisher","🗑️": "Wastebasket","🧹": "Broom","🧺": "Basket","🧻": "Roll of Paper","🧼": "Soap","🧽": "Sponge",
    "🧴": "Lotion Bottle","🛁": "Bathtub","🚿": "Shower","🪒": "Razor","🧻": "Roll of Paper","🚽": "Toilet","🚪": "Door",
    "🪑": "Chair","🛋️": "Couch and Lamp","🪓": "Axe","🪔": "Diya Lamp","🪕": "Banjo","🪁": "Kite","🥎": "Softball","🥏": "Flying Disc",
    "🥍": "Lacrosse","🧿": "Nazar Amulet","🧩": "Puzzle Piece","🧸": "Teddy Bear","🧺": "Basket","💢":"Anger or Frustration",
    "💤":"Sleeping","💦":"Sweat droplets or spelling water","☮":"Peace","🕉":"Om","🕳":"Hole","🆚":"versus","♾":"Infinity",
    "⚛":"Atom","☢":"Radioactive","🚭":"No smoking","⚠":"Warning","♻":"Recycling","▶":"Play","⏸":"Pause","📈":"Increasing",
    "📉":"Decreasing","📕":"Red book","📒":"Yellow book","📗":"Green book","📊":"Bar chart","🐶":"Dog","🐱":"Cat","👀":"Eyes","🦊":"Fox","🦄":"Unicorn","🐔":"Chicken","🐲":"Dragon","🦓":"Zebra","🐨":"Koala",
    "🐼":"Panda","🐸":"Frog","🦝":"Raccoon","🐮":"Cow","🐷":"Pig","🐗":"Boar","🐭":"Mouse","🐹":"Hamster","🦒":"Giraffe",
    "🐟":"Fish","🦀":"Crab","🦠":"Microbe","🕷":"Spider","🕸":"Spider web","🦷":"Tooth","🦴":"Bone","🧠":"Brain","👣":"Footprints",
    "👅":"Tongue","👄":"Mouth","👸":"Princess","🤴":"Prince","👵":"Old woman","👼":"Baby angel","👮":"Female police officer","👮":"Male police officer",
    "🕵":"Detective","🕵":"Detective","👷":"Construction worker","👷🏻‍♀️":"Construction worker","👨🏻‍🏫":"Teacher","👰":"Bride",
    "🤰":"Preagnant","🛀":"Taking bath","🤝":"Handshake","👌🏻":"Perfect","🔑":"Key","🧬":"DNA","💊":"Pill","💣":"Bomb",
    "🔬":"Microscope","🖨":"Printer","💻":"Laptop","🔗":"Link","🚬":"Cigarette","🔋":"Battery","🔌":"Electric plug",
    "✂":"Scissiors","📌":"Pushpin","⌚":"Watch","⚰":"Coffin","📺":"TV",
    ":-)": "Smile",":-(": "Frown",":-D": "Big Grin",":-P": "Sticking Out Tongue",";-)": "Wink",":-|": "Indifferent",":-/": "Skeptical",
    ":-*": "Kiss",":-O": "Surprised",":-X": "Sealed Lips","<3": "Heart","^_^": "Happy","T_T": "Crying",":-]": "Happy",":-[": "Sad",
    ":-||": "Angry",":')": "Tears of Joy",":-B": "Nerd",":3": "Cute Face",":|]": "Robot",":-#": "Braces",":-&": "Sick",":-%": "Confused",":->": "Sarcastic",":-\\": "Shrug",
    ":')-<": "Crying with a Mustache",":-o)": "Clown","(^_^)": "Joyful","(-_-)": "Disapproval","(*_*)": "Amazement","(-.-)": "Sigh",
    "(@_@)": "Dazed","(/_\)": "Distressed","(\*_\*)": "Excited","(\^.^)": "Happy","(;_;)": "Tearful","(+_+)": "Agitated","(-.-;)": "Worried",
    "(o_o)": "Surprised","(>_>)": "Shifty Eyes","(-'_'-)": "Nervous","(*^_^*)": "Blushing","(^o^)": "Cheerful","(#^.^#)": "Pleased",
    "(;^_^)/": "Joy","(/o\\)": "Tension","(^_-)": "Wink","(T_T)/": "Bowing","(@.@)": "Staring","(~o~)": "Drooling","(-_-)zzz": "Sleeping",
    "(>_>)<": "Evil Grin","(*_*)>": "Hypnotized","d[-_-]b": "Listening to Music","(^0^)/": "Excited","(*_*;)": "Embarrassed","(o^^)o": "Applause",
    "(@_@;": "Dizzy","(^o^;)": "Sweating","(-_-)/": "Salute","(@o@)/": "Cheers",":-Oo": "Surprised","(^_-)b": "Thumbs Up","O_O": "Wide-Eyed",
    "(o_o)": "Staring","(=_=)": "Bored","(>_<)": "Angry","(o_0)": "Confused","(-.-')": "Annoyance","(-_-)ゞ": "Sigh","(^,^)": "Giggling",
    "(-_-メ)": "Dissatisfied","(^_~)": "Winking","(-_-)凸": "Flipping the Bird","(o_ _)o": "Apology","(°ロ°)": "Disapproval","(◠‿◠✿)": "Cuteness Overload","( ͡° ͜ʖ ͡°)": "Lenny Face",
    "( ͡ᵔ ͜ʖ ͡ᵔ )": "Lenny Face with Glasses","(ง •̀_•́)ง": "Ready to Fight","¯_(ツ)_/¯": "Shrugging","( •_•)>⌐■-■": "Deal With It",
    "ಠ_ಠ": "Disapproval or Disbelief","(¬‿¬)": "Smirking","(¬_¬)": "Sarcasm","(☞ﾟヮﾟ)☞": "Finger Guns","(つ◕_◕)つ": "Sending a Hug",
    "( ͡~ ͜ʖ ͡°)": "Lenny Face with a Wink","(ง'̀-'́)ง": "Getting Ready for a Challenge","(¬‿¬) ": "Flirting","¯_(⊙_ʖ⊙)_/¯": "Confused Lenny Face",
    "(´・ω・)っ": "Kawaii Face","(••) ( ••)>⌐■-■ (⌐■_■)": "Sunglasses Deal With It","(¬‿¬) ": "Smirking with Style","(つ•̀ω•́)つ*:･ﾟ✧": "Sending Positive Vibes"}

    import numpy as np
    import pandas as pd
    import string
    
    tt=[]
    
    if remove_all == 'emj' or remove_all =='emoji':
        d.clear()
        #d1.clear()
        #d2.clear()
        print('All predefine emojies has been removed')
    elif remove_all == 'emt' or remove_all=='emoticon':
        d1.clear()
        print('All predefine emoticons has been removed')
    elif remove_all == 'both':
        d.clear()
        d1.clear()
        d2.clear()
        print('All predefine emojies and emoticons has been removed')
    elif remove_all not in('emj','emoji','emt','emoticon','both',None):
        raise ValueError("'remove_all' parameter can be set to either 'emj' or 'emoji', 'emt' or 'emoticon', or 'both'.")
        
    if add =='emj' or add == 'emoji' and add_em != None:
        d.update(add_em)
        d2.update(add_em)
    elif add =='emt' or add =='emoticon' and add_em != None:
        d1.update(add_em)
        d2.update(add_em)
    elif add =='emj' or add=='emoji' or add=='emt' or add=='emoticon' and add_em == None:
        raise ValueError("didn't find and dict to add")
    elif add not in(None,'emj','emt','emoji','emoticon'):
        raise ValueError("add value must be ether 'emj' or 'emt' | can be passed full form of 'emj' or 'emt'")
        
    if remove_em != None and remove == 'emj' or remove =='emoji':
        for i in remove_em:
            d.pop(i)
            d2.pop(i)
    elif remove_em != None and remove == 'emt' or remove =='emoticon':
        for i1 in remove_em:
            d1.pop(i1)
            d2.pop(i1)
    elif remove_em != None and remove == 'both':
        for i2 in remove_em:
            d2.pop(i2)
    elif remove not in(None,'emj','emt','emoji','emoticon','both'):
        raise ValueError("remove value must be ether 'emj' or 'emt' or 'both'")
            
    text1=text
    for t in text1.split():
        tt.append(t)
        
    if process_type == 'remove' and process_on == 'both':
        text1=' '.join([word for word in tt if word not in d2])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")

    elif process_type == 'remove' and process_on == 'emj':
        text1=' '.join([word1 for word1 in tt if word1 not in d])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")

    elif process_type == 'remove' and process_on == 'emt':
        text1=' '.join([word2 for word2 in tt if word2 not in d1])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")

    elif process_type == 'replace' and process_on == 'both':
        for ii in tt:
            if ii in d2:
                tt[tt.index(ii)]=d2[ii]
        text1=' '.join([w for w in tt])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")

    elif process_type == 'replace' and process_on =='emj' or process_on =='emoji':
        for ii1 in tt:
            if ii1 in d:
                tt[tt.index(ii1)]=d[ii1]
        text1=' '.join([w1 for w1 in tt])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")

    elif process_type == 'replace' and process_on =='emt' or process_on =='emoticon':
        for ii2 in tt:
            if ii2 in d1:
                tt[tt.index(ii2)]=d1[ii2]
        text1=' '.join([w2 for w2 in tt])
        if case == 'same':
            return text1
        elif case == 'lower':
            return text1.lower()
        elif case == 'upper':
            return text1.upper()
        else:
            raise ValueError("case value can be 'same','lower' or 'upper'")
        

def word_tokenizer(text,output_case='same',del_words=None,punc_tokenize=True,include_slash=True):
    """
    About :
        Tokenizes input text based on specified parameters and returns  tokens.

    Parameters:
        * text (str): The input text to be tokenized. 
    
        * output_case (str, optional) --> ['same','lower','upper']: The desired output format for tokens. Options include:
          - 'same' (default): Tokens are returned as they are.
          - 'lower': Tokens are converted to lowercase.
          - 'upper': Tokens are converted to uppercase. Default is 'same'
      
        * del_words (list, optional): A list of words to be excluded from the tokenization process. Default is None
        
        * punc_tokenize (bool, optional) : This parameter determines whether you want to include punctuation in your tokens.
                                           Default is True
                        
        * include_slash (bool,optional)  : If True then both kind of slash will be included among the tokens
                                           If False then slashes would be excluded from the the list of
                                           tokens. Default is True
    

    Returns:
        -  A list of tokens based on the specified parameters.

    Example Usage:
        >>> text = "This is a sample sentence."
        >>> del_words = ['is', 'a']
        >>> word_tokenize(text, output_case='lower', del_words=del_words)
    
    output --> ['this', 'sample', 'sentence']
    """
    slash =["/","\\"]
    pun=["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]
    if include_slash == False:
        for s in slash:
            pun.remove(s)
    elif include_slash not in(True, False):
        raise ValueError("include_slash value must be ether True or False")

    if punc_tokenize == True:
        for char in pun:
            text=text.replace(char, ' ' + char + ' ')
    elif punc_tokenize not in(True,False):
        raise ValueError("'Punc_tokenize' value must be a boolean object.")
    
    token=[]
    token1=[]
    token2=[]
    text1=text
    new_tok=[]
    new_tok1=[]
    new_tok2=[]
    for i in text.split():
        token.append(i)
        
    if del_words != None:
        for i2 in token:
            if i2 not in del_words:
                new_tok.append(i2)
        if output_case == 'same':
            return new_tok
        elif output_case == 'lower':
            for i3 in new_tok:
                new_tok1.append(i3.lower())
            return new_tok1
        elif output_case == 'upper':
            for i4 in new_tok:
                new_tok2.append(i4.upper())
            return new_tok2
        elif output_case not in('same','upper','lower'):
            raise ValueError("output value can be ether 'same','lower' or 'upper'")
            
    elif del_words == None:
        if output_case == 'same':
            return token
        elif output_case == 'lower':
            for p in token:
                token1.append(p.lower())
            return token1
        elif output_case == 'upper':
            for p1 in token:
                token2.append(p1.upper())
            return token2
        elif output_case not in('same','upper','lower'):
            raise ValueError("output value can be ether 'same','lower' or 'upper'")
    
    elif del_words != None or type(del_words) != list:
        raise TypeError("del_word value must be a list object")
    

Punctuations =["!","'",'"',"#","$","%","&","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","|","~","\\"]

EnglishPronouns = ['he','she','i','me','we','us','him','her','it','they','them','you','He','She','I','Me','We','Us','Him','Her','It','They','Them','You']