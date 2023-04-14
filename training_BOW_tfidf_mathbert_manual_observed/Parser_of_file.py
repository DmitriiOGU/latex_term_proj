# -*- coding: utf-8 -*-
import re, nltk

class Parser_of_file:
    def __init__(self, data:list):
        """
        Parameters
        ----------
        data : list
            DESCRIPTION. get document.readlines list

        """
        self.data = data
        self.data = self.cropping_document_begin_end()
        self.data = self.delete_all_figures()
        self.sentences = self.to_sentences()
        self.sentences = self.clean_stops_and_pos()
    def cropping_document_begin_end(self):
        """
        Parameters
        ----------
        data : list of str
            Latex-file strings
        Returns
        -------
        data : list of str
            Latex-file strings only with 'content' of document
        """
        #from the start of document
        my_data = self.data.copy()
        i=0
        while not my_data[i] in ['\\begin{document}\n', '\\begin{document}','\begin{figure}','\begin{figure}\n']:
            i+=1
        my_data= my_data[i+1:]
        #from the end of document
        i=len(my_data)-1
        while not my_data[i] in ['\\end{document}\n', '\\end{document}','\end{figure}','\end{figure}\n']:
            i-=1
        my_data = my_data[:i]
        return my_data
    def delete_all_figures (self):
        """
        Parameters
        ----------
        data : list of str
            Latex-file strings
        Returns
        -------
        data : list of str
            Latex-file strings without figures
        """
        my_data = self.data.copy()
        start = 0
        Flag= True
        special_start = ['\\begin{figure}','\\begin{figure}\n','\begin{figure}',\
                         '\begin{figure}\n','\begin{tikzpicture}','\\begin{tikzpicture}',\
                         '\begin{tikzpicture}\n','\\begin{tikzpicture}\n','\begin{picture}',\
                         '\\begin{picture}','\begin{picture}\n','\\begin{picture}\n']
        special_end = ['\\end{figure}','\\end{figure}\n','\end{figure}','\end{figure}\n',\
                       '\end{tikzpicture}','\\end{tikzpicture}','\end{tikzpicture}\n',\
                       '\\end{tikzpicture}\n','\end{picture}','\\end{picture}',\
                       '\end{picture}\n','\\end{picture}\n']
        while Flag:
            while (not (my_data[start][:14] in special_start) or\
                   not(my_data[start][:19] in special_start) or\
                   not (my_data[start][:13] in special_start))and\
                  (start<len(my_data)-1):
                start+=1
            if (not (my_data[start][:14] in special_start) or\
                not(my_data[start][:19] in special_start) or\
                not (my_data[start][:13] in special_start)):
                Flag = False
            if Flag:
                end = start
                while (not (my_data[end][:12] in special_end) or\
                       not(my_data[end][:17] in special_end) or\
                       not (my_data[end][:11] in special_end)) and (end<len(my_data)-1):
                        end+=1
                if (not (my_data[end][:12] in special_end) or\
                       not(my_data[end][:17] in special_end) or\
                       not (my_data[end][:11] in special_end)):
                    end+=1
                my_data = my_data[:start]+my_data[end+1:]
        return my_data
    def to_sentences(self):
        """
        Returns
        -------
        list of sentences
            list of sentences where unusable symbols was deleted
        """
        latex_words = ('\\end','\\begin','\\bibliographystyle','\\bibliography',\
               '\\section','\\maketitle','\\setcounter','\\addtocontents',\
                   '\\tableofcontents','\\subsection')
        i=0
        search_patterns = '(\\\\ref\{[^}]*\})|(\\\\item)|(\\\\textbf)|(\\\\label\{[^}]*\})|(\\\\cite\{[^}]*\})|(\+)|'
        search_patterns += '(\$)|(\[|\])|([^_\s]*_[^ ]*\s)|(\=|\:)|([-+]?\d+ )|(\>|\<)'
        search_patterns += '|(\(|\))|(\{|\})|( (?=\.))|(\n)|(\s+(?= .*))|(\d+pt)|(\d+mm)|(\d+cm)'
        search_patterns = re.compile(search_patterns)
        search_patterns_slashes = re.compile('(\\[^ ]*  )|([^\w\s\.])')
        my_data = self.data.copy()
        # k=0
        while i<=len(my_data)-1:
            my_data[i] = re.sub(search_patterns,'',(my_data[i])).strip()
            if (my_data[i].startswith(latex_words)) or (my_data[i]=='\n') or (my_data[i]=='')\
                or (my_data[i]=='\\\\') or (my_data[i] =='\\'):
                my_data=my_data[:i]+my_data[i+1:]  
            else:
                my_data[i] = re.sub(search_patterns_slashes,'',(my_data[i]))
                if  (my_data[i]=='\n') or (my_data[i]=='') or (my_data[i]=='\\\\')\
                    or (my_data[i] =='\\'):
                    my_data=my_data[:i]+my_data[i+1:]  
                else:
                    i+=1
        return ' '.join(my_data).lower().split('.')
    def clean_stops_and_pos(self):
        """
        Returns
        -------
        list of sentences
            deleted stop_words and_unknown part_of_speech the full sentences.
        """
        #lemmatize, tokenize, deleting stopwords
        def get_wordnet_pos(word):
            """
            Parameters
            ----------
            word : str
                word from sentence.
            Returns
            -------
            wordnet_pos: object
                returns nltk.corpus.wordnet
            """
            tag = nltk.pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": nltk.corpus.wordnet.ADJ,
                        "N": nltk.corpus.wordnet.NOUN,
                        "V": nltk.corpus.wordnet.VERB,
                        "R": nltk.corpus.wordnet.ADV,
                        "S": nltk.corpus.wordnet.ADJ_SAT}
            if tag !="V":
                tag="N"
            return tag_dict.get(tag, nltk.corpus.wordnet.NOUN) 
        
        lemmatizer = nltk.stem.WordNetLemmatizer()
        # stop_words = {'$',',',';','\\','+','-','&','^',"\'","\'\'","``","\`","corollary","follow","lemma","see","one","two","three","four",
        #               "five","six","seven","eight","nine","ten"}
        stop_words = {'$',',',';','\\','+','-','&','^',"\'","\'\'","``","\`",\
                      "follow","see","define","alse","either","even","every",\
                          "exact","exists","however","hence", "may","0rule0"}
        stop_words = set(nltk.corpus.stopwords.words("english")).union(stop_words)
        my_sentences = self.sentences.copy()
        for i in range(len(my_sentences)):
            my_sentences[i] = [lemmatizer.lemmatize(w, get_wordnet_pos(w)) \
                                  for w in nltk.word_tokenize(my_sentences[i])\
                                  if (not w in stop_words) and \
                                      (not w.isdigit()) and \
                                          ((get_wordnet_pos(w) == nltk.corpus.wordnet.NOUN))]
        return my_sentences
    
    def get_sentences(self):
        return self.sentences
    
    def get_data(self):
        return self.data