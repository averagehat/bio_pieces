'''
figure out parseargs by file extension and variable number.
'''
from functools import partial
from Bio.Seq import SeqIO
import itertools as it
#def amos_reds_as_df(amos_obj):
#    iids_and_seq_strings = (red.iid, red.seq) for red in am.reds.values() 
#    return pd.DataFrame(, columns=['iid', 'seq']).set_index('seq')
#

#def fastq_records_as_df(bioseq_recs):
#    strings_and_objects =(seq.seq.tostring(), seq) for seq in fq
#    columns=['seq', 'seq_obj']
#    df =  pd.DataFrame(strings_and_objects, columns)
#    return df.set_index('seq') 
SEQKEY='seq'

def flatten_multiple_seq_files(filenames, format):
    open_biofile = partial(SeqIO.parse, format=format)
    return it.chain(*map(open_biofile, filenames) 

def add_cumcount_index(df):
   return df.set_index(df.groupby(df.index).cumcount(), append=True)

# Assumes index has been properly set
def join_non_unique_dataframes(df1, df2):
   df_multi_index_1, df_multi_index_2 = map(add_cumcount_index, (df1, df2))
   return df_multi_index_1.join(df_multi_index_2)
        
def df_from_collection_attributes(columns, collection):
    lambdas = [lambda obj: getattr(obj, column) for column in columns]
    return collection_as_df(lambdas, columns, collection)
'''
Index defaults to first column
'''
def collection_as_df(lambdas, columns, collection, index=None):
    assert len(lambdas) == len(columns), "lambdas must have same length as columns"
    values = (( func(obj) for func in lambdas) for obj in collection)
    df = pd.DataFrame(values, columns=columns)
    return df.set_index(index) if index else df.set_index(columns[0])


amos_reds_as_df = partial(df_from_collection_attributes, ['seq', 'iid'])
bio_records_as_df = partial(collection_as_df, [lambda rec: rec.seq.tostring(), lambda rec: rec], ['seq', 'seq_obj'])
#bio_file_as_df = lambda filename, ftype: bio_records_as_df(SeqIO.parse(filename, ftype))
fastq_file_as_df = partial(bio_file_as_df, 'fastq') 
fasta_file_as_df = partial(bio_file_as_df, 'fasta')


def get_iids(contig):
   return (tle.src for tle in contig.tlelist)

def get_df_subset(df, iterable, key=None):
   return df[df.index.isin(iterable)] if not key else df[df[key].isin(iterable)]


def write_sequence_dataframe(df, outfile, format)
    records = df['seqs']
    SeqIO.write(records, outfile, format)

def extract_dfs_by_ctg(df, contigs):
    iids_by_ctg = map(get_iids, contigs)
    get_df_subset_seqs = partial(get_df_subset, df, key='seq')
    dfs_by_ctg = map(get_df_subset_seqs, iids_by_ctg)
    return dfs_by_ctg

def make_fastqs_by_contigs(fastq_filenames, amos_filename, format='fastq'):
    fastq_records = flatten_multiple_seq_files(fastq_filenames, format) 
    fastq_df = bio_records_as_df(fastq_records) 
    amos_obj = amos.AMOS(open(amos_filename))
    reds_df = amos_reds_as_df(amos_obj.reds)
    reds_with_seqs_df = join_non_unique_dataframes(reds_df, fastq_df)
    contigs = amos_obj.ctgs.values()
    dfs_by_ctg = extract_dfs_by_ctg(reds_with_seqs_df, contigs)
    write_to_file = partial(write_sequence_dataframe, format=out_format)
    filenames = ("{0}.{1}".format(ctg.eid, format) for ctg in contigs)
    map(write_to_file, dfs_by_ctg, filenames)
    return 0

def main():
    args = myargs.parse_args()
    return make_fastqs_by_contigs(fastqs, amos_file)

         

