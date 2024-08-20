# run Quality Check against new sub data

import os
import sys
import pandas as pd

def parse_cmd_args():
    import argparse
    parser = argparse.ArgumentParser(description='QC for ATS')
    parser.add_argument('-s', type=str, help='Path to submission')
    parser.add_argument('-o', type=str, help='Path to output for QC plots and Logs')
    parser.add_argument('-sub', type=str, help='Subject ID')

    return parser.parse_args()

def df(submission):
    submission = pd.read_csv(submission)
    return submission

def qc(submission):
    # convert submission to DataFrame
    submission = df(submission)
     # check if submission is a DataFrame
    if not isinstance(submission, pd.DataFrame):
        raise ValueError('Submission is not a DataFrame. Could not run QC')
    # check if submission is empty
    if submission.empty:
        raise ValueError('Submission is empty')

    # check if submission has correct number of rows (within 5% of expected = 180)
    if len(submission) < 171 or len(submission) > 189:
        raise ValueError('Submission has incorrect number of rows')
    
def plots(submission, output, sub):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os

    #load csv
    df = pd.read_csv(submission)

    #drop practice data
    df = df[df['block'] == 'test']

    percent_res = df['response'].apply(lambda x: 1 if x != 'None' else 0)
    percent_res = percent_res.groupby(df['block_cond']).mean()

    percent_corr = df['correct'].groupby(df['block_cond']).mean()

    #plot percent responded by block
    plt.figure()
    sns.barplot(x=percent_res.index, y=percent_res.values)
    plt.title('Percent Responded by Block')
    plt.xlabel('Block')
    plt.ylabel('Percent Responded')
    plt.savefig(os.path.join(output, f'{sub}_ATS_percent_responded.png'))
    plt.close()

    #plot percent correct by block
    plt.figure()
    sns.barplot(x=percent_corr.index, y=percent_corr.values)
    plt.title('Percent Correct by Condition')
    plt.xlabel('Condition')
    plt.ylabel('Percent Correct')
    plt.savefig(os.path.join(output, f'{sub}_ATS_percent_correct.png'))
    plt.close()

    #plot response time by block
    plt.figure()
    sns.stripplot(x='block_cond', y='response_time', data=df, hue='correct', jitter=True)
    sns.boxplot(x='block_cond', y='response_time', data=df, showcaps=False, boxprops={'facecolor':'None'}, showfliers=False)
    plt.title('Reaction Time by Condition')
    plt.ylabel('Reaction Time')
    plt.xlabel('Condition')
    plt.savefig(os.path.join(output, f'{sub}_ATS_rt.png'))
    plt.close()



    

def main():

    #parse command line arguments
    args = parse_cmd_args()
    submission = args.s
    output = args.o
    sub = args.sub

    # check if submission is a csv
    if not submission.endswith('.csv'):
        raise ValueError('Submission is not a csv')
    # check if submission exists
    if not os.path.exists(submission):
        raise ValueError('Submission does not exist')
    # run QC
    qc(submission)
    
    print(f'QC passed for {submission}, generating plots...')
    # generate plots
    plots(submission, output, sub)
    return submission
    
    
if __name__ == '__main__':
    main()


