import pandas as pd
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import nltk
import pickle
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
stop = stopwords.words('english')
#print("on line 11")
lemmatizer = WordNetLemmatizer()
stop = stopwords.words('english')
pattern_url = r'http[s]?://(?:[A-Za-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9A-Fa-f][0-9A-Fa-f]))+'
subs_url = r'url-web'
#print("on line 16")
energymodel= open('./model/energy_model.pkl','rb')
#print("on line 18")
energymodelz= pickle.load(energymodel)
energymodel.close()
#print("on line 21")
mindmodel= open('./model/mind_model.pkl','rb')
mindmodelz= pickle.load(mindmodel)
mindmodel.close()
#print("on line 25")
naturemodel= open('./model/nature_model.pkl','rb')
naturemodelz = pickle.load(naturemodel)
naturemodel.close()
#print("on line 29")
tacticsmodel= open('./model/tactics_model.pkl','rb')
tacticsmodelz= pickle.load(tacticsmodel)
tacticsmodel.close()

vectmind= open('./model/vect_mind.pkl','rb')
vectmindz = pickle.load(vectmind)
vectmind.close()

vectnature= open('./model/vect_nature.pkl','rb')
vectnaturez= pickle.load(vectnature)
vectnature.close()

vecttactics= open('./model/vect_tactics.pkl','rb')
vecttacticsz = pickle.load(vecttactics)
vecttactics.close()
#print("on line 45",vecttacticsz)
vectenergy= open('./model/vect_energy.pkl','rb')
vectenergyz = pickle.load(vectenergy)
vectenergy.close()
#print("on line 49")

def remove_stop_words(word):
    #print("on line 52")
    if word not in stop:
        return word
    else:
        return ''
def remove_delimiters(post):
    new = post.replace('|||',' ')
    #print("on line 59")
    return ' '.join(new.split())
def remove_punctuation(post):
    punc_numbers = string.punctuation + '0123456789'
    #print("on line 63")
    return ''.join([l for l in post if l not in punc_numbers])
def predict_personality_(post):
    ar=[post]
    ar2=[1]
    dicti={'id':ar2,'posts':ar}
    test=pd.DataFrame(dicti)
    test['posts'] = test['posts'].apply(remove_delimiters)
    #print("on line 71")
    test['posts'] = test['posts'].replace(to_replace = pattern_url, value = subs_url, regex = True)
    test['posts'] = test['posts'].str.lower()
    test['posts'] = test['posts'].apply(remove_punctuation)
    test['lemma'] = [' '.join([lemmatizer.lemmatize(word) for word in text.split(' ')])for text in test['posts']]
    #print("on line 76")
    stop = stopwords.words('english')
    test['stopwords'] = test['lemma'].apply(lambda x: len([x for x in x.split() if x in stop]))
    test['lemma_no_stop'] = [' '.join([remove_stop_words(word) for word in text.split(' ')])for text in test['lemma']]
 
    pred_mind_count =  vectmindz.transform(test['lemma_no_stop'])
    #print("on line 82")
    final_mind_predictions = mindmodelz.predict(pred_mind_count)

    test['E_pred'] = final_mind_predictions


    pred_mind_df = test[['id', 'E_pred']]


    pred_energy_count = vectenergyz.transform(test['lemma_no_stop'])


    final_energy_predictions = energymodelz.predict(pred_energy_count)

    test['N_pred'] = final_energy_predictions

    pred_energy_df = test[['id', 'N_pred']]

    
    pred_nature_count = vectnaturez.transform(test['lemma_no_stop'])


    final_nature_predictions = naturemodelz.predict(pred_nature_count)

    test['T_pred'] = final_nature_predictions

    pred_nature_df = test[['id', 'T_pred']]

    pred_tactics_count =vecttacticsz.transform(test['lemma_no_stop'])


    final_tactics_predictions =tacticsmodelz.predict(pred_tactics_count)

    test['J_pred'] = final_tactics_predictions

    pred_tactics_df = test[['id', 'J_pred']]


    my_submission = pd.merge(pred_mind_df[['id','E_pred']], pred_energy_df[['id','N_pred']], how ='inner', on ='id') 
    my_submission = pd.merge(my_submission[['id','E_pred', 'N_pred']], pred_nature_df[['id','T_pred']], how ='inner', on ='id')
    my_submission = pd.merge(my_submission[['id','E_pred', 'N_pred','T_pred']], pred_tactics_df[['id','J_pred']], how ='inner', on ='id') 
    my_submission.rename(columns={'id':'id',
                                'E_pred':'mind',
                                'N_pred': 'energy',
                                'T_pred': 'nature',
                                'J_pred': 'tactics'
                                }, 
                    inplace=True)

    my_submission.head()
    my_submission['Mind Pred'] = my_submission['mind'].map(lambda x: 'E' if x == 1 else 'I')
    my_submission['Energy Pred'] = my_submission['energy'].map(lambda x: 'N' if x == 1 else 'S')
    my_submission['Nature Pred'] = my_submission['nature'].map(lambda x: 'T' if x == 1 else 'F')
    my_submission['Tactics Pred'] = my_submission['tactics'].map(lambda x: 'J' if x == 1 else 'P')
    personality=''
    personality =my_submission['Mind Pred'].to_string()[5]+my_submission['Energy Pred'].to_string()[5]+my_submission['Nature Pred'].to_string()[5]+my_submission['Tactics Pred'].to_string()[5]
    ##print("personality")
    ##print(personality)
    return personality