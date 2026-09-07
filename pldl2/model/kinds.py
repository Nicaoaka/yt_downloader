"""The InfoKind registry -- one frozen dataclass per stored info type.

Today the taxonomy has no single definition: metadata_key is match-ed in three separate
methods (write_info:789, get_filtered_data:726, reorder_keys:736), so adding a sixth info
type means editing those three plus _Infos, MetadataPointers, _MetadataFiles_Lit and
default_path_tmpls.

It is a **container of strategies, not an object with read/write methods**. Giving each kind
its own I/O would recreate five little persistence implementations, which is exactly what
this rewrite deletes. store.write(kind, info) does the I/O once and dispatches through the
kind's fields; batch-vs-single is expressed as data via `payload`.

    name, tmpl_key, owner (PLDL | USER), epoch_of, reorder, payload, filter_of
"""
