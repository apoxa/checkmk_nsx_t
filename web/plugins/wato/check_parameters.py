register_check_parameters(
   subgroup_applications,
    "backups",
    _("Time since last backup"),
        Dictionary(
          elements = [
          ("levels",
            Tuple(
              title = _("Time since of last backup"),
              elements = [
                  Integer(
                      title = _("Warning Level for time since last backup"),
                      help = _("Warning Level for time since last backup."),
                      unit = _("days"),
                      default_value = 7,
                  ),
                  Integer(
                      title = _("Critical Level for time since last backup"),
                      help = _("Critical Level for time since last backup."),
                      unit = _("days"),
                      default_value = 14,
                  ),
              ]
            )
         )]
    ),
    None,
    "dict"
)

register_check_parameters(
    subgroup_os,
    "nsx_memory",
    _("Main memory usage of VMWare NSX system"),
    Dictionary(
      elements = [
      ("levels",
        Tuple(
          title = _("Specify levels in percentage of total RAM"),
          elements = [
            Percentage(
                title = _("Warning at a RAM usage of"),
                help = _("Warning level if memory usage is above"),
                default_value = 80.0
            ),
            Percentage(
                title = _("Critical at a RAM usage of"),
                help= _("Critical level if memory usage is above"),
                default_value = 90.0
            ),
          ]
        )
      )]
    ),
    None,
    match_type = "dict",
)
