import base64
from typing import Tuple, Union, Any
import os
import uuid
from datetime import datetime

VALID_FILE_EXT = {".mp4", ".mp3", ".wav", ".ogg"}


def replace_b64_with_input_path(args, output_dir: str = "./temp_videos") -> Any:
    if not isinstance(args, dict):
        return args
    if 'video' in args:
        is_b64, data_bytes = is_base64(args['video'])
        if is_b64:
            path_to_vid = save_base64_to_file(data_bytes,"from_b64_video", ".mp4", output_dir)
            args['video'] = path_to_vid
    if 'audio' in args:
        is_b64, data_bytes = is_base64(args['audio'])
        if is_b64:
            path_to_vid = save_base64_to_file(data_bytes,"from_b64_audio", ".mp3", output_dir)
            args['audio'] = path_to_vid
    return args


def is_base64(data) -> Tuple[bool, Union[None, bytes]]:
    try:
        if isinstance(data, str):
            data_bytes = base64.b64decode(data)
            return True, data_bytes
    except Exception as e:
        print(f"failed to decode string, likely not b64 {type(data)}")
        pass
    return False, None


def save_base64_to_file(
    data_bytes: bytes,
    file_prefix: str,
    file_ext: str,
    output_dir: str = "./temp"
) -> str:
    if file_ext not in VALID_FILE_EXT:
        raise Exception(f"invalid file extension: {file_ext}, valid: {VALID_FILE_EXT}")
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{file_prefix}_{timestamp}_{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(data_bytes)
        return file_path
    except Exception as e:
        raise Exception(f"Failed to save base64 video: {e}")


def _test_vid():
    _base_test(
        r"test_vid.mp4",
        "video",
        "test_vid",
        ".mp4"
    )
def _test_audio():
    _base_test(
        r"test_audio.mp3",
        "audio",
        "test_audio_b64",
        ".mp3"
    )

def _base_test(input_file_path: str, media_key: str, file_prefix: str, file_ext: str):
    try:
        with open(input_file_path, "rb") as video_file:
            video_data = video_file.read()
            video_b64 = base64.b64encode(video_data).decode("utf-8")
    except Exception as e:
        raise Exception(f"Failed to read or encode video file: {e}")

    # Step 3: Test the `is_base64` function
    is_valid, decoded_data = is_base64(video_b64)
    if not is_valid:
        raise Exception("The base64 string is invalid!")

    print("Base64 validation passed successfully.")

    # Step 4: Test the `save_base64_to_file` function
    try:
        saved_file_path = save_base64_to_file(decoded_data, file_prefix, file_ext)
        print(f"{media_key} saved successfully to: {saved_file_path}")
    except Exception as e:
        raise Exception(f"Failed to save base64 {media_key}: {e}")

    args = {
        media_key: video_b64
    }
    replace_b64_with_input_path(args)
    print(args)
    assert media_key in args
    assert os.path.exists(compare[media_key])
    assert os.path.isfile(compare[media_key])

if __name__ == "__main__":
    _test_vid()
    _test_audio()