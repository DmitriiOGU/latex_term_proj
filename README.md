# latex_term_proj

## Definition
Проект по распознаванию математических определений в <img src="https://render.githubusercontent.com/render/math?math=\LaTeX"> документах




## Requirements

apyori
## Class files
File_loader.py - Описывает класс File_loader (отвечает за методы для загрузки файлов и передачи их в Parser_of_file)

Parser_of_file.py -  Описывает класс Parser_of_file (отвечает за методы парсинга файлов)

## Folders

download/CO_fold - Папка с размеченными статьями

## Scripts

script.py - основной скрипт загрузки и обработки для майнинга понятий, заместо вызова apriori также можно использовать иной алгоритм, например TF-IDF

visualisation.ipynb - скрипт отвечающий за визауализацию эмбеддингов в 2D и 3D, для наглядного результата работы (данный алгоритм используется совместно с подбором перплексии)

Тренировка-Kfold-Xgboost-based.ipynb - скрипт для обучения моделей на задачу бинарной классификации "определения" в тексте документов

mathBERT_nn.ipynb - скрипт для обучения на векторном представлении MathBERT, модели нейронной сети

