def create_sample_sam_file(sam_file_path):
    # Create a sample SAM file for testing
    sample_sam_content = (
        "@SQ\tSN:Contig1\tLN:100\n"
        "read1\t0\tContig1\t1\t30\t30M\t*\t0\t0\tATCGATCGATATCGATCGATATCGATCGAT\n"
        "read2\t0\tContig1\t11\t30\t30M\t*\t0\t0\tGCTAGCTAGCGCTAGCTAGCGCTAGCTAGC\n"
    )
    with open(sam_file_path, "w") as f:
        f.write(sample_sam_content)


def create_sample_fasta_file(fasta_file_path):
    # Create a sample fasta file for testing
    sample_fasta_content = ">Contig1\nATCGATCGATCGATCGATATCGATCGATATCGATCGATGCTAGCTAGCGCTAGCTAGCGCTAGCTAGC\n>Contig2\nGCTAGCTAGCTAGCTAGCGCTAGCTAGCGCTAGCTAGCATCGATCGATATCGATCGATATCGATCGAT\n"
    with open(fasta_file_path, "w") as f:
        f.write(sample_fasta_content)


def create_sample_cov3_file(cov3_file_path):
    # Create a sample cov3 file for testing
    sample_cov3_content = [
        "log_cov,GC_content,sample,contig,length\n",
        "1.234,0.567,sample1,contig1,100\n",
        "1.234,0.567,sample1,contig1,100\n",
        "2.345,0.678,sample1,contig2,150\n",
        "3.456,0.789,sample2,contig2,150\n",
    ]
    with open(cov3_file_path, "w") as f:
        f.writelines(sample_cov3_content)
