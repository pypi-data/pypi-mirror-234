from oslo_config import cfg


plugin_group = cfg.OptGroup(
    name="aprsd_wxnow_plugin",
    title="APRSD WXNOW Plugin settings",
)

plugin_opts = [
    cfg.StrOpt(
        "haminfo_apiKey",
        help="Haminfo API key",
    ),
    cfg.StrOpt(
        "haminfo_base_url",
        help="The base url to the haminfo REST API",
    ),
]

ALL_OPTS = (
    plugin_opts
)


def register_opts(cfg):
    cfg.register_group(plugin_group)
    cfg.register_opts(ALL_OPTS, group=plugin_group)


def list_opts():
    return {
        plugin_group.name: plugin_opts,
    }
