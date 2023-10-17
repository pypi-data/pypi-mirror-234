import os

import pandas as pd

import stdflow as sf
from stdflow import Step

# from stdflow import Step
from tests.old import setup

setup()


def test_export():
    step = sf.Step()

    df = step.load(root="./data", attrs="fr", step="raw", version="1", file_name="random.csv")
    assert df.shape == (100, 4)

    df["new_col"] = "new_col"
    step.save(df, attrs="fr", step="with_new_col", version="1", file_name="random.csv")
    assert os.path.exists("./data/fr/step_with_new_col/v_1/random.csv")
    step.save(df, version="coucou%Y", file_name="coucou.csv")
    assert os.path.exists("./data/v_coucou2023/coucou.csv")


def test_save_merge():
    step = sf.Step()

    step.root = "./data"
    step.file_name_out = "merged.csv"
    step.attrs_out = "es"
    step.attrs_in = "es"

    # Load

    df1 = step.load(step="raw", version=None, file_name="random.csv")
    assert df1.shape == (100, 5)

    df2 = step.load(file_name="random_base.csv")
    assert df2.shape == (100, 2)

    df_full = pd.merge(df1, df2, on="id", how="left")

    # Save

    step.save(df_full, step="merge_left", version=None)
    assert os.path.exists("./data/es/step_merge_left/merged.csv")

    step.save(df_full, step="merge", version="v_202307241247")

    assert os.path.exists("./data/es/step_merge/v_202307241247/merged.csv")
    assert os.path.exists("./data/es/step_merge_left/merged.csv")
    assert os.path.exists("./data/es/step_merge/v_202307241247/metadata.json")
    assert os.path.exists("./data/es/step_merge_left/metadata.json")

    s = Step._from_file("./data/es/step_merge/v_202307241247/metadata.json")

    assert (
        len(s.md_all_files) == 4
    ), f"len(s.data_l)={len(s.md_all_files)}, s.data_l={s.md_all_files}"
    assert (
        len(s.md_direct_input_files) == 2
    ), f"len(s.data_l_in)={len(s.md_direct_input_files)}, s.data_l_in={s.md_direct_input_files}"


def test_2_step():
    test_save_merge()

    step = sf.Step()
    step.root = "./data"

    df1 = step.load(
        attrs="es",
        step="merge",
        version="v_202307241247",
        file_name="merged.csv",
    )
    df2 = step.load(root="./data", attrs="fr", step="raw", version="1", file_name="random.csv")

    df_full = pd.merge(df1, df2, on="id", how="left")
    step.save(
        df_full,
        attrs="global",
        step="es_fr_merge",
        version="0",
        file_name="merged_g.csv",
    )
    assert os.path.exists("./data/global/step_es_fr_merge/v_0/merged_g.csv")
    assert os.path.exists("./data/global/step_es_fr_merge/v_0/metadata.json")

    s = Step._from_file("data/global/step_es_fr_merge/v_0/metadata.json")
    assert (
        len(s.md_all_files) == 5
    ), f"len(s.data_l)={len(s.md_all_files)}, s.data_l={s.md_all_files}"
    assert (
        len(s.md_direct_input_files) == 2
    ), f"len(s.data_l_in)={len(s.md_direct_input_files)}, s.data_l_in={s.md_direct_input_files}"


def test_path_as_list():
    test_2_step()

    step = sf.Step()
    step.root = "./data"
    step.attrs_out = ["global", "all_combined"]
    step.step_out = "features"

    df1 = step.load(attrs="global", step="es_fr_merge", version="0", file_name="merged_g.csv")
    df2 = step.load(attrs=["es"], step="merge_left", file_name="merged.csv", version=None)
    df3 = step.load(attrs=["fr"], step="raw", version="1", file_name="random.csv")

    df_full = pd.merge(df1, df2, on="id", how="left")
    df_full = pd.merge(df_full, df3, on="id", how="left", suffixes=("_1", "_2"))

    step.save(df_full, file_name="features.csv", version=None)

    assert os.path.exists("./data/global/all_combined/step_features/features.csv")

    s = Step._from_file("data/global/step_es_fr_merge/v_0/metadata.json")
    assert (
        len(s.md_all_files) == 5
    ), f"len(s.data_l)={len(s.md_all_files)}, s.data_l={s.md_all_files}"
    assert (
        len(s.md_direct_input_files) == 2
    ), f"len(s.data_l_in)={len(s.md_direct_input_files)}, s.data_l_in={s.md_direct_input_files}"

    s = Step._from_file("./data/global/all_combined/step_features/metadata.json")
    assert (
        len(s.md_direct_input_files) == 3
    ), f"len(s.data_l_in)={len(s.md_direct_input_files)}, s.data_l_in={s.md_direct_input_files}"
    assert (
        len(s.md_all_files) == 7
    ), f"len(s.data_l)={len(s.md_all_files)}, s.data_l={s.md_all_files}"


if __name__ == "__main__":
    test_export()
    test_save_merge()
    test_2_step()
