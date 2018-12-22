def chars_after_symbol(string, symbol):
    """ (str, str) -> list of str
    
    Return a list of all the substrings that occur after the specified symbol. 
    A substring consists of all the characters after an occurence of the symbol 
    until a space, punctuation, or end of tweet is reached. The substrings in 
    the list do not include the symbol. This is meant to be a helper function 
    because both extract_mentions and extract_hashtags can make use of it.
    
    Examples:
    >>> chars_after_symbol("Hello world", "@")
    []
    >>> chars_after_symbol("I am #superman. Go #Superman!", "#")
    ['superman', 'Superman']
    >>> chars_after_symbol("I'm so @cool! I have so much @power now!", "@")
    ['cool', 'power']
    
    """
    
    start_adding_substr = False #dictates whether to start adding to substrings.
    substrings = []
    substr_num = -1    
    for index in range(len(string)): 
        if(not(string[index].isalnum()) and not(string[index] == symbol)):
            start_adding_substr = False  
        elif (index != 0 and string[index] == symbol and\
              string[index - 1] != " "):
            start_adding_substr = False
        elif(start_adding_substr):
            substrings[substr_num] = substrings[substr_num] + string[index]
        elif(string[index] == symbol):
            start_adding_substr = True
            substr_num += 1
            substrings.append("")                   
    return substrings
    
def extract_mentions(tweet):
    """ (str) -> list of str
    
    Return a list of the mentions in the tweet parameter in the order they 
    appear in the tweet. The returned mentions have the @ symbol removed. 
    Mentions may appear more than once in the list.
    
    Examples:
    >>> extract_mentions("@Martin hello there @Martin")
    ['Martin', 'Martin']
    >>> extract_mentions("Hello @Martin how is @Donald?")
    ['Martin', 'Donald']
    >>> extract_mentions("I love computer science.")
    []
    
    """
    
    return chars_after_symbol(tweet, "@")

def extract_hashtags(tweet):
    """ (str) -> list of str
    
    Return a list of the hashtags in the tweet in the order that the first
    instance of each hashtag appears in the tweet. Hashtags may only occur once
    in the list. The items in the list have the # symbol removed. Note that
    hashtags are not case sensitive. This function converts hashtags to their
    lowercase form.
    
    Examples:
    >>> extract_hashtags("this is #Incredible, absolutely #incredible")
    ['incredible']
    >>> extract_hashtags("this is #really #superb!")
    ['really', 'superb']
    >>> extract_hashtags("hello #world ")
    ['world']
    
    """
    
    total_hashtags = chars_after_symbol(tweet, "#")
    hashtags = total_hashtags[:] 
    if(hashtags == []): 
        return []
    hashtags[0] = hashtags[0].lower()
    index = 1
    while index < len(hashtags):
        hashtags[index] = hashtags[index].lower()
        if(hashtags[index] in hashtags[:index]): #no duplicate hashtags
            hashtags.pop(index)
            index -= 1
        index += 1
    return hashtags

def words_modifier(words):
    """ (list of str) -> NoneType
    
    Return nothing. Modifies a list of words to remove hashtags, mentions, and 
    URLs from the list, and removing non-alphanumeric characters from words in
    the list. It also lowercases the words. This is a helper function for 
    count_words.
    
    Examples:
    >>> words = ["Abc", "@Hello", "#hello", "don't"]
    >>> words_modifier(words)
    >>> words
    ['abc', 'dont']
    
    """
    
    index = 0
    while index < len(words):                      
            if(words[index][0] == "#" or words[index][0] == "@"):
                words.pop(index) #remove hashtags and mentions
                index -= 1
            elif(len(words[index]) >= 4 and words[index][:4].lower() == "http"):
                words.pop(index) #remove URLs
                index -= 1                
            else:
                ch_index = 0
                while ch_index < len(words[index]): #remove punctuation
                    if (not(words[index][ch_index].isalnum())):
                        words[index] = words[index][:ch_index] + \
                            words[index][ch_index + 1:]  
                        ch_index -= 1
                    ch_index += 1
            if(len(words) != 0):
                words[index] = words[index].lower()
            index += 1    
    

def count_words(tweet, word_dict):
    """ (str, dict of {str, int}) -> None
    
    Return nothing. This function updates the word_dictionary by adding words
    and updating the number of occurrences of each word in the dictionary by 
    incrementing them by the amount of times they appear in the tweet. Words are
    converted to lowercase in the dictionary. Words are separated by whitespace
    and punctuation does not comprise part of the word.
    
    Examples:
    >>> word_dict = {"i": 7, "love": 3, "milk": 1}
    >>> count_words("I love chocolate milk and milk chocolate", word_dict)
    >>> word_dict == {"i": 8, "love": 4, "milk": 3, "chocolate": 2, "and": 1}
    True
    >>> count_words("#cash I'm a rapper now @ChiefKeef http://gangsterrap.com",\
    word_dict)
    >>> word_dict == {"i": 8, "love": 4, "milk": 3, "chocolate": 2, "and": 1,\
    "im": 1, "a": 1, "rapper": 1, "now": 1}
    True
    
    """
       
    words = tweet.split(" ") 
    words_modifier(words)
    for word in words: 
        if word in word_dict: 
            word_dict[word] += 1
        else:
            word_dict[word] = 1   

def common_words(word_dict, max_words):
    """ (dict of {str, int}, int) -> None
    
    Return nothing. This function updates the dictionary to include only the 
    most common words with a maximum of max_words in the dictionary. If there is 
    a tie that results in there being more than max_words in the dictionary, 
    those tied items are not included.
    
    Examples: 
    >>> word_dict = {"a": 7, "b": 7, "c": 6, "d": 2, "e": 6}
    >>> common_words(word_dict, 2)
    >>> word_dict == {'a': 7, 'b': 7}
    True
    >>> word_dict = {"a": 7, "b": 7, "c": 6, "d": 2, "e": 6}
    >>> common_words(word_dict, 3)
    >>> word_dict == {'a': 7, 'b': 7}
    True
    >>> word_dict = {"a": 7, "b": 7, "c": 6, "d": 2, "e": 6}
    >>> common_words(word_dict, 1)
    >>> word_dict == {}
    True
    
    """
    
    nums = []
    for key in word_dict:
        nums.append(word_dict[key])
    nums.sort(reverse = True)
    popular_nums = []
    index = 0
    occurrences = 0
    while index < len(nums): #copy the largest ints to popular_nums (<= N)
        current_occurrences = nums.count(nums[index])    
        occurrences += current_occurrences
        if(not occurrences > max_words):
            popular_nums.append(nums[index])
        else:
            break
        index += current_occurrences
    word_dict_copy = dict(word_dict)    
    for key2 in word_dict_copy: #delete the less popular items
            if(not(word_dict[key2] in popular_nums)):
                del word_dict[key2]

def generate_fields(tweet_str, field_list):
    """ (list of str, list of str) -> int
    
    Generate all of the fields in the file and put them into field_list. This 
    is a helper function for read_tweets
    
    Examples:
    >>> field_list = []
    >>> tweet_str = "12,12,n,t,3,2Hello"
    >>> generate_fields(tweet_str, field_list)
    >>> field_list
    ['12', '12', 'n', 't', '3', '2', 'Hello']
    
    """
    
    comma_index = 0
    for i in range(5): #extract the first 5 fields (the ones with commas at end)
        new_comma_index = tweet_str.index(",", comma_index + 1)
        field_list.append(tweet_str[comma_index:new_comma_index])
        comma_index = new_comma_index + 1    
    last_two_fields = tweet_str[comma_index:]
    for index in range(len(last_two_fields)): #separate and extract last two
        if not(last_two_fields[index].isdigit()):
            field_list.append(last_two_fields[:index])
            field_list.append(last_two_fields[index:]) 
            break
    for j in range(6): #remove newlines except for tweet
        field_list[j] = field_list[j].replace("\n", "")            
             
def read_tweets(file):
    """ (file open for reading) -> dict of {str: list of tweet tuples}
    
    Return a dictionary with candidate names as keys and a list of tuples as
    values; with each tuple representing a tweet. The tuples are in the form
    (candidate, tweet text, date, source, favorite count, retweet count), where 
    every item is a string except date, favorite count and retweet count which
    are integers.
 
    """
    
    text = file.read()
    all_tweets = list(filter(None, text.split("<<<EOT"))) 
    cand_dict = {}
    cand_name = ""
    for index in range(len(all_tweets)):
        if(all_tweets[index][0] == "\n"): #remove newlines at beginning
            all_tweets[index] = all_tweets[index][1:]   
        if(all_tweets[index] == ""): #there was empty string at the end 
            break
        if(not(all_tweets[index][0].isdigit())): #e.g. "Donald Trump:791..."
            cand_name = all_tweets[index][:all_tweets[index].index(":")]
            all_tweets[index] = all_tweets[index]\
                [all_tweets[index].index(":") + 1:]
            cand_dict[cand_name] = []
        field_list = []
        generate_fields(all_tweets[index], field_list)
        cand_dict[cand_name].append(\
            (cand_name, field_list[6], int(field_list[1]), field_list[3], \
             int(field_list[4]), int(field_list[5]),))
    return cand_dict

def update_candidate_counts_names(cand_dict, date1, date2, candidate_counts, \
                            candidate_names):
    """ (dict of {str: list of tweet tuples}, int, int, list of int, 
    list of str -> NoneType
    
    Return nothing. This function is a helper function for most_popular. It
    modifies the candidate_counts and candidate_names lists of that function so 
    that they include the popularity counts (favorites + retweets) for each 
    candidate for candidate_counts and the names of the candidates for 
    candidate_names. The lists are meant to be parallel.
    
    Examples:
    >>> cand_dict = {"A": [("A", "x", 22, "n", 5, 6),\
    ("A", "x", 23, "n", 11, 12)], "B": [("B", "x", 22, "n", 15, 11),\
    ("B", "x", 24, "n", 4, 4)]}
    >>> candidate_counts = []
    >>> candidate_names = []
    >>> update_candidate_counts_names(cand_dict, 22, 25, candidate_counts, \
    candidate_names)
    >>> candidate_counts
    [34, 34]
    >>> candidate_names == ['A', 'B'] or candidate_names == ['B', 'A']
    True
    
    """
    
    key_index = 0
    for key in cand_dict:
        candidate_counts.append(0) 
        for index in range(len(cand_dict[key])):
            if (not(cand_dict[key][index][0] in candidate_names)):
                candidate_names.append(cand_dict[key][index][0])
            date = cand_dict[key][index][2]
            if (date1 <= date <= date2):
                candidate_counts[key_index] += (cand_dict[key][index][4]\
                                            + cand_dict[key][index][5]) 
        key_index += 1    

def most_popular(cand_dict, date1, date2):
    """ (dict of {str: list of tweet tuples}, int, int) -> str
    
    Return the most popular candidate between date1 and date2 (where date1 <= 
    date2). Populartity is defined by the sum of all favorites and retweets for
    a given candidate's tweets in the specified timeframe. Return "Tie" if there
    is a tie for the most popular candidate.
    
    Examples:
    >>> dictionary = {"A": [("A", "x", 22, "n", 5, 6),\
    ("A", "x", 23, "n", 11, 12)], "B": [("B", "x", 22, "n", 15, 11),\
    ("B", "x", 24, "n", 4, 4)]}
    >>> most_popular(dictionary, 22, 22)
    'B'
    >>> most_popular(dictionary, 22, 25)
    'Tie'
    
    """
    
    candidate_counts = []
    candidate_names = []
    update_candidate_counts_names(cand_dict, date1, date2, candidate_counts,\
                                  candidate_names)
    max_popularity = max(candidate_counts)
    tie_int = 0 #this will equal (number of ties for max popularity) + 1
    for count in candidate_counts:
        if(count == max_popularity):
            tie_int += 1
    if(tie_int > 1):
        return "Tie"
    else:
        i = candidate_counts.index(max_popularity)
        return candidate_names[i]
    
def update_hashtags_names(cand_dict, candidate_hashtags, candidate_names):
    """ (dict of {str: list of tweet tuples}, list of str, list of str)
    -> NoneType
    
    Return nothing. This function is a helper function for detect_author. This
    function modifies both candidate_hashtags and candidate_names to include
    lists of hashtags for each candidate and the names of each candidate 
    respectively.
    
    Examples:
    >>> dictionary = {"A": [("A", "h #a", 22, "n", 5, 6),\
    ("A", "h #b", 23, "n", 11, 12)], "B": [("B", "h #b", 22, "n", 15, 11),\
    ("B", "h #c", 24, "n", 4, 4), ("B", "h #d", 25, "n", 4, 4)]}
    >>> candidate_hashtags = []
    >>> candidate_names = []
    >>> update_hashtags_names(dictionary, candidate_hashtags, candidate_names)
    >>> candidate_hashtags == [['a', 'b'], ['b', 'c', 'd']] or\
    candidate_hashtags == [['b', 'c', 'd'], ['a', 'b']]
    True
    >>> candidate_names == ['A', 'B'] or candidate_names == ['B', 'A']
    True
    
    """
    
    candidate_index = 0
    for key in cand_dict:
        candidate_hashtags.append([])
        for index in range(len(cand_dict[key])):
            if(not(cand_dict[key][index][0] in candidate_names)):
                candidate_names.append(cand_dict[key][index][0])
            hashtags = extract_hashtags(cand_dict[key][index][1])
            for hashtag in hashtags:
                candidate_hashtags[candidate_index].append(hashtag)
        candidate_index += 1    

def find_likely_author(tweet_hashtags, candidate_hashtags, candidate_names):
    """ (list of str, list of str, list of str) -> str
    
    Return the most likely author of a tweet based on comparing the 
    tweet_hashtags to the candidate_hashtags.
    
    Examples:
    >>> candidate_names = ["A", "B"]
    >>> candidate_hashtags = [["#a","#b"], ["#b", "#c", "#d"]]
    >>> find_likely_author(["#a", "#b"], candidate_hashtags, candidate_names)
    'Unknown'
    >>> find_likely_author(["#c", "#d"], candidate_hashtags, candidate_names)
    'B'
    
    "
    
    """
    cand_tweeter = ""
    for tweet_hashtag in tweet_hashtags:
        cand_count = 0 #number of candidates that use this hashtag
        c_hashtag = "" #saves the list of hashtags with tweet_hashtag
        for candidate_hashtag in candidate_hashtags:
            if tweet_hashtag in candidate_hashtag:
                cand_count += 1
                if cand_count > 1:
                    return "Unknown"                
                c_hashtag = candidate_hashtag        
        if cand_count == 1:
            if(cand_tweeter == ""):
                cand_tweeter = candidate_names\
                    [candidate_hashtags.index(c_hashtag)]
            else: #compare author of this hashtag to author of previous ones
                new_cand_tweeter = cand_tweeter
                cand_tweeter = candidate_names\
                    [candidate_hashtags.index(c_hashtag)]
                if(cand_tweeter != new_cand_tweeter):
                    return "Unknown"
    return cand_tweeter 
      
    
def detect_author(cand_dict, tweet):
    """ (dict of {str: list of tweet tuples}, str) -> str
    
    Return the most likely author of the specified tweet. A candidate is the 
    most likely author of the specified tweet if the hashtags of the tweet 
    are used uniquely by that candidate. Return "Unknown" if there are no 
    hashtags or if any of the hashtags have been used by more than one 
    candidate.
    
    Examples:
    >>> dictionary = {"A": [("A", "h #a", 22, "n", 5, 6),\
    ("A", "h #b", 23, "n", 11, 12)], "B": [("B", "h #b", 22, "n", 15, 11),\
    ("B", "h #c", 24, "n", 4, 4), ("B", "h #d", 25, "n", 4, 4)]}
    >>> detect_author(dictionary, "h #a #b")
    'Unknown'
    >>> detect_author(dictionary, "h #c #d")
    'B'
    >>> detect_author(dictionary, "h #a #e")
    'A'
    
    """
    
    tweet_hashtags = extract_hashtags(tweet)
    candidate_hashtags = []
    candidate_names = []
    update_hashtags_names(cand_dict, candidate_hashtags, candidate_names)
    return find_likely_author(tweet_hashtags, candidate_hashtags,\
                              candidate_names)   