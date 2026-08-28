from pathlib import Path
import re

DIST = Path("dist")
INDEX = DIST / "index.html"
SW = DIST / "service-worker.js"

html = INDEX.read_text(encoding="utf-8")

# Version label.
html = html.replace("V1.0.2 PWA", "V1.0.3 PWA")

# UI styles: visible touch-friendly vocabulary chips.
css_marker = ".preset-row{display:flex;gap:5px;flex-wrap:wrap;margin:6px 0 0}"
css_add = """.trait-presets{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 8px}.trait-preset-chip,.trait-more,.relationship-type-chip{min-height:40px;border:1px solid #cbc7bf;background:#fff;border-radius:999px;padding:8px 14px;font-size:12px;line-height:1.2}.trait-preset-chip[aria-pressed=\"true\"],.relationship-type-chip[aria-pressed=\"true\"]{background:var(--accent2);border-color:var(--accent);font-weight:650}.trait-more{border-style:dashed;color:var(--muted)}.relationship-type-chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:7px}
"""
if css_add.strip() not in html:
    if css_marker not in html:
        raise SystemExit("CSS insertion marker not found")
    html = html.replace(css_marker, css_add + css_marker, 1)

# Static role markup: remove datalist dependency and duplicate option markup.
html = re.sub(r'\slist="trait-[^"]+"', '', html)
html = re.sub(r'<datalist id="trait-[^"]+">.*?</datalist>', '', html, flags=re.S)

# Dynamic fallback roleTemplate: make the free-text field independent of datalist.
old_trait_rows = """const opts=(PERSONALITY_VOCAB[cat]||[]).map(x=>`<option value=\"${esc(x.label)}\"></option>`).join('');
    return `<div class=\"trait-group\" data-trait-group=\"${cat}\"><div class=\"trait-title\"><span>${TRAIT_LABELS[cat]}</span><span class=\"trait-count\" data-trait-count=\"${cat}\">0</span></div><div class=\"tokens\" data-trait-tokens=\"${cat}\"></div><div class=\"trait-entry\"><input type=\"text\" data-trait-input=\"${cat}\" list=\"${dlPrefix}-${cat}\" placeholder=\"輸入後 Enter；也可自訂\"><button type=\"button\" class=\"trait-add\" data-trait-add=\"${cat}\" aria-label=\"加入\">＋</button><datalist id=\"${dlPrefix}-${cat}\">${opts}</datalist></div></div>`"""
new_trait_rows = """return `<div class=\"trait-group\" data-trait-group=\"${cat}\"><div class=\"trait-title\"><span>${TRAIT_LABELS[cat]}</span><span class=\"trait-count\" data-trait-count=\"${cat}\">0</span></div><div class=\"tokens\" data-trait-tokens=\"${cat}\"></div><div class=\"trait-entry\"><input type=\"text\" data-trait-input=\"${cat}\" placeholder=\"輸入後 Enter；也可自訂\"><button type=\"button\" class=\"trait-add\" data-trait-add=\"${cat}\" aria-label=\"加入\">＋</button></div></div>`"""
if old_trait_rows in html:
    html = html.replace(old_trait_rows, new_trait_rows, 1)
else:
    # Tolerate the already-static role markup while still forcing the fallback template clean.
    html = html.replace("const opts=(PERSONALITY_VOCAB[cat]||[]).map(x=>`<option value=\"${esc(x.label)}\"></option>`).join('');", "", 1)
    html = html.replace(' list="${dlPrefix}-${cat}"', '', 1)
    html = re.sub(r'<datalist id=\\?"\$\{dlPrefix\}-\$\{cat\}\\?">\$\{opts\}</datalist>', '', html)

# Relationship type: visible chips + free-text input, no datalist.
old_rel = '<label class="field"><span>關係類型</span><input id="relType" type="text" list="relationshipTypes" placeholder="例如：上下級、戀人、信仰／侍奉"></label>'
new_rel = '<label class="field"><span>關係類型</span><input id="relType" type="text" placeholder="例如：上下級、戀人、信仰／侍奉"><div class="relationship-type-chips" id="relationshipTypeChips"></div></label>'
if old_rel not in html:
    raise SystemExit("Relationship type input marker not found")
html = html.replace(old_rel, new_rel, 1)
html = re.sub(r'<datalist id="relationshipTypes">.*?</datalist>', '', html, flags=re.S)

# Relationship vocabulary becomes a single JS source of truth.
rel_const_marker = "const SPECIES_PRESETS = ['人類','獸人','貓人','犬人','蛇人','惡魔','精靈','外神／古神','ABO','偽娘','扶他'];"
rel_const = rel_const_marker + "\nconst RELATIONSHIP_TYPE_OPTIONS = ['戀人','曖昧','上下級','師生／師徒','信仰／侍奉','主從','宿敵','搭檔','舊識','契約關係'];"
if "const RELATIONSHIP_TYPE_OPTIONS" not in html:
    if rel_const_marker not in html:
        raise SystemExit("Relationship constant marker not found")
    html = html.replace(rel_const_marker, rel_const, 1)

# Preset renderer. setTraitState remains the single state update path.
old_set = "function setTraitState(role,cat,arr){\n  const box=$(`[data-role=\"${role}\"]`); box.dataset[`traits${cat}`]=JSON.stringify(arr); renderTraitTokens(role,cat);\n}"
new_set = "function setTraitState(role,cat,arr){\n  const box=$(`[data-role=\"${role}\"]`); box.dataset[`traits${cat}`]=JSON.stringify(arr); renderTraitTokens(role,cat); renderTraitPresetChips(role,cat);\n}"
if old_set not in html:
    raise SystemExit("setTraitState marker not found")
html = html.replace(old_set, new_set, 1)

insert_marker = "function addTrait(role,cat){\n  const input=$(`[data-role=\"${role}\"] [data-trait-input=\"${cat}\"]`), label=input.value.trim(); if(!label)return;\n  const arr=getTraitState(role,cat); if(!arr.some(x=>x.label===label)) arr.push(vocabTrait(cat,label)); setTraitState(role,cat,arr); input.value=''; onFormChange();\n}\n"
chip_functions = r'''
function renderTraitPresetChips(role,cat){
  const group=$(`[data-role="${role}"] [data-trait-group="${cat}"]`); if(!group)return;
  let box=$('.trait-presets',group); if(!box){box=document.createElement('div');box.className='trait-presets';const entry=$('.trait-entry',group);entry.before(box);}
  const vocab=PERSONALITY_VOCAB[cat]||[], selected=new Set(getTraitState(role,cat).map(x=>x.label));
  const expanded=group.dataset.presetsExpanded==='1', shown=expanded?vocab:vocab.slice(0,8);
  box.innerHTML=shown.map(x=>`<button type="button" class="trait-preset-chip" data-trait-preset="${cat}" data-label="${esc(x.label)}" aria-pressed="${selected.has(x.label)?'true':'false'}">${esc(x.label)}</button>`).join('')+
    (vocab.length>8?`<button type="button" class="trait-more" data-trait-more="${cat}">${expanded?'收合':'更多'}</button>`:'');
}
function togglePresetTrait(role,cat,label){
  const arr=getTraitState(role,cat), i=arr.findIndex(x=>x.label===label);
  if(i>=0)arr.splice(i,1);else arr.push(vocabTrait(cat,label));
  setTraitState(role,cat,arr);onFormChange();
}
function renderRelationshipTypeChips(){
  const box=$('#relationshipTypeChips');if(!box)return;const current=$('#relType').value.trim();
  box.innerHTML=RELATIONSHIP_TYPE_OPTIONS.map(label=>`<button type="button" class="relationship-type-chip" data-rel-type="${esc(label)}" aria-pressed="${current===label?'true':'false'}">${esc(label)}</button>`).join('');
}
'''
if "function renderTraitPresetChips" not in html:
    if insert_marker not in html:
        raise SystemExit("addTrait insertion marker not found")
    html = html.replace(insert_marker, insert_marker + chip_functions, 1)

# Trait click handler: preset toggles and More are handled before free-text/add/remove actions.
old_click = "const root=$(`[data-role=\"${k}\"]`);root.addEventListener('click',e=>{const add=e.target.closest('[data-trait-add]');if(add){addTrait(k,add.dataset.traitAdd);return}"
new_click = "const root=$(`[data-role=\"${k}\"]`);root.addEventListener('click',e=>{const presetTrait=e.target.closest('[data-trait-preset]');if(presetTrait){togglePresetTrait(k,presetTrait.dataset.traitPreset,presetTrait.dataset.label);return}const more=e.target.closest('[data-trait-more]');if(more){const group=more.closest('[data-trait-group]');group.dataset.presetsExpanded=group.dataset.presetsExpanded==='1'?'0':'1';renderTraitPresetChips(k,more.dataset.traitMore);return}const add=e.target.closest('[data-trait-add]');if(add){addTrait(k,add.dataset.traitAdd);return}"
if old_click not in html:
    raise SystemExit("Trait click handler marker not found")
html = html.replace(old_click, new_click, 1)

# Keep relationship chips synchronized for manual input and chip clicks.
on_change_marker = "for(const k of ['A','B'])updateRoleUI(k);updateValidation();updateCounts();refreshAssignmentLabels();"
if on_change_marker not in html:
    raise SystemExit("onFormChange marker not found")
html = html.replace(on_change_marker, on_change_marker + "renderRelationshipTypeChips();", 1)

wire_marker = "$('#swapRoles').onclick=swapRoles;"
wire_add = "$('#relationshipTypeChips').onclick=e=>{const chip=e.target.closest('[data-rel-type]');if(!chip)return;const input=$('#relType');input.value=input.value.trim()===chip.dataset.relType?'':chip.dataset.relType;onFormChange();};\n"
if wire_add not in html:
    if wire_marker not in html:
        raise SystemExit("Relationship event marker not found")
    html = html.replace(wire_marker, wire_add + wire_marker, 1)

# Ensure no datalist remains for trait / relationship vocabulary.
if re.search(r'<datalist id="trait-', html) or 'list="trait-' in html or 'id="relationshipTypes"' in html:
    raise SystemExit("Legacy datalist markup remains")

INDEX.write_text(html, encoding="utf-8")

sw = SW.read_text(encoding="utf-8")
sw = re.sub(r'adult-prompt-generator-pwa-v1-0-\d+', 'adult-prompt-generator-pwa-v1-0-3', sw, count=1)
SW.write_text(sw, encoding="utf-8")

print("Applied PWA V1.0.3 trait/relationship chip patch")
