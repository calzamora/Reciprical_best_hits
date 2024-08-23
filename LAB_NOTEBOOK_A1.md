# Assignment 1 - Reciprocal Best Hits 

data lives: 
```
/projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp
/projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp
```

working directory : 
/projects/bgmp/calz/bioinfo/Bi623/Assignment_1

Goal pt 1: 
sort by seq id and then sort by evalue and output to a new file 

```
$ sort -n -k 1 /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp | sort -n -k11 > ./Z_to_homodb_SORTED.blastp
$ sort -n -k 1 /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp | sort -n -k 11 > ./H-to_zfishdb_SORTED.blasp
```

python script to: 
filter blastp results to retain only best hit(s) (lowest e score) for each protein ID:\
[best_hits.py](best_hit.py)

ok the file is written but the output isnt comparing to wes' so i think my og sorted files were done wrong
the sort piping i was doing was was overwriting the sort of collum 1 w column 11 so I have to combine them into the same 
sort 

https://stackoverflow.com/questions/41231186/sort-by-multiple-columns-in-bash

```
$ sort -k 1,1 -k11,11g /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/Z_to_homodb.blastp > ./Z_to_homodb_SORTED.blastp
$ sort -k 1,1 -k11,11g /projects/bgmp/shared/Bi623/PS7_RBH_Bi623/H_to_zfishdb.blastp > ./H-to_zfishdb_SORTED.blastp
```
ok i think that should give me well sorted files so Im gunna rerun them:

```
$ ./best_hit.py -f H-to_zfishdb_SORTED.blastp -o H-to_zfishdb_BESTHIT.blastp
$ ./best_hit.py -f Z_to_homodb_SORTED.blastp -o Z_to_homodb_BESTHIT.blastp 
```

ok i think that worked!! 

### part 2: 

remove duplicates: 
loop through the file 2x 
1) is the query id (feild 0) a duplicate? if yes add it to a set 
2) write any line that is NOT IN THE SET to a new file 

eaving you with only 1 entry of every query id 