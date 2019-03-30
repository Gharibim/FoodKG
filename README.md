# FoodKG: A Software Tool to Enrich Knowledge Graphs on Food Datasets </br> </br>

**Required libraries:** 
1) TensorFlow 
2) Flask 
3) NLTK 
4) Werkzeug 
5) Beautiful Soup  </br></br>


**Run FoodKG**</br>
All what you need to run the software is `python3 FoodKG.py`. You can find a sample input file in `Sample_Input` folder. </br> </br>

**AGROVOC & AGROVEC**</br>
FoodKG will run and use our space vector `AGROVEC` by default. Our vectors can be found in `Prediction/AGROVEC/`. There are 2 versions: `agrovec.300d.txt` and `agrovec.50d.txt`. </br> 
Moreover, if you would like to use `Glove` or any other vector instead of `AGROVEC`, then add the new vector in the same directory and change the name in `prepare_Models.py`. Get Glvoe from [here](https://nlp.stanford.edu/projects/glove/) </br>
By default, the loaded words are `10000`, you can change the number in `prepare_Models.py`. </br></br>  



**Relations Prediction**</br>
FoodKG uses [Specialization Tensor Model (STM)](https://github.com/codogogo/stm) to predict triples predicates. However, we re-trained STM model on AGROVOC triples dataset. FoodKG will use our pre-trained model `Prediction/relations_prediction/args.output` by default. 

If you want to re-train the STM model by yourself, we provided for you the SPARQL queries that you need to extract the instances from a dataset `SPARQL_Queries`. In our case, we used `AGROVOC` triples dataset, which get be found [here](http://aims.fao.org/agrovoc/releases). After extracting the instances using SPARQL, check [STM Github](https://github.com/codogogo/stm) page to prepare the training data for STM. </br></br>


**Our vector vs. Glove**</br>
Classify an entity to a class
| Category | Instance | AGROVEC 300d | GloVe 300d | AGROVEC 50d | GloVe 50d |
| :---:       |     :---:      |      :---: | :---: | :---: | :---: |
| Fruit   | Apple     | .996    | .016 | .995 | .081 |




**References:** </br>

[Tensorflow](https://www.tensorflow.org/)</br>
[AGROVOC](http://aims.fao.org/vest-registry/vocabularies/agrovoc/)</br>
[GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)</br>
[Specialization Tensor Model (STM)](https://github.com/codogogo/stm)


