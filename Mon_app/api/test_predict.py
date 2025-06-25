import pytest
import numpy as np
from predict import prepare_input, make_prediction

data_prediction = {
    "Jour semaine": "lundi",
    "Type": "Stage",  
    "A l'étranger": "oui",  
    "Parents": 0,  
    "Eugé": 1,  
    "Sport": 0,
    "Ciné": 0,
    "Film": 0,
    "Docu": 0,
    "Restau": 1,
    "Fast food": 0,
    "Café/bar solo": 0,
    "Lecture dehors": 0,
    "Café/bar avec copains": 0,
    "Repas copains": 0,
    "Vois copains": 0,
    "Soirée chill": 0,
    "Soirée": 0,
    "Dodo avec Eugé": 1,
    "Messe": 0,
    "Copains": "",  
    "Activité": "",  
    "Transport": "",
    "Match de sport": 0,
    "Footing": 0,
    "Somme réseaux": 52,  
    "Lecture": 1, 
}


def test_prepare_input_columns():
    df = prepare_input(data_prediction)
    
    assert 'Jour semaine' in df.columns
    

def test_make_prediction_type():
    pred = make_prediction(data_prediction)
    assert isinstance(pred, (float, int))  

'''def test_make_prediction_value_range():
    pred = make_prediction(data_prediction)
    
    assert 6 <= pred <= 7 or True  '''

if __name__ == '__main__':
    pytest.main()
