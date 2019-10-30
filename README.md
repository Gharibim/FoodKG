# FoodKG: A Tool to Enrich Knowledge Graphs Using Machine Learning Techniques </br> </br>

**Run FoodKG with one command** </br>
FoodKG exists on Docker. To run our tool, just install docker on your machine: [Docker](https://docs.docker.com/docker-for-mac/install/) then run the following command:</br>
`docker run -p 5000:5000 gharibim/foodkg:3.1` </br>
FoodKG will start on the localhost, port 5000: `127.0.0.1:5000`</br>
You can find a sample input file in `Sample_Input` folder </br>
and sample context: `http://example.com`
</br></br>


**To reproduce the results and build from scratch follow these steps:** 

**Required libraries:** 
1) TensorFlow 
2) Flask 
3) NLTK 
4) Werkzeug 
5) Beautiful Soup
6) Requests </br>
Install [AGROVEC Embedding model](https://drive.google.com/file/d/1Xsw3C_Y0T52sawssbfyGsjA_0ig2EuLx/view?usp=sharing) from Google drive, unzip it then place in `FoodKG/Prediction/AGROVEC/`.</br>
After that, download [Apache Jena](https://jena.apache.org/download/index.cgi) and place it in Apache Jena directory.</br>
Finally run `python3 FoodKG.py` which is the main script that will start Flask server at localhost. </br>
</br>



**AGROVOC & AGROVEC**</br>
FoodKG will run and use our space vector `AGROVEC` by default. Our vector can be found in `Prediction/AGROVEC/`. </br> 
Moreover, if you would like to use `Glove` or any other vector instead of `AGROVEC`, then add the new vector in the same directory and change the name in `prepare_Models.py`. Get Glvoe from [here](https://nlp.stanford.edu/projects/glove/) </br>
By default, the loaded words are `1000000`, you can change the number in `prepare_Models.py`. </br></br>  



**Relations Prediction**</br>
FoodKG uses [Specialization Tensor Model (STM)](https://github.com/codogogo/stm) to predict the relation between newly added triples. However, we re-trained STM model on AGROVOC triples dataset. FoodKG will use our pre-trained model `Prediction/relations_prediction/args.output` by default. 

If you want to re-train the STM model by yourself, we provided the SPARQL queries that you will need to extract the instances from a dataset `SPARQL_Queries`. In our case, we used `AGROVOC` triples dataset, which get be found [here](http://aims.fao.org/agrovoc/releases). After extracting the instances using SPARQL, check [STM Github](https://github.com/codogogo/stm) page to prepare the training data for STM. </br></br>



**References:** </br>
[GEMSEC: Graph Embedding with Self Clustering](https://arxiv.org/pdf/1802.03997.pdf)
[Specialization Tensor Model (STM)](https://github.com/codogogo/stm)
[Stanford Parser](https://nlp.stanford.edu/software/lex-parser.shtml)
[Tensorflow](https://www.tensorflow.org/)</br>
[AGROVOC](http://aims.fao.org/vest-registry/vocabularies/agrovoc/)</br>
[GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)</br>
[Apache Jena](https://jena.apache.org/download/index.cgi)


