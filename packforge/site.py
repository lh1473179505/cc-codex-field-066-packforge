from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse, parse_qs

# 12 items, prices in cents
ITEMS = [
    ("SKU-A01", "Amber Vase", 1230),
    ("SKU-B02", "Brass Hook", 880),
    ("SKU-C03", "Clay Bowl", 450),
    ("SKU-D04", "Desk Tray", 2100),
    ("SKU-E05", "Elm Frame", 1675),
    ("SKU-F06", "Felt Mat", 300),
    ("SKU-G07", "Glass Jar", 990),
    ("SKU-H08", "Hemp Bag", 1540),
    ("SKU-I09", "Ink Stone", 3200),
    ("SKU-J10", "Jade Box", 5400),
    ("SKU-K11", "Knife Set", 2890),
    ("SKU-L12", "Linen Cloth", 760),
]
STATE = {"skin": "v2"}

def list_html_v1(page: int):
    per=4
    chunk=ITEMS[(page-1)*per:page*per]
    cards=[]
    for sku,title,price in chunk:
        cards.append(f'<div class="item"><span class="name">{title}</span><a href="/item/{sku}">{title}</a><span class="price">{price}</span></div>')
    nav=""
    if page*per < len(ITEMS):
        nav=f'<a class="next" href="/?page={page+1}">next</a>'
    return f"<!doctype html><html><body>{''.join(cards)}{nav}</body></html>"

def list_html_v2(page: int):
    per=4
    chunk=ITEMS[(page-1)*per:page*per]
    cards=[]
    for i,(sku,title,price) in enumerate(chunk):
        # alternate title location: even -> span.nm, odd -> only b
        if i%2==0:
            name=f'<span class="nm">{title}</span>'
        else:
            name=f"<b>{title}</b>"
        cards.append(f'<div class="product-row">{name}<a href="/item/{sku}">{sku}</a></div>')
    nav=""
    if page*per < len(ITEMS):
        nav=f'<a rel="next" href="/?page={page+1}">more</a>'
    return f"<!doctype html><html><body>{''.join(cards)}{nav}</body></html>"

def detail_v1(sku,title,price):
    return f'<!doctype html><html><body><span class="sku">{sku}</span><span class="price">{price}</span><h1>{title}</h1></body></html>'

def detail_v2(sku,title,price):
    # sku sometimes only in text; price sometimes only data-price
    if sku.endswith(("01","03","05","07","09","11")):
        sku_html=f'<span class="code">{sku}</span>'
    else:
        sku_html=f"<p>Catalog number SKU-{sku.split('-',1)[1]} is printed on the box. Wait, official id is {sku}.</p>"
        # regex SKU-([A-Z0-9-]+) would capture A01 from "SKU-A01" if we write it plainly
        sku_html=f"<p>Official code is {sku} on the label.</p>"
    if sku.endswith(("02","04","06","08","10","12")):
        price_html=f'<span data-price="{price}"></span>'
    else:
        price_html=f'<span class="amt">{price}</span>'
    return f"<!doctype html><html><body><h1>{title}</h1>{sku_html}{price_html}</body></html>"

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*a):
        return
    def _send(self,st,body):
        body=body.encode() if isinstance(body,str) else body
        self.send_response(st)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        parsed=urlparse(self.path)
        path=unquote(parsed.path)
        qs=parse_qs(parsed.query)
        skin=STATE["skin"]
        if path=="/":
            page=int(qs.get("page",["1"])[0])
            html=list_html_v1(page) if skin=="v1" else list_html_v2(page)
            return self._send(200,html)
        if path.startswith("/item/"):
            sku=path.split("/")[-1]
            it=next((x for x in ITEMS if x[0]==sku), None)
            if not it:
                return self._send(404,"no")
            sku,title,price=it
            html=detail_v1(sku,title,price) if skin=="v1" else detail_v2(sku,title,price)
            return self._send(200,html)
        return self._send(404,"no")

def serve(host="127.0.0.1", port=8766, skin="v2"):
    STATE["skin"]=skin
    httpd=ThreadingHTTPServer((host,port), Handler)
    print(f"packforge fixture site on http://{host}:{port} skin={skin}")
    httpd.serve_forever()
