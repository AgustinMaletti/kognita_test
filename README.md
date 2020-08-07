# Kognita Lab test
#### Objetivo:
* Desenvolver Scraper para Stack Overflow
* Disponibilizar dados por meio de uma Api Flask

Para usar por favor primeiro faça o download do repositorio.

Ative o virtualenv kognita_venv ou instale todas as dependencias no seu sistema python com:
* pip install -r requirements.txt

Para usar, por favor se posicionar na pasta kognita e correr alguma das siguintes opções:

*   python -m source.main -e scraper

*   python -m source.main -e api

*   python -m source.main -e test_api

*   python -m source.main -e test_scraper

*   python -m source.main --help

A primeira opção inicia o scraper para a coleta de dados, o programa vai pedir informação com inputs ao usuario, 
para configurar o coletor de dados.

A segunda opção inicia uma api flask no localhost porto 5000.

Tambem é possivel coletar dados usando a spider de scrapy, para isso deve se posicionar dentro da pasta spiders aonde se encontra o arquivo QuestionSpider.py,
ali se corre o siguinte comando:

* scrapy crawl QuestionSpider -o arquivo_novo.json -a tag=python


Os siguintes endpoints estão disponiveis no Api:
* GET /get_data/<author_name>

* Retorna 200 e a seguinte estrutura de dados se existir author com perguntas:


```
data = { "question": {"question_title": "",
                       "question_text": "",
                       "question_author_name": "",
                       "question_author_link": "",
                       "question_date": "",
                       "question_tags": "" ,
                       "question_comments": [{"text": "",
                                              "author": "",
                                                "date": ""}],
											          
                       "user_answers_made": "",
                       "user_questions_made": "",
                       "user_people_reached": "",
                       "user_member_since": "",
                       "user_profile_view": "",
                       "user_last_see": ""			          
          				      
                       "all_answer": [{"answer_text": "",
                                       "answer_author": "",
                                       "answer_date": "",
                                       "answer_comments": [{"text": "",
                                                             "author":"",
                                                             "date": "",
												 			       }],
                        	  }]
                   }
    }



```
* Retorna 404 se não encontro dados para esse author e a seguinte estrutura de dados:

```
{"data": "No data for that user"}
```

* GET /user_list

* Retorna 200 e a siguinte estrutura de dados:

```

{  "author_list": [
    "pher", 
    "Samirite", 
    "requiredtomato", 
    "Steelcrawler", 
    "joy jolie", 
    "tad321", 
    "Mike Williamson", 
    "BananaMaster", 
    "Vincent Stevenson", 
    "Saad Khalfaoui", 
    "George Frangs", 
    "saeed", 
    "Neel", 
    "PiCubed", 
    "Aurangzeb", 
    "etcTryAgain", 
    "Christian Magelssen", 
    "FlutterLover", 
    "Heisenberg666", 
    "Narfanator", 
    "Asmaa", 
    "nipun vats", 
    "Karthik Viz", 
    "Johnny_Mali39", 
    "Dkage", 
    "Manu Dua", }
    
    
```
