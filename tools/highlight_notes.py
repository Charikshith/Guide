"""Colour the code blocks in every *.notes.html page, using the handwritten skill's token classes:
kw keyword, st string, nu number, bi built-in, fn function call, cm comment.

Only wraps text in <span>. The visible text of each block never changes (checked on every block).
Blocks with no language, plain "text"/"markdown", and ASCII diagrams are left plain.
Safe to re-run: existing spans are stripped and the block is tokenised again.

Usage:  python tools/highlight_notes.py
"""
import glob
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W = lambda s: set(s.split())

C_LIKE_COMMENTS = r"//[^\n]*|/\*[\s\S]*?\*/"
DQ = r'"(?:\\.|[^"\\\n])*"'
SQ = r"'(?:\\.|[^'\\\n])*'"
NUM = r"\b(?:0[xX][0-9a-fA-F_]+|0[bB][01_]+|\d[\d_]*(?:\.\d+)?(?:[eE][+-]?\d+)?[a-zA-Z]{0,3})\b"

PY_KW = W("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case")
PY_BI = W("print len range int str float list dict set tuple bool open sum min max sorted enumerate zip map filter isinstance type super abs any all input iter next reversed round bytes id hash repr vars getattr setattr hasattr callable object Exception ValueError TypeError KeyError self cls frozenset bytearray divmod pow chr ord format slice property staticmethod classmethod")
RS_KW = W("as async await break const continue crate dyn else enum extern false fn for if impl in let loop match mod move mut pub ref return self Self static struct super trait true type unsafe use where while")
RS_BI = W("Vec String Option Result Some None Ok Err Box Rc Arc HashMap HashSet BTreeMap Mutex RefCell str i8 i16 i32 i64 i128 isize u8 u16 u32 u64 u128 usize f32 f64 bool char")
JS_KW = W("async await break case catch class const continue debugger default delete do else export extends false finally for from function if import in instanceof let new null of return static super switch this throw true try typeof undefined var void while with yield")
JS_BI = W("console Math JSON Object Array Promise Map Set Date Error String Number Boolean Symbol parseInt parseFloat setTimeout fetch require module window document")
C_KW = W("auto break case const continue default do else enum extern for goto if inline register return sizeof static struct switch typedef union volatile while NULL true false")
C_BI = W("int char short long float double void unsigned signed size_t uint8_t uint16_t uint32_t uint64_t int8_t int16_t int32_t int64_t bool printf malloc free")
GO_KW = W("break case chan const continue default defer else fallthrough for func go goto if import interface map package range return select struct switch type var true false nil")
GO_BI = W("string int int8 int16 int32 int64 uint uint8 uint16 uint32 uint64 float32 float64 bool byte rune error any make new len cap append copy delete panic recover close print println")
LUA_KW = W("and break do else elseif end false for function goto if in local nil not or repeat return then true until while")
SQL_KW = W("select from where group by having order limit offset join left right inner outer full cross on as and or not in is null like between exists case when then else end insert into values update set delete create table index unique primary key foreign references alter add drop column constraint default check distinct union all with recursive over partition begin commit rollback transaction explain analyze view using asc desc true false returning")
SQL_BI = W("count sum avg min max coalesce now row_number rank dense_rank lag lead cast int integer bigint smallint text varchar char boolean timestamp date serial numeric decimal jsonb json uuid")
SH_KW = W("if then else elif fi for while do done case esac function in select until return exit break continue local export set unset readonly")
SH_BI = W("echo cd ls cat grep sed awk sudo chmod chown mkdir rm cp mv curl wget docker kubectl git pip python python3 npm node make tar ssh scp kill ps top head tail sort uniq wc find xargs tee source helm terraform systemctl journalctl nginx redis-cli psql openssl")
HCL_KW = W("resource variable output module data provider locals terraform for_each count depends_on lifecycle dynamic content true false null")
GQL_KW = W("query mutation subscription type input enum interface union scalar fragment on schema extend directive implements true false null")
GQL_BI = W("Int Float String Boolean ID")
PB_KW = W("syntax package message service rpc returns repeated optional required enum import option oneof map reserved stream extend true false")
PB_BI = W("string int32 int64 uint32 uint64 sint32 sint64 fixed32 fixed64 sfixed32 sfixed64 bool bytes double float")
CY_KW = W("match where return create merge set delete detach remove with order by limit skip as and or not in distinct optional unwind call yield union case when then else end is null true false starts ends contains")
PQ_KW = W("by without on ignoring group_left group_right offset and or unless bool")
DOCKER_KW = W("FROM RUN CMD LABEL EXPOSE ENV ADD COPY ENTRYPOINT VOLUME USER WORKDIR ARG ONBUILD STOPSIGNAL HEALTHCHECK SHELL AS")
MAKE_KW = W("ifeq ifneq ifdef ifndef else endif include define endef export override .PHONY .DEFAULT_GOAL")

# language -> (ordered [(class, regex)], keywords, builtins, ignore_case, calls_are_fn)
LANGS = {
    "python": ([("cm", r"#[^\n]*"),
                ("st", r"[rRbBfFuU]{0,2}(?:\"\"\"[\s\S]*?\"\"\"|'''[\s\S]*?'''|" + DQ + "|" + SQ + ")"),
                ("bi", r"@[A-Za-z_][\w.]*"), ("nu", NUM)], PY_KW, PY_BI, False, True),
    "rust": ([("cm", C_LIKE_COMMENTS), ("st", r'r#*"[\s\S]*?"#*|b?' + DQ), ("st", r"b?'(?:\\.|[^'\\\n])'"),
              ("fn", r"\b[A-Za-z_]\w*!(?=[(\[{])"), ("bi", r"#!?\[[^\]\n]*\]"), ("nu", NUM)], RS_KW, RS_BI, False, True),
    "js": ([("cm", C_LIKE_COMMENTS), ("st", r"`(?:\\.|[^`\\])*`|" + DQ + "|" + SQ), ("nu", NUM)], JS_KW, JS_BI, False, True),
    "c": ([("cm", C_LIKE_COMMENTS), ("st", DQ + "|" + SQ), ("bi", r"^[ \t]*#\s*\w+"), ("nu", NUM)], C_KW, C_BI, False, True),
    "go": ([("cm", C_LIKE_COMMENTS), ("st", r"`[^`]*`|" + DQ + "|" + SQ), ("nu", NUM)], GO_KW, GO_BI, False, True),
    "lua": ([("cm", r"--\[\[[\s\S]*?\]\]|--[^\n]*"), ("st", r"\[\[[\s\S]*?\]\]|" + DQ + "|" + SQ), ("nu", NUM)], LUA_KW, set(), False, True),
    "sql": ([("cm", r"--[^\n]*|/\*[\s\S]*?\*/"), ("st", SQ), ("nu", NUM)], SQL_KW, SQL_BI, True, False),
    "bash": ([("cm", r"(?<![\w$])#[^\n]*"), ("st", DQ + "|" + SQ), ("bi", r"\$\{[^}\n]*\}|\$[A-Za-z_]\w*|\$[0-9?@#*!$]"),
              ("nu", r"\b\d+\b")], SH_KW, SH_BI, False, False),
    "yaml": ([("cm", r"(?<![^\s])#[^\n]*"), ("st", DQ + "|" + SQ),
              ("bi", r"^[ \t]*(?:-[ \t]+)?[A-Za-z_][\w./-]*(?=[ \t]*:(?:\s|$))"), ("nu", NUM)],
             W("true false null yes no on off True False"), set(), False, False),
    "toml": ([("cm", r"#[^\n]*"), ("st", r'"""[\s\S]*?"""|' + DQ + "|" + SQ), ("kw", r"^[ \t]*\[\[?[^\]\n]+\]\]?"),
              ("bi", r"^[ \t]*[A-Za-z_][\w.-]*(?=[ \t]*=)"), ("nu", NUM)], W("true false"), set(), False, False),
    "ini": ([("cm", r"[#;][^\n]*"), ("st", DQ + "|" + SQ), ("kw", r"^[ \t]*\[[^\]\n]+\]"),
             ("bi", r"^[ \t]*[A-Za-z_][\w.-]*(?=[ \t]*=)"), ("nu", NUM)], W("true false"), set(), False, False),
    "json": ([("bi", DQ + r"(?=\s*:)"), ("st", DQ), ("nu", r"-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b")],
             W("true false null"), set(), False, False),
    "hcl": ([("cm", r"#[^\n]*|//[^\n]*|/\*[\s\S]*?\*/"), ("st", DQ), ("nu", NUM)], HCL_KW, set(), False, True),
    "nginx": ([("cm", r"#[^\n]*"), ("st", DQ + "|" + SQ), ("bi", r"\$\w+"),
               ("kw", r"^[ \t]*[a-z_]+(?=[ \t;{])"), ("nu", NUM)], set(), set(), False, False),
    "dockerfile": ([("cm", r"^[ \t]*#[^\n]*"), ("st", DQ + "|" + SQ), ("bi", r"\$\{?\w+\}?"), ("nu", NUM)],
                   DOCKER_KW, set(), False, False),
    "make": ([("cm", r"#[^\n]*"), ("st", DQ + "|" + SQ), ("bi", r"\$[({][^)}\n]*[)}]|\$[@<^?*%]"),
              ("fn", r"^[A-Za-z0-9_./%-]+(?=[ \t]*:(?!=))")], MAKE_KW, set(), False, False),
    "graphql": ([("cm", r"#[^\n]*"), ("st", r'"""[\s\S]*?"""|' + DQ), ("bi", r"\$\w+"), ("nu", NUM)], GQL_KW, GQL_BI, False, False),
    "protobuf": ([("cm", C_LIKE_COMMENTS), ("st", DQ + "|" + SQ), ("nu", NUM)], PB_KW, PB_BI, False, False),
    "cypher": ([("cm", r"//[^\n]*"), ("st", DQ + "|" + SQ), ("bi", r":[A-Za-z_]\w*"), ("nu", NUM)], CY_KW, set(), True, True),
    "promql": ([("cm", r"#[^\n]*"), ("st", DQ + "|" + SQ + r"|`[^`]*`"), ("nu", r"\b\d+(?:\.\d+)?(?:ms|[smhdwy])?\b")],
               PQ_KW, set(), False, True),
    "http": ([("kw", r"^(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS|CONNECT|TRACE)\b"), ("bi", r"HTTP/\d(?:\.\d)?"),
              ("bi", r"^[A-Za-z][A-Za-z0-9-]*(?=:)"), ("st", DQ), ("nu", r"\b\d+\b")], set(), set(), False, False),
}
ALIAS = {"js": "js", "javascript": "js", "typescript": "js", "ts": "js", "py": "python", "sh": "bash", "shell": "bash",
         "yml": "yaml", "proto": "protobuf", "tf": "hcl", "makefile": "make", "docker": "dockerfile", "gql": "graphql"}
SKIP = {"text", "markdown", "md", "search result", "-", ""}


def compile_lang(name):
    pats, kws, bis, icase, calls = LANGS[name]
    parts = [f"(?P<g{i}_{c}>{rx})" for i, (c, rx) in enumerate(pats)]
    parts.append(r"(?P<id>[A-Za-z_][\w.-]*)" if name in ("nginx", "dockerfile", "make") else r"(?P<id>[A-Za-z_]\w*)")
    return re.compile("|".join(parts), re.M), kws, bis, icase, calls


COMPILED = {n: compile_lang(n) for n in LANGS}


def highlight(code, lang):
    rx, kws, bis, icase, calls = COMPILED[lang]
    out, pos = [], 0
    for m in rx.finditer(code):
        if m.start() > pos:
            out.append(html.escape(code[pos:m.start()], quote=False))
        text, cls = m.group(0), None
        if m.lastgroup == "id":
            key = text.lower() if icase else text
            if key in kws:
                cls = "kw"
            elif key in bis:
                cls = "bi"
            elif calls and code[m.end():m.end() + 1] == "(":
                cls = "fn"
        else:
            cls = m.lastgroup.split("_", 1)[1]
        esc = html.escape(text, quote=False)
        out.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
        pos = m.end()
    out.append(html.escape(code[pos:], quote=False))
    return "".join(out)


BLOCK = re.compile(r'(<span class="lang">([^<]*)</span>\s*)?(<pre class="code">)<code>(.*?)</code></pre>', re.S)
TAGS = re.compile(r"<[^>]+>")


def process(text, stats):
    def sub(m):
        lang = (m.group(2) or "").strip().lower()
        lang = ALIAS.get(lang, lang)
        if lang in SKIP or lang not in LANGS:
            stats["skipped"] += 1
            return m.group(0)
        code = html.unescape(TAGS.sub("", m.group(4)))          # plain text, whatever was there before
        new = highlight(code, lang)
        assert html.unescape(TAGS.sub("", new)) == code, "visible text changed"
        stats["coloured"] += 1
        return f'{m.group(1) or ""}{m.group(3)}<code>{new}</code></pre>'
    return BLOCK.sub(sub, text)


def main():
    stats = {"coloured": 0, "skipped": 0}
    files = 0
    for f in sorted(glob.glob(str(ROOT / "volumes/*/ch*.notes.html"))):
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        new = process(text, stats)
        if new != text:
            p.write_text(new, encoding="utf-8")
            files += 1
    print(f"files changed: {files}, blocks coloured: {stats['coloured']}, left plain: {stats['skipped']}")


if __name__ == "__main__":
    main()
