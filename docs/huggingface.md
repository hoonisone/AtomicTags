---
license: other
task_categories:
- image-to-text
language:
- ko
- en
tags:
- scene-text-recognition
- ocr
pretty_name: An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models
size_categories:
- 10K<n<100K
configs:
- config_name: K_STR_Bench
  data_files:
  - split: test
    path: K_STR_Bench/text.v1.0.csv
  default: true
- config_name: Union14M_Benchmark
  data_files:
  - split: test
    path: Union14M_Benchmark/text.v1.0.csv
- config_name: Union14M_General
  data_files:
  - split: test
    path: Union14M_General/text_v.1.0.csv
---

# An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models

Atomic multi-tag annotations for **K-STR-Bench** and **Union14M**. Each text crop may contain multiple visual challenge tags, enabling fine-grained analysis of recognition performance under individual and co-occurring challenges. Images are stored once. Tags are columns in the CSV. `image_path` is relative to the folder that contains the CSV.

Myounghun Han, Jin-Hyuk Hong · WACV 2027

![Paper](https://img.shields.io/badge/Paper-WACV%202027-blue) ![GitHub](https://img.shields.io/badge/GitHub-AtomicTags-black)

Accepted to **WACV 2027**. The proceedings link is not available yet. Code and documentation are on [GitHub](https://github.com/hoonisone/AtomicTags).

## Data Sources

**K-STR-Bench.** A challenge-aware benchmark for Korean scene text recognition. [GitHub](https://github.com/hoonisone/K-STR-Bench) | [Hugging Face](https://huggingface.co/datasets/hoonisone/K-STR-Bench). The split here is `K_STR_Bench`, from **GIST_Signboard** and **KAIST_Corrected**. **AIHub_Standardized** is part of K-STR-Bench and is not included. The K-STR-Bench release includes every crop and the columns `is_only_korean` and `is_illegible` for filtering. This release is already filtered: `text.v1.0.csv` and the image folders contain only crops where `is_only_korean` is true and `is_illegible` is false.

**Union14M.** A scene text recognition dataset collected from 14 public datasets (Jiang et al., ICCV 2023). [GitHub](https://github.com/Mountchicken/Union14M). Union14M-L and Union14M-Benchmark are released from that repository. The splits here are `Union14M_Benchmark` and `Union14M_General`. We annotate 7,888 samples from the six challenge-specific subsets of Union14M-Benchmark other than Incomplete, along with 9,994 randomly sampled images from its General subset. Each CSV and its image folder already contain only the crops in this release. Tag columns in these tables are separate from the original Union14M annotations.

Image folders are stored as `text_images.tar`. The CSV files stay beside those archives. Extracting an archive recreates a `text_images` folder next to it. This release does not include the inclusive and exclusive label files.

```text
K_STR_Bench/
├── text.v1.0.csv
├── GIST_Signboard/text_images.tar
└── KAIST_Corrected/text_images.tar
Union14M_Benchmark/
├── text.v1.0.csv
└── text_images.tar
Union14M_General/
├── text_v.1.0.csv
└── text_images.tar
```

## How to use

Download this dataset, then extract each `text_images.tar`. The CSV files are already unpacked. `image_path` is relative to the folder that contains the CSV. Create the inclusive and exclusive label files from the CSV with the code on [GitHub](https://github.com/hoonisone/AtomicTags).

```bash
git clone https://github.com/hoonisone/AtomicTags.git
cd AtomicTags
pip install -U huggingface_hub
hf download hoonisone/AtomicTags --repo-type dataset --local-dir data
python prepare.py --dataset-dir data --pipeline extract_images
python prepare.py --dataset-dir data --pipeline make_tag_labels
```

`./K_STR_Bench/labels/inclusive/stylized.txt`

```text
0/gist_7_4.jpg	이글
0/gist_7_5.jpg	피플
```

`./K_STR_Bench/labels/inclusive/stylized.jsonl`

```json
{"filename":"0/gist_7_4.jpg","text":"이글","width":87,"height":74}
{"filename":"0/gist_7_5.jpg","text":"피플","width":104,"height":202}
```

`./K_STR_Bench/labels/exclusive/stylized.txt` and `./K_STR_Bench/labels/exclusive/stylized.jsonl` use the same two formats.

## License

Source code is under the [MIT License](https://github.com/hoonisone/AtomicTags/blob/main/LICENSE). That license does not cover the images or the annotations. The Atomic Tag annotations are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

These files do not share one license. Union14M-Benchmark and Union14M-General are not separate licenses. An image keeps the license of the Union14M dataset it came from. Names and terms below follow the [Union14M source table](https://github.com/Mountchicken/Union14M/blob/main/docs/source_dataset.md). Unknown means that table does not state a license.


| Source      | Subset             | License / terms                                     |
| ----------- | ------------------ | --------------------------------------------------- |
| K-STR-Bench | GIST_Signboard     | CC BY 4.0                                           |
| K-STR-Bench | KAIST_Corrected    | CC BY-SA 3.0                                        |
| K-STR-Bench | AIHub_Standardized | Not included. Not redistributed; AIHub Terms of Use |
| Union14M    | KAIST              | CC BY-SA 3.0                                        |
| Union14M    | NEOCR              | CC BY-NC-SA 4.0                                     |
| Union14M    | Uber-Text          | Unknown                                             |
| Union14M    | RCTW               | Unknown                                             |
| Union14M    | IIIT-ILST          | CC BY 4.0                                           |
| Union14M    | MTWI               | CC BY-NC 4.0                                        |
| Union14M    | COCOTextV2         | CC BY 4.0                                           |
| Union14M    | LSVT               | Unknown                                             |
| Union14M    | MLT19              | CC BY-NC 4.0                                        |
| Union14M    | ReCTS              | Unknown                                             |
| Union14M    | ArT                | Unknown                                             |
| Union14M    | IntelOCR           | Apache License 2.0                                  |
| Union14M    | TextOCR            | CC BY 4.0                                           |
| Union14M    | HierText           | CC BY-SA 4.0                                        |


## Statistics

**Inclusive** counts crops where that tag is true, including crops with other true tags. **Exclusive** counts crops whose only true tag is that tag.


<table>
  <thead>
    <tr>
      <th rowspan="2">Tag</th>
      <th colspan="2">K-STR-Bench</th>
      <th colspan="2">Union14M-General</th>
      <th colspan="2">Union14M-Benchmark</th>
    </tr>
    <tr>
      <th>Inclusive</th>
      <th>Exclusive</th>
      <th>Inclusive</th>
      <th>Exclusive</th>
      <th>Inclusive</th>
      <th>Exclusive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Crops</td>
      <td colspan="2">20,086</td>
      <td colspan="2">9,994</td>
      <td colspan="2">7,888</td>
    </tr>
    <tr><td>Stylized</td><td>2,273</td><td>821</td><td>791</td><td>171</td><td>1,727</td><td>311</td></tr>
    <tr><td>Inconsistent size</td><td>602</td><td>88</td><td>253</td><td>25</td><td>599</td><td>19</td></tr>
    <tr><td>Incomplete</td><td>767</td><td>193</td><td>844</td><td>133</td><td>759</td><td>82</td></tr>
    <tr><td>Low visibility</td><td>1,352</td><td>550</td><td>6,984</td><td>4,743</td><td>307</td><td>25</td></tr>
    <tr><td>Noisy</td><td>2,844</td><td>1,466</td><td>696</td><td>109</td><td>1,540</td><td>143</td></tr>
    <tr><td>Distracted</td><td>3,019</td><td>457</td><td>880</td><td>31</td><td>3,733</td><td>127</td></tr>
    <tr><td>Perspective distortion</td><td>3,268</td><td>181</td><td>1,231</td><td>33</td><td>676</td><td>4</td></tr>
    <tr><td>Non-single-line</td><td>118</td><td>34</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
    <tr><td>Non-straight</td><td>479</td><td>60</td><td>155</td><td>6</td><td>2,731</td><td>203</td></tr>
    <tr><td>Rotated</td><td>4,554</td><td>1,052</td><td>2,127</td><td>214</td><td>4,928</td><td>536</td></tr>
  </tbody>
</table>



| True tags on a crop | K-STR-Bench | Union14M-General | Union14M-Benchmark |
| ------------------- | ----------- | ---------------- | ------------------ |
| 0                   | 9,889       | 1,389            | 745                |
| 1                   | 4,902       | 5,465            | 1,450              |
| 2                   | 2,560       | 1,685            | 2,671              |
| 3                   | 1,892       | 852              | 2,100              |
| 4                   | 676         | 467              | 738                |
| 5                   | 135         | 115              | 156                |
| 6                   | 27          | 20               | 21                 |
| 7                   | 3           | 1                | 6                  |
| 8                   | 2           | 0                | 1                  |


## Citation

If you use these annotations, please cite:

```bibtex
@inproceedings{atomicmultitag2027,
    title     = {An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models},
    author    = {Han, Myounghun and Hong, Jin-Hyuk},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
    year      = {2027}
}
```

