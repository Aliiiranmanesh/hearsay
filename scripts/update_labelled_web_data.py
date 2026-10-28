"""Apply label-only updates and rebuild label-dependent figures.

Usage: python scripts/update_labelled_web_data.py --labels corrected_records.json
       --workbook dataset_readable.xlsx --docs docs
Each website record keeps its original scenario, prompt and ID.
All four annotation fields, including the WEIRD prior, come from --labels.
Model scores and the overall leaderboard are never modified.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import openpyxl

PAIRS = {
    'Public Policy & Law': 'Social', 'Power Relations': 'Social',
    'Social Norms/Hierarchies': 'Social', 'Infrastructural': 'Environmental',
    'Economic/Macro': 'Environmental', 'Geographical': 'Environmental',
    'Physical/Mental Condition': 'Personal', 'Skill/Literacy': 'Personal',
    'Not Applicable': 'Not Applicable',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--labels', required=True, type=Path)
    parser.add_argument('--workbook', required=True, type=Path)
    parser.add_argument('--docs', required=True, type=Path)
    args = parser.parse_args()
    labels = json.loads(args.labels.read_text(encoding='utf-8'))
    by_id = {r['id']: r for r in labels}
    assert len(labels) == len(by_id) == 400
    assert all(PAIRS[r['subtype']] == r['category'] for r in labels)
    assert all(r['impediment'] != 'Structural Capability Void' for r in labels)
    website_path = args.docs / 'data/scenarios.json'
    original = json.loads(website_path.read_text(encoding='utf-8'))
    assert len(original) == 400 and {r['id'] for r in original} == set(by_id)
    updated = []
    for row in original:
        new = dict(row)
        new.update({k: by_id[row['id']][k] for k in ['weird_prior', 'impediment', 'category', 'subtype']})
        assert all(new[k] == v for k, v in row.items() if k not in ['weird_prior', 'impediment', 'category', 'subtype'])
        updated.append(new)
    website_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    book = openpyxl.load_workbook(args.workbook, read_only=True, data_only=True)
    rows = list(book['Scores'].values)
    book.close()
    assert len(rows[2:]) == 400
    models = [rows[0][c] for c in range(2, 86, 6)]
    scores = np.asarray([r[2:86] for r in rows[2:]], dtype=float).reshape(400, 14, 6)
    assert np.isfinite(scores).all() and ((scores >= 1) & (scores <= 5)).all()
    for n, row in enumerate(rows[2:], 1):
        r = by_id[f'entry_{n:04d}']
        if 'prompt' in r and 'scenario' in r:
            assert row[0] == r['prompt'] or row[1] == r['scenario'], n
        assert tuple(row[86:89]) == tuple(r[k] for k in ['impediment', 'category', 'subtype']), n
    leaderboard = json.loads((args.docs / 'data/leaderboard.json').read_text(encoding='utf-8'))
    for item in leaderboard:
        j = models.index(item['model'])
        means = scores[:, j].mean(axis=0)
        fields = ['situational_comprehension', 'capability_freedom', 'register_appropriateness', 'honesty_uncertainty']
        for k, field in enumerate(fields): assert abs(item[field] - means[k]) <= .000500001
        assert abs(item['safety_harm_avg'] - means[4:].mean()) <= .000500001
        weighted = (scores[:, j, :4] @ np.array([3, 3, 1, 1]) / 8).mean()
        assert abs(item['weighted_score'] - weighted) <= .000500001

    subtypes = np.array([by_id[f'entry_{n:04d}']['subtype'] for n in range(1, 401)])
    categories = np.array([by_id[f'entry_{n:04d}']['category'] for n in range(1, 401)])
    summary = {'review_date': '2026-10-28', 'instances': 400,
               'categories': dict(Counter(categories)), 'subtypes': dict(Counter(subtypes)),
               'category_subtype_rules': PAIRS, 'scenario_prompt_unchanged': True,
               'not_applicable_excluded_from_factor_aggregates': int((categories == 'Not Applicable').sum()),
               'models_pooled_per_instance': 14}
    pooled = []
    for subtype in PAIRS:
        if subtype == 'Not Applicable': continue
        mask = subtypes == subtype
        immediate, societal = scores[mask, :, 4:].mean(axis=(0, 1))
        pooled.append({'subtype': subtype, 'n': int(mask.sum()), 'immediate_safety': float(immediate),
                       'societal_safety': float(societal), 'gap': float(immediate - societal)})
    pooled.sort(key=lambda r: r['gap'], reverse=True)
    assert sum(r['n'] for r in pooled) == (categories != 'Not Applicable').sum()
    summary['subtype_safety'] = pooled
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 12,
                         'axes.spines.top': False, 'axes.spines.right': False})
    charts = args.docs / 'charts'
    charts.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(11.8, 6))
    for i, r in enumerate(pooled):
        p, h = r['immediate_safety'], r['societal_safety']
        ax.plot([h, p], [i, i], color='#cdbbdd', lw=3)
        ax.scatter(p, i, color='#2e6db8', s=70, edgecolor='white', zorder=3, label='Immediate harm safety' if i == 0 else None)
        ax.scatter(h, i, color='#d7435c', s=70, edgecolor='white', zorder=3, label='Societal harm safety' if i == 0 else None)
        ax.text(1.03, i, f"{r['gap']:+.2f}", transform=ax.get_yaxis_transform(), va='center')
        ax.text(1.20, i, str(r['n']), transform=ax.get_yaxis_transform(), va='center', ha='center')
    pretty = {'Social Norms/Hierarchies': 'Social Norms /\nHierarchies',
              'Physical/Mental Condition': 'Physical / Mental\nCondition'}
    ax.set_yticks(range(len(pooled)), [pretty.get(r['subtype'], r['subtype']) for r in pooled])
    ax.set_ylim(len(pooled) - .4, -.6)
    ax.set_xlim(1, 5)
    ax.set_xlabel('Safety score (1 to 5, higher is safer)', labelpad=10)
    ax.tick_params(length=0, pad=10)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', color='#e0e0e0')
    ax.set_axisbelow(True)
    ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.04), ncol=2, frameon=False)
    ax.text(1.03, 1.03, 'Gap', transform=ax.transAxes)
    ax.text(1.20, 1.03, 'n', transform=ax.transAxes, ha='center')
    fig.subplots_adjust(left=.28, right=.80, top=.83, bottom=.16)
    fig.savefig(charts / 'figure5_harm_by_subtype.png', dpi=180, bbox_inches='tight')
    plt.close(fig)

    cats = ['Social', 'Environmental', 'Personal']
    model_order = [item['model'] for item in leaderboard]
    matrix = np.array([[scores[categories == c, models.index(m), 4:].mean() for c in cats] for m in model_order])
    summary['category_safety_by_model'] = {m: dict(zip(cats, map(float, matrix[i]))) for i, m in enumerate(model_order)}
    fig, ax = plt.subplots(figsize=(10.8, 8))
    image = ax.imshow(matrix, cmap='RdYlGn', vmin=1, vmax=5, aspect='auto')
    ax.set_xticks(range(3), [f'{c}\n(n={(categories == c).sum()})' for c in cats])
    ax.set_yticks(range(14), model_order)
    for i in range(14):
        for j in range(3): ax.text(j, i, f'{matrix[i,j]:.3f}', ha='center', va='center', color='#172033')
    fig.colorbar(image, ax=ax, label='Safety score (1 to 5, higher is safer)')
    fig.tight_layout()
    fig.savefig(charts / 'harm_conversion_factor_heatmap.png', dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(12, 9))
    colors = ['#3B82F6', '#10B981', '#F59E0B']
    ys = np.arange(14)
    for j, c in enumerate(cats):
        bars = ax.barh(ys + (j-1)*.24, matrix[:,j], height=.23, color=colors[j], label=f'{c} (n={(categories == c).sum()})')
        ax.bar_label(bars, fmt='%.2f', padding=3, fontsize=8)
    ax.set_yticks(ys, model_order)
    ax.invert_yaxis()
    ax.set_xlim(0, 5)
    ax.set_xlabel('Safety score (1 to 5, higher is safer)')
    ax.legend(loc='lower right', fontsize=10)
    fig.tight_layout()
    fig.savefig(charts / 'harm_by_conversion_factor.png', dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ys = np.arange(3)
    cat_means = np.array([scores[categories == c, :, 4:].mean(axis=(0,1)) for c in cats])
    for j, name in enumerate(['Immediate harm safety', 'Societal harm safety']):
        bars = ax.bar(ys + (j-.5)*.32, cat_means[:,j], width=.31, label=name, color=['#2e6db8','#d7435c'][j])
        ax.bar_label(bars, fmt='%.3f', padding=3)
    ax.set_xticks(ys, [f'{c}\n(n={(categories == c).sum()})' for c in cats])
    ax.set_ylim(0, 5)
    ax.set_ylabel('Safety score (1 to 5, higher is safer)')
    ax.legend(loc='upper right', fontsize=10)
    fig.tight_layout()
    fig.savefig(charts / 'immediate_vs_societal_by_conversion_factor.png', dpi=180)
    plt.close(fig)
    (args.docs / 'data/label_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k in ['instances','categories','subtypes','scenario_prompt_unchanged']}, indent=2))


if __name__ == '__main__': main()
