# An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models

Myounghun Han, Jin-Hyuk Hong · WACV 2027

[![Paper](https://img.shields.io/badge/Paper-WACV%202027-blue)](#citation) [![Dataset](https://img.shields.io/badge/Dataset-Hugging%20Face-yellow)](https://huggingface.co/datasets/hoonisone/AtomicTags)

Official annotations of the paper ["An Atomic Multi-Tag Taxonomy for Fine-Grained Diagnosis of Scene Text Recognition Models"](#citation). Accepted to **WACV 2027**. The proceedings link is not available yet.

<p align="center">
  <img src="assets/texonomy.png" alt="Atomic multi-tag taxonomy: Font, Visibility, Background, View, and Layout" width="520">
</p>

<p align="center">
  <img src="assets/tag_example.png" alt="Real text-crop examples for each atomic tag" width="680">
</p>

This repository provides atomic multi-tag annotations for **K-STR-Bench** and **Union14M**. A text crop can carry several tags from the taxonomy above, so a scene text recognition model can be diagnosed by the type of failure. `image_path` is relative to the folder that contains the CSV.

The release is on Hugging Face: [hoonisone/AtomicTags](https://huggingface.co/datasets/hoonisone/AtomicTags).

## Release format

Each split is a folder of image files and one CSV. This is not an LMDB release.

One crop can have several tags. A folder or archive per tag would store that file many times. Images are stored once. All tags for a crop are columns in the CSV, so a subset is a filter on that table.

```text
K_STR_Bench/
├── text.v1.0.csv
├── GIST_Signboard/text_images/
└── KAIST_Corrected/text_images/
Union14M_Benchmark/
├── text.v1.0.csv
└── text_images/
Union14M_General/
├── text_v.1.0.csv
└── text_images/
```



## License

Source code in this repository is under the [MIT License](LICENSE). That license does not cover the images or the annotations.

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




## Data Sources

**K-STR-Bench.** A challenge-aware benchmark for Korean scene text recognition. [GitHub](https://github.com/hoonisone/K-STR-Bench) | [Hugging Face](https://huggingface.co/datasets/hoonisone/K-STR-Bench). The split here is `K_STR_Bench`, from **GIST_Signboard** and **KAIST_Corrected**. **AIHub_Standardized** is part of K-STR-Bench and is not included. The K-STR-Bench release includes every crop and the columns `is_only_korean` and `is_illegible` for filtering. This release is already filtered: `text.v1.0.csv` and the image folders contain only crops where `is_only_korean` is true and `is_illegible` is false.

**Union14M.** A scene text recognition dataset collected from 14 public datasets (Jiang et al., ICCV 2023). [GitHub](https://github.com/Mountchicken/Union14M). Union14M-L and Union14M-Benchmark are released from that repository. The splits here are `Union14M_Benchmark` and `Union14M_General`. Each CSV and its image folder already contain only the crops in this release. Tag columns in these tables are separate from the original Union14M annotations.

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
