import os, glob, csv
import matplotlib.pyplot as plt
import numpy as np

def find_latest_results_csv():
    files = glob.glob(os.path.join('results', 'sorting_comparison_results*.csv'))
    if not files: return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def read_results(csv_path):
    data = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({'data_size': int(row['data_size']), 'algorithm': row['algorithm'], 'time_ms': float(row['time_ms'])})
    return data

def main():
    csvp = find_latest_results_csv()
    if not csvp:
        print('No results file found in results/. Run app_fullcomparison_nskip.py first.')
        return
    print('Reading:', csvp)
    data = read_results(csvp)
    results_by_size = {}
    for r in data:
        results_by_size.setdefault(r['data_size'], {})[r['algorithm']] = r['time_ms']
    algorithms = sorted({r['algorithm'] for r in data})
    sizes = sorted(results_by_size.keys())
    series = {algo: [results_by_size[s].get(algo, float('nan')) for s in sizes] for algo in algorithms}

    # Plot 1 - line (log scale)
    plt.figure(figsize=(10,6))
    for algo in algorithms:
        plt.plot(sizes, series[algo], marker='o', label=algo)
    plt.title('Perbandingan Waktu Eksekusi Sorting (ms) — Line (log scale)')
    plt.xlabel('Ukuran Data (n)')
    plt.ylabel('Waktu (ms)')
    plt.yscale('log')
    plt.grid(True, which='both', linestyle='--', alpha=0.4)
    plt.legend()
    os.makedirs('results', exist_ok=True)
    line_path = os.path.join('results', 'sorting_comparison_line.png')
    plt.savefig(line_path, dpi=150, bbox_inches='tight')
    plt.close()

    # Plot 2 - grouped bar (log scale)
    plt.figure(figsize=(12,6))
    x = range(len(sizes))
    width = 0.15
    for i, algo in enumerate(algorithms):
        offsets = [xi + (i - len(algorithms)/2)*width + width/2 for xi in x]
        plt.bar(offsets, series[algo], width=width, label=algo)
    plt.title('Perbandingan Waktu Eksekusi Sorting (ms) — Grouped Bars (log scale)')
    plt.xlabel('Ukuran Data (n)')
    plt.ylabel('Waktu (ms)')
    plt.yscale('log')
    plt.xticks(list(x), [f"{s:,}" for s in sizes])
    plt.grid(True, which='both', axis='y', linestyle='--', alpha=0.4)
    plt.legend()
    bar_path = os.path.join('results', 'sorting_comparison_bars.png')
    plt.savefig(bar_path, dpi=150, bbox_inches='tight')
    plt.close()

    print('Grafik tersimpan:')
    print('-', line_path)
    print('-', bar_path)

if __name__ == '__main__':
    main()
