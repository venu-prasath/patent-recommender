import re
from spacy import load as spacyload
from sentence_transformers import SentenceTransformer
from string import punctuation


def get_tokens(doc, lemmatized=False, remove_stopword=False,
                   remove_punct = True, pos_tag = False, remove_num=False):
    nlp=spacyload("en_core_web_sm")
    doc=nlp(doc.lower().strip())

    tokens=[]

    for token in doc:
        if (remove_stopword and token.is_stop) or (token.text=='') or (token.text.isspace()) or (remove_num and token.text.isnumeric()):
            continue

        token_ls=token.text

        if lemmatized:
            token_ls=token.lemma_
        if pos_tag:
            token_ls=(token_ls, token.pos_)

        if remove_punct:
            if token.is_punct:
                continue
            token_no_punct=''
            for character in token_ls:
                if character not in punctuation:
                    token_no_punct+=character
                else:
                    token_no_punct+=' '

            for tok in token_no_punct.split(' '):
                tokens.append(tok)
        else:
            tokens.append(token_ls)
    return tokens

def get_claims(claims):#, tokenize=True, as_sentence=True):
    '''

    claims:      A list of strings
    as_sentence: If True, gives a list of strings where each string is a single space-separated combination of tokens
    
    '''
    claims = [ claim.replace("\n", " ") for claim in re.split(r"[0-9]+\.", claims) if claim!='']
    # if tokenize:
    #     if as_sentence:
    #         claims = [ ' '.join(get_tokens(doc=claim, lemmatized=True, remove_punct=True, remove_stopword=True, remove_num=True)) for claim in claims ]

    #     else:
    #         claims = [ get_tokens(doc=claim, lemmatized=True, remove_punct=True, remove_stopword=True, remove_num=True) for claim in claims ]
    return claims

def get_embeddings(claims):
    '''
    claims: A list of strings where each string is tokenized words combined into a single space-separated combination of tokens 
            Example: "computer implement method detect pressure touch region occur time distinct location plane device comprise"
    '''

    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings = model.encode(claims, convert_to_numpy=True)
    return embeddings