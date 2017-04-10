# Anpassung

Die zwei Hauptfunktionen von PlasTeX sind das Parsen und das Rendern
Beides kann nach Bedarf angepasst werden.

Siehe hierzu auch https://tiarno.github.io/plastex/plastex/plastex.pdf

## Parsen

Um PlasTeX die Regeln zum Parsen eines Latex-Befehls zu vermitteln, muss im Ordner 
plastexcustom/packages eine neue Datei angelegt werden, die den Namen des jeweiligen Latex-Pakets
hat und die Endung ".py".

Innerhalb dieser Datei wird nun für jeden Befehl bzw. jede Umgebung eine Klasse angelegt.
Beispielsweise sieht die Klasse für edtext aus dem Paket ledmac folgendermaßen aus:

```python
class edtext(Base.Command):
    """\edtext{text}{content}"""
    args = 'text content'
```

Der Klassenname entspricht dem Latex-Befehl edtext. Da es ein Befehl ist, muss die Klasse eine
Unterklasse von Base.Command sein.
Die einzige neue Information, die wir unserer neuen Klasse noch mitgeben, ist die Variable args,
die aus einem String bestehend aus zwei Wörtern besteht.
So erfährt PlasTeX, dass dieser Befehl zwei Argumente benötigt.

Wäre eines der Argumente in Latex optional, müsste es im args String in Klammern ("()" oder "[]")
gesetzt werden.

Die Namen der Argumente innerhalb des args Strings sind frei wählbar. Im schließlich geparsten
Dokument sind sie im entsprechenden Knoten des Dokumentenbaums im "attributes" Dictionary zu finden.

Die Argumente eines Knoten vom Typ edtext könnte man beispielweise per

```python
text = node.attributes["text"]
content = node.attributes["content"]
```

abrufen.


## Rendern

Beim Rendern geht es nur noch darum, in welcher Form die geparsten Informationen aus dem Latex-Dokument
dargestellt werden.

Der XML-Renderer ist zu finden unter plastexcustom/custom_renderer.py
Er rendert jeden Node aus dem von Plastex erstellten Dokumentenbaum, indem er das Attribut
"nodeName" in spitze Klammern setzt.

Hat man den Renderer mittels

```python
renderer = Renderer()
```

erzeugt, kann man nun auch Renderfunktionen für bestimmte Befehle nachträglich anpassen.
Dies geschieht, indem man in plastexcustom/main.py zuerst eine neue Renderfunktion definiert.

Diese Renderfunktion muss genau einen Parameter entgegennehmen können (nämlich einen Knoten aus dem
Plastex-Dokumentenbaum), und einen unicode-String zurückgeben.
Um bei dem edtext-Beispiel zu bleiben:

```python
def convert_edtext(node):
    """Rendert das edtext Kommando in der Form 
    <edtext><text> ... </text><app> ... </app></edtext>"""
    return u'<edtext><text>{}</text><app>{}</app></edtext>'.format(
        unicode(node.attributes["text"]), unicode(node.attributes["content"]))
```

Nun muss man nur noch dem Renderer mitteilen, dass man statt der Default-Funktion die neue Funktion
zum Rendern benutzen möchte.
Dies tut man mittels

```python
renderer["edtext"] = convert_edtext
```
