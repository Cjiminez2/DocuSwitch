class Citation:
    def __init__(self, cid=None, author=None, year=None, source_type=None,
                 link=None, pages=None, volume=None, issue=None,
                 publisher=None, doi=None, isbn=None, title=None, style='APA7'):
        self.cid        = cid
        self.author     = author
        self.year       = year
        self.source_type = source_type
        self.link       = link
        self.pages      = pages
        self.volume     = volume
        self.issue      = issue
        self.publisher  = publisher
        self.doi        = doi
        self.isbn       = isbn
        self.title      = title
        self.style      = style.upper() if style else 'APA7'
        self.inlineCites = []

    # ── helpers ───────────────────────────────────────────────────────────────

    def _a(self):   return self.author    or ''
    def _t(self):   return self.title     or ''
    def _p(self):   return self.publisher or ''
    def _y(self):   return self.year      or ''
    def _pg(self):  return self.pages     or ''
    def _v(self):   return self.volume    or ''
    def _i(self):   return self.issue     or ''
    def _doi(self): return self.doi       or ''

    # ── inline citation ───────────────────────────────────────────────────────

    def inline(self, style=None, number=None):
        style = (style or self.style).upper()
        a, y, pg = self._a(), self._y(), self._pg()
        n = self.cid if number is None else number

        if style == 'APA7':
            return f'({a}, {y})'
        elif style == 'MLA8':
            return f'({a} {pg})' if pg else f'({a})'
        elif style == 'CHICAGO':
            # Chicago author-date
            return f'({a} {y})'
        elif style == 'CHICAGO_NOTES':
            return f'{n}'          # footnote number
        elif style == 'HARVARD':
            return f'({a}, {y})'
        elif style == 'IEEE':
            return f'[{n}]'
        elif style == 'VANCOUVER':
            return f'({n})'        # superscript in text; shown as (n) here
        elif style == 'AMA':
            return f'{n}'          # superscript number
        elif style == 'ACS':
            return f'{n}'          # superscript number
        elif style == 'TURABIAN':
            return f'({a}, {y})'
        elif style == 'BLUEBOOK':
            return f'{n}'
        elif style == 'ASA':
            return f'({a} {y})'
        elif style == 'CSE':
            return f'[{n}]'        # citation-sequence system
        elif style == 'OXFORD':
            return f'{n}'          # footnote number
        elif style == 'APSA':
            return f'({a} {y})'
        elif style == 'AAA':
            return f'({a} {y}:{pg})' if pg else f'({a} {y})'
        elif style == 'ABNT':
            return f'({a.upper()}, {y})'
        elif style == 'NLM':
            return f'[{n}]'
        elif style == 'OSCOLA':
            return f'{n}'          # footnote number
        else:
            return f'({a}, {y})'

    # ── full reference entry ──────────────────────────────────────────────────

    def reference(self, style=None, number=None):
        style = (style or self.style).upper()
        a, t, p, y = self._a(), self._t(), self._p(), self._y()
        v, i, pg, doi = self._v(), self._i(), self._pg(), self._doi()
        n = self.cid if number is None else number
        ref = ''

        # ── APA 7th edition ──────────────────────────────────────────────────
        # Author, A. A. (Year). Title of article. Journal Name, volume(issue), pages.
        # https://doi.org/xxxxx
        if style == 'APA7':
            ref = f'{a} ({y}). {t}.'
            if p:
                ref += f' {p}'
                if v:
                    ref += f', {v}'
                    if i:
                        ref += f'({i})'
                if pg:
                    ref += f', {pg}'
            if doi:
                ref += f'. https://doi.org/{doi}'

        # ── MLA 8th/9th edition ──────────────────────────────────────────────
        # Author. "Title." Publisher/Journal, vol. V, no. I, Year, pp. P.
        elif style == 'MLA8':
            ref = f'{a}. "{t}." {p}'
            if v:
                ref += f', vol. {v}'
            if i:
                ref += f', no. {i}'
            ref += f', {y}'
            if pg:
                ref += f', pp. {pg}'
            if doi:
                ref += f'. DOI: {doi}'

        # ── Chicago Author-Date ───────────────────────────────────────────────
        # Author. Year. "Title." Publisher volume (issue): pages. doi.
        elif style == 'CHICAGO':
            ref = f'{a}. {y}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f' ({i})'
            if pg:
                ref += f': {pg}'
            if doi:
                ref += f'. https://doi.org/{doi}'

        # ── Chicago Notes-Bibliography ────────────────────────────────────────
        # Similar to author-date but used with footnotes
        elif style == 'CHICAGO_NOTES':
            ref = f'{a}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f', no. {i}'
            if y:
                ref += f' ({y})'
            if pg:
                ref += f': {pg}'
            if doi:
                ref += f'. https://doi.org/{doi}'

        # ── Harvard ──────────────────────────────────────────────────────────
        # Author (Year) Title. Publisher, vol. V, no. I, pp. P.
        elif style == 'HARVARD':
            ref = f'{a} ({y}) "{t}." {p}'
            if v:
                ref += f', vol. {v}'
            if i:
                ref += f', no. {i}'
            if pg:
                ref += f', pp. {pg}'
            if doi:
                ref += f'. doi: {doi}'

        # ── IEEE ─────────────────────────────────────────────────────────────
        # [N] A. Author, "Title," Journal, vol. V, no. I, pp. P, Year. doi: D.
        elif style == 'IEEE':
            ref = f'[{n}] {a}, "{t}," {p}'
            if v:
                ref += f', vol. {v}'
            if i:
                ref += f', no. {i}'
            if pg:
                ref += f', pp. {pg}'
            if y:
                ref += f', {y}'
            if doi:
                ref += f'. doi: {doi}'

        # ── Vancouver ────────────────────────────────────────────────────────
        # N. Author. Title. Publisher. Year;V(I):P. doi:D
        elif style == 'VANCOUVER':
            ref = f'{n}. {a}. {t}. {p}. {y}'
            if v:
                ref += f';{v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. doi:{doi}'

        # ── AMA (American Medical Association) ───────────────────────────────
        # N. Author. Title. Abbrev Journal. Year;V(I):P. doi:D
        elif style == 'AMA':
            ref = f'{n}. {a}. {t}. {p}. {y}'
            if v:
                ref += f';{v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. doi:{doi}'

        # ── ACS (American Chemical Society) ──────────────────────────────────
        # Author. Title. Journal Year, V (I), P. DOI: D.
        elif style == 'ACS':
            ref = f'{a}. {t}. {p} {y}'
            if v:
                ref += f', {v}'
            if i:
                ref += f' ({i})'
            if pg:
                ref += f', {pg}'
            if doi:
                ref += f'. DOI: {doi}'

        # ── Turabian ─────────────────────────────────────────────────────────
        # Very close to Chicago author-date; used in student papers
        # Author. Year. "Title." Publisher V, no. I: P. doi.
        elif style == 'TURABIAN':
            ref = f'{a}. {y}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f', no. {i}'
            if pg:
                ref += f': {pg}'
            if doi:
                ref += f'. https://doi.org/{doi}'

        # ── Bluebook (legal) ─────────────────────────────────────────────────
        # Author, Title, V PUB. P (Year).
        elif style == 'BLUEBOOK':
            ref = f'{a}, {t}'
            if v:
                ref += f', {v}'
            ref += f' {p}'
            if pg:
                ref += f' {pg}'
            ref += f' ({y})'

        # ── ASA (American Sociological Association) ───────────────────────────
        # Author. Year. "Title." Publisher V(I):P.
        elif style == 'ASA':
            ref = f'{a}. {y}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. https://doi.org/{doi}'

        # ── CSE (Council of Science Editors, citation-sequence) ──────────────
        # N. Author. Title. Publisher. Year;V(I):P. doi:D.
        elif style == 'CSE':
            ref = f'{n}. {a}. {t}. {p}. {y}'
            if v:
                ref += f';{v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. doi:{doi}'

        # ── Oxford ───────────────────────────────────────────────────────────
        # Footnote: N Author, 'Title', Publisher, Year, pp. P.
        elif style == 'OXFORD':
            ref = f'{n} {a}, \'{t}\', {p}, {y}'
            if pg:
                ref += f', pp. {pg}'
            if doi:
                ref += f'. DOI: {doi}'

        # ── APSA (American Political Science Association) ─────────────────────
        # Author. Year. "Title." Publisher V(I): P.
        elif style == 'APSA':
            ref = f'{a}. {y}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f': {pg}'
            if doi:
                ref += f'. doi:{doi}'

        # ── AAA (American Anthropological Association) ────────────────────────
        # Author. Year. "Title." Publisher V(I):P.
        elif style == 'AAA':
            ref = f'{a}. {y}. "{t}." {p}'
            if v:
                ref += f' {v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. DOI: {doi}'

        # ── ABNT (Brazilian — NBR 6023) ───────────────────────────────────────
        # AUTHOR. Title. Publisher, Year. V. I. p. P.
        elif style == 'ABNT':
            ref = f'{a.upper()}. {t}. {p}, {y}'
            if v:
                ref += f'. v. {v}'
            if i:
                ref += f'. n. {i}'
            if pg:
                ref += f'. p. {pg}'
            if doi:
                ref += f'. DOI: {doi}'

        # ── NLM (National Library of Medicine / PubMed) ───────────────────────
        # Author. Title. Publisher. Year Vol(Issue):Pages. doi:D. PMID: ...
        elif style == 'NLM':
            ref = f'{a}. {t}. {p}. {y}'
            if v:
                ref += f' {v}'
            if i:
                ref += f'({i})'
            if pg:
                ref += f':{pg}'
            if doi:
                ref += f'. doi:{doi}'

        # ── OSCOLA (Oxford legal, UK) ─────────────────────────────────────────
        # N Author, 'Title' (Publisher Year) pages.
        elif style == 'OSCOLA':
            ref = f'{n} {a}, \'{t}\' ({p} {y})'
            if pg:
                ref += f' {pg}'
            if doi:
                ref += f' <https://doi.org/{doi}>'

        else:
            ref = f'{a}. {t}. {p}. {y}'

        # Append URL if present (all styles)
        if self.link:
            ref += f'. Available at: {self.link}'

        # Collapse any double-periods that arise when fields already end with '.'
        import re as _re
        ref = _re.sub(r'[.]{2,}', '.', ref)
        # Ensure single trailing period
        ref = ref.rstrip('.') + '.'

        return ref

    # ── position tracking (unchanged) ────────────────────────────────────────

    def onNewInsert(self, position, append=True):
        inline_citation = self.inline(self.style)
        n = len(inline_citation)
        for i in range(len(self.inlineCites)):
            if self.inlineCites[i] >= position:
                self.inlineCites[i] += n
        if append:
            self.inlineCites.append(position)

    def onDeleteCitation(self, content):
        inline_citation = self.inline(self.style)
        n = len(inline_citation)
        for i in range(len(self.inlineCites) - 1, -1, -1):
            before = content[:self.inlineCites[i]]
            after  = content[self.inlineCites[i] + n:]
            content = before + after
        return content

    def onUpdateStyle(self, style, content):
        self.inlineCites.sort()
        old_inline = self.inline(self.style)
        n = len(old_inline)
        for i in range(len(self.inlineCites) - 1, -1, -1):
            before = content[:self.inlineCites[i]]
            after  = content[self.inlineCites[i] + n:]
            content = before + after
            for j in range(i + 1, len(self.inlineCites)):
                if self.inlineCites[j] >= self.inlineCites[i]:
                    self.inlineCites[j] -= n
        self.style = style.upper()
        new_inline = self.inline(self.style)
        newn = len(new_inline)
        for i in range(len(self.inlineCites)):
            for j in range(i + 1, len(self.inlineCites)):
                if self.inlineCites[j] >= self.inlineCites[i]:
                    self.inlineCites[j] += newn
            before = content[:self.inlineCites[i]]
            after  = content[self.inlineCites[i]:]
            content = before + new_inline + after
        return content
