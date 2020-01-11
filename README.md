https://drive.google.com/file/d/17j6pSKZt5TtJ8oQCDNIwlSZ0q5w7NNBg/view?usp=sharing  
Распаковать архив по ссылке в папку BIOBERT_DIR  
launch.sh output/directory для запуска  
  

В папке заданной при запуске sh скрипта создаётся две папки для каждого фолда.Первая с результатами теста на Cadec, вторая с результатами теста на psytar.Внутри этих папок будет папка brat_output с тестовыми данными, размеченными после работы biobert, в формате брат и файл metrics.txt с оценками  
  
Папку brat_files из https://github.com/dartrevan/medical_text_processing/blob/master/dataset/russian_reviews.tar.gz скопировать в папку data.  
one_corpus.sh output/directory для запуска

