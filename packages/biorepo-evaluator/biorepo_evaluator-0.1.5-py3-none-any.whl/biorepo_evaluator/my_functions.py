import pkgutil
import pandas as pd
import plotly.express as px
import glob

data = pkgutil.get_data(__name__, 'all_corpuses.xlsx')

# excel_files = glob.glob("*.xlsx")

# excel_file_path = excel_files[0]
xls = pd.ExcelFile(data)

def get_all_entities():
    return ['dataset', 'analysis', 'tool', 'gene', 'genome', 'nucleotide']


def get_query_terms(entity):
    if entity=="dataset":
        return ["publication_title", "publication_description", "publication_keywords"]
    elif entity=="analysis":
        return ["publication_title", "publication_description", "publication_keywords"]
    elif entity=="tool":
        return ["dataset_title", "dataset_description", "dataset_keywords"]


def get_queries(entity, term):
    df = pd.read_excel(xls, entity)
    return df[term].tolist()

def get_evaluations(entity, term, question_answers_from_user):

    query_list = []
    actual_output_list = []
    position_list = []
    total_outputs_list = []    

    if(entity=="dataset"):
        dataset_df = pd.read_excel(xls, 'dataset')
        if term=="publication_title":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_title'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_dataset']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))
                    
        elif term=="publication_description":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_description'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_dataset']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))

        elif term=="publication_keywords":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_keywords'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_dataset']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))

    elif(entity=="tool"):
        dataset_df = pd.read_excel(xls, 'tool')
        if term=="publication_title":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_title'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_tool']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))
                    
        elif term=="publication_description":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_description'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_dataset']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))

        elif term=="publication_keywords":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['publication_keywords'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_dataset']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))

    elif(entity=="analysis"):
        dataset_df = pd.read_excel(xls, 'analysis')
        if term=="dataset_title":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['dataset_title'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_analysis']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))
                    
        elif term=="dataset_description":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['dataset_description'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_analysis']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))

        elif term=="dataset_keywords":
            for data in question_answers_from_user:
                query = data["query"]
                user_outputs = data["answers"]

                filtered_df = dataset_df[dataset_df['dataset_keywords'] == query]
                if not filtered_df.empty:
                    actual_output = filtered_df.iloc[0]['original_analysis']
                    position = user_outputs.index(actual_output) + 1 if actual_output in user_outputs else 0

                    query_list.append(query)
                    actual_output_list.append(actual_output)
                    position_list.append(position)
                    total_outputs_list.append(len(user_outputs))
    
    elif(entity=="gene"):
        pass    
    elif(entity=="genome"):
        pass
    elif(entity=="nucleotide"):
        pass

    df = pd.DataFrame({
        'query': query_list,
        "actual_output": actual_output_list,
        'position': position_list,
        'num_of_results': total_outputs_list
    })
    get_precision(df)
    get_precision_rate(df)
    get_retrieval_rate(df)

def get_precision(df):
    precision_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['position']==0:
            row['precision'] = 0
            row['TP'] = 0
            row['FP'] = 0
        else:
            row['TP'] = 1
            row['FP'] = row['num_of_results'] - 1
            row['precision'] = row['TP'] / (row['TP']+row['FP'])

        new_data = {
            'query': row['query'],
            'actual_output': row['actual_output'],
            'TP': row['TP'],
            'FP': row['FP'],
            'precision': row['precision']
        }
        precision_df = pd.concat([precision_df, pd.DataFrame([new_data])], ignore_index=True)

    fig = px.scatter(precision_df, x='query', y='precision', title='Precision plot')
    fig.update_traces(mode='markers', marker=dict(size=12))
    fig.update_layout(xaxis_title='Query', yaxis_title='Precision')
    fig.show()
    print("The mean precision is ", precision_df['precision'].mean())
    precision_df.to_csv('precisions.csv', index=False)


def get_precision_rate(df):
    precision_rate_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['position']==0:
            row['precision_rate'] = 0
            row['TP_rate'] = 0
            row['FP_rate'] = 0
        else:
            row['TP_rate'] = (row['num_of_results'] - row['position'] + 1) / row['num_of_results']
            row['FP_rate'] = 1 - row['TP_rate']
            row['precision_rate'] = row['TP_rate'] / (row['TP_rate']+row['FP_rate'])

        new_data = {
            'query': row['query'],
            'actual_output': row['actual_output'],
            'TP_rate': row['TP_rate'],
            'FP_rate': row['FP_rate'],
            'precision_rate': row['precision_rate']
        }
        precision_rate_df = pd.concat([precision_rate_df, pd.DataFrame([new_data])], ignore_index=True)

    fig = px.scatter(precision_rate_df, x='query', y='precision_rate', title='Precision rate plot')
    fig.update_traces(mode='markers', marker=dict(size=12))
    fig.update_layout(xaxis_title='Query', yaxis_title='Precision Rate')
    fig.show()
    print("The mean precision rate is ", precision_rate_df['precision_rate'].mean())
    precision_rate_df.to_csv('precision_rates.csv', index=False)

def get_retrieval_rate(df):
    retrieval_rate_df = pd.DataFrame()
    for index, row in df.iterrows():
        if row['position']==0:
            row['retrieval_rate'] = 0
        else:
            row['retrieval_rate'] = 1

        new_data = {
            'query': row['query'],
            'actual_output': row['actual_output'],
            'retrieval_rate': row['retrieval_rate']
        }
        retrieval_rate_df = pd.concat([retrieval_rate_df, pd.DataFrame([new_data])], ignore_index=True)

    fig = px.scatter(retrieval_rate_df, x='query', y='retrieval_rate', title='Retrieval rate plot')
    fig.update_traces(mode='markers', marker=dict(size=12))
    fig.update_layout(xaxis_title='Query', yaxis_title='Retrieval Rate')
    fig.show()
    print("The mean retrieval rate is ", retrieval_rate_df['retrieval_rate'].mean())
    retrieval_rate_df.to_csv('retrieval_rates.csv', index=False)



# get_evaluations('dataset', 'publication_title', [{
#     "query": "FGFR3 stimulates stearoyl CoA desaturase 1 activity to promote bladder tumor growth",
#     "answers": ["x", "y", "FGFR3 stimulates stearoyl CoA desaturase 1 activity to promote bladder tumor growth"]
# },
# {
#     "query": "TranscriptomeWide Cleavage Site Mapping on Cellular mRNAs Reveals Features Underlying SequenceSpecific Cleavage by the Viral Ribonuclease SOX",
#     "answers": ["i","Transcriptome-wide mapping of cut sites of the viral endoribonuclease SOX from Kaposi's sarcoma-associated herpesvirus (KSHV)", "y", "FGFR3 stimulates stearoyl CoA desaturase 1 activity to promote bladder tumor growth"]
# }])