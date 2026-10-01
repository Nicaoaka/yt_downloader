"""Read and write _metadata.json (schema v2): identity, resolved paths, download history.

Template drift is a reported Issue that relocate() resolves, not an exception. Today
_validate_metadata_config_sync raises when config.path_tmpls differs from what the metadata
recorded, so changing a template for a playlist with data on disk means renaming files by
hand.

Also home-level: _playlists.json, the id -> playlist_dir index that makes a record findable
by id even after the folder is renamed.
"""
