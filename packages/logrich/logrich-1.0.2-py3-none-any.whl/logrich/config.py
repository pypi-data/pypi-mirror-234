from dotenv import dotenv_values


config = dict(
    COLUMNS=110,  # type: ignore
    # https://rich.readthedocs.io/en/stable/appendix/colors.html
    LOG_LEVEL_ELAPCE_TPL="[reverse turquoise2] ELAPCE [/]",
    LOG_LEVEL_START_TPL="[reverse i aquamarine1] START  [/]",
    LOG_LEVEL_END_TPL="[reverse i green4] END    [/reverse i green4]",
    LOG_LEVEL_TEST_TPL="[reverse grey70] TEST   [/]",
    LOG_LEVEL_DATA_TPL="[reverse cornflower_blue] DATA   [/]",
    LOG_LEVEL_DEV_TPL="[reverse grey70] DEV    [/]",
    LOG_LEVEL_INFO_TPL="[reverse blue] INFO   [/]",
    LOG_LEVEL_TRACE_TPL="[reverse dodger_blue2] TRACE  [/]",
    LOG_LEVEL_RUN_TPL="[reverse yellow] RUN    [/]",
    LOG_LEVEL_GO_TPL="[reverse royal_blue1] GO     [/]",
    LOG_LEVEL_LIST_TPL="[reverse wheat4] LIST   [/]",
    LOG_LEVEL_DEBUG_TPL="[reverse #9f2844] DEBUG  [/]",
    LOG_LEVEL_SUCCESS_TPL="[reverse green] SUCCS  [/]",
    LOG_LEVEL_LOG_TPL="[reverse chartreuse4] LOG    [/]",
    LOG_LEVEL_TIME_TPL="[reverse spring_green4] TIME   [/]",
    LOG_LEVEL_WARN_TPL="[reverse bright_red] WARN   [/]",
    LOG_LEVEL_WARNING_TPL="[reverse bright_red] WARN   [/]",
    LOG_LEVEL_FATAL_TPL="[reverse bright_red] FATAL  [/]",
    LOG_LEVEL_ERR_TPL="[reverse #ff5252] ERR    [/]",
    LOG_LEVEL_ERROR_TPL="[reverse #ff5252] ERROR  [/]",
)

config.update(
    **dotenv_values(),
)
