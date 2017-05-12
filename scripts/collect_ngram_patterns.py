############################################################
# Module  : collect ngrams matching linguistic patterns
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import re
from utils   import *
from scripts import *


'''
    @Use: winnow ngram files by those that contain words found in word_path
          Note if you run this on multiple batchs of words from different `word_path`
          then there will be duplicate ngrams

          then you would need to prune the output files for duplicates

    @Input: - path to words  `word_path`     :: String
            - path to ngrams  `ngram_dir`    :: String
            - output directory `out_dir`     :: String
            - log path `log_dir`             :: String 
            - debug flag                     :: Bool
                 if true only output part of ngrams
    @Output: None
            save results of parse to out_path
            log program trace to log_dir
'''
def ngram_by_words(word_path, ngram_dir, out_path, log_dir, debug = False):

    writer = Writer(log_dir, 1)
    writer.tell('running ngram_by_words ...')

    if debug: msg = 'debug'
    else:     msg = 'non-debug'
    writer.tell('Streaming ngrams from ' + ngram_dir +  ' in ' + msg + ' mode')

    words   = [x for x in open(word_path, 'rb').read().split('\n') if x]

    output  = open(out_path, 'wb')

    '''
        iterate over all ngrams and save if any word in words appear
    '''
    for gram,n in with_ngram(ngram_dir, debug):
        if any(w in gram for w in words):
            output.write(gram + '\t' + n + '\n')

    output.write('=== END')
    output.close()


'''
    @Use  : find all ngrams matching "word_a pattern word_b" regex

    @Input: - path to words  `word_path`     :: String
            - path to pattern `pattern_path` :: String
            - path to ngrams  `ngram_dir`    :: String
            - path to no-data file `no_data_path` :: String
                - this is created the last time we crawled and found no data
            - output directory `out_dir`     :: String
            - log path `log_dir`             :: String 

            - refresh flag                   :: Bool

                 if true then do not rerun if file exits

            - debug flag                     :: Bool
                 if true only output part of ngrams
    @Output: None
            save results of parse to out_path
            log program trace to log_dir
'''
def collect_ngram_patterns( word_path
                          , pattern_path
                          , no_data_path
                          , ngram_dir
                          , out_dir
                          , log_dir
                          , refresh = True
                          , debug   = False):
    
    # log output
    writer = Writer(log_dir, 1, debug = debug, console = False)

    s_refresh = 'refresh' if refresh else 'non-refresh'

    patterns  = read_pattern(pattern_path)

    all_pairs   = [x.split(', ') for x in open(word_path,'rb').read().split('\n') if x]
    chunk       = 50
    pair_chunks = chunks(all_pairs,chunk)

    '''
        if we crawled this set of words before, then we
        encountered words with no data and saved them.
        so open them up
    '''
    if os.path.exists(no_data_path):

        tup = lambda xs : (xs[0], xs[1])

        writer.tell('found path to list of pairs with no data at ' + no_data_path)
        no_data_pairs = [tup(x.split(', ')) for x in open(no_data_path,'rb').read().split('\n') if x]

    else:
        writer.tell('could not locate list of pairs with no data at ' + no_data_path)
        no_data_pairs = []

  
    writer.tell('running collect_ngram_patterns over chunks of length ' + str(chunks))

    writer.tell('found word pair path at ' + word_path)
    writer.tell('found ngram directory at ' + ngram_dir)
    writer.tell('collect ngram over all words in ' + s_refresh + ' mode...')

    '''
        loop over pairs so we can save as data for each pair is collected
        re-save the no_data_pairs to disk for every new k pairs added
    '''
    save_curr = 0

    for pairs in pair_chunks:

        new_no_data = collect_pairs( pairs
                                   , patterns
                                   , no_data_pairs
                                   , ngram_dir
                                   , out_dir
                                   , writer
                                   , refresh
                                   , debug)
        
        writer.tell('chunk done ...')    

        '''
            update no data pairs and increment
            save no data counter
        '''   
        no_data_pairs = new_no_data
        save_curr     += 1

        '''
            update no-data-pairs on disk
        '''
        if save_curr == 5: 
            writer.tell('saving partial results for no-data-pairs')
            save_no_data_pairs(no_data_pairs, no_data_path)
            save_curr = 0


    writer.tell('saving list of words with no data at ' + no_data_path)

    if no_data_pairs:
        with open(no_data_path,'wb') as h:
            for s,t in set(no_data_pairs):
                h.write(s + ', ' + t + '\n')


def save_no_data_pairs(pairs, path):
    if pairs:
        with open(path, 'wb') as h:
            for s, t in set(pairs):
                h.write(s + ', ' + t + '\n')


'''
    @Use: collect data for subset of words {(s,t)} over all `patterns`
          from ngrams found at `ngram_dir`
          save output to `s_t_path`
          and respect `debug` flag
'''
def collect_pairs( pairs
                 , patterns
                 , no_data
                 , ngram_dir
                 , out_dir
                 , writer
                 , refresh
                 , debug):

    outputs = {(s,t) : { s + '>' + t : []
                       , s + '<' + t : []
                       , 'regexp'    : compile_patterns(s,t,patterns)
                       , 'path'      : os.path.join(out_dir, s + '-' + t + '.txt')} \
                       for s,t in pairs }

    '''
        iterate through all ngrams
    '''                   
    for gram, n in with_ngram(ngram_dir, debug):

        '''
            iterate though all pairs and search for results
        '''
        for (s,t), out in outputs.iteritems():

            # if no data last time we looked, then skip
            if (s,t) in no_data:
                writer.tell(s + ', ' + t + ' did not have data the last time we crawled. skipping ...')

            # if we already found the data, then skip
            elif refresh and os.path.exists(out['path']):
                writer.tell('data for ' + s + ', ' + t + ' already exists. skipping ...')

            # if both s and t are in the n-gram `gram`, then collect the data
            elif s in gram and t in gram:

                writer.tell('collecting data for ' + s + ', ' + t)

                patts = out['regexp']

                s_stronger_t = [gram + '\t' + n for r in patts[s + '>' + t] if r.match(gram)]
                s_weaker_t   = [gram + '\t' + n for r in patts[s + '<' + t] if r.match(gram)]

                out[s + '>' + t] += s_stronger_t             
                out[s + '<' + t] += s_weaker_t

            else:
                pass

    '''
        Save outputs where we found data
        output list of pairs where no data is found
    '''
    for (s,t), out in outputs.iteritems():

        if out[s + '>' + t] or out[s + '<' + t]:

            s_t_path = os.path.join(out_dir, s + '-' + t + '.txt')

            with open(s_t_path, 'wb') as h:

                h.write('=== ' + s + ' > ' + t  + '\n')

                for p in out[s + '>' + t]: h.write(p + '\n')

                h.write('\n=== ' + s + ' < ' + t  + '\n')

                for q in out[s + '<' + t]: h.write(q + '\n')

                h.write('=== END')       

        else:
            no_data.append((s,t))

    return list(set(no_data))        

'''
    @Use: collect data for words s,t over all `patterns`
          from ngrams found at `ngram_dir`
          save output to `s_t_path`
          and respect `debug` flag
'''
def collect_one_pair(s, t, patterns, ngram_dir, s_t_path, debug):

    out   = {s + '>' + t : [], s + '<' + t : []}
    patts = compile_patterns(s,t,patterns)

    for gram,n in with_ngram(ngram_dir, debug):

        if s in gram and t in gram:

            s_stronger_t = [gram + '\t' + n for _,r in patts[s + '>' + t] if r.match(gram)]
            s_weaker_t   = [gram + '\t' + n for _,r in patts[s + '<' + t] if r.match(gram)]

            out[s + '>' + t] += s_stronger_t             
            out[s + '<' + t] += s_weaker_t
    
    if out[s + '>' + t] or out[s + '<' + t]:

        with open(s_t_path, 'wb') as h:

            h.write('=== ' + s + ' > ' + t  + '\n')

            for p in out[s + '>' + t]: h.write(p + '\n')

            h.write('\n=== ' + s + ' < ' + t  + '\n')

            for q in out[s + '<' + t]: h.write(q + '\n')

            h.write('=== END')       

        return True
    else:

        return False



'''
    @Use  : compile word pattern for every pattern
    @Input: s     :: String  word1
            t     :: String  word2
            patts :: Dict String [String]
                      with keys: strong-weak
                                 weak-strong
                      and values that is a list of patterns
    @Output a dictionary of regular expressions for 
            s t at each pattern
'''
def compile_patterns(s,t, patts):

    s_stronger_t = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['strong-weak']] \
                 + [(R,re.compile(parse_re(R,[t,s]))) for R in patts['weak-strong']]

    s_weaker_t  = [(R,re.compile(parse_re(R,[s,t]))) for R in patts['weak-strong']]  \
                + [(R,re.compile(parse_re(R,[t,s]))) for R in patts['strong-weak']]

    return { s + '>' + t : s_stronger_t, s + '<' + t : s_weaker_t }




