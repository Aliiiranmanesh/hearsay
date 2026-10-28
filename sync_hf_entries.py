"""Prepare the published HearSay dataset from entries.txt, preserving annotations."""
import json
import re
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'entries.txt'
OUT = ROOT / 'hf_dataset/data/train-00000-of-00001.parquet'
BASE = OUT if OUT.exists() else ROOT / 'hf_remote_snapshot/data/train-00000-of-00001.parquet'


def main():
    source = SOURCE.read_text(encoding='utf-8-sig')
    blocks = list(re.finditer(r'(?ms)^(\d+)\. ([^\r\n]+)\r?\n(.*?)(?=^\d+\. |\Z)', source))
    assert [int(b[1]) for b in blocks] == list(range(1, 401)), 'Expected entries 1–400 exactly'
    table = pq.read_table(BASE)
    original = table.to_pandas()
    label_source = ROOT / 'scripts/labels_2026_10_28.json'
    if label_source.exists():
        labels = json.loads(label_source.read_text(encoding='utf-8'))
        assert len(labels) == 400 and {r['id'] for r in labels} == set(original.id)
        for row in labels:
            idx = original.index[original.id == row['id']][0]
            for field in ['weird_prior', 'impediment', 'category', 'subtype']:
                original.at[idx, field] = row[field]
    frame = original.copy(deep=True)
    assert frame.id.is_unique and set(frame.id) == {f'entry_{n:04d}' for n in range(1, 401)}
    changes = []
    for block in blocks:
        identifier = f'entry_{int(block[1]):04d}'
        parts = re.split(r'(?m)^—[ \t]*\r?$', block[3])
        assert len(parts) == 2, f'{identifier}: expected one prompt separator'
        scenario, prompt = block[2].strip(), parts[1].strip()
        assert scenario and prompt, identifier
        idx = frame.index[frame.id == identifier][0]
        for field, value in [('scenario', scenario), ('prompt', prompt)]:
            if frame.at[idx, field] != value:
                changes.append({'id': identifier, 'field': field, 'before': frame.at[idx, field], 'after': value})
            frame.at[idx, field] = value
    annotations = ['id', 'weird_prior', 'impediment', 'category', 'subtype']
    assert frame[annotations].equals(original[annotations])
    updated = pa.Table.from_pandas(frame, schema=table.schema, preserve_index=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(updated, OUT, compression='snappy')
    assert pq.read_table(OUT).to_pandas().equals(frame)
    card_path = ROOT / 'hf_dataset/README.md'
    if not card_path.exists():
        card_path = ROOT / 'hf_remote_snapshot/README.md'
    card = card_path.read_text(encoding='utf-8')
    card = re.sub(r'(num_bytes: )\d+', lambda m: m[1] + str(updated.nbytes), card)
    card = re.sub(r'(download_size: )\d+', lambda m: m[1] + str(OUT.stat().st_size), card)
    card = re.sub(r'(dataset_size: )\d+', lambda m: m[1] + str(updated.nbytes), card)
    (ROOT / 'hf_dataset/README.md').write_text(card, encoding='utf-8')
    frame.to_csv(ROOT / 'hf_dataset/hearsay_bench.csv', index=False, lineterminator='\n')
    with (ROOT / 'hf_dataset/hearsay_bench.jsonl').open('w', encoding='utf-8', newline='\n') as f:
        for row in frame.to_dict(orient='records'):
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
    assert pd.read_csv(ROOT / 'hf_dataset/hearsay_bench.csv', keep_default_na=False).equals(frame)
    summary = {'rows': len(frame), 'changed_rows': len({c['id'] for c in changes}),
               'scenario_changes': sum(c['field'] == 'scenario' for c in changes),
               'prompt_changes': sum(c['field'] == 'prompt' for c in changes),
               'annotations_preserved': True, 'parquet_path': str(OUT), 'changes': changes}
    (ROOT / 'hf_dataset/sync_changes.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'changes'}, indent=2))


if __name__ == '__main__':
    main()
