# NetworkSecurity
## Gruppennamen
- Samuel Amoah
- Yichen Zhang
- Pascal Weider
- Benedikt Gebauer
## Gewählte Anriffsmethode
Für die Erfüllung der Aufgabe wurde die Extraktion der Daten über DNS Requests gewählt
## Technische Beschreibung der Gegenmaßnahmen
![Ablauf der Extraktion](networksecurity.drawio.png)
### Phase 1 (grün)
In der ersten Phase schickt der Client eine DNS Anfrage an den Server mit dem qname: {filename}.com, der Client gibt dadurch an, für welche Datei er Informationen erhalten möchte. Um die Antwort zu generieren liest der Server die gewünschte Datei ein und codiert den Text in Base64. Die codierten Daten werden vom Server in 32 Zeichen große Fragment unterteilt. Das ist notwendig, da die größe eines DNS qnames begrenzt ist. Als Antwort schickt der Server eine DNS Antwort mit der Anzahl an Fragmenten die er zuvor unterteilt hat. Die Antwort besitzt daher folgenden qname: {fragmentcount}.com.
### Phase 2 (gelb) 
Die zweite Phase repräsentiert die eigentliche Datenübertragung. Dafür schickt der Client in jeder Itteration eine Anfrage mit dem qname: {current fragment count}.{filename}.com. Durch den filename wird angegeben welche Datei der Client haben möchte. Der current fragment count gibt an welches Fragment der Datei, der Client haben möchte. Als Antwort schickt der Server eine DNS Antwort mit dem qname: {data}.com. In Data wird der base64 codierten Text übertragen. 
Der Client ist dadurch in der Lage nach und nach alle Fragment des Textes anzufragen und zu empfangen. 
### Phase 3 (rot)
Die dritte Phase dient als Fehlerüberprüfung des vorherigen Datenaustausches. Dafür wird serverseitig ein Hash von dem base64 codierten Text generiert. Der Client geniert sich ebenfalls einen Hash der empfangenen Daten. Um den serverseitig generierten Hash abzufragen schickt der Client eine Anfrage mit dem qname: {fragmentcount+1}.com an den Server. Anschließend antwortet der Server mit einer DNS Antwort mit dem qname: {hash}.com. Der Client vergleicht den empfangenen und den selber genierten Hash. Dadurch kann festgestellt werden, ob bei der Datenübertragung ein Fehler aufgetreten ist. 
## Gewähltes Codierungsverfahren
Als Codierungsverfahren für die Daten wurde die Base64 Codierung gewählt. Die Base64-Codierung ist ein Verfahren zur Darstellung von Binärdaten in einem Textformat, das ausschließlich aus ASCII-Zeichen besteht. Es wird häufig verwendet, um Binärdaten wie Bilder, Audiodateien oder andere nicht-textbasierte Daten in Textformaten wie JSON oder XML zu übertragen, die normalerweise nur Text unterstützen.

Bei der Base64-Codierung werden 3 Byte (24 Bit) Binärdaten in eine Gruppe von 4 ASCII-Zeichen umgewandelt. Jedes ASCII-Zeichen repräsentiert dabei 6 Bits der ursprünglichen Daten. Falls die Länge der Eingabedaten nicht durch 3 teilbar ist, werden am Ende des Datenstroms Nullbytes hinzugefügt, und das letzte Zeichen in der Codierung wird mit dem '=' Zeichen aufgefüllt.
## Empfohlene Gegenmaßnahmen
### Betrachten von DNS Requests
Eine empfohlene Gegenmaßnahme ist das Analysieren der über das Netzwerk laufenden DNS Anfragen. Die von uns gewählte Angriffsmethode überträgt die Daten durch das Ersetzen des qnames einer DNS Anfrage. Es ist daher eine Möglichkeit die qnames von DNS Request auf ungewöhnliche oder verdächtige Muster in aufeinander Folgenden DNS Anfragen zu achten. Des Weiteren besitzen die von uns übertragenen qnames in der Regel die maximale Länge eines qnames, diese Verhalten ist untypisch für einen normalen DNS Traffic und kann daher als auffällig erkannt werden.

### Traffic Analysis
Die Überwachung der Anzahl von DNS-Anfragen an bestimmte Domainnamen kann eine Methode sein, um DNS-Tunneling-Aktivitäten zu erkennen. Wenn ein ungewöhnlich hoher Anstieg von DNS-Anfragen auf eine einzelne Domain auftritt, könnte dies auf mögliche Daten Extraktionen über Versuche hinweisen.

### Limitierung von DNS Requests
Eine mögliche Gegenmaßnahme ist das Limitieren von DNS Requests, bzw. Erkennen von einer hohen Anzahl an DNS Requests die gleichzeitig gesendet werden. Diese Gegenmaßnahme ist insbesondere effektiv, wenn eine große Menge an Daten über DNS Requests extrahiert wird. Durch das Erkennnen und ggf. Begrenzen von DNS Anfragen wird die Extraktion verlangsamt.

### Whitelisting von vertrauenswürdigen DNS Servern
In einem Netzwerk ist es sinnvoll eine Whitelist für vertrauenswürdige DNS Server anzulegen. In unserem Szenario würde der von uns entwickelte Server logischerweise nicht auf der Whitelist stehen. Dadurch können DNS Antworten die von und DNS Anfragen die an diesen Server gesendet werden als verdächtig eingestuft und geblockt werden.

### Einsatz von DNSSEC(DNS Security Extension)
DNSSEC (Domain Name System Security Extensions) ist eine Sicherheitstechnologie, die entwickelt wurde, um die Integrität und Authentizität von DNS-Daten zu gewährleisten. Durch die Verwendung digitaler Signaturen ermöglicht DNSSEC die Überprüfung der Echtheit von DNS-Antworten. In einem Netzwerk könnten anschließend alle DNS Antworten auf Integrität und Authentizität überprüft werden. Sobald eine DNS Antwort diese Anforderung nicht erfüllt, wäre das ein Indiz für die Extraktion von Daten über DNS. Anschließend könnten solche Anfragen geblockt werden.
 

