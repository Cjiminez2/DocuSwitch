class Citation:
    def __init__(self, cid=None, author=None, year=None, source_type=None, link=None, pages=None, volume=None, issue=None, publisher=None, doi=None, isbn=None, title=None, style='APA7'):
        self.cid = cid
        self.author = author
        self.year = year
        self.source_type = source_type
        self.link = link
        self.pages = pages
        self.volume = volume
        self.issue = issue
        self.publisher = publisher
        self.doi = doi 
        self.isbn = isbn
        self.title = title
        self.style = style.upper() if style else 'APA7'
        self.inlineCites = []

    def inline(self, style=None, number=None):
        # if no style passed use the citation's own style
        style = (style or self.style).upper()

        if style == "IEEE":
          return f"[{self.cid}]"
        elif style == "APA7":
            return f"({self.author}, {self.year})"
        elif style == "MLA8":
            return f"({self.author} {self.pages})" if self.pages else f"({self.author})"
        elif style == "CHICAGO":
            return f"({self.author} {self.year})"
        elif style == "HARVARD":
            return f"({self.author}, {self.year})"
        elif style == "VANCOUVER":
            return f"{self.cid}"
        elif style == "AMA":
            return f"{self.cid}"
        elif style == "ACS":
            return f"({self.cid})"
        elif style == "TURABIAN":
            return f"({self.author} {self.year})"
        elif style == "BLUEBOOK":
            return f"{self.cid}"
        elif style == "ASA":
            return f"({self.author} {self.year})"
        elif style == "CSE":
            return f"[{self.cid}]"
        else:
            return f"({self.author}, {self.year})"

    def reference(self, style=None, number=None):

        # choose provided style or stored style
        style = (style or self.style).upper()

        ref = ""

        if style == "IEEE":
            ref = f"[{number}] {self.author}, \"{self.title},\" {self.publisher}, {self.year}."
            if self.volume:
                ref += f", vol. {self.volume}"
            if self.issue:
                ref += f", no. {self.issue}"
            if self.pages:
                ref += f", pp. {self.pages}"
            if self.doi:
                ref += f", doi: {self.doi}"

        elif style == "APA7":
            ref = f"{self.author} ({self.year}). {self.title}. {self.publisher}"
            if self.volume:
                ref += f", {self.volume}"
            if self.issue:
                ref += f"({self.issue})"
            if self.pages:
                ref += f", {self.pages}"
            if self.doi:
                ref += f". https://doi.org/{self.doi}"

        elif style == "MLA8":
            ref = f"{self.author}. \"{self.title}.\" {self.publisher}, {self.year}."
            if self.volume:
                ref += f", vol. {self.volume}"
            if self.issue:
                ref += f", no. {self.issue}"
            ref += f", {self.year}"
            if self.pages:
                ref += f", pp. {self.pages}"
            if self.doi:
                ref += f". DOI: {self.doi}"

        elif style == "CHICAGO":
            ref = f"{self.author}. {self.year}. \"{self.title}.\" {self.publisher}"
            if self.volume:
                ref += f" {self.volume}"
            if self.issue:
                ref += f", no. {self.issue}"
            if self.pages:
                ref += f": {self.pages}"
            if self.doi:
                ref += f". https://doi.org/{self.doi}"

        elif style == "HARVARD":
            ref = f"{self.author} ({self.year}) {self.title}. {self.publisher}"
            if self.volume:
                ref += f", vol. {self.volume}"
            if self.issue:
                ref += f", no. {self.issue}"
            if self.pages:
                ref += f", pp. {self.pages}"
            if self.doi:
                ref += f", doi: {self.doi}"

        elif style == "VANCOUVER":
            ref = f"{self.author}. {self.title}. {self.publisher}. {self.year}"
            if self.volume:
                ref += f";{self.volume}"
            if self.issue:
                ref += f"({self.issue})"
            if self.pages:
                ref += f":{self.pages}"
            if self.doi:
                ref += f". doi:{self.doi}"

        elif style == "AMA":
            ref = f"{self.author}. {self.title}. {self.publisher}. {self.year}"
            if self.volume:
                ref += f";{self.volume}"
            if self.issue:
                ref += f"({self.issue})"
            if self.pages:
                ref += f":{self.pages}"
            if self.doi:
                ref += f". doi:{self.doi}"

        elif style == "ACS":
            ref = f"{self.author}. {self.title}. {self.publisher} {self.year}"
            if self.volume:
                ref += f", {self.volume}"
            if self.issue:
                ref += f" ({self.issue})"
            if self.pages:
                ref += f", {self.pages}"
            if self.doi:
                ref += f". DOI: {self.doi}"

        elif style == "TURABIAN":
            ref = f"{self.author}. {self.year}. \"{self.title}.\" {self.publisher}"
            if self.volume:
                ref += f" {self.volume}"
            if self.issue:
                ref += f", no. {self.issue}"
            if self.pages:
                ref += f": {self.pages}"

        elif style == "BLUEBOOK":
            ref = f"{self.author}, {self.title} ({self.publisher} {self.year})"
            if self.pages:
                ref += f", {self.pages}"

        elif style == "ASA":
            ref = f"{self.author}. {self.year}. \"{self.title}.\" {self.publisher}"
            if self.volume:
                ref += f" {self.volume}"
            if self.issue:
                ref += f"({self.issue})"
            if self.pages:
                ref += f":{self.pages}"

        elif style == "CSE":
            ref = f"{self.author}. {self.year}. {self.title}. {self.publisher}"
            if self.volume:
                ref += f";{self.volume}"
            if self.issue:
                ref += f"({self.issue})"
            if self.pages:
                ref += f":{self.pages}"
            if self.doi:
                ref += f". doi:{self.doi}"

        else:
            ref = f"{self.author}. {self.title}. {self.publisher}. {self.year}"

        if self.link:
            ref += f". {self.link}"

        ref += "."

        return ref
    
    def onNewInsert(self, position, append=True):
        inline_citation = self.inline(self.style)
        n = len(inline_citation)

        for i in range(len(self.inlineCites)):
            if self.inlineCites[i] >= position:
                print("Location",self.inlineCites[i],"needs shifting down.")
                self.inlineCites[i] += n
                print("New location is", self.inlineCites[i])

        if append: self.inlineCites.append(position)
        print(self.inlineCites)

    def onDeleteCitation(self, content):
        print(self,"I've been deleted!")
        inline_citation = self.inline(self.style)
        n = len(inline_citation)

        print("Removing inline citations")
        for i in range(len(self.inlineCites) - 1, -1, -1):
            before = content[:self.inlineCites[i]]
            after = content[self.inlineCites[i] + n:]
            content = before + after
        print("Content to return:",content)
        return content

    def onUpdateStyle(self, style, content):
        print(self,"My style's been updated!")

        self.inlineCites.sort()

        old_inline = self.inline(self.style)
        n = len(old_inline)

        print("Removing old inline citations")
        for i in range(len(self.inlineCites) - 1, -1, -1):
            before = content[:self.inlineCites[i]]
            after = content[self.inlineCites[i] + n:]
            print(before,after)
            content = before + after
            print("New content",content)
            for j in range(i + 1, len(self.inlineCites)):
                if self.inlineCites[j] >= self.inlineCites[i]:
                    print("Position need to be adjusted from",self.inlineCites[j],"to",self.inlineCites[j]-n)
                    self.inlineCites[j] -= n

        print(self.inlineCites)
        self.style = style.upper()
        print(self,"stlye is now",self.style)
        print("Adding new inline citations")

        new_inline = self.inline(self.style)
        newn = len(new_inline)
        for i in range(len(self.inlineCites)):
            for j in range(i + 1,len(self.inlineCites)):
                if self.inlineCites[j] >= self.inlineCites[i]:
                    print("Location",self.inlineCites[j],"needs shifting down.")
                    self.inlineCites[j] += newn
                    print("New location is", self.inlineCites[j])
            before = content[:self.inlineCites[i]]
            after = content[self.inlineCites[i]:]
            content = before + new_inline + after

        print("New content:",content)
        return content
