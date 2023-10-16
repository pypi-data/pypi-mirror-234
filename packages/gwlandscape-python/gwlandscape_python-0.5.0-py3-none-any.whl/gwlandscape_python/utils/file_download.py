import concurrent.futures
from functools import partial
import requests
from tqdm import tqdm
from ..settings import GWLANDSCAPE_FILE_DOWNLOAD_ENDPOINT


def _get_file_map_fn(file_ref, progress_bar, **kwargs):
    download_url = GWLANDSCAPE_FILE_DOWNLOAD_ENDPOINT + str(file_ref.download_token)

    content = b''

    with requests.get(download_url, stream=True) as request:
        for chunk in request.iter_content(chunk_size=1024 * 16, decode_unicode=True):
            progress_bar.update(len(chunk))
            content += chunk
    return (file_ref.path, content)


def _save_file_map_fn(file_ref, progress_bar, root_path):
    download_url = GWLANDSCAPE_FILE_DOWNLOAD_ENDPOINT + str(file_ref.download_token)

    output_path = root_path / file_ref.path
    output_path.parents[0].mkdir(parents=True, exist_ok=True)

    with requests.get(download_url, stream=True) as request:
        with output_path.open("wb+") as f:
            for chunk in request.iter_content(chunk_size=1024 * 16):
                progress_bar.update(len(chunk))
                f.write(chunk)


def _download_files(map_fn, file_refs, root_path=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        progress = tqdm(total=file_refs.get_total_bytes(), leave=True, unit='B', unit_scale=True)
        files = list(
            executor.map(
                partial(
                    map_fn,
                    progress_bar=progress,
                    root_path=root_path
                ),
                file_refs
            )
        )
        progress.close()
    return files
