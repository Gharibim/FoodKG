# FoodKG: A Software Tool to Enrich Knowledge Graphs on Food Datasets </br> </br>

**Required libraries:** 
1) TensorFlow 
2) Flask 
3) NLTK 
4) Werkzeug 
5) Beautiful Soup  </br></br>


**Run FoodKG**</br>
All what you need to run the software is `python3 FoodKG.py`. You can find a simple input file in `Sample_Input` folder. </br> </br>

**AGROVOC & AGROVEC**</br>
Our space vectors `AGROVEC` can be found in `Prediction/AGROVEC/` and there are 2 vectos `vectors.300d.txt` which is the default vector that FoodKG uses. If you want to try `vectors.50d.txt` then just change the vector name in `prepare_Models.py`. Moreover, if you would like to use `glove.42B.300d.txt` or compare it to our vector, then just add the vector to `Prediction/AGROVEC/` and change the name in `prepare_Models.py`. Get Glvoe from [here](https://nlp.stanford.edu/projects/glove/) </br>
By default, the loaded words are `10000`, you can change the number in `prepare_Models.py`. </br> 

Our vector was trained using `AGROVOC` triples dataset, which get be found [here](http://aims.fao.org/agrovoc/releases). </br>
To extract classes and instances, use SPARQL queries in `SPARQL_Queries` folder.
</br> </br> 


**Relations Prediction**</br>
FoodKG uses [Specialization Tensor Model (STM)](https://github.com/codogogo/stm) to predict triples predicates. We re-trained STM model on AGROVOC. FoodKG will use our model `Prediction/relations_prediction/args.output` by default. To re-train this model, you can use the SPARQL Queries that can be found in `SPARQL_Queries` to extract AGROVOC instances, then check [STM Github](https://github.com/codogogo/stm) page to prepare the training data. </br></br>




**References:** </br>

[Tensorflow](https://www.tensorflow.org/)</br>
[AGROVOC](http://aims.fao.org/vest-registry/vocabularies/agrovoc/)</br>
[GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)</br>
[Specialization Tensor Model (STM)](https://github.com/codogogo/stm)


