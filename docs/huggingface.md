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

## License

Source code is under the [MIT License](https://github.com/hoonisone/AtomicTags/blob/main/LICENSE). That license does not cover the images or the annotations. The Atomic Tag annotations are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

These files do not share one license. Union14M-Benchmark and Union14M-General are not separate licenses. An image keeps the license of the Union14M dataset it came from. Names and terms below follow the [Union14M source table](https://github.com/Mountchicken/Union14M/blob/main/docs/source_dataset.md). Unknown means that table does not state a license.


<table>
  <thead>
    <tr>
      <th>Source</th>
      <th>Subset</th>
      <th>License / terms</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>K-STR-Bench</td><td>GIST_Signboard</td><td>CC BY 4.0</td></tr>
    <tr><td>K-STR-Bench</td><td>KAIST_Corrected</td><td>CC BY-SA 3.0</td></tr>
    <tr><td>K-STR-Bench</td><td>AIHub_Standardized</td><td>Not included. Not redistributed; AIHub Terms of Use</td></tr>
    <tr><td>Union14M</td><td>KAIST</td><td>CC BY-SA 3.0</td></tr>
    <tr><td>Union14M</td><td>NEOCR</td><td>CC BY-NC-SA 4.0</td></tr>
    <tr><td>Union14M</td><td>Uber-Text</td><td>Unknown</td></tr>
    <tr><td>Union14M</td><td>RCTW</td><td>Unknown</td></tr>
    <tr><td>Union14M</td><td>IIIT-ILST</td><td>CC BY 4.0</td></tr>
    <tr><td>Union14M</td><td>MTWI</td><td>CC BY-NC 4.0</td></tr>
    <tr><td>Union14M</td><td>COCOTextV2</td><td>CC BY 4.0</td></tr>
    <tr><td>Union14M</td><td>LSVT</td><td>Unknown</td></tr>
    <tr><td>Union14M</td><td>MLT19</td><td>CC BY-NC 4.0</td></tr>
    <tr><td>Union14M</td><td>ReCTS</td><td>Unknown</td></tr>
    <tr><td>Union14M</td><td>ArT</td><td>Unknown</td></tr>
    <tr><td>Union14M</td><td>IntelOCR</td><td>Apache License 2.0</td></tr>
    <tr><td>Union14M</td><td>TextOCR</td><td>CC BY 4.0</td></tr>
    <tr><td>Union14M</td><td>HierText</td><td>CC BY-SA 4.0</td></tr>
  </tbody>
</table>


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



<table>
  <thead>
    <tr>
      <th>True tags on a crop</th>
      <th>K-STR-Bench</th>
      <th>Union14M-General</th>
      <th>Union14M-Benchmark</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>0</td><td>9,889</td><td>1,389</td><td>745</td></tr>
    <tr><td>1</td><td>4,902</td><td>5,465</td><td>1,450</td></tr>
    <tr><td>2</td><td>2,560</td><td>1,685</td><td>2,671</td></tr>
    <tr><td>3</td><td>1,892</td><td>852</td><td>2,100</td></tr>
    <tr><td>4</td><td>676</td><td>467</td><td>738</td></tr>
    <tr><td>5</td><td>135</td><td>115</td><td>156</td></tr>
    <tr><td>6</td><td>27</td><td>20</td><td>21</td></tr>
    <tr><td>7</td><td>3</td><td>1</td><td>6</td></tr>
    <tr><td>8</td><td>2</td><td>0</td><td>1</td></tr>
  </tbody>
</table>


## Citation

If you use these annotations, please cite:

```bibtex
@inproceedings{atomicmultitag2027,
    title     = {An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models},
    author    = {Han, MyoungHun and Hong, Jin-Hyuk},
    booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)},
    year      = {2027}
}
```

