from collections import namedtuple


nt_coding_snv = namedtuple('CodingSNV', 
                        ['indel_frameshift', 'indel_nonframeshift', 'nonsynonymous', 'splicing', 'stopgain', 'stoploss', 'synonymous'])
coding_snv = nt_coding_snv(indel_frameshift='#FF8C00', indel_nonframeshift='#003366', nonsynonymous='#698B69',
                            splicing='#00CED1', stopgain='#8B4789', stoploss='#DA70D6', synonymous='#FFD700')


nt_noncoding_snv = namedtuple('NoncodingSNV',
                            ['enhancer', 'insulator', 'intergenic', 'intronic', 'lncRNA', 'miRNA', 'noncoding', 'operator', 'promoter',
                            'rRNA', 'silencer', 'sncRNA', 'tRNA', 'telomeres', 'utr5_utr3'])
noncoding_snv = nt_noncoding_snv(enhancer='#7F000F', insulator='#FFC1C9', intergenic='#7F7F7F', intronic='#4D4D4D', lncRNA='#331900',
                                miRNA='#FFE0C1', noncoding='#A80015', operator='#A84955', promoter='#4C191E', rRNA='#E7B98A',
                                silencer='#E78A96', sncRNA='#594027', tRNA='#A87849', telomeres='#B3B3B3', utr5_utr3='#1A1A1A')


nt_structural_variants = namedtuple('StructuralVariants', ['CNA_gain', 'CNA_loss', 'inversion', 'translocation', 'transposition'])
structural_variants = nt_structural_variants(CNA_gain='#FF0000', CNA_loss='#0000FF', inversion='#FFA500', translocation='#458B00',
                                            transposition='#7300E7')


nt_chromosomes = namedtuple('Chromosomes', ['chr1', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17',
                                            'chr18', 'chr19', 'chr2', 'chr20', 'chr21', 'chr22', 'chr3', 'chr4', 'chr5', 'chr6',
                                            'chr7', 'chr8', 'chr9', 'chrX', 'chrY'])
chromosomes = nt_chromosomes(chr1='#DE47AB', chr10='#7D32B3', chr11='#88DB68', chr12='#78AAF1', chr13='#D9C6CA', chr14='#336C80',
                            chr15='#F7CA44', chr16='#32C7C7', chr17='#D4C5F2', chr18='#995493', chr19='#F88B78', chr2='#72BE97',
                            chr20='#475ECC', chr21='#E0BD8C', chr22='#9E2800', chr3='#F7F797', chr4='#7C749B', chr5='#E85726',
                            chr6='#B395F8', chr7='#DC8747', chr8='#96D53D', chr9='#DC85EE', chrX='#F2BBD2', chrY='#B6EBEA')


nt_sex = namedtuple('Sex', ['male', 'female'])
sex = nt_sex(male='#B6EBEA', female='#F2BBD2')


nt_stage_arabic = namedtuple('StageArabic', ['st1', 'st2', 'st3', 'st4'])
stage_arabic = nt_stage_arabic(st1='#FFFFFF', st2='#FFFF00', st3='#FFA500', st4='#FF0000')


nt_stage_roman = namedtuple('StageRoman', ['st1', 'st2', 'st3', 'st4'])
stage_roman = nt_stage_roman(st1='#FFFFFF', st2='#FFE4B5', st3='#EEE8AA', st4='#FFFF00')


nt_t_category = namedtuple('TCategory', ['t0', 't1', 't2', 't3', 't4', 'tx'])
t_category = nt_t_category(t0='#FFFFFF', t1='#FFD399', t2='#FFAE45', t3='#B87217', t4='#774607', tx='#708090')


nt_n_category = namedtuple('NCategory', ['n0', 'n1', 'n2', 'n3', 'n4', 'nx'])
n_category = nt_n_category(n0='#FFFFFF', n1='#FFD399', n2='#FFAE45', n3='#B87217', n4='#774607', nx='#708090')


nt_m_category = namedtuple('MCategory', ['m0', 'm1', 'mx'])
m_category = nt_m_category(m0='#FFFFFF', m1='#000000', mx='#708090')


nt_grade = namedtuple('Grade', ['g1', 'g2', 'g3', 'g4'])
grade = nt_grade(g1='#FFFFFF', g2='#9CF0FC', g3='#335FE5', g4='#003366')


nt_prostate_grade = namedtuple('ProstateGrade', ['g3_3', 'g3_4', 'g3_5', 'g4_3', 'g4_4', 'g4_5', 'g5_3', 'g5_4', 'g5_5'])
prostate_grade = nt_prostate_grade(g3_3='#FFFFFF', g3_4='#FFFF00', g3_5='#CD2990', g4_3='#FFA500', g4_4='#FF0000',
                                    g4_5='#A52A2A', g5_3='#8B008B', g5_4='#0000CD', g5_5='#000000')


nt_primary_met = namedtuple('PrimaryMet', ['metastatic', 'primary'])
primary_met = nt_primary_met(metastatic='#7217A5', primary='#FFFFFF')


nt_tumour_subtype = namedtuple('TumourSubtype', ['Biliary_AdenoCA', 'Bladder_TCC', 'Bone_Epith', 'Bone_Osteosarc',
                                                    'Breast_AdenoCA', 'CNS_GBM', 'CNS_Medullo', 'CNS_Oligo', 'CNS_PiloAstro',
                                                    'Cervix_SCC', 'ColoRect_AdenoCA', 'Eso_AdenoCA', 'Head_SCC', 'Kidney_ChRCC',
                                                    'Kidney_RCC', 'Liver_HCC', 'Lung_AdenoCA', 'Lung_SCC', 'Lymph_BNHL', 'Lymph_CLL',
                                                    'Myeloid_AML', 'Myeloid_MPN', 'Ovary_AdenoCA', 'Panc_AdenoCA', 'Panc_Endocrine',
                                                    'Prost_AdenoCA', 'Skin_Melanoma', 'SoftTissue_Leiomyo', 'SoftTissue_Liposarc',
                                                    'Stomach_AdenoCA', 'Thy_AdenoCA', 'Uterus_AdenoCA'])
tumour_subtype = nt_tumour_subtype(Biliary_AdenoCA='#00CD66', Bladder_TCC='#EEAD0E', Bone_Epith='#ADAC44', Bone_Osteosarc='#FFD700',
                                    Breast_AdenoCA='#CD6090', CNS_GBM='#3D3D3D', CNS_Medullo='#D8BFD8', CNS_Oligo='#787878',
                                    CNS_PiloAstro='#B0B0B0', Cervix_SCC='#79CDCD', ColoRect_AdenoCA='#191970', Eso_AdenoCA='#1E90FF',
                                    Head_SCC='#8B2323', Kidney_ChRCC='#B32F0B', Kidney_RCC='#FF4500', Liver_HCC='#006400',
                                    Lung_AdenoCA='#FFFFFF', Lung_SCC='#FDF5E6', Lymph_BNHL='#698B22', Lymph_CLL='#698B22',
                                    Myeloid_AML='#CD6600', Myeloid_MPN='#FFC100', Ovary_AdenoCA='#008B8B', Panc_AdenoCA='#7A378B',
                                    Panc_Endocrine='#E066FF', Prost_AdenoCA='#87CEFA', Skin_Melanoma='#000000', SoftTissue_Leiomyo='#FFEC8B',
                                    SoftTissue_Liposarc='#CDCB50', Stomach_AdenoCA='#BFEFFF', Thy_AdenoCA='#9370DB', Uterus_AdenoCA='#FF8C69')


nt_low_sample_size_cohort = namedtuple('LowSampleSizeCohort', ['Bone_Cart', 'Breast_DCIS', 'Breast_LobularCA', 'Cervix_AdenoCA',
                                                                'Lymph_NOS', 'Myeloid_MDS'])
low_sample_size_cohort = nt_low_sample_size_cohort(Bone_Cart='#DDCDCD', Breast_DCIS='#DDCDCD', Breast_LobularCA='#DDCDCD',
                                                    Cervix_AdenoCA='#DDCDCD', Lymph_NOS='#DDCDCD', Myeloid_MDS='#DDCDCD')


nt_organ_system = namedtuple('OrganSystem', ['biliary', 'bladder', 'bone_softtissue', 'breast', 'cervix', 'cns', 'colon_rectum',
                                                'esophagus', 'head_neck', 'kidney', 'liver', 'lung', 'lymphoid', 'myeloid', 'ovary',
                                                'pancreas', 'prostate', 'skin', 'stomach', 'thyroid', 'uterus'])
organ_system = nt_organ_system(biliary='#00CD66', bladder='#EEAD0E', bone_softtissue='#FFEC8B', breast='#CD6090', cervix='#79CDCD',
                                cns='#787878', colon_rectum='#191970', esophagus='#1E90FF', head_neck='#8B2323', kidney='#FF4500',
                                liver='#006400', lung='#FDF5E6', lymphoid='#698B22', myeloid='#CD6600', ovary='#008B8B',
                                pancreas='#7A378B', prostate='#87CEFA', skin='#000000', stomach='#BFEFFF', thyroid='#9370DB',
                                uterus='#FF8C69')
