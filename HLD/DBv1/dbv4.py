1. Data in sorted. read in login
2. key value -> 



a|1
b|2
c|3


ram
shyam
ujjwal-+

Full database
Full persistance
Fast read 
Fast write
Durable


Memory -> 
    Tree -> 
        update -> log(n)
        read -> log(n)

    10k

    Problem -> 
        Disk -> 
            save it on file 
                Journal -> 

Job -> 


Tree -> inorder traversal -> 
        Sorted data

File -> Sorted data -> 
        log(n)




# Log Structured Merge Tree LSM DB

tree -> 10000
    3000 Node
Journal -> 
File 
    2-file
    1-file
    0-file

Read -> 
    1. Search on Tree -> log(10000) -> O(1)
    2. Search on Files ->   
        log(n)

Write -> 
    Journal -> Ultra fast -> Sequential Write
    Tree Add -> Ultra fast -> 

Job 
    -> Inorder
    -> Seq Write 
    -> CPU, IOPS
    -> Limited Number IOPS. 
    -> 50GBPS -> 45GBPS -> 5 gbps > 6Terabyte

Tombstone

Problems -> 
