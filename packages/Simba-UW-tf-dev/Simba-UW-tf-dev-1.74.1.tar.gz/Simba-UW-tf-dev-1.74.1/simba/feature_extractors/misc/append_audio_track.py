import os
from typing import Union
from simba.utils.read_write import get_video_meta_data, get_fn_ext
from simba.utils.checks import check_file_exist_and_readable, check_ffmpeg_available
from simba.utils.warnings import InValidUserInputWarning
import subprocess
from simba.utils.errors import FFMPEGNotFoundError, NoDataError
from simba.utils.printing import stdout_success
try:
    from typing import Literal
except:
    from typing_extensions import Literal


def append_audio(video_path: Union[str, os.PathLike],
                 audio_path: Union[str, os.PathLike],
                 audio_src_type: Literal['video', 'audio'] = 'video') -> None:

    """
    Append audio track from one video to another video without an audio track.

    :param str video_one_path: Path to video file without audio track.
    :param str video_two_path: Path to file (e.g., video) with audio track.
    :param Literal['video', 'audio'] audio_src_type: Type of audio source of "video_two_path" (e.g., video or audio file).

    :example:
    >>> append_audio(video_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/videos/merged_video_20230425201637.mp4',
    >>> audio_path="/Users/simon/Documents/Zoom/ddd/video1180732233.mp4")
    """

    if not check_ffmpeg_available():
        raise FFMPEGNotFoundError(msg='FFMpeg not found on computer. See SimBA docs for install instructions.')
    check_file_exist_and_readable(file_path=video_path)
    check_file_exist_and_readable(file_path=audio_path)
    video_meta_data = get_video_meta_data(video_path=video_path)
    audio_src_meta_data = get_video_meta_data(video_path=audio_path)

    save_path = os.path.join(os.path.dirname(video_path), get_fn_ext(filepath=video_path)[1] + '_w_audio.mp4')
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
    try:
        track_type = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        raise NoDataError(msg=f'No audio track found in file {audio_path}', source=__name__)

    if video_meta_data['frame_count'] != audio_src_meta_data['frame_count']:
        InValidUserInputWarning(msg=f'The video ({video_meta_data["frame_count"]}) and audio source ({audio_src_meta_data["frame_count"]}) does not have an equal number of frames.', source=append_audio.__name__)

    cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -map 0:v:0 -map 1:a:0 "{save_path}" -y'

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)

    stdout_success(msg=f"Audio merged successfully, file saved at {save_path}!")



