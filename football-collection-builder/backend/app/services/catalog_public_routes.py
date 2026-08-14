from __future__ import annotations

def public_item_route(country_slug:str,team_slug:str,item_slug:str,collection_slug:str|None=None)->str:
    if collection_slug:
        return f"/items/{country_slug}/teams/{team_slug}/collections/{collection_slug}/{item_slug}"
    return f"/items/{country_slug}/teams/{team_slug}/items/{item_slug}"

def item_breadcrumbs(country_slug:str,country_name:str,team_slug:str,team_name:str,item_slug:str,item_title:str,collection_slug:str|None=None,collection_name:str|None=None):
    crumbs=[{'type':'country','slug':country_slug,'label':country_name},{'type':'team','slug':team_slug,'label':team_name}]
    if collection_slug:crumbs.append({'type':'collection','slug':collection_slug,'label':collection_name or collection_slug})
    crumbs.append({'type':'item','slug':item_slug,'label':item_title})
    return crumbs
