# Sim test data

MaxBin contigs under `fastas/` are ~2000 bp contigs pulled from Akkermansia and B fragilis genomes.

SAM files under `sams/` are 250 length reads distributed over the MaxBin contigs:

-   Akk_001.sam
    -   over k141_0 has a clump towards the end
    -   over k141_2 is evenly spaced
-   Bfrag_001.sam
    -   over k141_0 has a clump towards the start
    -   over k141_2 has a clump towards the end
-   Akk_002.sam is 
-   Bfrag_002.sam is 

These patterns should be observable in the first column of the output. The only fields that meaningfully change in the test SAMs are the first (read name), third (contig name), and fourth (starting position on contig). If other fields become interesting in future versions (i.e. start using the sequence somehow), the test data will have to be updated.
