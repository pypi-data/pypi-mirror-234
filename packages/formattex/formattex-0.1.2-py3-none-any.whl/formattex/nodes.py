from textwrap import dedent
from dataclasses import dataclass

from TexSoup import data as texsoup_classes


from .util import (
    unprotect_backslash_space,
    wrap,
    remove_more_than_3_spaces,
)

from .intermediate_repr import InternalRepr


class BaseLatexNode:
    @property
    def code(self):
        return self.text

    def get_code(self, formatter_state=None):
        return self.code

    def get_formatted_code(self, formatter_state=None):
        return self.code


@dataclass
class LinesOfText(BaseLatexNode):
    expressions: list

    def __init__(self, expressions):
        self.expressions = expressions.copy()
        expressions.clear()

    @property
    def code_protected(self):
        return "".join(str(expr) for expr in self.expressions)

    @property
    def code(self):
        return unprotect_backslash_space(self.code_protected)

    def __repr__(self):
        code = repr(self.code)
        if len(code) > 20:
            code = code[:20] + "[...]"
        return f"LinesOfText(code='{code}')"

    def get_formatted_code(self, formatter_state=None):
        code = self.code_protected

        if code.strip().endswith(r"\\"):
            main, doublebackslash, end = code.rpartition(r"\\")
            code = main.rstrip() + end

        if r"\\[" in code:
            pass
            # TODO: nice regex, something like
            # re.findall(r"\\\\\[.*\]", code)

        last = formatter_state.get_last()

        if last.endswith("\n"):
            code = code.lstrip(" ").lstrip("\t")

        parts = last.rsplit("\n", 1)
        if len(parts) == 2:
            last_line = parts[1]
            if (
                last_line.startswith(r"\end{")
                and last_line.endswith("}")
                and not code.startswith("\n")
            ):
                code = "\n" + code.lstrip()

        for to_be_suppressed in ("\n ", "\n\t"):
            while to_be_suppressed in code:
                code = code.replace(to_be_suppressed, "\n")

        return unprotect_backslash_space(wrap(code))


@dataclass
class CommentLine(BaseLatexNode):
    text: str

    def get_code(self, formatter_state=None):
        self._check_format_instruction(formatter_state)
        return self.text

    def get_formatted_code(self, formatter_state=None):
        self._check_format_instruction(formatter_state)
        return self.text

    def _check_format_instruction(self, formatter_state):
        comment = self.text[1:].strip()
        if comment.startswith("fmt:"):
            fmt_status = comment[5:].strip()
            if fmt_status == "on":
                formatter_state.active = True
            elif fmt_status == "off":
                formatter_state.active = False
            else:
                raise print("Unknown instruction for formattex")


@dataclass
class TexCmd(BaseLatexNode):
    name: str
    text: str
    expr: texsoup_classes.TexCmd

    def get_formatted_code(self, formatter_state=None):
        code = (
            "\\"
            + self.expr.name
            + "".join(
                [arg.begin + arg.string.strip() + arg.end for arg in self.expr.args]
            )
            + self.expr.string
        )
        return unprotect_backslash_space(wrap(code))

    def __repr__(self) -> str:
        text = self.text
        if len(text) > 79:
            text = text[:70] + "[...]"
        return f"TexCmd(name={self.name}, text='{text})'"


class BraceGroup(BaseLatexNode):
    def __init__(self, expr):
        self.content = str(expr).strip()[1:-1]

    @property
    def code(self):
        return "{" + self.content + "}"

    def get_formatted_code(self, formatter_state=None):
        repr_content = InternalRepr(self.content)
        return "{" + repr_content.get_formatted(ensure_empty_line=False) + "}"


class DoubleDollarGroup(BaseLatexNode):
    def __init__(self, expr):
        self.content = str(expr).strip()[2:-2].strip()

    @property
    def code(self):
        return "$$\n" + self.content + "\n$$"

    def get_formatted_code(self, formatter_state=None):
        repr_content = InternalRepr(self.content)
        return "$$\n" + repr_content.get_formatted().strip() + "\n$$"


@dataclass
class BeginEndBlock(BaseLatexNode):
    kind: str
    content: str
    expr: texsoup_classes.TexNamedEnv

    @property
    def code(self):
        return self._get_code_from_content(self.content)

    def __repr__(self):
        if len(self.content) < 10:
            content_repr = self.content.strip()
        else:
            content_repr = self.content[:10].strip() + "[...]"

        return f"BeginEndBlock(kind='{self.kind}', content='{content_repr}'"

    def get_formatted_code(self, formatter_state=None):
        content = dedent(self.content)
        if self.kind == "figure":
            before_caption, after_caption = content.split(r"\caption{")
            after_caption = remove_more_than_3_spaces(
                wrap(r"\caption{" + after_caption)
            )
            content = (
                "\n"
                + before_caption.strip()
                + "\n"
                + unprotect_backslash_space(after_caption)
            )
        elif any(
            self.kind.startswith(start)
            for start in ("equation", "align", "algorithm", "tabular")
        ):
            content = "\n" + content.strip() + "\n"
        else:
            # print(f"\n{self.content = }")

            # cannot do that because TexSoup bug (see input12.tex)
            # print(f"{self.expr.contents = }")
            # expressions = create_internal_repr_from_expressions(
            #     cleanup_expressions(self.expr.contents),
            #     verbose=formatter_state.verbose,
            # )
            # content = _format_expressions(expressions, formatter_state)

            repr_content = InternalRepr(content, verbose=formatter_state.verbose)
            content = repr_content.get_formatted(ensure_empty_line=False)

            # print(f"{content = }")

        result = self._get_code_from_content(content)

        last = formatter_state.get_last()
        if not last.endswith("\n"):
            result = "\n" + result

        return result

    def _get_args_code(self):
        return "".join(
            arg.begin + arg.string.strip() + arg.end for arg in self.expr.args
        )

    def _get_code_from_content(self, content):
        if not content.startswith("\n") and not content.startswith(" "):
            content = " " + content

        return (
            rf"\begin{{{self.kind}}}{self._get_args_code()}"
            rf"{content}\end{{{self.kind}}}"
        )


@dataclass
class NewLine(BaseLatexNode):
    code = "\n"


@dataclass
class EmptyLine(BaseLatexNode):
    code = "\n\n"
