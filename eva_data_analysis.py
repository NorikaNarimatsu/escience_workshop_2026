import matplotlib.pyplot as plt
import pandas as pd

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
# Local input filename (hyphenated) -- matches workspace file
input_file = './eva-data.json'
output_file = './eva_data.csv'
graph_file = './cumulative_eva_graph.png'


def read_json_to_clean_dataframe(file_name):
    df = pd.read_json(file_name, convert_dates=['date'], encoding='ascii')
    df['eva'] = df['eva'].astype(float)
    df.dropna(axis=0, subset=['duration', 'date'], inplace=True)
    df.sort_values('date', inplace=True)
    return df


def text_to_duration(duration):
    hours, minutes = duration.split(":")
    duration = int(hours) + int(minutes) / 60
    return duration


def compute_durations(df):
    df_copy = df.copy()
    df_copy['duration_hours'] = df_copy['duration'].apply(text_to_duration)
    df_copy['cumulative_time'] = df_copy['duration_hours'].cumsum()
    return df_copy


def plot_eva_durations(file_name, df):
    plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()

def main():
    eva_df = read_json_to_clean_dataframe(input_file)
    eva_df.to_csv(output_file, index=False, encoding='utf-8')
    eva_df = compute_durations(eva_df)
    plot_eva_durations(graph_file, eva_df)


if __name__ == '__main__':
    main()