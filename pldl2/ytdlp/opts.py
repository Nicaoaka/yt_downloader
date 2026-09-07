"""**Exactly one function builds the opts handed to yt-dlp, and it deep-merges.**

The single highest-value structural fix in the plan. Today four call sites assemble opts
independently (:359, :1058, :1219, :1312) and three are wrong in different ways -- all
confirmed by the repro harness:

  - download_v_infos's ternary binds looser than `|`, so the default path silently drops the
    cookie file (cookies_for_vids is dead) *and* an explicit opts= **replaces** self.opts
    wholesale, losing paths, outtmpl, download_archive, format, subtitle and postprocessor
    settings. Videos land in the cwd under yt-dlp's default names and the archive is never
    updated (#1).
  - the constructor's flat extract passes only {'cookiefile': ...}, ignoring retries, rate
    limits and sleeps (#19).
  - the top-level `|` merge destroys config.opts['paths']['temp'] by replacing the whole
    paths dict (#28).

Test: the generated keys are present on every path.
"""
