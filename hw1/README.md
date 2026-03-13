# ДЗ 1
Данная директория содержит выполненное ДЗ 1.

## Task 1
### Файлы:
[complement.py](complement.py) -- содержит код, написанные в рамках задания 2.2.

### Описание:
Репозиторий был успешно скопирован и заполнен необходимыми файлами. Код, печатающий reverse-complement последовательности и ее GC-состав, был помещен в файл [complement.py](complement.py) и проверен на работоспособность. Файл был сохранен, закоммичен и отправлен на github командой ```git add ./hw1/*; git commit -m "task1"; git push origin main``` . Тег был прикреплен к "голове" командой ```git tag task1``` .

## Task 2
### Файлы:
[count_kmers.py](count_kmers.py) -- содержит код, написанные в рамках задания 3.1.
[test.fna](test.fna) -- fasta файл для тестирования скрипта [count_kmers.py](count_kmers.py).
[cnts.json](cnts.json) -- результат работы скрипта [count_kmers.py](count_kmers.py) на [test.fna](test.fna).

### Описание:
Код, считающий количество 4-меров в последовательностях fasta файла, был помещен в файл [count_kmers.py](count_kmers.py) и проверен на работоспособность. Файл был сохранен, закоммичен и отправлен на github командой ```git add *; git commit -m "task2.2"; git push origin main``` . В коде на github значение k было заменено с 4 на 2 и был добавлен небольшой комментарий. Далее в локальной реплике были добавлены опции ```-k``` и ```--out``` в соответствии с заданием. Попытка коммита с помощью команды ```git add *; git commit -m "task2.5"``` прошла успешно, проблемы возникли на стадии пуша:
```
To https://github.com/AeddCirran/fbb_orch_hw.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/AeddCirran/fbb_orch_hw.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
Для решения проблемы был осуществлен пулл (```git pull origin main```), проблемный файл был опознан командой ```git status```. Несовместимости (рис. 1) в ```count_kmers.py``` были исправлены вручную.

<img src="merge_conflict.png" alt="Рис. 1" width="600" height="250">

Итоговый файл был успешно сохранен, закоммичен и отправлен на github (```git add count_kmers.py; git commit -m "task2.6"; git push origin main```) .