from pathlib import Path
import json,re

P=Path('index.html')
text=P.read_text(encoding='utf-8')

# Version / product positioning
text=text.replace('V1.0.3 PWA','V1.1.0 Dictionary')
text=text.replace('角色可直接填，也可存進本機角色庫重複使用。','基本資訊就足夠使用；人格、種族與幻想能力屬進階設定，可交給 LLM 補完，需要時再展開。')
text=text.replace('<h2>4. 玩法</h2><div class="subtle">玩法是方向，不是待辦清單。沒有數量上限。</div>','<h2>4. 成人玩法辭典</h2><div class="subtle">先用辭典探索「原來還有這種玩法」，再把想看的項目加入本篇。玩法是方向，不是待辦清單。</div>')
text=text.replace('placeholder="搜尋玩法名稱或說明"','placeholder="搜尋名稱、別名、英文、感受或說明"')
text=text.replace('V1 Final · Single-file HTML · Vanilla JS · Deterministic Compiler · Master Data v0.10','V1.1 Dictionary · Vanilla JS · Deterministic Compiler · Expanded Play Dictionary')
# collapse personality by default (static + fallback templates)
text=text.replace('<details open><summary><span>一般性格</span>','<details><summary><span>一般性格（進階）</span>')
text=text.replace('<details open><summary><span>親密互動特徵</span>','<details><summary><span>親密互動特徵（進階）</span>')
text=text.replace('<details open><summary><span>一般性格</span>', '<details><summary><span>一般性格（進階）</span>')
text=text.replace('<details open><summary><span>親密互動特徵</span>', '<details><summary><span>親密互動特徵（進階）</span>')

# CSS for dictionary details
css_anchor='.play-meta{display:flex;align-items:center;gap:6px;justify-content:space-between}'
css_add='''.play-dict{margin-top:1px;padding-top:6px;border-top:1px dashed var(--line)}.play-dict summary{font-size:11px;font-weight:600;color:var(--accent);justify-content:flex-start;gap:6px}.play-dict summary:after{content:"＋"}.play-dict[open]>summary:after{content:"－"}.play-dict-body{padding:7px 0 0;font-size:11.5px;color:#5f5b54;line-height:1.55}.play-dict-line{margin:3px 0}.play-dict-line b{color:#3f3c37}.play-category-badge{display:inline-block;background:#f5f3ef;color:#625e57;border-radius:999px;padding:2px 6px;font-size:10px;margin-right:4px}'''
if css_add not in text:
    text=text.replace(css_anchor,css_anchor+css_add,1)

# Parse and expand master data
m=re.search(r'(<script id="masterData" type="application/json">)(.*?)(</script>)',text,re.S)
if not m: raise SystemExit('masterData not found')
obj=json.loads(m.group(2))
obj['version']='0.11'
obj['status']='expanded_play_dictionary_v1_1'
obj['sourceSpec']='V1.1 Dictionary Expansion'
items=obj['items']
existing_ids={x['id'] for x in items}
existing_labels={x.get('label') for x in items}

def p(id,cat,label,desc,english='',aliases=None,keywords=None,feel='',confusable='',direction='direction',caps=None):
    return {'id':id,'type':'play','category':cat,'label':label,'description':desc,'english':english,'aliases':aliases or [],'keywords':keywords or [],'feel':feel,'confusable':confusable,'coversCapability':caps or [],'directionMode':direction}

NEW=[
# intimacy / touch
p('slow_kissing','intimacy_touch','慢吻','以較慢的接吻與停頓累積親密感，重點是節奏、等待與回應。','slow kissing',[],['接吻','親密','慢熱'],'溫柔、期待、拉近距離'),
p('deep_kissing','intimacy_touch','深吻','較深入而持續的接吻，適合強調呼吸、節奏與雙方回應。','deep kissing',['法式接吻'],['接吻','舌吻'],'投入、失去距離感'),
p('neck_kissing','intimacy_touch','頸側親吻','集中在頸側、耳下等敏感區域的親吻與停留。','neck kissing',[],['脖子','頸部','親吻'],'貼近、敏感、被包圍感'),
p('ear_teasing','intimacy_touch','耳側挑逗','以耳廓、耳後與低聲靠近造成細小但明顯的感官刺激。','ear teasing',[],['耳朵','耳後','低語'],'敏感、近距離、容易分心'),
p('hair_touching','intimacy_touch','撫髮／整理頭髮','透過撫摸、撥開或整理頭髮製造自然的親密接觸。','hair touching',[],['頭髮','撫摸','日常親密'],'照顧感、不經意親密'),
p('face_touching','intimacy_touch','撫臉','以掌心、指尖觸碰臉頰、下巴等位置，常用於確認、安撫或拉近距離。','face touching',[],['臉頰','下巴','撫摸'],'溫柔、確認、專注'),
p('full_body_caress','intimacy_touch','全身撫摸','以連續撫摸探索身體，不急著集中到單一部位。','full-body caressing',[],['撫摸','全身','探索'],'慢熱、探索、期待'),
p('massage_to_intimacy','intimacy_touch','按摩轉親密','從肩頸、背部或腿部按摩逐漸轉為更私人、更曖昧的接觸。','massage to intimacy',[],['按摩','放鬆','漸進'],'放鬆、界線逐步改變'),
p('lap_sitting','intimacy_touch','坐在腿上','一方坐到另一方腿上，以距離、重量與姿勢本身形成親密互動。','lap sitting',[],['大腿','坐腿','貼近'],'貼合、被環抱、主動靠近'),
p('mutual_touching','intimacy_touch','互相撫摸','雙方同時以手或身體接觸彼此，重點是來回回應而非單向刺激。','mutual touching',[],['雙向','撫摸','互動'],'平等、同步、互相試探','單向撫摸'),
p('body_rubbing','intimacy_touch','身體磨蹭','透過身體貼合、磨蹭或移動累積刺激，不以特定器具為核心。','body rubbing',['磨蹭'],['貼合','摩擦'],'黏著感、失去距離'),
p('clothed_grinding','intimacy_touch','隔衣磨蹭','隔著衣物進行身體摩擦，重點是壓抑與尚未完全脫離日常狀態的反差。','clothed grinding',['dry humping'],['隔衣','摩擦','衣物'],'壓抑、偷跑、未完全越界'),
p('hand_holding_during_intimacy','intimacy_touch','親密時牽手／扣手','在成人互動中仍持續牽手、十指相扣或壓住彼此手掌。','hand holding during intimacy',[],['牽手','十指緊扣'],'信任、依戀、反差'),
p('hugging_from_behind','intimacy_touch','從後環抱','由背後抱住對方並維持貼合，可用於安撫、限制或曖昧靠近。','back hug',['背後抱'],['擁抱','後方'],'包圍感、安心或被限制'),
p('prolonged_eye_contact','intimacy_touch','長時間對視','在近距離互動中刻意維持視線接觸，讓心理張力與身體反應彼此放大。','prolonged eye contact',[],['視線','對視','眼神'],'被看穿、專注、難以逃避'),
# orgasm/control
p('orgasm_denial','orgasm_control','高潮禁止','允許刺激持續，但明確要求暫時不能達到高潮，重點是等待與控制。','orgasm denial',['禁止高潮'],['高潮','控制','等待'],'控制、挫折、期待','邊緣控制'),
p('orgasm_permission','orgasm_control','高潮許可','把「何時可以高潮」變成需要取得對方允許的規則。','orgasm permission',[],['許可','高潮','命令'],'服從、期待、儀式感','高潮禁止'),
p('ruined_orgasm','orgasm_control','中斷式高潮','在高潮發生前後刻意降低或移除刺激，使高潮感受不完整。','ruined orgasm',['破壞式高潮'],['高潮','中斷'],'挫折、控制、意猶未盡','邊緣控制'),
p('multiple_orgasms','orgasm_control','連續高潮','在短時間內安排多次高潮，重點是持續刺激與反應累積。','multiple orgasms',[],['多次高潮','連續'],'失控、累積、耐力'),
p('simultaneous_orgasm','orgasm_control','同步高潮','把雙方接近高潮的節奏調整到同一時間。','simultaneous orgasm',['同時高潮'],['同步','高潮'],'同步感、親密、節奏協調'),
p('orgasm_counting','orgasm_control','高潮計數','把高潮次數本身變成規則、挑戰或遊戲的一部分。','orgasm counting',[],['計數','次數','規則'],'遊戲感、壓力、期待'),
p('stop_start_control','orgasm_control','停止—再開始','在刺激進行中反覆停止再恢復，藉由節奏中斷控制興奮程度。','stop-start',[],['停止','重啟','節奏'],'吊胃口、被控制','邊緣控制'),
p('slow_build_to_orgasm','orgasm_control','長時間累積高潮','把高潮前的累積過程拉長，以低至中等強度逐步提高刺激。','slow build',[],['慢慢','累積','高潮'],'耐心、期待、逐步失控'),
p('post_orgasm_sensitivity','orgasm_control','高潮後敏感延續','在高潮後仍利用變得敏感的狀態延續較輕或間歇性的刺激。','post-orgasm sensitivity',[],['高潮後','敏感','延續'],'脆弱、敏感、餘韻'),
# sensory
p('ice_play','sensory_stimulation','冰冷刺激','利用冰塊或低溫接觸形成明顯的溫度反差。','ice play',[],['冰','低溫','溫差'],'驚縮、敏感、預期差'),
p('warm_cold_contrast','sensory_stimulation','冷熱交替','在安全範圍內交替冷與暖的感覺，利用溫差放大感官注意。','temperature contrast',['溫差玩法'],['冷熱','溫度'],'反差、不可預測'),
p('feather_light_touch','sensory_stimulation','羽毛式輕觸','以極輕、若有似無的觸碰造成癢、期待與注意力集中。','feather-light touch',[],['羽毛','輕觸','癢'],'吊胃口、敏感、難以忽略'),
p('nail_tracing','sensory_stimulation','指甲輕劃','用指甲或指尖沿皮膚輕劃，重點是細線般的觸覺與預期。','nail tracing',[],['指甲','輕劃','皮膚'],'細微、發癢、緊張'),
p('scent_focus','sensory_stimulation','氣味偏好','把香水、洗髮香氣、皮膚氣味等嗅覺細節作為親密刺激的一部分。','scent focus',[],['氣味','香味','嗅覺'],'記憶感、貼近、私人感'),
p('voice_focus','sensory_stimulation','聲音／語氣刺激','特別利用聲線、耳語、命令語氣或喘息聲形成心理與感官刺激。','voice kink',['聲控'],['聲音','語氣','耳語'],'近距離、服從或被誘惑'),
p('music_rhythm_play','sensory_stimulation','配合音樂節奏','讓動作、停頓或刺激跟隨音樂節拍，形成外部節奏規則。','rhythm play',[],['音樂','節拍','節奏'],'遊戲感、節律、可預測與變化'),
p('mirror_viewing','sensory_stimulation','鏡中觀看','透過鏡子觀看自己或對方的動作與反應，使視覺注意成為玩法的一部分。','mirror play',['鏡子玩法'],['鏡子','觀看','視覺'],'自我意識、被看見、反差'),
p('lights_on_visibility','sensory_stimulation','保持明亮照明','刻意不關燈或提高可見度，讓彼此能清楚看到表情與身體反應。','lights-on intimacy',[],['開燈','看清楚','視覺'],'坦露、被注視'),
p('sensory_deprivation_combo','sensory_stimulation','多重感官限制','同時限制視覺、聲音或部分行動，使剩餘感官更集中。','sensory deprivation',[],['蒙眼','耳塞','感官限制'],'未知、專注、期待'),
# clothing/exposure
p('slow_undressing','clothing_exposure','慢慢脫衣','把解開、拉下與停頓本身當成前戲，而不是直接完成脫衣。','slow undressing',[],['脫衣','慢慢','前戲'],'期待、觀察、逐步越界'),
p('partial_undressing','clothing_exposure','部分脫衣','保留部分衣物，只讓需要的部位暴露，以衣著與裸露形成對比。','partial undressing',[],['半脫','部分裸露'],'反差、急迫或刻意保留'),
p('clothed_vs_nude','clothing_exposure','一方著衣一方裸身','讓雙方裸露程度不對等，藉由視覺與身分差異形成張力。','clothed vs nude',[],['著衣','裸身','不對等'],'權力差、被觀看、脆弱感'),
p('lingerie_focus','clothing_exposure','內衣／貼身衣物偏好','把內衣、睡衣或貼身衣物的材質、剪裁與穿脫過程作為刺激重點。','lingerie kink',[],['內衣','睡衣','貼身衣物'],'精心準備、視覺、材質感'),
p('stockings_focus','clothing_exposure','絲襪／長襪偏好','把絲襪、長襪或腿部覆蓋材質作為視覺與觸覺重點。','stockings kink',[],['絲襪','長襪','腿'],'材質、腿部焦點'),
p('gloves_focus','clothing_exposure','手套偏好','保留手套進行觸碰，使材質、距離感與角色形象持續存在。','glove kink',[],['手套','材質','手'],'冷感、儀式感、角色感'),
p('uniform_focus','clothing_exposure','制服／職業服裝偏好','保留具有職業或身分象徵的服裝，利用日常角色與私人互動的反差。','uniform kink',[],['制服','西裝','職業服'],'身分反差、角色延續'),
p('shirt_only','clothing_exposure','只穿上衣','保留襯衫、T 恤等上衣，其餘衣物減少，形成上半身仍日常、下半身更私人化的反差。','shirt only',[],['襯衫','上衣','半裸'],'日常與裸露反差'),
p('accessory_kept_on','clothing_exposure','保留配件','刻意保留眼鏡、領帶、飾品等角色標誌物，維持人物辨識與反差。','accessories kept on',[],['眼鏡','領帶','飾品'],'角色感、視覺焦點'),
# power/protocol
p('permission_to_touch','power_control','觸碰許可','把能否碰觸特定部位設成需要詢問或取得允許的規則。','permission to touch',[],['許可','觸碰','規則'],'控制、克制、等待'),
p('do_not_move_rule','power_control','不准亂動','要求一方維持姿勢或不主動移動，讓主導權更集中。','do not move',[],['不准動','命令','保持姿勢'],'服從、忍耐、被掌控'),
p('hands_off_rule','power_control','手不准碰','限制一方不能用手主動碰觸自己或對方。','hands off',[],['手','禁止碰','規則'],'克制、挫折、控制'),
p('countdown_command','power_control','倒數指令','利用倒數作為開始、停止、變換動作或允許某件事的訊號。','countdown command',[],['倒數','指令','計時'],'預期、壓力、儀式感'),
p('rules_and_consequences','power_control','規則與後果','先訂下少量明確規則，違反後觸發事先同意的後果或額外要求。','rules and consequences',['規則玩法'],['規則','懲罰','契約'],'遊戲化、服從、期待','即興命令'),
p('praise_focus','psychological_contrast','稱讚偏好','以具體稱讚、肯定與鼓勵強化對方反應，使被肯定本身成為刺激。','praise kink',['誇獎'],['稱讚','肯定','好孩子'],'被認可、依賴、安心'),
p('embarrassing_praise','psychological_contrast','讓人害羞的直白稱讚','刻意把對方的反應說得很具體、很直接，使稱讚同時帶有羞恥感。','embarrassing praise',[],['稱讚','害羞','反應'],'被看穿、羞恥與肯定並存'),
p('asking_for_more','psychological_contrast','要求親口說想要更多','讓一方必須自己說出需求，而不是由對方猜測或直接繼續。','ask for more',[],['開口','需求','說出來'],'承認慾望、害羞、主動性'),
p('name_calling_focus','psychological_contrast','反覆叫名字','在親密時反覆使用對方名字或特定稱呼，強化注意力與關係感。','name calling',[],['名字','稱呼','呼喚'],'專注、被鎖定、親密'),
p('formal_speech_contrast','psychological_contrast','維持敬語／正式稱呼','即使情境已非常私人，仍維持敬語、職稱或正式口吻，製造語言與行為反差。','formal speech contrast',[],['敬語','職稱','正式'],'身分反差、克制'),
p('confession_during_intimacy','psychological_contrast','親密中坦白心意','在身體距離已拉近時說出平常不會承認的感情、需要或不安。','confession during intimacy',[],['告白','坦白','心意'],'脆弱、關係推進'),
p('jealousy_reassurance','psychological_contrast','吃醋後確認關係','把嫉妒或不安轉成需要對方明確確認偏愛與關係位置的互動。','jealousy reassurance',[],['吃醋','確認','偏愛'],'佔有、安心、脆弱'),
# roleplay / scenario
p('boss_subordinate_roleplay','roleplay_scenario','上司／部下角色扮演','由成年人扮演具有職場權力差的上司與部下，把命令、敬語與身分反差帶入互動。','boss/subordinate roleplay',[],['職場','上司','部下'],'權力差、正式與私人反差'),
p('doctor_patient_roleplay','roleplay_scenario','醫師／病患角色扮演','由成年人進行醫師與病患的情境扮演，重點在檢查、指示與專業口吻的戲劇性。','doctor/patient roleplay',[],['醫生','病患','檢查'],'專業感、被檢視、角色扮演'),
p('instructor_trainee_roleplay','roleplay_scenario','教官／受訓者角色扮演','由成年人扮演指導者與受訓者，以口令、示範與糾正形成情境。','instructor/trainee roleplay',[],['教官','訓練','指導'],'規則、考核、權威'),
p('master_servant_roleplay','roleplay_scenario','主人／侍從角色扮演','以主人與侍從、管家或女僕等成年角色扮演服務與命令關係。','master/servant roleplay',[],['主人','侍從','女僕','管家'],'服務、階級、儀式感'),
p('deity_worshipper_roleplay','roleplay_scenario','神祇／信徒角色扮演','以神祇與成年信徒的身分差異，結合崇拜、奉獻與命令。','deity/worshipper roleplay',[],['神','信徒','崇拜'],'神聖與私密反差、奉獻'),
p('captor_captive_roleplay','roleplay_scenario','俘虜情境角色扮演','在事先同意的幻想框架下扮演控制者與被俘者，重點在情境式權力不對等。','captor/captive roleplay',[],['俘虜','囚禁','權力差'],'危險幻想、控制、戲劇性'),
p('strangers_roleplay','roleplay_scenario','假裝陌生人','原本熟悉的兩人暫時假裝不認識，以初次搭話、試探與重新追求製造新鮮感。','strangers roleplay',[],['陌生人','搭訕','初次見面'],'新鮮、試探、角色切換'),
p('service_roleplay','roleplay_scenario','服務情境角色扮演','以旅館、酒吧、私人服務等成年職業情境扮演「提供服務／接受服務」的關係。','service roleplay',[],['服務','旅館','酒吧'],'禮貌、職業角色、曖昧'),
p('interrogation_roleplay','roleplay_scenario','審問角色扮演','以問答、命令與拒絕回答等方式扮演審問情境，重點在語言壓力與權力差。','interrogation roleplay',[],['審問','問答','情報'],'壓力、心理攻防、權威'),
p('contract_ritual_roleplay','roleplay_scenario','契約／儀式角色扮演','以簽訂契約、宣誓、魔法儀式等形式把親密互動包裝成具有規則的正式事件。','contract ritual roleplay',[],['契約','儀式','宣誓'],'正式感、不可逆、象徵性'),
# body / position extras
p('spooning_intimacy','position_body_relation','側躺相擁／湯匙式','雙方側躺並前後貼合，適合較慢、較黏著的互動。','spooning',[],['側躺','抱著','貼合'],'安心、貼合、慢節奏'),
p('seated_face_to_face','position_body_relation','坐姿面對面','雙方坐著面對面並保持近距離，便於接吻、對視與環抱。','seated face-to-face',[],['坐姿','面對面','對視'],'親密、視線、擁抱'),
p('lap_straddle','position_body_relation','跨坐腿上','一方跨坐在另一方腿上，使主動權、視線與身體距離都非常明顯。','lap straddle',[],['跨坐','腿上','面對面'],'主動、貼近、視覺'),
p('kneeling_between_legs','position_body_relation','跪坐於雙腿之間','一方位於另一方雙腿之間的較低位置，常帶有服務、仰視或權力高度差。','kneeling between legs',[],['跪姿','雙腿','高度差'],'服務感、權力差、視線差'),
p('edge_of_bed_position','position_body_relation','床緣姿勢','一方靠近床沿，另一方站立或跪在床邊，利用高度差與穩定支撐改變互動。','edge of bed',[],['床邊','床緣','高度差'],'方便調整、位置鮮明'),
p('chair_position','position_body_relation','椅子姿勢','以椅子作為固定支點，進行坐姿、跨坐或前後貼合的互動。','chair position',[],['椅子','坐姿'],'日常家具反差、固定支點'),
p('against_desk_position','position_body_relation','靠桌／辦公桌姿勢','利用桌面或桌緣支撐身體，讓場景中的家具直接參與位置關係。','against desk',[],['桌子','辦公桌','桌緣'],'場景感、支撐、職場反差'),
p('shower_wall_position','position_body_relation','淋浴間靠牆','在浴室或淋浴間利用牆面保持站姿或貼合。','shower wall',[],['浴室','淋浴','牆'],'濕滑環境、貼近、站姿'),
# nonhuman / fantasy extras
p('tail_touching','nonhuman_fantasy','尾巴互動','以角色的尾巴纏繞、撫摸、掃過或表達情緒，讓非人身體特徵直接參與親密互動。','tail play',[],['尾巴','獸人','非人'],'非人特色、情緒外顯',direction='direction',caps=['body_extension']),
p('wing_envelopment','nonhuman_fantasy','翅膀包覆','用大型翅膀遮蔽、環抱或形成私人空間，讓翅膀兼具保護與限制效果。','wing envelopment',[],['翅膀','包覆','羽翼'],'安全感、包圍、非人感',direction='direction',caps=['body_extension']),
p('horn_handhold','nonhuman_fantasy','角部觸碰／扶角','把角、冠角等非人部位作為可觸碰或握持的身體特徵。','horn play',[],['角','惡魔','龍'],'非人身體、敏感部位'),
p('shapeshift_for_intimacy','nonhuman_fantasy','親密時變形','角色依情境改變部分外觀、肢體或體型，使變形本身成為互動的一部分。','shapeshifting for intimacy',[],['變形','形態','身體改變'],'幻想、適應、不可預期',direction='direction',caps=['body_rule_recovery']),
p('size_change','nonhuman_fantasy','體型變化','以魔法或種族能力暫時改變身高或整體體型，放大尺寸差與位置關係。','size change',[],['巨大化','縮小','尺寸差'],'尺度差、幻想感',direction='direction',caps=['body_rule_recovery']),
p('magical_marks','nonhuman_fantasy','魔法印記／契約紋','以發光紋路、契約印記或魔法標記呈現關係、刺激或能力啟動。','magical marks',['契約紋'],['印記','紋路','契約'],'象徵、歸屬、幻想'),
p('pheromone_influence','nonhuman_fantasy','費洛蒙／氣味影響','利用非人種族或幻想設定中的氣味、費洛蒙等機制放大吸引與注意力。','pheromone influence',[],['費洛蒙','氣味','吸引'],'本能、失去平常距離感',direction='direction',caps=['sensory_mental']),
p('heat_cycle_fantasy','nonhuman_fantasy','發情期／熱期幻想','以成年角色的幻想生理週期作為慾望變化與關係互動背景。','heat cycle fantasy',['熱期'],['發情期','熱期','ABO'],'本能、需求增強、照顧'),
p('telepathic_intimacy','nonhuman_fantasy','心靈感應親密','在身體互動之外共享片段情緒、意念或需求，使心理距離同步縮短。','telepathic intimacy',[],['心靈感應','讀心','意念'],'被理解、無法隱藏、心理親密',direction='direction',caps=['sensory_mental']),
p('time_slowing_scene','nonhuman_fantasy','時間感減速','用超自然能力讓主觀或局部時間變慢，使短暫互動被拉長。','time slowing',[],['時間','減速','時間停止'],'延長感、與外界隔離',direction='direction',caps=['space_environment']),
]

for x in NEW:
    if x['id'] not in existing_ids and x['label'] not in existing_labels:
        items.append(x);existing_ids.add(x['id']);existing_labels.add(x['label'])

# Add lightweight search metadata to all old plays without changing compiler fields
for x in items:
    if x.get('type')!='play': continue
    x.setdefault('aliases',[]);x.setdefault('english','');x.setdefault('keywords',[]);x.setdefault('feel','');x.setdefault('confusable','')

new_json=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
text=text[:m.start(2)]+new_json+text[m.end(2):]

# Categories / tab order
old="""const PLAY_CATEGORY_LABELS = {\n  power_control:'權力與主導', bondage_restriction:'束縛與限制', toys_devices:'玩具與器具', sensory_stimulation:'感官與刺激',\n  position_body_relation:'姿勢與身體關係', psychological_contrast:'心理／羞恥／反差', nonhuman_fantasy:'非人／幻想玩法'\n};\nconst PLAY_CATEGORY_ORDER = ['power_control','bondage_restriction','toys_devices','sensory_stimulation','position_body_relation','psychological_contrast','nonhuman_fantasy'];"""
new="""const PLAY_CATEGORY_LABELS = {\n  intimacy_touch:'親密接觸', power_control:'權力與主導', bondage_restriction:'束縛與限制', toys_devices:'玩具與器具', sensory_stimulation:'感官與刺激',\n  position_body_relation:'姿勢與身體關係', orgasm_control:'高潮與節制', psychological_contrast:'心理／羞恥／反差', clothing_exposure:'衣著／暴露', roleplay_scenario:'角色扮演／情境', nonhuman_fantasy:'非人／幻想玩法'\n};\nconst PLAY_CATEGORY_ORDER = ['intimacy_touch','power_control','bondage_restriction','toys_devices','sensory_stimulation','position_body_relation','orgasm_control','psychological_contrast','clothing_exposure','roleplay_scenario','nonhuman_fantasy'];"""
if old not in text: raise SystemExit('category block not found')
text=text.replace(old,new,1)

# Search across dictionary metadata
old_search="if(q)items=items.filter(x=>(x.label+' '+(x.description||'')).toLowerCase().includes(q));"
new_search="if(q)items=items.filter(x=>[x.label,x.description,x.english,(x.aliases||[]).join(' '),(x.keywords||[]).join(' '),x.feel,x.confusable,PLAY_CATEGORY_LABELS[x.category]].filter(Boolean).join(' ').toLowerCase().includes(q));"
if old_search not in text: raise SystemExit('search marker not found')
text=text.replace(old_search,new_search,1)

# More useful tabs include all
text=text.replace("const tabs=[['selected',`已選 ${selectedPlays.size}`],...PLAY_CATEGORY_ORDER.map(id=>[id,PLAY_CATEGORY_LABELS[id]])];","const tabs=[['selected',`已選 ${selectedPlays.size}`],['all',`全部 ${byType('play').length}`],...PLAY_CATEGORY_ORDER.map(id=>[id,PLAY_CATEGORY_LABELS[id]])];",1)
text=text.replace("else items=items.filter(x=>x.category===currentPlayTab);","else if(currentPlayTab!=='all')items=items.filter(x=>x.category===currentPlayTab);",1)

# Replace renderPlays with dictionary-aware card while preserving selection/assignment semantics
pat=r"function renderPlays\(\)\{.*?\n\}\nfunction updatePlayCounts"
mm=re.search(pat,text,re.S)
if not mm: raise SystemExit('renderPlays block not found')
render="""function renderPlays(){
  renderPlayTabs();const items=getDisplayPlays(),box=$('#playList');
  if(!items.length){box.innerHTML='<div class=\"empty\" style=\"grid-column:1/-1\">沒有符合條件的玩法。</div>';return}
  box.innerHTML=items.map(item=>{
    const selected=selectedPlays.has(item.id), assignment=selectedPlays.get(item.id)||'llm', opts=assignmentOptions(item).map(([v,l])=>`<option value=\"${v}\" ${assignment===v?'selected':''}>${esc(l)}</option>`).join('');
    const alias=(item.aliases||[]).length?`<div class=\"play-dict-line\"><b>別名：</b>${esc(item.aliases.join('、'))}</div>`:'';
    const en=item.english?`<div class=\"play-dict-line\"><b>英文：</b>${esc(item.english)}</div>`:'';
    const feel=item.feel?`<div class=\"play-dict-line\"><b>常見互動感受：</b>${esc(item.feel)}</div>`:'';
    const confuse=item.confusable?`<div class=\"play-dict-line\"><b>容易混淆：</b>${esc(item.confusable)}</div>`:'';
    const category=`<span class=\"play-category-badge\">${esc(PLAY_CATEGORY_LABELS[item.category]||item.category)}</span>`;
    return `<div class=\"play-item ${selected?'selected':''}\" data-play-card=\"${item.id}\"><div class=\"play-top\"><input type=\"checkbox\" data-play=\"${item.id}\" ${selected?'checked':''}><div><div class=\"play-label\">${esc(item.label)}</div><div class=\"play-desc\">${esc(item.description||'')}</div></div></div><div class=\"play-meta\"><div>${category}${(item.coversCapability||[]).length?'<span class=\"badge\">超自然</span>':''}</div>${item.directionMode!=='none'&&selected?`<select class=\"assignment\" data-assignment=\"${item.id}\">${opts}</select>`:''}</div><details class=\"play-dict\"><summary>名詞解釋／相關資訊</summary><div class=\"play-dict-body\"><div class=\"play-dict-line\"><b>定義：</b>${esc(item.description||'')}</div>${en}${alias}${feel}${confuse}</div></details></div>`;
  }).join('');
}
function updatePlayCounts"""
text=text[:mm.start()]+render+text[mm.end():]

# Default clear state to exploration-friendly first category; keep existing selected tab behavior elsewhere
text=text.replace("currentPlayTab='power_control';","currentPlayTab='intimacy_touch';")

P.write_text(text,encoding='utf-8')

# service worker cache bump
sw=Path('service-worker.js')
s=sw.read_text(encoding='utf-8')
s=re.sub(r'adult-prompt-generator-pwa-v\d+-\d+-\d+','adult-prompt-generator-pwa-v1-1-0',s,count=1)
sw.write_text(s,encoding='utf-8')

# Assertions
assert 'V1.1.0 Dictionary' in text
assert '成人玩法辭典' in text
assert 'orgasm_control' in text and 'roleplay_scenario' in text
assert 'play-dict-body' in text
assert '搜尋名稱、別名、英文、感受或說明' in text
assert len([x for x in obj['items'] if x.get('type')=='play']) >= 140
print('V1.1 dictionary plays:',len([x for x in obj['items'] if x.get('type')=='play']))
