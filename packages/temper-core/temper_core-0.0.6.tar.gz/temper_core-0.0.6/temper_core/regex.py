import re
import temper_core
import typing
import types


def compiled_regex_compiled_find(_, compiled: re.Pattern, text: str, regex_refs):
    match = compiled.search(text)
    if match is None:
        raise temper_core.BubbleException()
    return _convert_match(match, regex_refs)


def _convert_match(match, regex_refs):
    Group = regex_refs.group.__class__
    groups = match.groupdict()
    # Python indices are already in code points.
    result = {}
    if "full" not in groups:
        result["full"] = Group("full", match.group(), match.start())
    for name, value in groups.items():
        result[name] = Group(name, value or "", match.start(name))
    return result


def compiled_regex_compiled_found(_, compiled: re.Pattern, text: str):
    return compiled.search(text) is not None


def compiled_regex_compiled_replace(
    _,
    compiled: re.Pattern,
    text: str,
    format: typing.Callable[[types.MappingProxyType[str, typing.Any]], str],
    regex_refs,
):
    def adapted_format(match):
        return format(_convert_match(match, regex_refs))

    return compiled.sub(adapted_format, text)


def compiled_regex_compile_formatted(_, formatted: str):
    return re.compile(formatted, re.ASCII)


def regex_formatter_push_capture_name(_, out: typing.MutableSequence[str], name: str):
    out.append(rf"?P<{name}>")


def regex_formatter_push_code_to(
    _, out: typing.MutableSequence[str], code: int, insideCodeSet: bool
):
    # Ignore insideCodeSet for now.
    # TODO(tjp, regex): Get fancier, including with work in Temper.
    out.append(rf"\U{code:08x}")
