"""The Cookies handle -- validation, scope and emptying, owned by whoever opened the file.

    with pldl2.cookies('secrets/cookie_file.txt') as ck:
        pl.refresh(cookies=ck)     # was cookies_for_pl=True
        pl.download(policy)        # was cookies_for_vids=False -- just do not pass them

cookies_for_pl / cookies_for_vids become *passing the argument or not*, which is what two
booleans were simulating. empty_cookies stops being the playlist's business: today
PlaylistDL.close() truncates a file that is global and shared, so two playlists in one script
race to blank each other's credentials.

**The pre-flight check is kept and strengthened.** The objection is where it runs, never that
it runs -- yt-dlp reports a private playlist you cannot see as "playlist does not exist", so
'LL' with a bad cookie file produces an error pointing at the wrong thing entirely. Failing
before the call is the only way the message stays truthful. Checks, each a one-line rule over
a parsed jar, all pure over file text so fixtures replace real credentials:

    exists + non-empty              a placeholder or wiped file (today's check)
    Netscape header present         a wrong file, or a JSON export from the wrong extension
    >= 1 .youtube.com cookie        an export taken on the wrong site
    required auth names (SID, ...)  a logged-out export -- passes a size check today
    no expires in the past          an expired export -- the case that currently sails
                                    through and produces the misleading "doesn't exist"
"""
