import argparse
import json
import os
import shutil
from collections import defaultdict
from inspect import signature
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional, Set, Tuple

import torch

from huggingface_hub import CommitInfo, CommitOperationAdd, Discussion, HfApi, hf_hub_download
from huggingface_hub.file_download import repo_folder_name
from safetensors.torch import load_file, save_file
from transformers import AutoConfig


COMMIT_DESCRIPTION = """
This is an automated PR created with https://huggingface.co/spaces/safetensors/convert

This new file is equivalent to `pytorch_model.bin` but safe in the sense that
no arbitrary code can be put into it.

These files also happen to load much faster than their pytorch counterpart:
https://colab.research.google.com/github/huggingface/notebooks/blob/main/safetensors_doc/en/speed.ipynb

The widgets on your model page will run using this model even if this is not merged
making sure the file actually works.

If you find any issues: please report here: https://huggingface.co/spaces/safetensors/convert/discussions

Feel free to ignore this PR.
"""

ConversionResult = Tuple[List["CommitOperationAdd"], List[Tuple[str, "Exception"]]]


class AlreadyExists(Exception):
    pass


def shared_pointers(tensors):
    ptrs = defaultdict(list)
    for k, v in tensors.items():
        ptrs[v.data_ptr()].append(k)
    failing = []
    for ptr, names in ptrs.items():
        if len(names) > 1:
            failing.append(names)
    return failing


def check_file_size(sf_filename: str, pt_filename: str):
    sf_size = os.stat(sf_filename).st_size
    pt_size = os.stat(pt_filename).st_size

    if (sf_size - pt_size) / pt_size > 0.01:
        raise RuntimeError(
            f"""The file size different is more than 1%:
         - {sf_filename}: {sf_size}
         - {pt_filename}: {pt_size}
         """
        )


def rename(pt_filename: str) -> str:
    filename, ext = os.path.splitext(pt_filename)
    local = f"{filename}.safetensors"
    local = local.replace("pytorch_model", "model")
    return local


def convert_multi(model_id: str, folder: str, token: Optional[str]) -> ConversionResult:
    filename = hf_hub_download(repo_id=model_id, filename="pytorch_model.bin.index.json", token=token, cache_dir=folder)
    with open(filename, "r") as f:
        data = json.load(f)

    filenames = set(data["weight_map"].values())
    local_filenames = []
    for filename in filenames:
        pt_filename = hf_hub_download(repo_id=model_id, filename=filename, token=token, cache_dir=folder)

        sf_filename = rename(pt_filename)
        sf_filename = os.path.join(folder, sf_filename)
        convert_file(pt_filename, sf_filename)
        local_filenames.append(sf_filename)

    index = os.path.join(folder, "model.safetensors.index.json")
    with open(index, "w") as f:
        newdata = {k: v for k, v in data.items()}
        newmap = {k: rename(v) for k, v in data["weight_map"].items()}
        newdata["weight_map"] = newmap
        json.dump(newdata, f, indent=4)
    local_filenames.append(index)

    operations = [
        CommitOperationAdd(path_in_repo=local.split("/")[-1], path_or_fileobj=local) for local in local_filenames
    ]
    errors: List[Tuple[str, "Exception"]] = []

    return operations, errors


def convert_single(model_id: str, folder: str, token: Optional[str]) -> ConversionResult:
    pt_filename = hf_hub_download(repo_id=model_id, filename="pytorch_model.bin", token=token, cache_dir=folder)

    sf_name = "model.safetensors"
    sf_filename = os.path.join(folder, sf_name)
    convert_file(pt_filename, sf_filename)
    operations = [CommitOperationAdd(path_in_repo=sf_name, path_or_fileobj=sf_filename)]
    errors: List[Tuple[str, "Exception"]] = []
    return operations, errors


def convert_file(
    pt_filename: str,
    sf_filename: str,
):
    loaded = torch.load(pt_filename, map_location="cpu")
    if "state_dict" in loaded:
        loaded = loaded["state_dict"]
    shared = shared_pointers(loaded)
    for shared_weights in shared:
        for name in shared_weights[1:]:
            loaded.pop(name)

    # For tensors to be contiguous
    loaded = {k: v.contiguous() for k, v in loaded.items()}

    dirname = os.path.dirname(sf_filename)
    os.makedirs(dirname, exist_ok=True)
    save_file(loaded, sf_filename, metadata={"format": "pt"})
    check_file_size(sf_filename, pt_filename)
    reloaded = load_file(sf_filename)
    for k in loaded:
        pt_tensor = loaded[k]
        sf_tensor = reloaded[k]
        if not torch.equal(pt_tensor, sf_tensor):
            raise RuntimeError(f"The output tensors do not match for key {k}")


def create_diff(pt_infos: Dict[str, List[str]], sf_infos: Dict[str, List[str]]) -> str:
    errors = []
    for key in ["missing_keys", "mismatched_keys", "unexpected_keys"]:
        pt_set = set(pt_infos[key])
        sf_set = set(sf_infos[key])

        pt_only = pt_set - sf_set
        sf_only = sf_set - pt_set

        if pt_only:
            errors.append(f"{key} : PT warnings contain {pt_only} which are not present in SF warnings")
        if sf_only:
            errors.append(f"{key} : SF warnings contain {sf_only} which are not present in PT warnings")
    return "\n".join(errors)


def check_final_model(model_id: str, folder: str, token: Optional[str]):
    config = hf_hub_download(repo_id=model_id, filename="config.json", token=token, cache_dir=folder)
    shutil.copy(config, os.path.join(folder, "config.json"))
    config = AutoConfig.from_pretrained(folder)

    import transformers

    class_ = getattr(transformers, config.architectures[0])
    (pt_model, pt_infos) = class_.from_pretrained(folder, output_loading_info=True)
    (sf_model, sf_infos) = class_.from_pretrained(folder, output_loading_info=True)

    if pt_infos != sf_infos:
        error_string = create_diff(pt_infos, sf_infos)
        raise ValueError(f"Different infos when reloading the model: {error_string}")

    pt_params = pt_model.state_dict()
    sf_params = sf_model.state_dict()

    pt_shared = shared_pointers(pt_params)
    sf_shared = shared_pointers(sf_params)
    if pt_shared != sf_shared:
        raise RuntimeError("The reconstructed model is wrong, shared tensors are different {shared_pt} != {shared_tf}")

    sig = signature(pt_model.forward)
    input_ids = torch.arange(10).unsqueeze(0)
    pixel_values = torch.randn(1, 3, 224, 224)
    input_values = torch.arange(1000).float().unsqueeze(0)
    # Hardcoded for whisper basically
    input_features = torch.zeros((1, 80, 3000))
    kwargs = {}
    if "input_ids" in sig.parameters:
        kwargs["input_ids"] = input_ids
    if "input_features" in sig.parameters:
        kwargs["input_features"] = input_features
    if "decoder_input_ids" in sig.parameters:
        kwargs["decoder_input_ids"] = input_ids
    if "pixel_values" in sig.parameters:
        kwargs["pixel_values"] = pixel_values
    if "input_values" in sig.parameters:
        kwargs["input_values"] = input_values
    if "bbox" in sig.parameters:
        kwargs["bbox"] = torch.zeros((1, 10, 4)).long()
    if "image" in sig.parameters:
        kwargs["image"] = pixel_values

    if torch.cuda.is_available():
        pt_model = pt_model.cuda()
        sf_model = sf_model.cuda()
        kwargs = {k: v.cuda() for k, v in kwargs.items()}

    try:
        pt_logits = pt_model(**kwargs)[0]
    except Exception as e:
        try:
            # Musicgen special exception.
            decoder_input_ids = torch.ones((input_ids.shape[0] * pt_model.decoder.num_codebooks, 1), dtype=torch.long)
            if torch.cuda.is_available():
                decoder_input_ids = decoder_input_ids.cuda()

            kwargs["decoder_input_ids"] = decoder_input_ids
            pt_logits = pt_model(**kwargs)[0]
        except Exception:
            raise e
    sf_logits = sf_model(**kwargs)[0]

    torch.testing.assert_close(sf_logits, pt_logits)
    print(f"Model {model_id} is ok !")


def previous_pr(api: "HfApi", model_id: str, pr_title: str) -> Optional["Discussion"]:
    try:
        main_commit = api.list_repo_commits(model_id)[0].commit_id
        discussions = api.get_repo_discussions(repo_id=model_id)
    except Exception:
        return None
    for discussion in discussions:
        if discussion.status == "open" and discussion.is_pull_request and discussion.title == pr_title:
            commits = api.list_repo_commits(model_id, revision=discussion.git_reference)

            if main_commit == commits[1].commit_id:
                return discussion
    return None


def convert_generic(model_id: str, folder: str, filenames: Set[str], token: Optional[str]) -> ConversionResult:
    operations = []
    errors = []

    extensions = set([".bin", ".ckpt"])
    for filename in filenames:
        prefix, ext = os.path.splitext(filename)
        if ext in extensions:
            pt_filename = hf_hub_download(model_id, filename=filename, token=token, cache_dir=folder)
            dirname, raw_filename = os.path.split(filename)
            if raw_filename == "pytorch_model.bin":
                # XXX: This is a special case to handle `transformers` and the
                # `transformers` part of the model which is actually loaded by `transformers`.
                sf_in_repo = os.path.join(dirname, "model.safetensors")
            else:
                sf_in_repo = f"{prefix}.safetensors"
            sf_filename = os.path.join(folder, sf_in_repo)
            try:
                convert_file(pt_filename, sf_filename)
                operations.append(CommitOperationAdd(path_in_repo=sf_in_repo, path_or_fileobj=sf_filename))
            except Exception as e:
                errors.append((pt_filename, e))
    return operations, errors


def convert(api: "HfApi", model_id: str, force: bool = False) -> Tuple["CommitInfo", List[Tuple[str, "Exception"]]]:
    pr_title = "Adding `safetensors` variant of this model"
    info = api.model_info(model_id)
    filenames = set(s.rfilename for s in info.siblings)

    with TemporaryDirectory() as d:
        folder = os.path.join(d, repo_folder_name(repo_id=model_id, repo_type="models"))
        os.makedirs(folder)
        new_pr = None
        try:
            operations = None
            pr = previous_pr(api, model_id, pr_title)

            library_name = getattr(info, "library_name", None)
            if any(filename.endswith(".safetensors") for filename in filenames) and not force:
                raise AlreadyExists(f"Model {model_id} is already converted, skipping..")
            elif pr is not None and not force:
                url = f"https://huggingface.co/{model_id}/discussions/{pr.num}"
                new_pr = pr
                raise AlreadyExists(f"Model {model_id} already has an open PR check out {url}")
            elif library_name == "transformers":
                if "pytorch_model.bin" in filenames:
                    operations, errors = convert_single(model_id, folder, token=api.token)
                elif "pytorch_model.bin.index.json" in filenames:
                    operations, errors = convert_multi(model_id, folder, token=api.token)
                else:
                    raise RuntimeError(f"Model {model_id} doesn't seem to be a valid pytorch model. Cannot convert")
                check_final_model(model_id, folder, token=api.token)
            else:
                operations, errors = convert_generic(model_id, folder, filenames, token=api.token)

            if operations:
                new_pr = api.create_commit(
                    repo_id=model_id,
                    operations=operations,
                    commit_message=pr_title,
                    commit_description=COMMIT_DESCRIPTION,
                    create_pr=True,
                )
                print(f"Pr created at {new_pr.pr_url}")
            else:
                print("No files to convert")
        finally:
            shutil.rmtree(folder)
        return new_pr, errors


if __name__ == "__main__":
    DESCRIPTION = """
    Simple utility tool to convert automatically some weights on the hub to `safetensors` format.
    It is PyTorch exclusive for now.
    It works by downloading the weights (PT), converting them locally, and uploading them back
    as a PR on the hub.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "model_id",
        type=str,
        help="The name of the model on the hub to convert. E.g. `gpt2` or `facebook/wav2vec2-base-960h`",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Create the PR even if it already exists of if the model was already converted.",
    )
    parser.add_argument(
        "-y",
        action="store_true",
        help="Ignore safety prompt",
    )
    args = parser.parse_args()
    model_id = args.model_id
    api = HfApi()
    if args.y:
        txt = "y"
    else:
        txt = input(
            "This conversion script will unpickle a pickled file, which is inherently unsafe. If you do not trust this file, we invite you to use"
            " https://huggingface.co/spaces/safetensors/convert or google colab or other hosted solution to avoid potential issues with this file."
            " Continue [Y/n] ?"
        )
    if txt.lower() in {"", "y"}:
        try:
            commit_info, errors = convert(api, model_id, force=args.force)
            string = f"""
### Success 🔥
Yay! This model was successfully converted and a PR was open using your token, here:
[{commit_info.pr_url}]({commit_info.pr_url})
            """
            if errors:
                string += "\nErrors during conversion:\n"
                string += "\n".join(
                    f"Error while converting {filename}: {e}, skipped conversion" for filename, e in errors
                )
            print(string)
        except Exception as e:
            print(
                f"""
### Error 😢😢😢

{e}
            """
            )
    else:
        print(f"Answer was `{txt}` aborting.")
