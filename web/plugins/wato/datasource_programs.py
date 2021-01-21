group = 'datasource_programs'
register_rule(
    group,
    "special_agents:nsx",
    Dictionary(
        optional_keys = [ "cert" ],
        elements = [
            ("user", TextAscii(title = _("Username"), allow_empty = False)),
            ("password", Password(title = _("Password"), allow_empty = False)),
            ("cert", DropdownChoice(
                            title = _("SSL certificate verification"),
                            choices = [
                                (True, _("Activate")),
                                (False, _("Deactivate")),
                            ] )),
        ],
    ),
    title = _("Check VMWare NSX"),
    help = _("This rule set selects the special agent for VMWare NSX "
             "instead of the normal Check_MK agent and allows monitoring via Web API. "
             "Resource value is optional and used for monitoring the NSX host "
             "preparation status"),
    match = "first",
)
