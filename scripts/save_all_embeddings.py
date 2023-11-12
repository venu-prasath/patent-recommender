import os
from glob import glob
import numpy as np
import shutil
import json
import pandas as pd
from preprocess import get_claims, get_embeddings, get_tokens
from tqdm import tqdm

base_dir = 'patent-recommender/dataset'
file_list=glob(os.path.join(base_dir,'*.json'))

df=pd.DataFrame.from_dict(json.load(open(file_list[0])), orient="index").T
for patent_loc in file_list[1:]:
    patent_file=json.load(open(patent_loc))
    temp_df=pd.DataFrame.from_dict(patent_file, orient="index").T
    df=pd.concat([df, temp_df], ignore_index=True)

for row in tqdm(df.values):
    patent_id=row[0]
    patent_folder=os.path.join(base_dir, patent_id)
    if not os.path.exists(patent_folder):
        os.mkdir(patent_folder)

    shutil.copyfile(os.path.join(base_dir, patent_id+'.json'), os.path.join(patent_folder, patent_id+'.json'))

    # for idx, i in enumerate(row):
    #     print(idx, i)
    abstract_emb=get_embeddings(" ".join(get_tokens(row[7], lemmatized=True, remove_num=True, remove_punct=True, remove_stopword=True)))
    np.save(os.path.join(patent_folder, patent_id+'_abstract_emb.npy'), abstract_emb)
    # print(os.path.join(base_dir, patent_id+'.npy'))
    
    claims=[claim for claim in get_claims(row[8]) if not claim.isspace()]
    claims = [ ' '.join(get_tokens(doc=claim, lemmatized=True, remove_punct=True, remove_stopword=True, remove_num=True)) for claim in claims ]
    claims_emb = np.array([get_embeddings(claim) for claim in claims])
    np.save(os.path.join(patent_folder, patent_id+'_claim_emb.npy'), claims_emb)

    # break

# 100%|██████████| 737/737 [3:47:20<00:00, 18.51s/it]  