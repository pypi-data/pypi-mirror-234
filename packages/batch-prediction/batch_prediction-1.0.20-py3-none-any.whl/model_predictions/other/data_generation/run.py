import os, re

from utility.model_train import fetch_and_clean_data, get_numerical_and_categorical_col, set_hyperparameters, \
    train_model, train_conditional
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from refractio import get_dataframe


def main():
    print(f"Starting data generation execution!")
    print(f'os.getenv("data_source"): {os.getenv("data_source")}')
    print(f'os.getenv("reference_data_path"):  {os.getenv("reference_data_path")}')
    print(f'os.getenv("sample_size") : {os.getenv("sample_size")}')
    print(f'os.getenv("filter_condition") : {os.getenv("filter_condition")}')
    print(f'os.getenv("numeric_columns"): {os.getenv("numeric_columns")}')
    print(f'os.getenv("categorical_columns") : {os.getenv("categorical_columns")}')
    print(f'os.getenv("conditional_columns"): {os.getenv("conditional_columns")}')
    print(f'os.getenv("set_conditional"): {os.getenv("set_conditional")}')
    print(f'os.getenv("default_container_size"): {os.getenv("default_container_size")}')
    print(f'os.getenv("learning_rate"): {os.getenv("learning_rate")}')
    print(f'os.getenv("epoch"): {os.getenv("epoch")}')
    if os.getenv('data_source').lower() == 'local data files':
        data = fetch_and_clean_data(os.getenv('reference_data_path'))
        _, filename = os.path.split(os.getenv('reference_data_path'))
        output_filename = 'data_generated_' + filename
        print(f"data read from local data file, {data.head(3)}")
    elif os.getenv('data_source').lower() == 'refract datasets':
        print(f"reading {os.getenv('reference_data_path')} dataset for {os.getenv('sample_size')} rows"
              f" with filter_condition: {os.getenv('filter_condition')}")
        data = get_dataframe(os.getenv('reference_data_path'),
                             row_count=os.getenv('sample_size'),
                             filter_condition=os.getenv('filter_condition'))
        print(f"data read from refract dataset using refractio,"
              f"data.head(3): {data.head(3)}\ndata.shape: {data.shape}")
        data.dropna()
        output_filename = 'data_generated_' + os.getenv('reference_data_path') + ".csv"

    print(f"output_filename: {output_filename}")
    num_cols = os.getenv('numeric_columns') if os.getenv('numeric_columns') and os.getenv('numeric_columns') != "[]" else 'auto'
    cat_cols = os.getenv('categorical_columns') if os.getenv('categorical_columns') and os.getenv('categorical_columns') != "[]" else 'auto'
    print(f'num_cols: {num_cols}, cat_cols: {cat_cols}')
    numerical_columns, categorical_columns, boolean_columns = get_numerical_and_categorical_col(data, num_cols, cat_cols)
    print(f"numerical_columns: {numerical_columns}\ncategorical_columns:{categorical_columns}\nboolean_columns:{boolean_columns}")
    data = data[numerical_columns + categorical_columns]
    model_parameters, train_args = set_hyperparameters(os.getenv('epoch'), os.getenv('learning_rate'))
    if os.getenv('set_conditional') == 'False':
        synth = train_model(data, model_parameters, train_args, numerical_columns, categorical_columns)
        output_data = synth.sample(int(os.getenv('sample_size')))
    else:
        cols = os.getenv('conditional_columns')
        pattern = re.compile('\'(.*?)\'')
        conditional_columns = pattern.findall(cols)
        numerical_columns.remove(conditional_columns[0])
        synth = train_conditional(data, model_parameters, train_args, numerical_columns, categorical_columns,
                                  conditional_columns)
        output_data = synth.sample(data[conditional_columns])

    output_data = output_data.head(int(os.getenv('sample_size')))

    # writing output data
    output_data.to_csv("/data/" + output_filename, index=False)

    # writing report
    report = Report(metrics=[
        DataDriftPreset(),
    ])
    report.run(reference_data=output_data, current_data=data)
    output_file = os.getenv('output_path') + '/data_generation.html'
    report.save_html(output_file)
    print(f"Finishing data generation execution, output html saved to {output_file}")


main()
