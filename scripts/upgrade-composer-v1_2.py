from pathlib import Path
import re

P=Path('index.html')
text=P.read_text(encoding='utf-8')

text=text.replace('V1.1.0 Dictionary','V1.2.0 Composer')
text=text.replace('V1.1 Dictionary · Vanilla JS · Deterministic Compiler · Expanded Play Dictionary','V1.2 Composer · Core Elements + Functional Modifiers · Deterministic Compiler')

css_marker='.play-list{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}'
css_add='''.composer{border:1px solid #d5d1c9;background:#faf9f7;border-radius:12px;padding:12px;margin-bottom:14px}.composer-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;margin-bottom:9px}.composer-head h3{margin:0;font-size:14px}.composer-core-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}.core-chip{min-height:44px;border:1px solid #cbc7bf;background:#fff;border-radius:10px;padding:8px 9px;text-align:left}.core-chip[aria-pressed="true"]{border-color:var(--accent);background:var(--accent2);font-weight:650}.core-chip small{display:block;color:var(--muted);font-size:10.5px;font-weight:400;margin-top:2px}.composer-editor{margin-top:10px;border-top:1px dashed var(--line);padding-top:10px}.composer-editor-title{font-weight:700;margin-bottom:2px}.modifier-grid{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}.modifier-chip{min-height:40px;border:1px solid #cbc7bf;background:#fff;border-radius:999px;padding:7px 11px;font-size:12px}.modifier-chip[aria-pressed="true"]{border-color:var(--accent);background:var(--accent2);font-weight:650}.combo-list{display:flex;flex-direction:column;gap:6px;margin-top:10px}.combo-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;border:1px solid var(--line);background:#fff;border-radius:9px;padding:8px}.combo-row b{font-size:12px}.combo-row span{font-size:11px;color:var(--muted)}.composer-empty{font-size:12px;color:var(--muted);padding:7px 0}.composer-note{font-size:11px;color:var(--muted);margin-top:7px}@media(max-width:760px){.composer-core-grid{grid-template-columns:1fr 1fr}.core-chip{min-height:48px}.composer{padding:10px}}
'''
if css_add.strip() not in text:
    text=text.replace(css_marker,css_add+css_marker,1)

old='''    <div class="card-body">\n      <div class="play-toolbar"><div class="search-wrap"><input id="playSearch" type="text" placeholder="搜尋名稱、別名、英文、感受或說明"></div><label class="check-chip"><input id="supernaturalOnly" type="checkbox"><span>只看超自然玩法</span></label></div>'''
new='''    <div class="card-body">\n      <section class="composer" id="elementComposer">\n        <div class="composer-head"><div><h3>核心元素組合器</h3><div class="subtle">先選「是什麼」，再選真正會改變互動機制的功能。避免把身體位置或近義詞拆成大量無效標籤。</div></div><span class="count-badge" id="comboCount">已選 0</span></div>\n        <div class="composer-core-grid" id="coreElementGrid"></div>\n        <div class="composer-editor hidden" id="modifierEditor"><div class="composer-editor-title" id="modifierTitle"></div><div class="subtle" id="modifierDesc"></div><div class="modifier-grid" id="modifierGrid"></div><div class="composer-note">功能可以複選；沒有選 modifier 時，只會把核心元素本身交給模型。</div></div>\n        <div class="combo-list" id="comboList"></div>\n      </section>\n      <details><summary><span>其他元素辭典</span><span class="subtle">搜尋既有玩法</span></summary><div class="details-content">\n      <div class="play-toolbar"><div class="search-wrap"><input id="playSearch" type="text" placeholder="搜尋名稱、別名、英文、感受或說明"></div><label class="check-chip"><input id="supernaturalOnly" type="checkbox"><span>只看超自然玩法</span></label></div>'''
if old not in text: raise SystemExit('play card marker not found')
text=text.replace(old,new,1)
old2='''      <div class="play-tabs" id="playTabs"></div>\n      <div id="playList" class="play-list"></div>\n    </div>\n  </section>'''
new2='''      <div class="play-tabs" id="playTabs"></div>\n      <div id="playList" class="play-list"></div>\n      </div></details>\n    </div>\n  </section>'''
if old2 not in text: raise SystemExit('play list closing marker not found')
text=text.replace(old2,new2,1)

# Add composer data after category constants.
marker="const ROLE_STORE_KEY = 'adultNovelPromptGenerator.roles.v1';"
data=r'''const ELEMENT_MODIFIERS = Object.freeze({
  penetration:{label:'插入',desc:'以插入作為主要作用方式。'},
  injection:{label:'注入',desc:'帶有液體、分泌物或幻想能量的注入機制。'},
  suction:{label:'吸附／吸吮',desc:'以持續吸附或負壓方式刺激，而非單純摩擦。'},
  breast_suction:{label:'胸部吸附',desc:'以胸部整體吸附／包覆刺激為主要功能。'},
  nipple_suction:{label:'乳首吸附',desc:'集中在乳首的吸附或吸吮機制。'},
  restraint:{label:'束縛功能',desc:'此元素同時負責限制活動，而不指定綁住哪個肢體。'},
  pulse:{label:'脈動',desc:'元素本身會有規律或不規律的脈動。'},
  expansion:{label:'膨脹／變粗',desc:'尺寸或壓迫感會在使用過程中改變。'},
  secretion:{label:'分泌液',desc:'持續產生潤滑液或其他幻想分泌物。'},
  autonomous:{label:'自主活動',desc:'不需要角色逐動作直接操控，可自行活動。'},
  reactive:{label:'依反應調整',desc:'會根據對方反應改變速度、強度或模式。'},
  multiple:{label:'多條／多點',desc:'同時以多個作用點進行不同功能。'},
  light_limit:{label:'輕度限制',desc:'仍能大幅活動，只限制部分自由度。'},
  medium_limit:{label:'中度限制',desc:'主要姿勢與活動範圍受到限制，但仍可局部移動。'},
  high_limit:{label:'高度限制',desc:'只能進行很有限的自主動作。'},
  immobilized:{label:'完全無法動彈',desc:'幾乎無法自行改變姿勢或位置。'},
  pose_lock:{label:'姿勢固定',desc:'維持指定姿勢，但不額外規定綁在哪裡。'},
  dynamic_limit:{label:'動態限制',desc:'可以活動，但活動範圍被持續控制。'},
  tightening:{label:'逐步收緊',desc:'限制程度會隨場景逐步增加。'},
  gradual_release:{label:'逐步解除',desc:'限制會在互動中逐步放寬。'},
  vibration:{label:'震動',desc:'以震動作為主要刺激機制。'},
  air_pulse:{label:'氣壓脈衝',desc:'以空氣壓力／負壓脈衝刺激。'},
  thrusting:{label:'自動往復',desc:'以規律插入／退出的機械往復作為核心。'},
  multi_point:{label:'多點同步',desc:'同時對多個位置提供不同刺激。'},
  toy_operation:{label:'操控其他玩具',desc:'機械臂或裝置負責持有、移動其他器具。'},
  steady:{label:'固定節奏',desc:'維持穩定而可預期的節奏。'},
  gradual:{label:'漸進增強',desc:'速度或強度逐步提高。'},
  random:{label:'隨機節奏',desc:'節奏與強度不可預測地變化。'},
  start_stop:{label:'反覆停止／開始',desc:'在進行中反覆停止再恢復。'},
  remote_control:{label:'由另一角色控制',desc:'控制權明確交給另一角色。'},
  automatic:{label:'自動程序',desc:'依預先設定程序運作，不需持續手動操作。'},
  cannot_stop:{label:'無法自行停止',desc:'被作用的一方不能直接關閉或解除。'},
  long_duration:{label:'長時間運作',desc:'以持續運作和累積反應為重點。'}
});
const CORE_ELEMENTS = Object.freeze([
  {id:'tentacles',label:'觸手',desc:'非人肢體；功能差異比綁在哪裡更重要。',mods:['penetration','injection','suction','breast_suction','nipple_suction','restraint','pulse','expansion','secretion','autonomous','reactive','multiple']},
  {id:'bondage',label:'束縛',desc:'用限制程度描述自由度，不指定肢體位置。',mods:['light_limit','medium_limit','high_limit','immobilized','pose_lock','dynamic_limit','tightening','gradual_release']},
  {id:'bullet_vibrator_core',label:'跳蛋／小型震動器',desc:'小型、可固定或遙控的震動器具。',mods:['vibration','steady','gradual','random','start_stop','remote_control','cannot_stop','long_duration']},
  {id:'air_pulse_core',label:'吸吮器／氣壓刺激器',desc:'以負壓或氣壓脈衝造成不同於震動的刺激。',mods:['air_pulse','steady','gradual','random','start_stop','remote_control','long_duration']},
  {id:'strap_on_core',label:'Strap-on',desc:'穿戴式插入器具；適合女女或不依賴原生器官的插入互動。',mods:['penetration','steady','gradual']},
  {id:'fuck_machine',label:'炮機',desc:'固定式自動往復插入裝置，核心是機械節奏與控制權。',mods:['thrusting','steady','gradual','random','start_stop','remote_control','automatic','cannot_stop','long_duration']},
  {id:'octopus_chair',label:'八爪椅',desc:'多支機械臂／器具圍繞座位工作，適合多點刺激與限制。',mods:['multi_point','restraint','pose_lock','vibration','penetration','suction','toy_operation','remote_control','automatic','reactive']},
  {id:'mechanical_arms',label:'機械臂',desc:'以一支或多支機械臂負責固定、操作器具或多點互動。',mods:['restraint','pose_lock','toy_operation','multi_point','remote_control','automatic','reactive']},
  {id:'insertable_toy_core',label:'插入式玩具',desc:'以插入本身為核心的泛用器具。',mods:['penetration','vibration','pulse','expansion','remote_control','long_duration']},
  {id:'remote_toy_core',label:'遙控玩具',desc:'重點在操作權與身體作用點分離。',mods:['vibration','air_pulse','random','start_stop','remote_control','cannot_stop','long_duration']},
  {id:'slime_core',label:'史萊姆／液態體',desc:'以包覆、變形與流動身體作為互動機制。',mods:['restraint','suction','penetration','secretion','autonomous','reactive','multiple']},
  {id:'magic_restraint_core',label:'魔法拘束',desc:'以超自然力量限制自由度，不需要實體綁具。',mods:['light_limit','medium_limit','high_limit','immobilized','pose_lock','dynamic_limit','tightening','gradual_release']}
]);
let selectedCombos = new Map();
let activeCoreElement = null;
'''
if 'const CORE_ELEMENTS' not in text:
    text=text.replace(marker,data+marker,1)

# compileStory: add combo output after normal play block.
marker_story="""  if (playSelections.length) {\n    if (lines.length > 1) lines.push('');\n    lines.push('本篇希望自然融入的元素（依故事需要取用，不必全部出現，也不需依序）：');\n    lines.push(...playSelections.map(({ item }) => item.label));\n    const note = compileDirectionNote(playSelections, input);\n    if (note) {\n      lines.push('');\n      lines.push(note);\n    }\n  }\n"""
insert_story=marker_story+"""\n  if ((input?.elementCombos || []).length) {\n    if (lines.length > 1) lines.push('');\n    lines.push('核心成人元素與功能：');\n    for (const combo of input.elementCombos) {\n      const suffix=(combo.modifierLabels||[]).length ? `：${combo.modifierLabels.join('、')}` : '';\n      lines.push(`${combo.label}${suffix}`);\n    }\n  }\n"""
if '核心成人元素與功能：' not in text:
    if marker_story not in text: raise SystemExit('compileStory marker not found')
    text=text.replace(marker_story,insert_story,1)

# minimum validation includes composer selections
text=text.replace("(input?.plays || []).length ||\n    cleanString(input?.scene?.opening)","(input?.plays || []).length ||\n    (input?.elementCombos || []).length ||\n    cleanString(input?.scene?.opening)",1)

# Insert composer rendering before assignmentOptions.
marker_fn='function assignmentOptions(item){'
composer_fn=r'''function getCombo(coreId){return selectedCombos.get(coreId)||new Set();}
function renderCoreElements(){
  const box=$('#coreElementGrid'); if(!box)return;
  box.innerHTML=CORE_ELEMENTS.map(core=>`<button type="button" class="core-chip" data-core-element="${core.id}" aria-pressed="${selectedCombos.has(core.id)?'true':'false'}"><b>${esc(core.label)}</b><small>${esc(core.desc)}</small></button>`).join('');
  $('#comboCount').textContent=`已選 ${selectedCombos.size}`;
  renderComboList();
}
function renderModifierEditor(){
  const editor=$('#modifierEditor'); if(!activeCoreElement){editor.classList.add('hidden');return}
  const core=CORE_ELEMENTS.find(x=>x.id===activeCoreElement); if(!core){editor.classList.add('hidden');return}
  editor.classList.remove('hidden'); $('#modifierTitle').textContent=`${core.label}：功能選擇`; $('#modifierDesc').textContent=core.desc;
  const selected=getCombo(core.id);
  $('#modifierGrid').innerHTML=core.mods.map(id=>{const m=ELEMENT_MODIFIERS[id];return `<button type="button" class="modifier-chip" data-modifier="${id}" aria-pressed="${selected.has(id)?'true':'false'}" title="${esc(m.desc)}">${esc(m.label)}</button>`}).join('');
}
function renderComboList(){
  const box=$('#comboList'); if(!selectedCombos.size){box.innerHTML='<div class="composer-empty">尚未加入核心元素。</div>';return}
  box.innerHTML=[...selectedCombos.entries()].map(([id,mods])=>{const core=CORE_ELEMENTS.find(x=>x.id===id);const labels=[...mods].map(m=>ELEMENT_MODIFIERS[m]?.label).filter(Boolean);return `<div class="combo-row"><div><b>${esc(core?.label||id)}</b><br><span>${labels.length?esc(labels.join('、')):'未指定功能，由模型自然處理'}</span></div><button type="button" class="btn small danger" data-remove-core="${id}">移除</button></div>`}).join('');
}
function toggleCoreElement(id){
  if(selectedCombos.has(id)){activeCoreElement=id}else{selectedCombos.set(id,new Set());activeCoreElement=id}
  renderCoreElements();renderModifierEditor();onFormChange();
}
function toggleModifier(id){
  if(!activeCoreElement)return;const set=getCombo(activeCoreElement);if(set.has(id))set.delete(id);else set.add(id);selectedCombos.set(activeCoreElement,set);renderCoreElements();renderModifierEditor();onFormChange();
}
function readElementCombos(){
  return [...selectedCombos.entries()].map(([id,mods])=>{const core=CORE_ELEMENTS.find(x=>x.id===id);return {id,label:core?.label||id,modifierIds:[...mods],modifierLabels:[...mods].map(m=>ELEMENT_MODIFIERS[m]?.label).filter(Boolean)}});
}

'''
if 'function renderCoreElements()' not in text:
    text=text.replace(marker_fn,composer_fn+marker_fn,1)

# readInput add elementCombos
old_read="return {task:{lengthId:$('input[name=\"length\"]:checked')?.value||null,contentOrientationId:$('input[name=\"orientation\"]:checked')?.value||null},characters:{A:readRole('A'),B:readRole('B')},relationship:"
new_read="return {task:{lengthId:$('input[name=\"length\"]:checked')?.value||null,contentOrientationId:$('input[name=\"orientation\"]:checked')?.value||null},characters:{A:readRole('A'),B:readRole('B')},elementCombos:readElementCombos(),relationship:"
if old_read not in text: raise SystemExit('readInput marker not found')
text=text.replace(old_read,new_read,1)

# clear story resets composer
old_clear="selectedPlays.clear();$('#playSearch').value='';"
new_clear="selectedPlays.clear();selectedCombos.clear();activeCoreElement=null;renderCoreElements();renderModifierEditor();$('#playSearch').value='';"
text=text.replace(old_clear,new_clear,1)

# Wire composer before playTabs wiring
wire="$('#playTabs').onclick=e=>{const t=e.target.closest('[data-tab]');if(t){currentPlayTab=t.dataset.tab;renderPlays()}};"
wire_new="""$('#elementComposer').onclick=e=>{const core=e.target.closest('[data-core-element]');if(core){toggleCoreElement(core.dataset.coreElement);return}const mod=e.target.closest('[data-modifier]');if(mod){toggleModifier(mod.dataset.modifier);return}const rem=e.target.closest('[data-remove-core]');if(rem){selectedCombos.delete(rem.dataset.removeCore);if(activeCoreElement===rem.dataset.removeCore)activeCoreElement=null;renderCoreElements();renderModifierEditor();onFormChange();return}};\n"""+wire
if "$('#elementComposer').onclick" not in text:
    text=text.replace(wire,wire_new,1)

# initialization
init="refreshRoleLibrarySelects();for(const k of ['A','B'])for(const cat of [...GENERAL_TRAITS,...INTIMATE_TRAITS])setTraitState(k,cat,[]);onFormChange();"
init_new="renderCoreElements();renderModifierEditor();"+init
if 'renderCoreElements();renderModifierEditor();refreshRoleLibrarySelects()' not in text:
    text=text.replace(init,init_new,1)

# bump cache via service worker separately
P.write_text(text,encoding='utf-8')
print('Applied V1.2 composer upgrade')