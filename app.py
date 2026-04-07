from flask import Flask, request, send_file, render_template, jsonify
from flask import redirect, url_for
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from citation import Citation

app = Flask(__name__)

# Global storage
citations = []
content = ''

# keep a running counter to assign unique citation IDs
next_cid = 1

# remember current sort settings (None means unsorted)
sort_by = None
sort_dir = 'asc'  # 'asc' or 'desc'


# ---------------- HOME ----------------
@app.route('/')
def index():
    # apply existing sort before rendering
    global citations
    if sort_by:
        citations.sort(
            key=lambda c: (getattr(c, sort_by) or "").lower(),
            reverse=(sort_dir == 'desc')
        )
    
    return render_template(
        "page.html",
        citations=citations,
        content=content,
        sort_by=sort_by,
        sort_dir=sort_dir
    )

# ---------------- LOAD FILE ----------------
@app.route('/load', methods=['POST'])
def load_file():
    global content
    global citations
    global sort_by
    global sort_dir

    file = request.files.get('file')

    if file and file.filename:

        if file.filename.lower().endswith('.txt'):

            content = file.read().decode('utf-8')

        elif file.filename.lower().endswith('.docx'):

            doc = Document(file)

            content = "\n".join(
                p.text for p in doc.paragraphs
            )

    print("File loaded")

    # apply sort so new view respects the selected order
    if sort_by:
        citations.sort(
            key=lambda c: (getattr(c, sort_by) or "").lower(),
            reverse=(sort_dir == 'desc')
        )

    # Post-Redirect-Get: redirect to index to avoid reload re-submitting the POST
    return render_template(
        "page.html",
        citations=citations,
        content=content,
        sort_by=sort_by,
        sort_dir=sort_dir
    )


# ---------------- ADD CITATION ----------------
@app.route('/add_citation', methods=['POST'])
def add_citation():

    global next_cid
    global citations
    global content
    global sort_by
    global sort_dir

    cid = next_cid
    next_cid += 1

    citation = Citation(

        cid=cid,

        author=request.form.get('citation_author'),

        year=request.form.get('citation_year'),

        source_type=request.form.get('citation_type'),

        link=request.form.get('citation_link'),

        title=request.form.get('citation_title'),

        issue=request.form.get('citation_journal'),

        publisher=request.form.get('citation_publisher'),

        volume=request.form.get('citation_volume'),

        pages=request.form.get('citation_pages'),

        doi=request.form.get('citation_doi'),

        style=request.form.get('citation_style') or 'APA7'

    )

    citations.append(citation)

    print("Citation added:", citation.author)

    # reapply sort
    if sort_by:
        citations.sort(
            key=lambda c: (getattr(c, sort_by) or "").lower(),
            reverse=(sort_dir == 'desc')
        )

    # Post-Redirect-Get: redirect to index to avoid reload re-submitting the POST
    return render_template(
        "page.html",
        citations=citations,
        content=content,
        sort_by=sort_by,
        sort_dir=sort_dir
    )


# ---------------- DELETE CITATION ----------------
@app.route('/delete_citation', methods=['POST'])
def delete_citation():

    global citations
    global content
    global sort_dir
    global sort_by
    # route should handle both form-encoded and JSON bodies
    data = request.get_json(silent=True)
    if data is None:
        # fall back to form data
        cid = request.form.get("citation_id")
    else:
        cid = data.get("citation_id")

    print("DELETE ROUTE HIT, cid =", cid)

    if cid is None:
        return jsonify({"success": False, "error": "no cid"})

    try:
        cid = int(cid)
    except ValueError:
        return jsonify({"success": False, "error": "invalid cid"})

    citation = next((c for c in citations if c.cid == cid), None)
    if citation is None:
        return jsonify({"success": False, "error": "citation not found"}), 404

    content = citation.onDeleteCitation(content)
    print("My new content:", content)
    # remove the citation
    citations = [c for c in citations if c.cid != cid]

    # renumber remaining citations so cids are contiguous starting at 1
    for i, c in enumerate(citations):
        c.cid = i + 1

    # update next_cid so new citations continue after the last current id
    global next_cid
    next_cid = len(citations) + 1

    print("Remaining citations:", len(citations))

    #return render_template("page.html",citations=citations,content=content,sort_by=sort_by,sort_dir=sort_dir)
    return jsonify({"success": True})


# ---------------- UPDATE CITATION STYLE ----------------
@app.route('/update_citation_style', methods=['POST'])
def update_citation_style():
    """Change the style of a single citation."""
    global content
    global sort_by
    global sort_dir
    global citations

    data = request.get_json()
    cid = data.get('citation_id')
    new_style = data.get('style')
    if cid is None or new_style is None:
        return jsonify({"success": False, "error": "missing parameters"}), 400
    try:
        cid = int(cid)
    except ValueError:
        return jsonify({"success": False, "error": "invalid cid"}), 400

    citation = next((c for c in citations if c.cid == cid), None)
    if citation is None:
        return jsonify({"success": False, "error": "not found"}), 404

    content = citation.onUpdateStyle(new_style,content)
    print(f"Citation {cid} style changed to {citation.style}")
    
    return jsonify({"success": True})


# ---------------- SORT CITATIONS ----------------
@app.route('/sort_citations', methods=['POST'])
def sort_citations():
    """Sort the global citations list by a specified attribute and direction."""

    global sort_by, sort_dir, content, citations

    valid_keys = ['author', 'title', 'publisher', 'pages']
    key = request.form.get('sort_by')
    direction = request.form.get('sort_dir', 'asc')
    if direction not in ['asc', 'desc']:
        direction = 'asc'

    if key not in valid_keys:
        return render_template(
            "page.html",
            citations=citations,
            content=content,
            sort_by=sort_by,
            sort_dir=sort_dir
        )

    sort_by = key
    sort_dir = direction

    citations.sort(
        key=lambda c: (getattr(c, sort_by) or "").lower(),
        reverse=(sort_dir == 'desc')
    )
    print(f"Citations sorted by {sort_by} ({sort_dir})")

    # use Post-Redirect-Get so the selected sort persists without leaving the page in a POST state
    return render_template(
        "page.html",
        citations=citations,
        content=content,
        sort_by=sort_by,
        sort_dir=sort_dir
    )



# ---------------- SAVE TEXT ----------------
@app.route('/save-data', methods=['POST'])
def save_text():

    global content

    data = request.get_json()

    content = data.get('content')

    return jsonify({"success": True})


# ---------------- INSERT CITATION ----------------
@app.route('/insert-citation', methods=['POST'])
def insert_citation():
    global citations

    data = request.get_json() or {}

    try:
        cid = int(data.get('citation_id'))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid citation_id"}), 400

    cursor = data.get('cursor')
    try:
        cursor = int(cursor) if cursor is not None else 0
    except (TypeError, ValueError):
        cursor = 0

    # locate citation by its stable cid value
    citation = next((c for c in citations if c.cid == cid), None)
    if citation is None:
        return jsonify({"error": "citation not found"}), 404
    
    for c in citations:
        c.onNewInsert(cursor)

    inline = citation.inline()  # uses citation.style by default

    print("Inline citation created:", inline)

    return jsonify({
        "citation": inline
    })


# ---------------- EXPORT ----------------
@app.route('/export', methods=['POST'])
def export():

    title = request.form.get('title')

    # doc_content = request.form.get('content')

    fmt = request.form.get('format')

    full_text = content

    # Add references (each citation has its own style)
    for i, citation in enumerate(citations):
        full_text += "\n" + citation.reference(citation.style, i)

    print("Exporting", fmt)


    # TXT
    if fmt == "txt":

        buf = io.BytesIO(
            full_text.encode()
        )

        return send_file(
            buf,
            as_attachment=True,
            download_name=title + ".txt"
        )


    # DOCX
    elif fmt == "docx":

        doc = Document()

        for line in full_text.split("\n"):

            doc.add_paragraph(line)

        buf = io.BytesIO()

        doc.save(buf)

        buf.seek(0)

        return send_file(
            buf,
            as_attachment=True,
            download_name=title + ".docx"
        )


    # PDF
    elif fmt == "pdf":

        buf = io.BytesIO()

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(buf)

        elements = []

        for line in full_text.split("\n"):

            elements.append(
                Paragraph(line, styles["Normal"])
            )

        pdf.build(elements)
 
        buf.seek(0)

        return send_file(
            buf,
            as_attachment=True,
            download_name=title + ".pdf"
        )


# ---------------- RUN ----------------
if __name__ == '__main__':

    app.run(
        port=5000,
        debug=False
    )