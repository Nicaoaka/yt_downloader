import time



def do_thing():
    # if they are not cached it can take a couple seconds
    # if they are cached it will take around a third of a second
    start = time.perf_counter()
    from yt_dlp.extractor.youtube import YoutubeIE
    from yt_dlp.extractor.archiveorg import YoutubeWebArchiveIE

    YT_IE_KEY = YoutubeIE.ie_key()
    YTWA_IE_KEY = YoutubeWebArchiveIE.ie_key()

    print(YT_IE_KEY)
    print(YTWA_IE_KEY)

    end = time.perf_counter()
    print(f"Took {end - start} seconds")




do_thing()

time.sleep(1)
do_thing()

time.sleep(1)
do_thing()
