# FoodKG: A Software Tool to Enrich Knowledge Graphs on Food Datasets </br>

# Required libraries: 
1) TensorFlow 
2) Flask 
3) NLTK 
4) Werkzeug 
5) Beautiful Soup  


# Run FoodKG
All what you need to run the software is `python3 FoodKG.py`. You can find a simple input file in `Sample_Input` folder. </br>

# AGROVOC & AGROVEC
Our space vectors `AGROVEC` can be found in `Prediction/AGROVEC/` and there are 2 vectos `vectors.300d.txt` which is the default vector that FoodKG uses. If you want to try `vectors.50d.txt` then just change the vector name in `prepare_Models.py`. Moreover, if you would like to use `glove.42B.300d.txt` or compare it to our vector, then just add the vector to `Prediction/AGROVEC/` and change the name in `prepare_Models.py`. Get Glvoe from [here](https://nlp.stanford.edu/projects/glove/) </br>
By default, the loaded words are `10000`, you can change the number in `prepare_Models.py`. </br> </br>

Our vector was trained using `AGROVOC` triples dataset, which get be found [here](http://aims.fao.org/agrovoc/releases).




**References:** </br>
[NLTK](https://www.nltk.org/)</br>
