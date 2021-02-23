import argparse
import os

from pytube import YouTube


def parse_arguments():
    parser = argparse.ArgumentParser(description='Modifies a video file to play at different speeds when there is sound vs. silence.')
    parser.add_argument('--input_file', type=str, default=None, help='the video file you want modified')
    parser.add_argument('--url', type=str, default=None, help='A youtube url to download and process')
    parser.add_argument('--output_file', type=str, default=None, help="the output file. (optional. if not included, it'll just modify the input file name)")
    parser.add_argument('--silent_threshold', type=float, default=0.01, help="the volume amount that frames' audio needs to surpass to be consider \"sounded\". It ranges from 0 (silence) to 1 (max volume)")
    parser.add_argument('--sounded_speed', type=float, default=1.00, help="the speed that sounded (spoken) frames should be played at. Typically 1.")
    parser.add_argument('--silent_speed', type=float, default=5.00, help="the speed that silent frames should be played at. 999999 for jumpcutting.")
    parser.add_argument('--frame_margin', type=float, default=1, help="some silent frames adjacent to sounded frames are included to provide context. How many frames on either the side of speech should be included? That's this variable.")
    parser.add_argument('--sample_rate', type=float, default=44100, help="sample rate of the input and output videos")
    parser.add_argument('--frame_rate', type=float, default=30, help="frame rate of the input and output videos. optional... I try to find it out myself, but it doesn't always work.")
    parser.add_argument('--frame_quality', type=int, default=3, help="quality of frames to be extracted from input video. 1 is highest, 31 is lowest, 3 is the default.")

    return parser.parse_args()


def download_file(url):
    print("downloading file or getting path if file exists")
    yt = YouTube(url)
    name = yt.title.replace(" ", "_").lower()
    try:
        print("trying 720p")
        filepath = yt.streams.get_by_resolution("720p").download(filename=name, skip_existing=True)
    except:
        print("720p failed, getting highest available resolution")
        filepath = yt.streams.get_highest_resolution().download(filename=name, skip_existing=True)
    print("downloading or getting path finished")
    return filepath


def main():
    args = parse_arguments()

    assert args.url is not None or args.input_file is not None, "no input url or file, please provide one of them"
    assert not (args.url is not None and args.input_file is not None), "both url and input_file is provided, choose only one"

    if args.url is not None:
        args.input_file = download_file(args.url)

    print("working with file:", args.input_file)


if __name__ == "__main__":
    main()
