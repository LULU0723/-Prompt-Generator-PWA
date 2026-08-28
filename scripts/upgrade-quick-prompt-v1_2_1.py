from pathlib import Path
import re

P = Path('index.html')
text = P.read_text(encoding='utf-8')

assert 'V1.2.0 Composer' in text
assert 'function readElementCombos()' in text
assert 'function compilePrompt(input, masterItems)' in text

text = text.replace('V1.2.0 Composer', 'V1.2.1 Quick Prompt')
text = text.replace('V1.2 Composer · Core Elements + Functional Modifiers · Deterministic Compiler', 'V1.2.1 Quick Prompt · Full + Quick Compilers · Core Element Composer')

# Mode-switch UI styles and quick-mode visibility.
css = r'''
.mode-switcher{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;gap:10px;box-shadow:var(--shadow)}
.mode-switcher-copy{min-width:0}.mode-switcher-copy b{display:block;font-size:13px}.mode-switcher-copy span{display:block;color:var(--muted);font-size:11px;margin-top:2px}.mode-buttons{display:flex;gap:6px;flex-shrink:0}.mode-btn{min-height:40px;border:1px solid #cbc7bf;background:#fff;border-radius:999px;padding:7px 12px;font-size:12px}.mode-btn[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:650}
.quick-mode #roleSection,.quick-mode #relationshipSection{display:none}.quick-mode .full-only{display:none!important}.quick-mode #loadExample{display:none}.quick-mode #roleStorageNotice{display:none}.quick-mode #quickCopyPrompt{display:none}
@media(max-width:760px){.mode-switcher{align-items:stretch;flex-direction:column}.mode-buttons{display:grid;grid-template-columns:1fr 1fr}.mode-btn{width:100%}}
'''
text = text.replace('</style>', css + '\n</style>', 1)

# Page-level mode switch.
marker = '  <section class="card" id="roleSection">'
mode_ui = '''  <section class="mode-switcher" id="generatorModeSwitcher">
    <div class="mode-switcher-copy"><b>輸出模式</b><span id="modeHelp">完整模式會使用角色、關係與場景；玩法速貼只輸出成人元素、節奏與補充。</span></div>
    <div class="mode-buttons"><button type="button" class="mode-btn" data-generator-mode="full" aria-pressed="true">完整模式</button><button type="button" class="mode-btn" data-generator-mode="quick" aria-pressed="false">玩法速貼</button></div>
  </section>
'''
assert marker in text
text = text.replace(marker, mode_ui + marker, 1)

# Identify major sections and make story-only controls hideable.
text = text.replace('<section class="card">\n    <div class="card-head"><div><h2>2. 兩人關係</h2>', '<section class="card" id="relationshipSection">\n    <div class="card-head"><div><h2>2. 兩人關係</h2>', 1)
text = text.replace('<section class="card">\n    <div class="card-head"><div><h2>3. 本篇</h2>', '<section class="card" id="storySection">\n    <div class="card-head"><div><h2 id="storySectionTitle">3. 本篇</h2>', 1)
text = text.replace('<div class="subtle">開場描述是主力欄位；玩法、開場或自由補充至少填一項。</div>', '<div class="subtle" id="storySectionSubtle">開場描述是主力欄位；玩法、開場或自由補充至少填一項。</div>', 1)
text = text.replace('<label class="field" style="margin-top:14px"><span>開場描述</span>', '<label class="field full-only" style="margin-top:14px"><span>開場描述</span>', 1)
text = text.replace('<details id="sceneAdvanced">', '<details class="full-only" id="sceneAdvanced">', 1)
text = text.replace('<details><summary><span>篇幅</span><span class="subtle" id="lengthSummary">', '<details class="full-only"><summary><span>篇幅</span><span class="subtle" id="lengthSummary">', 1)

# Rename section headings through stable IDs so numbering can adapt in quick mode.
text = text.replace('<h2>4. 成人元素辭典</h2>', '<h2 id="adultSectionTitle">4. 成人元素辭典</h2>', 1)
text = text.replace('<h2>5. 節奏</h2>', '<h2 id="pacingSectionTitle">5. 節奏</h2>', 1)
text = text.replace('<h2>6. 自由補充</h2>', '<h2 id="supplementSectionTitle">6. 自由補充</h2>', 1)
text = text.replace('<textarea id="storySupplement" placeholder="原樣保留，不由 Compiler 改寫。"></textarea>', '<textarea id="storySupplement" placeholder="原樣保留，不由 Compiler 改寫。"></textarea>', 1)

# Preview labels and quick-copy action.
text = text.replace('<div class="card-head"><div><h2>Prompt</h2><div class="subtle">符合最小必填後即可產生。</div></div></div>', '<div class="card-head"><div><h2 id="previewTitle">Prompt</h2><div class="subtle" id="previewSubtle">符合最小必填後即可產生。</div></div></div>', 1)
old_actions = '<div class="floating-actions"><button class="btn primary" id="generate" disabled>產生 Prompt</button><button class="btn" id="copyPrompt" disabled>複製</button><button class="btn" id="downloadPrompt" disabled>下載 TXT</button></div>'
new_actions = '<div class="floating-actions"><button class="btn primary" id="generate" disabled>產生完整 Prompt</button><button class="btn" id="copyPrompt" disabled>複製完整 Prompt</button><button class="btn" id="downloadPrompt" disabled>下載 TXT</button><button class="btn" id="quickCopyPrompt" disabled>只複製玩法 Prompt</button></div>'
assert old_actions in text
text = text.replace(old_actions, new_actions, 1)
text = text.replace('<button class="btn" id="clearStory">清空本篇（保留角色）</button>', '<button class="btn" id="clearStory">清空本篇（保留角色）</button>', 1)
text = text.replace('<div class="notice" style="margin-top:10px">角色庫使用 localStorage。', '<div class="notice" id="roleStorageNotice" style="margin-top:10px">角色庫使用 localStorage。', 1)

# Add independent quick compiler. It deliberately ignores role assignment semantics on legacy plays.
compiler_anchor = '''function compilePrompt(input, masterItems) {
'''
idx = text.index(compiler_anchor)
# insert before compilePrompt, after validateMinimumInput block
quick_compiler = r'''
function validateQuickInput(input) {
  const hasWanted = Boolean(
    (input?.elementCombos || []).length ||
    (input?.plays || []).length ||
    cleanString(input?.supplement)
  );
  return { ok: hasWanted, hasWanted };
}

function compileQuickPrompt(input, masterItems) {
  const minimum = validateQuickInput(input);
  if (!minimum.ok) throw new Error('Quick Prompt requires at least one core element, other element, or free supplement');

  const masterIndex = buildMasterIndex(masterItems);
  const sections = ['請根據以下方向創作一篇所有角色皆為成年人的成人小說。'];
  const orientationId = cleanString(input?.task?.contentOrientationId);
  if (orientationId) {
    if (!CONTENT_ORIENTATION_OPTIONS[orientationId]) throw new Error(`Unknown content-orientation option: ${orientationId}`);
    sections.push(`【內容方向】\n${CONTENT_ORIENTATION_OPTIONS[orientationId].promptText}。`);
  }

  if ((input?.elementCombos || []).length) {
    const lines = ['【核心成人元素與功能】'];
    for (const combo of input.elementCombos) {
      const labels = (combo.modifierLabels || []).filter(Boolean);
      lines.push(labels.length ? `${combo.label}：${labels.join('、')}` : combo.label);
    }
    sections.push(lines.join('\n'));
  }

  if ((input?.plays || []).length) {
    const labels = input.plays.map(selection => resolveItem(masterIndex, selection?.id, 'play')?.label).filter(Boolean);
    if (labels.length) sections.push(`【其他想加入的元素】\n${labels.join('\n')}`);
  }

  const pacing = (input?.pacingIds || []).map(id => resolveItem(masterIndex, id, 'pacing')?.label).filter(Boolean);
  if (pacing.length) sections.push(`【節奏】\n${pacing.join('、')}`);

  if (cleanString(input?.supplement)) sections.push(`【自由補充】\n${input.supplement}`);

  sections.push('人物、關係與場景可依故事需要合理補完。\n選中的元素是希望自然融入的方向，不必逐項展示，也不需依序完成。');
  return sections.join('\n\n');
}

'''
text = text[:idx] + quick_compiler + text[idx:]

# Add mode state next to existing UI state.
text = text.replace("let currentPlayTab = 'intimacy_touch';", "let generatorMode = 'full';\nlet currentPlayTab = 'intimacy_touch';", 1)

# Mode-aware validation.
pattern = re.compile(r'''function uiValidation\(\)\{.*?\n\}\nfunction updateValidation\(\)\{.*?\n\}\n(?=function updateCounts\(\)\{)''', re.S)
replacement = r'''function uiValidation(){
  const input=readInput();
  if(generatorMode==='quick') return validateQuickInput(input);
  const m=validateMinimumInput(input),ageA=input.characters.A.age,ageB=input.characters.B.age;
  const ageOkA=!ageA||ageA>=18,ageOkB=!ageB||ageB>=18; return {...m,ageOkA,ageOkB,ok:m.ok&&ageOkA&&ageOkB};
}
function updateValidation(){
  const input=readInput(),v=uiValidation(),box=$('#validationBox');
  if(generatorMode==='quick'){
    box.className=`status-box ${v.ok?'ok':'warn'}`;
    box.innerHTML=v.ok?'✓ 已選擇玩法內容，可以產生玩法 Prompt。':'尚缺：<div class="missing-list">• 至少選擇一個核心元素、其他元素，或填寫自由補充</div>';
  }else{
    const missing=[];if(!v.hasA)missing.push('角色 A 名稱');if(!v.hasB)missing.push('角色 B 名稱');if(!v.hasWanted)missing.push('本篇想看什麼（核心元素／玩法／開場／自由補充擇一）');if(!v.ageOkA)missing.push('角色 A 年齡需 ≥18');if(!v.ageOkB)missing.push('角色 B 年齡需 ≥18');
    box.className=`status-box ${v.ok?'ok':'warn'}`;box.innerHTML=v.ok?'✓ 已滿足最小必填，可以產生完整 Prompt。':`尚缺：<div class="missing-list">${missing.map(x=>`• ${esc(x)}`).join('<br>')}</div>`;
  }
  $('#generate').disabled=!v.ok;
  $('#quickCopyPrompt').disabled=!validateQuickInput(input).ok;
}
'''
text, n = pattern.subn(replacement, text, count=1)
assert n == 1, 'validation block not replaced'

# Mode rendering and mode-safe generation/copy.
anchor = 'function generatePrompt(){\n'
idx = text.index(anchor)
mode_logic = r'''
function renderGeneratorMode(){
  const quick=generatorMode==='quick';
  document.documentElement.classList.toggle('quick-mode',quick);
  $$('[data-generator-mode]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.generatorMode===generatorMode)));
  $('#storySectionTitle').textContent=quick?'1. 內容方向':'3. 本篇';
  $('#storySectionSubtle').textContent=quick?'只保留內容取向；人物、關係與場景交給 LLM 合理補完。':'開場描述是主力欄位；玩法、開場或自由補充至少填一項。';
  $('#adultSectionTitle').textContent=quick?'2. 成人元素':'4. 成人元素辭典';
  $('#pacingSectionTitle').textContent=quick?'3. 節奏':'5. 節奏';
  $('#supplementSectionTitle').textContent=quick?'4. 自由補充':'6. 自由補充';
  $('#previewTitle').textContent=quick?'玩法 Prompt':'Prompt';
  $('#previewSubtle').textContent=quick?'不需要角色資料；選好玩法即可產生。':'符合最小必填後即可產生。';
  $('#generate').textContent=quick?'產生玩法 Prompt':'產生完整 Prompt';
  $('#copyPrompt').textContent=quick?'複製玩法 Prompt':'複製完整 Prompt';
  $('#clearStory').textContent=quick?'清空玩法':'清空本篇（保留角色）';
  $('#storySupplement').placeholder=quick?'例如：希望其中一方較主動；觸手由另一方控制；不需要太多劇情鋪陳。':'原樣保留，不由 Compiler 改寫。';
  if($('#output').value){promptDirty=true;$('#copyPrompt').disabled=true;$('#downloadPrompt').disabled=true;$('#outputState').textContent='模式已變更，請重新產生';}
  updateValidation();
}
function setGeneratorMode(mode){
  if(!['full','quick'].includes(mode)||mode===generatorMode)return;
  generatorMode=mode;renderGeneratorMode();
}

'''
text = text[:idx] + mode_logic + text[idx:]

old_generate = r'''function generatePrompt(){
  $('#compileError').classList.add('hidden');try{const out=compilePrompt(readInput(),MASTER_ITEMS);$('#output').value=out;$('#outputChars').textContent=`${[...out].length} 字元`;$('#copyPrompt').disabled=false;$('#downloadPrompt').disabled=false;promptDirty=false;$('#outputState').textContent='已是最新設定';flashStatus('Prompt 已產生');}
  catch(e){$('#compileError').textContent=e.message;$('#compileError').classList.remove('hidden');}
}
'''
new_generate = r'''function generatePrompt(){
  $('#compileError').classList.add('hidden');try{const input=readInput(),out=generatorMode==='quick'?compileQuickPrompt(input,MASTER_ITEMS):compilePrompt(input,MASTER_ITEMS);$('#output').value=out;$('#outputChars').textContent=`${[...out].length} 字元`;$('#copyPrompt').disabled=false;$('#downloadPrompt').disabled=false;promptDirty=false;$('#outputState').textContent='已是最新設定';flashStatus(generatorMode==='quick'?'玩法 Prompt 已產生':'完整 Prompt 已產生');}
  catch(e){$('#compileError').textContent=e.message;$('#compileError').classList.remove('hidden');}
}
'''
assert old_generate in text
text = text.replace(old_generate, new_generate, 1)

# Quick-copy is available directly from full mode and never mutates the preview.
copy_anchor = "async function copyPrompt(){try{await navigator.clipboard.writeText($('#output').value);flashStatus('已複製 Prompt')}catch{ $('#output').select();document.execCommand('copy');flashStatus('已複製 Prompt')}}\n"
assert copy_anchor in text
quick_copy = copy_anchor + r'''async function copyTextDirect(text,status){
  try{await navigator.clipboard.writeText(text);flashStatus(status);return}
  catch{}
  const tmp=document.createElement('textarea');tmp.value=text;tmp.style.position='fixed';tmp.style.opacity='0';document.body.appendChild(tmp);tmp.select();document.execCommand('copy');tmp.remove();flashStatus(status);
}
async function copyQuickPrompt(){
  try{const out=compileQuickPrompt(readInput(),MASTER_ITEMS);await copyTextDirect(out,'已複製玩法 Prompt')}
  catch(e){$('#compileError').textContent=e.message;$('#compileError').classList.remove('hidden');}
}
'''
text = text.replace(copy_anchor, quick_copy, 1)

# Quick clear only clears quick-visible inputs; hidden full-mode work remains intact.
clear_anchor = 'function clearStory(){\n'
idx = text.index(clear_anchor)
clear_quick = r'''
function clearQuickPrompt(){
  $('#storySupplement').value='';$$('[data-pacing]').forEach(x=>x.checked=false);selectedPlays.clear();selectedCombos.clear();activeCoreElement=null;renderCoreElements();renderModifierEditor();$('#playSearch').value='';$('#supernaturalOnly').checked=false;currentPlayTab='intimacy_touch';$('input[name="orientation"][value=""]').checked=true;$('#output').value='';$('#copyPrompt').disabled=true;$('#downloadPrompt').disabled=true;$('#outputChars').textContent='0 字元';$('#outputState').textContent='尚未產生';promptDirty=false;renderPlays();onFormChange();
}
'''
text = text[:idx] + clear_quick + text[idx:]
text = text.replace('function clearStory(){\n  for(const id of', "function clearStory(){\n  if(generatorMode==='quick'){clearQuickPrompt();return}\n  for(const id of", 1)

# Event wiring for mode and quick copy.
wire_anchor = "$('#relationshipTypeChips').onclick=e=>{"
idx = text.index(wire_anchor)
wire = "$('#generatorModeSwitcher').onclick=e=>{const btn=e.target.closest('[data-generator-mode]');if(btn)setGeneratorMode(btn.dataset.generatorMode)};\n"
text = text[:idx] + wire + text[idx:]
text = text.replace("$('#orientationOptions').onchange=onFormChange;", "$('#orientationOptions').onchange=onFormChange;$('#quickCopyPrompt').onclick=copyQuickPrompt;", 1)

# Initial mode render after normal initialization.
init_anchor = "refreshRoleLibrarySelects();for(const k of ['A','B'])for(const cat of [...GENERAL_TRAITS,...INTIMATE_TRAITS])setTraitState(k,cat,[]);onFormChange();"
assert init_anchor in text
text = text.replace(init_anchor, init_anchor + 'renderGeneratorMode();', 1)

P.write_text(text, encoding='utf-8')
print('V1.2.1 Quick Prompt materialized')
