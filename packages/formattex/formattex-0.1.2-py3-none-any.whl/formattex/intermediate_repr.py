from dataclasses import dataclass, field

from TexSoup import TexSoup
from TexSoup import data as texsoup_classes

from .util import (
    protect_backslash_space,
    unprotect_backslash_space,
    remove_trailing_whitespaces,
    wrapper,
)


class TexSoupError(RuntimeError):
    """Error from texsoup"""


@dataclass
class FormatterState:
    active: bool = True
    verbose: bool = False
    formatted_things: list = field(default_factory=list)

    def get_last(self):
        try:
            last = self.formatted_things[-1]
        except IndexError:
            last = "\n"
        return last


class InternalRepr:
    def __init__(self, full_code, verbose=False):
        self.full_code = full_code

        if r"\begin{document}" in full_code:
            self.has_document_env = True
            self.before_begin_doc, rest = full_code.split(
                r"\begin{document}", maxsplit=1
            )
            self.code_document_env, self.after_end_doc = rest.split(
                r"\end{document}", maxsplit=1
            )
        else:
            self.has_document_env = False
            self.code_document_env = full_code

        self.expressions = create_internal_repr_document_env(
            self.code_document_env, verbose=verbose
        )
        self.verbose = verbose

    def dump(self):
        code_out = "".join(t.code for t in self.expressions)

        if self.has_document_env:
            code_out = (
                self.before_begin_doc
                + r"\begin{document}"
                + code_out
                + r"\end{document}"
                + self.after_end_doc
            )

        return unprotect_backslash_space(code_out)

    def get_formatted(
        self, line_length=87, ensure_empty_line=True, formatter_state=None
    ):
        if formatter_state is None:
            formatter_state = FormatterState(verbose=self.verbose)

        wrapper.width = line_length

        code_out = _format_expressions(self.expressions, formatter_state)

        if self.has_document_env:
            code_out = (
                self.before_begin_doc
                + r"\begin{document}"
                + code_out
                + r"\end{document}"
                + self.after_end_doc
            )

        while "\n\n\n\n" in code_out:
            code_out = code_out.replace("\n\n\n\n", "\n\n\n")
        if ensure_empty_line and code_out[-1] != "\n":
            code_out += "\n"
        return unprotect_backslash_space(code_out)

    def save_formatted(self, path_output="tmp_formatted.tex", line_length=87):
        code_out = self.get_formatted(line_length)
        with open(path_output, "w") as file:
            file.write(code_out)
        return code_out


def _format_expressions(expressions, formatter_state):
    for thing in expressions:
        if formatter_state.active:
            code = thing.get_formatted_code(formatter_state)
        else:
            code = thing.get_code(formatter_state)
        formatter_state.formatted_things.append(code)
    return "".join(formatter_state.formatted_things)


def create_internal_repr_texfile(path_in, verbose=False):
    with open(path_in) as file:
        full_code = file.read()

    return InternalRepr(full_code, verbose=verbose)


def remove_double_newline(expressions):
    expressions_cleaned = [expressions[0]]
    for e0, e1 in zip(expressions[:-1], expressions[1:]):
        if e0 == e1 == "\n":
            expressions_cleaned[-1] = texsoup_classes.TexText("\n\n")
        else:
            expressions_cleaned.append(e1)
    return expressions_cleaned


def cleanup_expressions(expressions):
    expressions_cleaned = []
    for expr in expressions:
        if not isinstance(expr, (texsoup_classes.TexText, str)) or "\n\n" not in expr:
            expressions_cleaned.append(expr)
            continue
        pieces_without_emptylines = [
            texsoup_classes.TexText(text) for text in expr.split("\n\n")
        ]
        empty_line = texsoup_classes.TexText("\n\n")
        pieces = [empty_line] * (len(pieces_without_emptylines) * 2 - 1)
        pieces[0::2] = pieces_without_emptylines
        expressions_cleaned.extend(piece for piece in pieces if piece)
    return expressions_cleaned


def _expressions_from_text(text):
    try:
        soup = TexSoup(text)
    except EOFError as err:
        if len(text) > 100:
            text = text[:100] + "[...]"

        raise TexSoupError(text) from err

    expressions = [node.expr for node in soup.all]
    expressions = cleanup_expressions(expressions)
    return remove_double_newline(expressions)


def create_internal_repr_document_env(code_document_env, verbose=False):
    code_document_env = protect_backslash_space(code_document_env)
    code_document_env = remove_trailing_whitespaces(code_document_env)
    expressions = _expressions_from_text(code_document_env)
    things = create_internal_repr_from_expressions(expressions, verbose=verbose)

    if verbose > 1:
        print(f"{things = }")

    return things


def create_internal_repr_from_expressions(
    expressions,
    verbose=False,
    things=None,
    exprs_piece_of_text=None,
):
    if things is None:
        things = []

    if exprs_piece_of_text is None:
        exprs_piece_of_text = []

    _create_internal_repr_internal(
        expressions,
        verbose=verbose,
        things=things,
        exprs_piece_of_text=exprs_piece_of_text,
    )

    if exprs_piece_of_text:
        things.append(LinesOfText(exprs_piece_of_text))

    return things


def _create_internal_repr_internal(
    expressions,
    verbose=False,
    things=None,
    exprs_piece_of_text=None,
    name_next_error="text",
    str_next_error="",
):
    index = 0
    while index < len(expressions):
        expr = expressions[index]

        if verbose > 1:
            print(
                f"{type(expr).__name__:14} "
                f"{repr(expr)[:59] = :60}{bool(exprs_piece_of_text) = }"
            )

        try:
            expr_next = expressions[index + 1]
        except IndexError:
            name_next = name_next_error
            str_next = str_next_error
        else:
            if isinstance(expr_next, str):
                name_next = "text"
            else:
                name_next = expr_next.name
            str_next = str(expr_next)

        if isinstance(expr, str) or expr.name == "text":
            text = str(expr)

            if text.strip().startswith("%"):
                if exprs_piece_of_text:
                    things.append(LinesOfText(exprs_piece_of_text))

                things.append(CommentLine(text))
            elif text == "\n\n":
                if exprs_piece_of_text:
                    things.append(LinesOfText(exprs_piece_of_text))
                things.append(EmptyLine())

            elif text == "\n":
                if exprs_piece_of_text:
                    if name_next == "text" and str_next.startswith("\n"):
                        things.append(LinesOfText(exprs_piece_of_text))
                        things.append(NewLine())
                    else:
                        exprs_piece_of_text.append(text)
                else:
                    things.append(NewLine())
            elif not exprs_piece_of_text and text != "\n":
                exprs_piece_of_text.append(text)
            elif exprs_piece_of_text:
                exprs_piece_of_text.append(text)

            if exprs_piece_of_text and name_next == "text" and str_next == "\n\n":
                things.append(LinesOfText(exprs_piece_of_text))

        elif isinstance(expr, texsoup_classes.TexMathModeEnv):
            exprs_piece_of_text.append(expr)

        elif isinstance(expr, texsoup_classes.TexCmd):

            has_to_create_TexCmd = False
            if not exprs_piece_of_text and expr.args:
                if expr.string == "\n":
                    has_to_create_TexCmd = True
                elif expr.string == "" and (
                    name_next == "text" and str_next.startswith("\n")
                ):
                    has_to_create_TexCmd = True

            if has_to_create_TexCmd:
                things.append(TexCmd(expr.name, str(expr), expr))
            else:
                text = (
                    "\\"
                    + expr.name
                    + "".join(
                        [arg.begin + arg.string.strip() + arg.end for arg in expr.args]
                    )
                )
                exprs_piece_of_text.append(text)
                if expr.string:
                    expressions1 = _expressions_from_text(expr.string)
                    _create_internal_repr_internal(
                        expressions1,
                        verbose,
                        things,
                        exprs_piece_of_text,
                        name_next_error=name_next,
                        str_next_error=str_next,
                    )

        elif isinstance(expr, texsoup_classes.TexNamedEnv):
            if exprs_piece_of_text:
                things.append(LinesOfText(exprs_piece_of_text))
            things.append(BeginEndBlock(expr.name, expr.string, expr))

        elif isinstance(expr, texsoup_classes.BraceGroup):
            if exprs_piece_of_text:
                exprs_piece_of_text.append(expr)
            else:
                things.append(BraceGroup(expr))

        elif isinstance(expr, texsoup_classes.TexDisplayMathModeEnv):
            if exprs_piece_of_text:
                things.append(LinesOfText(exprs_piece_of_text))
            things.append(DoubleDollarGroup(expr))

        else:
            raise NotImplementedError(f"{expr = }")

        index += 1

    return things


from .nodes import (
    LinesOfText,
    CommentLine,
    EmptyLine,
    NewLine,
    TexCmd,
    BeginEndBlock,
    BraceGroup,
    DoubleDollarGroup,
)  # noqa: E402
