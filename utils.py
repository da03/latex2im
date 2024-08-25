import sys, os
import uuid
import shutil
import subprocess


def normalize_formula(formula):
    unique_filename = str(uuid.uuid4()) + '.tex'
    with open(unique_filename, 'w') as fout:
        fout.write(formula)

    input_file = unique_filename
    output_file = unique_filename + '.out'
    assert os.path.exists(input_file), input_file
    cmd = "perl -pe 's|hskip(.*?)(cm\\|in\\|pt\\|mm\\|em)|hspace{\\1\\2}|g' %s > %s"%(input_file, output_file)
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        assert False

    temp_file = output_file + '.tmp'
    with open(temp_file, 'w') as fout:  
        with open(output_file) as fin:
            for line in fin:
                fout.write(line.replace('\r', ' ').strip() + '\n')  # delete \r

    cmd = "cat %s | node scripts/preprocessing/preprocess_latex.js %s > %s "%(temp_file, 'normalize', output_file)
    ret = subprocess.call(cmd, shell=True)
    os.remove(temp_file)
    if ret != 0:
        assert False
    temp_file = output_file + '.tmp'
    shutil.move(output_file, temp_file)
    with open(temp_file) as fin:
        with open(output_file, 'w') as fout:
            for line in fin:
                tokens = line.strip().split()
                tokens_out = []
                for token in tokens:
                    if True or is_ascii(token):
                        tokens_out.append(token)
                fout.write(' '.join(tokens_out)+'\n')
    formula_normalized = open(output_file).read().strip()
    os.remove(temp_file)
    os.remove(input_file)
    os.remove(output_file)
    return formula_normalized
#import pdb; pdb.set_trace()
#a = 'Markup-to-Image Diffusion Models with Scheduled Sampling'
#b = normalize_formula(a)
#
#a = 'Yuntian Deng, Noriyuki Kojima, Alexander M. Rush'
#b = normalize_formula(a)
#
#
#a = r'\frac{Yuntian Deng}{,} Noriyuki Kojima, Alexander M. Rush'
#b = normalize_formula(a)
#a = r'\frac{Yuntian Deng{,} Noriyuki Kojima, Alexander M. Rush'
#b = normalize_formula(a)
