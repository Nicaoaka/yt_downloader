from yt_downloader import *


def main():
    dl = YT_Downloader(existing_info_path=r'test list [...DQL3Lagn1AW]/info.json')
    dl.download_playlist()
    dl.number_videos()
    # write_json(union_pl_info([
    #     load_json(r'test list [...DQL3Lagn1AW]/flat_info.json'),
    #     load_json(r'test list [...DQL3Lagn1AW]/flat_info (2).json')
    # ]), r'test list [...DQL3Lagn1AW]/unioned.json')

if __name__ == "__main__":
    main()