# -*- coding: utf-8 -*-
"""
花印 HANAJIRUSHI — product catalogue for premium v1.3 (products.html + one page per product).

Source: the official Rakuten store (https://www.rakuten.co.jp/hanajirushi/), read 2026-10-02,
as the client asked (feedback 2026-10: 「商品の詳しい情報は楽天から取得してください」).
Copy is condensed from each listing: rankings, sale wording and absorption ("浸透") claims
left out; the quasi-drug eye cream keeps to its approved 薬用 claims. English is ours.

One dict per product, field for field the `product` post type in WORDPRESS.md, so adding a
product is adding one entry. Order = display order on the products page.

  slug     page file is product-<slug>.html; also the ?item= value for the contact form
  legacy   the id the v1–v1.2 pages used (p1–p4), so old links and slides still resolve
  cat      a key of CATS()
  img      a photo in assets/img/ (clean packshot) — or None to use `rimg`
  rimg     the Rakuten main image, linked (not downloaded); some carry store banners
  rk       Rakuten item code (the JA "buy" button opens item.rakuten.co.jp/hanajirushi/<rk>/)
  new      shown as 新商品 (as labelled on Rakuten)
  soon     not on sale in Japan yet (no page; listed as coming soon)
"""
from build import t, tbd

RAKUTEN = "https://item.rakuten.co.jp/hanajirushi/"
RIMG = "https://shop.r10s.jp/hanajirushi/cabinet/"

def CATS():
    return [("cleansing", t("クレンジング", "Cleansing")),
            ("lotion", t("化粧水・美容液", "Lotions &amp; serums")),
            ("cream", t("クリーム・ジェル", "Creams &amp; gels")),
            ("mask", t("マスク・パック", "Masks &amp; packs")),
            ("uv", t("UV・化粧下地", "UV &amp; primer")),
            ("mens", t("メンズ", "Men"))]

def SERIES():
    return {"hatomugi": t("ハトムギシリーズ", "Hatomugi series"), "amino": t("アミノ酸保湿シリーズ", "Amino acid series")}

def _WIPE():   # functions, not constants: t() must run per language
    return (t("キャップをはずし、コットンにたっぷり含ませ、ゆっくりふき取ってください。アイメイクを落とす際は目に入らないように注意し、しばらくなじませてからやさしくふき取ってください。しっかりメイクの時は新しいコットンに替えて、汚れがつかなくなるまで繰り返しお使いください。",
           "Soak a cotton pad and wipe gently. For eye make-up, hold the pad in place for a moment first and keep the lotion out of your eyes. For heavier make-up, repeat with a fresh pad until it comes away clean."))

def _MASK_USE():
    return t("パックとして：お手入れの最後にたっぷり塗ってください。口元や目元などには重ね塗りがおすすめです。オールインワンジェルとして：洗顔後に適量を手に取り、お顔に塗ってください。化粧下地としてもお使いいただけます。",
              "As a pack: apply generously as the last step of your routine, layering on areas such as the eyes and mouth. As an all-in-one gel: after cleansing, smooth a little over the face. It also works as a make-up base.")

def _HATO_FREE():
    return t(["合成香料フリー", "合成着色剤フリー", "鉱物油フリー", "シリコンフリー", "弱酸性"],
               ["No synthetic fragrance", "No synthetic colour", "Mineral-oil free", "Silicone free", "Weakly acidic"])

def PRODUCTS13():
    return [
     dict(slug="cleansing-lotion-ma", legacy="p1", rk="10000091", cat="cleansing", series=None, new=False, soon=False,
          img="hanajirushi_cl.jpg", rimg=RIMG + "11261505/11-25-2.jpg",
          name=t("花印クレンジングローションMa", "Cleansing Lotion Ma"), sub=t("Cleansing Lotion Ma", "花印クレンジングローションMa"),
          size="380mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("特許技術", "Patented"), t("ダブル洗顔不要", "No double cleanse"), t("まつエクOK", "Lash-extension safe")],
          short=t("うるおいを残して、しっかり落とす拭き取りクレンジング。", "A wipe-off cleanser that removes make-up and leaves moisture behind."),
          catch=t("うるおい残して、<br>しっかり落ちる。", "Removes thoroughly.<br><em>Leaves moisture behind.</em>"),
          desc=t("ローションならではのさっぱりとした使用感で、メイクや汚れをコットンで拭き取るだけでしっかり落とします。保湿成分ヒアルロン酸Na・加水分解コラーゲン・アロエベラ葉エキス・ベタインを配合し、メイクオフしながらふっくら潤う肌に整えます。",
                 "A light, fresh lotion that lifts make-up and impurities with a cotton pad. Hyaluronic acid, hydrolysed collagen, aloe vera leaf extract and betaine keep skin soft and moist while you cleanse."),
          points=[(t("特許技術のクレンジング力", "Patented cleansing"), t("特許取得技術を採用した処方で、メイク汚れから皮脂・古い角質まで拭き取るだけで落とします。", "A patented formula lifts make-up, sebum and dead skin cells with just a cotton pad."), "patent"),
                  (t("4つの保湿成分", "Four moisturisers"), t("ヒアルロン酸Na・加水分解コラーゲン・アロエベラ葉エキス・ベタイン。", "Hyaluronic acid, hydrolysed collagen, aloe vera leaf extract and betaine."), None),
                  (t("ダブル洗顔不要", "No double cleanse"), t("拭き取った後の洗顔は不要。まつエクの方も安心してお使いいただけます。", "No need to wash your face afterwards — and safe with eyelash extensions."), None)],
          free=t(["無香料", "無着色", "オイルフリー", "アルコールフリー"], ["Fragrance-free", "Colorant-free", "Oil-free", "Alcohol-free"]),
          usage=_WIPE(),
          inci="水、DPG、PEG-7(カプリル／カプリン酸)グリセリズ、PEG-8(カプリル酸／カプリン酸)グリセリズ、フェノキシエタノール、ラウリルベタイン、メチルパラベン、クエン酸Na、クエン酸、ヒアルロン酸Na、ベタイン、BG、加水分解コラーゲン、アロエベラ葉エキス"),

     dict(slug="juicy-cleansing-lotion", legacy=None, rk="10000090peach-2", cat="cleansing", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "mem_item/imgrc0114516936.jpg",
          name=t("花印ジューシークレンジングローション", "Juicy Cleansing Lotion"), sub=t("Juicy Cleansing Lotion", "花印ジューシークレンジングローション"),
          size="380mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("桃エキス配合", "Peach extracts"), t("まつエクOK", "Lash-extension safe")],
          short=t("3種類の桃エキスを配合した、みずみずしい拭き取りクレンジング。", "A juicy wipe-off cleanser with three peach extracts."),
          catch=t("みずみずしく落として、<br>つっぱらない。", "Fresh to use —<br><em>never tight after.</em>"),
          desc=t("花印クレンジングローションの処方に、保湿成分として3種類の桃エキス（モモ果汁・モモ種子エキス・モモ葉エキス）を配合。みずみずしい使用感で肌をいたわりながら潤いを与えるので、クレンジング後もつっぱりません。",
                 "Our cleansing-lotion formula with three peach extracts — peach juice, peach kernel and peach leaf — for moisture. Fresh and gentle, so skin never feels tight after cleansing."),
          points=[(t("3種類の桃エキス", "Three peach extracts"), t("モモ果汁・モモ種子エキス・モモ葉エキスが、クレンジング中も肌にうるおいを与えます。", "Peach juice, kernel and leaf extracts keep skin moist while you cleanse."), None),
                  (t("ダブル洗顔不要", "No double cleanse"), t("拭き取った後の洗顔は不要。まつエクの方もお使いいただけます。", "No need to wash afterwards, and safe with eyelash extensions."), None),
                  (t("やさしい処方", "Gentle formula"), t("無着色・オイルフリー・アルコールフリー。", "Colorant-free, oil-free and alcohol-free."), None)],
          free=t(["無着色", "オイルフリー", "アルコールフリー"], ["Colorant-free", "Oil-free", "Alcohol-free"]),
          usage=_WIPE(),
          inci="水、DPG、PEG-7（カプリル/カプリン酸）グリセリズ、PEG-8（カプリル酸/カプリン酸）グリセリズ、ラウリルベタイン、フェノキシエタノール、メチルパラベン、クエン酸Na、香料、クエン酸、BG、モモ果汁、モモ種子エキス、モモ葉エキス"),

     dict(slug="hatomugi-skin-conditioner", legacy="p3", rk="10001008-set", cat="lotion", series="hatomugi", new=False, soon=False,
          img="hanajirushi_hsc.jpg", rimg=RIMG + "imgrc0129957473.jpg",
          name=t("花印ハトムギ化粧水", "Hatomugi Skin Conditioner"), sub=t("Hatomugi Skin Conditioner", "花印ハトムギ化粧水"),
          size="500mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("北海道産ハトムギ", "Hokkaido coix seed"), t("大容量", "Large size")],
          short=t("北海道産ハトムギ種子エキスを高配合。顔にも全身にも使える500mL。", "Rich in Hokkaido coix seed extract. A generous 500mL for face and body."),
          catch=t("毎日たっぷり、<br>惜しみなく。", "Generous enough<br><em>for every day.</em>"),
          desc=t("厳選した北海道産ハトムギ種子エキス（保湿成分）を高配合。ヨモギ葉エキス・ヒキオコシ葉/茎エキス・ユズ果実エキスが肌にうるおいを与え、なめらかで明るい印象の肌へ導きます。肌と同じ弱酸性で、べたつかないみずみずしい使用感です。",
                 "Rich in carefully selected coix seed extract from Hokkaido, with mugwort leaf, isodon and yuzu extracts for moisture and a smooth, bright look. Weakly acidic like skin, with a fresh, non-sticky feel."),
          points=[(t("北海道産ハトムギ", "Hokkaido coix seed"), t("保湿成分のハトムギ種子エキスを高配合。乾燥から肌を守り、肌荒れを防ぎます。", "A high level of coix seed extract protects against dryness and prevents rough skin."), None),
                  (t("3つの植物エキス", "Three plant extracts"), t("ヨモギ葉・ヒキオコシ葉/茎・ユズ果実のエキスが、うるおいと透明感のある肌へ。", "Mugwort leaf, isodon and yuzu fruit extracts for moist, clear-looking skin."), None),
                  (t("使い方いろいろ", "Many ways to use it"), t("ブースター、コットンパック、全身ローション、日焼け後のほてりのケアにも。", "As a booster, a cotton pack, a body lotion, or to cool skin after the sun."), None)],
          free=_HATO_FREE(),
          usage=t("適量を手に取り、顔・体全体になじませてください。", "Smooth a little over the face and body."),
          inci="水、DPG、グリセリン、メチルパラベン、エタノール、（スチレン/アクリレーツ）コポリマー、クエン酸Na、クエン酸、BG、ヨモギ葉エキス、ヒキオコシ葉/茎エキス、ハトムギ種子エキス、ユズ果実エキス"),

     dict(slug="hatomugi-essence", legacy=None, rk="10001051", cat="lotion", series="hatomugi", new=True, soon=False,
          img=None, rimg=RIMG + "mem_product/11741495/imgrc0135285519.jpg",
          name=t("花印ハトムギ豊潤美容液", "Hatomugi Rich Essence"), sub=t("Hatomugi Rich Essence", "花印ハトムギ豊潤美容液"),
          size="200mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("新商品", "New")],
          short=t("ハトムギ化粧水と相性のよい、とろみのあるジェル美容液。", "A silky gel essence made to follow the Hatomugi lotion."),
          catch=t("表面はさらり、<br>内側はしっとり。", "Light on the surface,<br><em>moist underneath.</em>"),
          desc=t("国産ハトムギ種子エキス（保湿成分）を高配合した、とろみのあるジェル状美容液。伸びがよく、かさつく部分にもすっとなじみ、使用後もべたつきません。お客様の声から生まれた、ハトムギシリーズの美容液です。",
                 "A silky gel essence rich in Japanese coix seed extract. It spreads easily, settles into dry patches and leaves no stickiness. Made because customers asked for a serum to go with the Hatomugi lotion."),
          points=[(t("ハトムギ種子エキス高配合", "Rich in coix seed"), t("天然保湿因子を補い、角質層の水分量を高めて、みずみずしい肌を保ちます。", "Supports skin's natural moisturising factors for lasting hydration."), None),
                  (t("3種類の発酵エキス", "Three fermented extracts"), t("ハトムギ種子発酵液・コメ発酵液・乳酸桿菌/豆乳発酵液で、肌のバランスを整えます。", "Fermented coix seed, rice and soy milk extracts help keep skin balanced."), None),
                  (t("9種類のボタニカル", "Nine botanicals"), t("ヨモギ葉・ユズ果実・ユキノシタ・ツボクサ葉エキス、バクチオールなどを配合。", "Including mugwort, yuzu, saxifrage, centella and bakuchiol."), None)],
          free=_HATO_FREE(),
          usage=t("化粧水などでお肌を整えた後、適量を手にとり、お肌全体になじませてください。", "After your lotion, smooth a little over the whole face."),
          inci="水、DPG、グリセリン、グリセレス-26、ペンチレングリコール、イヌリン、PEG-60水添ヒマシ油、BG、フェノキシエタノール、(アクリレーツ/アクリル酸アルキル（C10-30）)クロスポリマー、水酸化K、オキシベンゾン-4、シロキクラゲ多糖体、ハトムギ種子エキス、ツボクサ葉エキス、バクチオール、コメ発酵液、異性化糖、クエン酸、乳酸桿菌/豆乳発酵液、ロドデンドロンフェルギネウムエキス、ユキノシタエキス、ヨモギ葉エキス、サッカロミセス/ハトムギ種子発酵液、ユズ果実エキス、クエン酸Na"),

     dict(slug="hatomugi-cream", legacy=None, rk="10001050", cat="cream", series="hatomugi", new=True, soon=False,
          img=None, rimg=RIMG + "mem_item/hatomugi-cream-mpr.jpg",
          name=t("花印ハトムギクリーム", "Hatomugi Cream"), sub=t("Hatomugi Cream", "花印ハトムギクリーム"),
          size="100g", kind=t("化粧品", "Cosmetic"),
          badges=[t("新商品", "New")],
          short=t("ハトムギ化粧水と一緒に使える、みずみずしい保湿クリーム。", "A light moisturising cream to pair with the Hatomugi lotion."),
          catch=t("伸びがよく、<br>べたつかない。", "Spreads easily,<br><em>never sticky.</em>"),
          desc=t("「ハトムギ化粧水と一緒に使えるクリームが欲しい」というお客様の声から生まれた保湿クリーム。日本産ハトムギ種子エキスを高配合し、3つの発酵エキスと和漢植物エキス、植物由来スクワランでうるおいを守ります。",
                 "Made because customers asked for a cream to go with the Hatomugi lotion. Rich in Japanese coix seed extract, with three fermented extracts, traditional botanicals and plant-derived squalane to lock in moisture."),
          points=[(t("ハトムギ種子エキス高配合", "Rich in coix seed"), t("角層の水分量を高め、肌をみずみずしく健やかに保ちます。", "Keeps the skin's surface layer hydrated and healthy-looking."), None),
                  (t("3つの発酵エキス", "Three fermented extracts"), t("ハトムギ種子発酵液・コメ発酵液・豆乳発酵液を独自に配合。", "Fermented coix seed, rice and soy milk extracts."), None),
                  (t("植物由来スクワラン", "Plant-derived squalane"), t("うるおいを閉じ込め、乾燥から肌を守ります。", "Seals moisture in and protects against dryness."), None)],
          free=_HATO_FREE(),
          usage=t("化粧水の後に適量を手に取り、顔・体全体になじませてください。入浴後や日焼け後のボディケアにも。", "After your lotion, smooth a little over the face and body. Also good after a bath or a day in the sun."),
          inci="水、スクワラン、グリセリン、BG、ジグリセリン、ステアリン酸ポリグリセリル-10、カルボマー、ステアリン酸グリセリル、ペンチレングリコール、メチルパラベン、フェノキシエタノール、水酸化K、オキシベンゾン-4、ハトムギ種子エキス、ツボクサ葉エキス、コメ発酵液、異性化糖、乳酸桿菌/豆乳発酵液、ユキノシタエキス、ヨモギ葉エキス、サッカロミセス/ハトムギ種子発酵液、ユズ果実エキス、クエン酸Na、クエン酸"),

     dict(slug="booster-conditioner", legacy=None, rk="1003335", cat="lotion", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "mem_item/imgrc0099431473.jpg",
          name=t("花印ブースターコンディショナー", "Booster Conditioner"), sub=t("Booster Conditioner — pre-serum", "花印ブースターコンディショナー（導入美容液）"),
          size="48mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("導入美容液", "Pre-serum")],
          short=t("化粧水の前のひと手間で、次のスキンケアがなじみやすい肌に。", "One step before your lotion, so the rest of your routine settles in."),
          catch=t("化粧水の前に、<br>ひと押し。", "One step<br><em>before your lotion.</em>"),
          desc=t("洗顔後、化粧水の前に使う導入美容液。ナノキューブなどの成分が肌をやわらかく整え、後に使うスキンケアがなじみやすい肌に。アーティチョーク葉エキスが肌を引き締め、5種類の保湿成分がキメを整えます。",
                 "A pre-serum for after cleansing and before your lotion. Ingredients such as NanoCube soften skin so the products that follow settle in better. Artichoke leaf extract tightens, and five moisturisers smooth the skin's texture."),
          points=[(t("スキンケアの前に", "Before your routine"), t("肌をやわらかく整え、化粧水や美容液がなじみやすい状態に。", "Softens skin so your lotion and serum settle in."), None),
                  (t("引き締め成分", "Tightening"), t("アーティチョーク葉エキスが肌と毛穴を引き締めます。", "Artichoke leaf extract tightens skin and pores."), None),
                  (t("5つの保湿成分", "Five moisturisers"), t("イザヨイバラ・ハナビラタケ・キリンサイ・オウゴン根エキス、ビサボロール。", "Rosa roxburghii, cauliflower mushroom, kappaphycus and scutellaria extracts, and bisabolol."), None)],
          free=t(["パラベンフリー", "着色料フリー", "香料フリー"], ["Paraben-free", "Colorant-free", "Fragrance-free"]),
          usage=t("洗顔後、化粧水などをつける前にお使いください。手のひらに適量（2〜3プッシュ）をとり、やさしくお顔全体になじませてください。", "After cleansing and before your lotion, press 2–3 pumps into your palms and smooth gently over the face."),
          inci="水、BG、グリセリン、エタノール、ジメチコン、ペンチレングリコール、PEG-150、ベタイン、シクロヘキサン-1,4-ジカルボン酸ビスエトキシジグリコール、（アクリレーツ/アクリル酸アルキル（C10-30））クロスポリマー、水酸化K、オクチルドデセス-20、スクワラン、ビサボロール、水酸化レシチン、アーチチョーク葉エキス、オウゴン根エキス、イザヨイバラエキス、ハナビラタケエキス、テトラヒドロファルネシル酢酸グリセリル、カッパフィカスアルバレジエキス、ザクロ果実エキス、トコフェロール、フェノキシエタノール"),

     dict(slug="moisture-face-cream", legacy=None, rk="10000072", cat="cream", series="amino", new=False, soon=False,
          img=None, rimg=RIMG + "mem_item/imgrc0117465392.jpg",
          name=t("花印モイスチュアフェイスクリーム", "Moisture Face Cream"), sub=t("Moisture Face Cream — Amino Acid", "花印モイスチュアフェイスクリーム"),
          size="80g", kind=t("化粧品", "Cosmetic"),
          badges=[t("セラミド3種", "3 ceramides"), t("アミノ酸11種", "11 amino acids")],
          short=t("アミノ酸11種類とヒト型セラミド3種類を配合した保湿クリーム。", "A moisturising cream with 11 amino acids and three human-type ceramides."),
          catch=t("乾燥を防いで、<br>みずみずしい肌に。", "Keeps dryness away,<br><em>keeps skin fresh.</em>"),
          desc=t("乾燥を防ぎ、みずみずしく透明感のある肌に導くフェイスクリーム。アミノ酸11種類、ヒアルロン酸3種類、水溶性コラーゲン、ヒト型セラミド3種類、ハトムギエキスを配合。リニューアルで保湿力を高めました。",
                 "A face cream that guards against dryness for fresh, clear-looking skin. With 11 amino acids, three hyaluronic acids, soluble collagen, three human-type ceramides and coix seed extract — renewed for more moisture."),
          points=[(t("アミノ酸11種類", "11 amino acids"), t("肌のうるおいを支えるアミノ酸を11種類配合。", "Eleven amino acids that support skin's moisture."), None),
                  (t("ヒアルロン酸3種類", "Three hyaluronic acids"), t("アセチルヒアルロン酸Na・ヒアルロン酸Na・加水分解ヒアルロン酸。", "Acetyl, sodium and hydrolysed hyaluronic acid."), None),
                  (t("ヒト型セラミド3種類", "Three ceramides"), t("セラミドAP・NP・EOPに、水溶性コラーゲンとハトムギエキス。", "Ceramides AP, NP and EOP, with soluble collagen and coix seed extract."), None)],
          free=[],
          usage=None,
          inci="水、エチルヘキサン酸セチル、BG、グリセリン、トリ（カプリル酸/カプリン酸）グリセリル、ダイマージリノール酸（フィトステリル/イソステアリル/セチル/ステアリル/ベヘニル）、セテアリルアルコール、ベヘニルアルコール、マルチトール、水添パーム油、脂肪酸グリセリズ、マカデミアナッツ脂肪酸フィトステリル、ステアリン酸グリセリル（SE）、セテス-20、アセチルヒアルロン酸Na、ヒアルロン酸Na、ハトムギ種子エキス、ペンチレングリコール、PCA-Na、アルギニン、アスパラギン酸、PCA、グリシン、アラニン、セリン、バリン、イソロイシン、トレオニン、プロリン、ヒスチジン、フェニルアラニン、エチルヘキシルグリセリン、加水分解ヒアルロン酸、水溶性コラーゲン、ダイズステロール、ラウロイルグルタミン酸ジ(フィトステリル/オクチルドデシル)、セラミドNP、セラミドAP、フィトスフィンゴシン、セラミドEOP、ジフェニルシロキシフェニルトリメチコン、ジメチコン、乳酸Na、コレステロール、キサンタンガム、カルボマー、水添レシチン、ラウロイルラクチレートNa、エタノール、水酸化K、トコフェロール、EDTA-2Na、メチルパラベン、フェノキシエタノール、カラメル、シアノコバラミン"),

     dict(slug="wrinkle-eye-cream", legacy=None, rk="10000074", cat="cream", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "mem_product/wrinkle-repair-cream/imgrc0131518738.jpg",
          name=t("花印薬用リンクルアイクリーム", "Medicated Wrinkle Eye Cream"), sub=t("Whitening &amp; Wrinkle Repair Cream", "花印薬用リンクルアイクリーム"),
          size="30g", kind=t("医薬部外品", "Quasi-drug"),
          badges=[t("医薬部外品", "Quasi-drug"), t("ナイアシンアミド", "Niacinamide")],
          short=t("有効成分ナイアシンアミドで、美白とシワ改善のWアプローチ。", "Niacinamide for brightening and wrinkle care in one eye cream."),
          catch=t("美白とシワ改善を、<br>ひとつの目元ケアで。", "Brightening and wrinkle care<br><em>in one eye cream.</em>"),
          desc=t("有効成分ナイアシンアミドを配合した薬用アイクリーム。メラニンの生成を抑えてシミ・そばかすを防ぎ、シワを改善します。12種類の保湿成分を配合し、目元にぴったり密着してうるおい感が続きます。",
                 "A medicated eye cream with niacinamide as its active ingredient: it suppresses melanin to prevent dark spots and freckles, and improves wrinkles (approved quasi-drug claims in Japan). Twelve moisturisers keep the eye area comfortable."),
          points=[(t("有効成分ナイアシンアミド", "Active: niacinamide"), t("美白（メラニンの生成を抑え、シミ・そばかすを防ぐ）とシワ改善の効能。", "Brightening (prevents dark spots and freckles) and wrinkle improvement."), None),
                  (t("12種類の保湿成分", "Twelve moisturisers"), t("プルーン酵素分解物、サクラ葉抽出液、ヨクイニンエキスなど。", "Including prune, cherry leaf and coix seed extracts."), None),
                  (t("目元以外にも", "Not only for the eyes"), t("おでこや眉間、口周りなど、気になる部分にもお使いいただけます。", "Also for the forehead, between the brows and around the mouth."), None)],
          free=t(["香料フリー", "着色料フリー", "アルコールフリー", "鉱物油フリー", "パラベンフリー"], ["Fragrance-free", "Colorant-free", "Alcohol-free", "Mineral-oil free", "Paraben-free"]),
          usage=t("適量（米粒大）を目元など肌の気になるところになじませてください。気になる部分には重ね付けしてください。", "Smooth a rice-grain amount over the eye area or other areas of concern; layer where needed."),
          inci="有効成分：ナイアシンアミド　その他の成分：精製水、1,3-ブチレングリコール、ジグリセリン、濃グリセリン、シュガースクワラン、ベヘニルアルコール、イソノナン酸イソノニル、ポリオキシエチレンソルビットミツロウ、親油型モノステアリン酸グリセリル、ステアリン酸、ジプロピレングリコール、トリステアリン酸ポリオキシエチレンソルビタン（20E.O.）、メチルポリシロキサン、トリポリヒドロキシステアリン酸ジペンタエリスリチル、アマチャヅルエキス、レモングラス抽出液、ジエチレントリアミン五酢酸五ナトリウム液、ポリエチレングリコール1540、グリセリンモノ2-エチルヘキシルエーテル、グリセリン脂肪酸エステル、プルーン酵素分解物、サクラ葉抽出液、ノバラエキス、キウイエキス、ヒメフウロエキス、メマツヨイグサ抽出液、オウゴンエキス、エイジツエキス、ヨクイニンエキス、ビルベリー葉エキス、N-ステアロイル-L-グルタミン酸ナトリウム、キサンタンガム、モノオレイン酸ポリオキシエチレンソルビタン（20E.O.）、フェノキシエタノール"),

     dict(slug="amino-face-mask", legacy="p2", rk="10000057", cat="mask", series="amino", new=False, soon=False,
          img="hanajirushi_smfm.jpg", rimg=RIMG + "mem_item/item_57_1.jpg",
          name=t("花印スーパーモイスチュアフェイスマスク", "Super Moisture Face Mask"), sub=t("Super Moisture Face Mask — Amino Acid 80g", "花印スーパーモイスチュアフェイスマスク AMINO ACID"),
          size="80g", kind=t("化粧品", "Cosmetic"),
          badges=[t("6in1", "6-in-1"), t("オールインワン", "All-in-one")],
          short=t("肌になじませると美容液に変わる、6つの機能のジェルマスク。", "A six-in-one gel mask that turns into a serum on the skin."),
          catch=t("うるおいチャージで、<br>しっとりなめらかに。", "A moisture charge<br><em>for soft, smooth skin.</em>"),
          desc=t("化粧水・乳液・美容液・クリーム・化粧下地・パックの6つの機能をひとつに。アミノ酸、加水分解コラーゲン、ヒアルロン酸Na、カミツレ花エキスが、乾燥しがちな肌をしっとりなめらかでハリのある肌に整えます。",
                 "Lotion, emulsion, serum, cream, primer and pack in one. Amino acids, hydrolysed collagen, hyaluronic acid and chamomile extract leave dry skin soft, smooth and firm-looking."),
          points=[(t("6つの機能", "Six in one"), t("化粧水・乳液・美容液・クリーム・化粧下地・パック。", "Lotion, emulsion, serum, cream, primer and pack."), None),
                  (t("アミノ酸とコラーゲン", "Amino acids &amp; collagen"), t("アミノ酸、加水分解コラーゲン、ヒアルロン酸Naを配合。", "With amino acids, hydrolysed collagen and hyaluronic acid."), None),
                  (t("2通りの使い方", "Two ways to use it"), t("夜のパックにも、朝のオールインワンジェルにも。", "A night pack or a morning all-in-one gel."), None)],
          free=[],
          usage=_MASK_USE(),
          inci="水、ジメチコン、BG、エタノール、シクロペンタシロキサン、（ジメチコン、（PEG-10/15））クロスポリマー、加水分解コラーゲン、ヒアルロン酸Na、カミツレ花エキス、ベタイン、PCA-Na、セリン、グリシン、グルタミン酸、アラニン、リシン、アルギニン、トレオニン、プロリン、フラーレン、ソルビトール、ペンチレングリコール、塩化Na、クエン酸、クエン酸Na、トコフェロール、PVP、フェノキシエタノール、メチルパラベン、プロピルパラベン"),

     dict(slug="super-moisture-gel", legacy=None, rk="10000002", cat="mask", series="amino", new=False, soon=False,
          img=None, rimg=RIMG + "mem_product/13773545/imgrc0159567170.jpg",
          name=t("花印スーパーモイスチュアフェイスマスク 200g", "Super Moisture Face Mask 200g"), sub=t("Super Moisture Face Mask — All-in-one Gel", "オールインワンジェル・ジェルパック"),
          size="200g", kind=t("化粧品", "Cosmetic"),
          badges=[t("オールインワン", "All-in-one"), t("大容量", "Large size")],
          short=t("パックにも、オールインワンジェルにも。うるおいチャージの200g。", "A pack or an all-in-one gel — 200g of moisture."),
          catch=t("乾燥、キメ、弾力が<br>気になる肌へ。", "For dry skin,<br><em>texture and firmness.</em>"),
          desc=t("乾燥しがちな肌、キメや弾力が気になる肌へ。アミノ酸、ヒアルロン酸Na、水溶性コラーゲン、セラミドを配合し、しっとりなめらかでハリのある肌に整えます。たっぷり使える200gです。",
                 "For dry skin and skin concerned with texture and firmness. Amino acids, hyaluronic acid, soluble collagen and ceramides leave it soft, smooth and firm-looking — in a generous 200g jar."),
          points=[(t("アミノ酸とセラミド", "Amino acids &amp; ceramides"), t("アミノ酸、セラミド3種、水溶性コラーゲン、ヒアルロン酸Na。", "Amino acids, three ceramides, soluble collagen and hyaluronic acid."), None),
                  (t("3つの使い方", "Three ways to use it"), t("パック、オールインワンジェル、化粧下地として。", "As a pack, an all-in-one gel or a make-up base."), None),
                  (t("たっぷり200g", "A generous 200g"), t("顔全体にたっぷり塗れる大容量。", "Enough to apply generously every day."), None)],
          free=[],
          usage=_MASK_USE(),
          inci="水、ジメチコン、BG、シクロペンタシロキサン、DPG、グリセリン、（ジメチコン/（PEG-10/15））クロスポリマー、（ジメチコン/ビニルジメチコン）クロスポリマー、プルラン、マルチトール、ヒノキ水、ローズマリー葉水、オレンジフラワー水、PCA-Na、アスコルビルグルコシド、アルギニン、アスパラギン酸、PCA、グリシン、アラニン、ヒアルロン酸Na、セリン、バリン、イソロイシン、トレオニン、プロリン、ヒスチジン、フェニルアラニン、ポリクオタニウム-51、水溶性コラーゲン、グリチルリチン酸2K、セラミド3、コレステロール、セラミド6Ⅱ、フィトスフィンゴシン、セラミド1、塩化Na、海水、温泉水、乳酸Na、カルボマー、キサンタンガム、ラウロイル乳酸Na、クエン酸Na、クエン酸、トコフェロール、ペンテト酸5Na、フェノキシエタノール、メチルパラベン、エチルパラベン、プロピルパラベン"),

     dict(slug="clay-pack", legacy=None, rk="10000105", cat="mask", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "11261505/11294025/imgrc0129945835.jpg",
          name=t("花印クレーパック", "Volcanic Clay Pack"), sub=t("Volcanic Clay Pack", "花印クレーパック（火山灰マスク）"),
          size="195g", kind=t("化粧品", "Cosmetic"),
          badges=[t("洗い流すタイプ", "Wash-off"), t("モロッコ溶岩クレイ", "Moroccan lava clay")],
          short=t("4種類のクレイが毛穴の汚れを吸着する、洗い流すタイプのパック。", "A wash-off pack with four clays that lift dirt from pores."),
          catch=t("週に1〜2回の、<br>毛穴のスペシャルケア。", "A weekly treat<br><em>for your pores.</em>"),
          desc=t("吸着力と洗浄力に優れた4種類のクレイを配合。モロッコ溶岩クレイ（ガッスール）が余分な皮脂や毛穴の汚れを吸着し、肌を引き締めます。ミネラルを含み、潤いを残してなめらかな肌に整えます。",
                 "Four absorbent clays, including Moroccan lava clay (ghassoul), lift excess sebum and dirt from pores and tighten the skin. Rich in minerals, it leaves skin smooth without stripping moisture."),
          points=[(t("4種類のクレイ", "Four clays"), t("余分な皮脂や毛穴の奥の汚れを吸着します。", "Lift excess sebum and dirt from deep in the pores."), None),
                  (t("モロッコ溶岩クレイ", "Moroccan lava clay"), t("多孔質構造で皮脂を吸着し、ミネラルで潤いを残します。", "A porous clay that absorbs sebum, with minerals that leave moisture behind."), None),
                  (t("たっぷり195g", "A generous 195g"), t("ピールオフではなく、洗い流すタイプです。日本製。", "A wash-off pack, not a peel-off. Made in Japan."), None)],
          free=[],
          usage=t("洗顔後、水分をふき取ってから適量をとり、皮脂や毛穴の気になるTゾーン・Uゾーンに均一に伸ばします。そのまま5〜10分置き、ぬるま湯でくるくるなじませて洗い流します。週に1〜2回のご使用をおすすめします。",
                  "After cleansing, pat dry and spread evenly over the T-zone and U-zone. Leave for 5–10 minutes, then massage gently with lukewarm water and rinse. Use once or twice a week."),
          inci="水、カオリン、グリセリン、BG、ベントナイト、グリコシルトレハロース、酸化チタン、加水分解水添デンプン、モロッコ溶岩クレイ、フェノキシエタノール、ヒドロキシプロピルメチルセルロース、メチルパラベン、香料、エチルパラベン、水酸化Al、ジミリスチン酸Al、海シルト、酸化鉄、酸化クロム"),

     dict(slug="uv-primer", legacy=None, rk="10001006-copyy", cat="uv", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "mem_product/10049686/4941.jpg",
          name=t("花印トーンアップUVプライマー", "Tone-up UV Primer"), sub=t("Tone-up UV Primer SPF50+ PA++++", "花印トーンアップUVプライマー"),
          size="35g", kind=t("化粧品", "Cosmetic"),
          badges=["SPF50+・PA++++", t("ウォータープルーフ", "Waterproof")],
          short=t("SPF50+・PA++++。ピンクパールで明るく見せるクリーム下地。", "SPF50+ PA++++ — a pink-pearl primer for brighter-looking skin."),
          catch=t("光をコントロールして、<br>肌を明るく。", "Light-controlling,<br><em>for brighter skin.</em>"),
          desc=t("色ムラやくすみ、毛穴をぼかし、明るくツヤのある肌に見せるクリームタイプの化粧下地。SPF50+・PA++++で日やけによるシミ・そばかすを防ぎます。ウォータープルーフでありながら、普段の洗顔料や石けんで落とせます。",
                 "A cream primer that blurs uneven tone, dullness and pores for a bright, dewy look. SPF50+ PA++++ prevents dark spots and freckles caused by the sun. Waterproof, yet it washes off with your usual cleanser or soap."),
          points=[(t("SPF50+・PA++++", "SPF50+ PA++++"), t("最高レベルの紫外線防御効果で、日やけによるシミ・そばかすを防ぎます。", "The highest UV protection rating, preventing sun-induced spots and freckles."), None),
                  (t("トーンアップ", "Tone-up"), t("血色感のあるピンクカラーとパールで、立体的なツヤ肌に。", "A rosy pink tint and pearl for a dimensional glow."), None),
                  (t("崩れにくく、落としやすい", "Lasting, easy to remove"), t("皮脂吸着パウダーでメイクが長持ち。ウォータープルーフなのに洗顔料でオフ。", "Sebum-absorbing powder keeps make-up in place; waterproof yet washes off with cleanser."), "patent")],
          free=t(["鉱物油不使用", "石油系合成界面活性剤不使用", "動物由来原料不使用", "無香料"], ["Mineral-oil free", "No petroleum surfactants", "No animal-derived ingredients", "Fragrance-free"]),
          usage=t("パール一粒大を手のひらに取り、おでこ・鼻先・両頬・あごの5点にのせ、内側から外側へやさしく伸ばします。頬骨など高いところから塗ると立体的に仕上がります。",
                  "Take a pearl-sized amount, dot it on the forehead, nose, cheeks and chin, and blend from the centre outwards. Starting on the cheekbones gives a more sculpted finish."),
          inci="水、メトキシケイヒ酸エチルヘキシル、BG、ジエチルアミノヒドロキシベンゾイル安息香酸ヘキシル、イソノナン酸イソノニル、エタノール、イソステアリン酸、トリエチルヘキサノイン、ビスエチルヘキシルオキシフェノールメトキシフェニルトリアジン、水酸化K、フェノキシエタノール、（アクリレーツ/アクリル酸アルキル（C10-30））クロスポリマー、メチルパラベン、ステアリン酸、キサンタンガム、アルミナ、トコフェロール、トリエトキシカプリリルシラン、イノシトール、セラミドNP、グリセリン、アクリレーツクロスポリマー、ザクロ果実エキス、ノイバラ果実エキス、酸化チタン、酸化鉄、シリカ、マイカ、水酸化Al、赤227"),

     dict(slug="vital-gel-men", legacy=None, rk="10000042", cat="mens", series=None, new=False, soon=False,
          img=None, rimg=RIMG + "mem_item/item_42_01.jpg",
          name=t("花印バイタル オールインワンジェル", "Vital All-in-One Gel"), sub=t("Vital All-in-One Gel for Men", "花印バイタル オールインワンジェル（メンズ）"),
          size="80mL", kind=t("化粧品", "Cosmetic"),
          badges=[t("メンズ", "For men"), t("オールインワン", "All-in-one")],
          short=t("これ1本で。テカリとべたつきを抑える、メンズのジェルクリーム。", "One step for men: a gel cream that keeps shine and stickiness down."),
          catch=t("1本で、<br>男の肌に。", "One bottle<br><em>for men's skin.</em>"),
          desc=t("パウダーが余分な皮脂を吸着し、テカリやべたつきを抑えてさらさらの肌に仕上げるジェル状クリーム。爽快なメントールが肌を引き締め、不快なべたつきを長時間抑えます。",
                 "A gel cream whose powder absorbs excess sebum, keeping shine and stickiness down for a matte finish. Cooling menthol tightens the skin and keeps it feeling fresh for hours."),
          points=[(t("皮脂吸着パウダー", "Sebum-absorbing powder"), t("テカリ・べたつきを抑えて、さらさらの仕上がり。", "Controls shine for a matte finish."), None),
                  (t("爽快メントール", "Cooling menthol"), t("肌を引き締め、すっきりとした使用感。", "Tightens skin with a refreshing feel."), None),
                  (t("オールインワン", "All-in-one"), t("化粧水・乳液・美容液の役割を1本で。", "Lotion, emulsion and serum in one step."), None)],
          free=[],
          usage=None,
          inci="水、グリセリン、パルミチン酸エチルヘキシル、ペンチレングリコール、タルク、BG、ヘキサ（ヒドロキシステアリン酸/ステアリン酸/ロジン酸）ジペンタエリスリチル、アルギニン、ステアリン酸ポリグリセリル-10、カルボマー、ヒドロキシプロピルメチルセルロース、メチルパラベン、香料、メントール、ジメチコン、カンフル、シリカ、ノイバラ果実エキス、チャ葉エキス、ダイズ種子エキス、ハマメリスエキス"),

     dict(slug="cleansing-oil", legacy="p4", rk=None, cat="cleansing", series=None, new=False, soon=True,
          img=None, rimg=None,
          name=t("花印クレンジングオイル", "Cleansing Oil"), sub=t("Cleansing Oil", "花印クレンジングオイル"),
          size=None, kind=None, badges=[t("近日公開", "Coming soon")],
          short=t("中国市場の看板アイテム。日本公式サイトへの掲載準備中です。", "Our signature item in the China market. Details coming soon."),
          catch="", desc="", points=[], free=[], usage=None, inci=None),
    ]

def BY_SLUG():
    return {p["slug"]: p for p in PRODUCTS13()}

def BY_LEGACY():
    return {p["legacy"]: p for p in PRODUCTS13() if p["legacy"]}

FEATURED = ["cleansing-lotion-ma", "hatomugi-skin-conditioner", "hatomugi-essence", "hatomugi-cream", "amino-face-mask", "uv-primer"]

def page_of(p):
    return f"product-{p['slug']}.html"

def photo(p, img_base):
    """URL of the product photo: our own packshot when we have one, else the Rakuten image."""
    if p["img"]:
        return img_base + p["img"]
    return p["rimg"]

def TBC(p):
    """Facts still to confirm, per product (shown as 要確認 chips in the specification)."""
    return [(t("全成分（INCI表記）", "Full INCI list"), tbd("掲載予定", "To be listed")),
            (t("使用期限", "Shelf life"), t("未開封 ", "Unopened ") + tbd() + t("　開封後 ", " · After opening ") + tbd()),
            (t("JANコード", "JAN / EAN"), tbd()),
            (t("入数・ケースサイズ", "Case pack"), tbd()),
            (t("製造販売元", "Manufacturer"), tbd())]
