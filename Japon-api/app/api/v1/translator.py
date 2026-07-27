from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import re

router = APIRouter(prefix="/translator", tags=["translator"])


class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "es"


def has_japanese(text: str) -> bool:
    return bool(re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uF900-\uFAFF]', text))


TRANSLATIONS = {
    "básico": [
        {"japanese": "はい", "romaji": "hai", "spanish": "Sí", "pronunciation": "hai"},
        {"japanese": "いいえ", "romaji": "iie", "spanish": "No", "pronunciation": "ee-eh"},
        {"japanese": "すみません", "romaji": "sumimasen", "spanish": "Disculpe / Perdón", "pronunciation": "soo-mee-mah-sen"},
        {"japanese": "ありがとうございます", "romaji": "arigatou gozaimasu", "spanish": "Muchas gracias", "pronunciation": "ah-ree-gah-toh goh-zai-mahs"},
        {"japanese": "こんばんは", "romaji": "konbanwa", "spanish": "Buenas noches", "pronunciation": "kohn-bahn-wah"},
        {"japanese": "おはようございます", "romaji": "ohayou gozaimasu", "spanish": "Buenos días", "pronunciation": "oh-hah-yoh goh-zai-mahs"},
        {"japanese": "こんにちは", "romaji": "konnichiwa", "spanish": "Hola (día)", "pronunciation": "kohn-nee-chee-wah"},
        {"japanese": "さようなら", "romaji": "sayounara", "spanish": "Adiós", "pronunciation": "sah-yoh-nah-rah"},
        {"japanese": "お願いします", "romaji": "onegaishimasu", "spanish": "Por favor", "pronunciation": "oh-neh-gai-shee-mahs"},
        {"japanese": "大丈夫", "romaji": "daijoubu", "spanish": "Está bien / No hay problema", "pronunciation": "dai-joh-boo"},
        {"japanese": "はい、そうです", "romaji": "hai, sou desu", "spanish": "Sí, eso es", "pronunciation": "hai, soh des"},
        {"japanese": "違います", "romaji": "chigaimasu", "spanish": "No, es diferente", "pronunciation": "chee-gai-mahs"},
        {"japanese": "わかりました", "romaji": "wakarimashita", "spanish": "Entendido", "pronunciation": "wah-kah-ree-mah-shee-tah"},
        {"japanese": "わかりません", "romaji": "wakarimasen", "spanish": "No entiendo", "pronunciation": "wah-kah-ree-mah-sen"},
        {"japanese": "すみません、英語は話せますか？", "romaji": "sumimasen, eigo wa hanasemasu ka?", "spanish": "Disculpe, ¿habla inglés?", "pronunciation": "soo-mee-mah-sen, eh-goh wah hah-nah-seh-mahs kah"},
        {"japanese": "日本語が少しだけわかります", "romaji": "nihongo ga sukoshi dake wakarimasu", "spanish": "Entiendo un poco de japonés", "pronunciation": "nee-hohn-goh gah skoh-shee dah-keh wah-kah-ree-mahs"},
        {"japanese": "ありがとう", "romaji": "arigatou", "spanish": "Gracias (casual)", "pronunciation": "ah-ree-gah-toh"},
        {"japanese": "おねがいします", "romaji": "onegaishimasu", "spanish": "Por favor (casual)", "pronunciation": "oh-neh-gai-shee-mahs"},
        {"japanese": "はじめまして", "romaji": "hajimemashite", "spanish": "Mucho gusto (al conocer)", "pronunciation": "hah-jee-meh-mah-shee-teh"},
        {"japanese": "よろしくお願いします", "romaji": "yoroshiku onegaishimasu", "spanish": "Encantado de conocerle", "pronunciation": "yoh-roh-shee-koo oh-neh-gai-shee-mahs"},
    ],
    "restaurantes": [
        {"japanese": "メニューお願いします", "romaji": "menyuu onegaishimasu", "spanish": "La carta, por favor", "pronunciation": "men-yoo oh-neh-gai-shee-mahs"},
        {"japanese": "ご注文は", "romaji": "go-chuumon wa", "spanish": "¿Qué va a pedir?", "pronunciation": "goo-choo-mohn wah"},
        {"japanese": "これお願いします", "romaji": "kore onegaishimasu", "spanish": "Esto, por favor", "pronunciation": "koh-reh oh-neh-gai-shee-mahs"},
        {"japanese": "お会計お願いします", "romaji": "okaikei onegaishimasu", "spanish": "La cuenta, por favor", "pronunciation": "oh-kai-keh oh-neh-gai-shee-mahs"},
        {"japanese": "美味しい", "romaji": "oishii", "spanish": "Delicioso", "pronunciation": "oh-ee-shee"},
        {"japanese": "お勧めは何ですか", "romaji": "osusume wa nan desu ka", "spanish": "¿Qué me recomienda?", "pronunciation": "oh-soo-soo-meh wah nahn des kah"},
        {"japanese": "アレルギーがあります", "romaji": "arerugii ga arimasu", "spanish": "Tengo alergia", "pronunciation": "ah-reh-roo-gee gah ah-ree-mahs"},
        {"japanese": "ベジタリアンです", "romaji": "bejitarian desu", "spanish": "Soy vegetariano/a", "pronunciation": "beh-jee-tah-ree-ahn des"},
        {"japanese": "お水ください", "romaji": "omizu kudasai", "spanish": "Agua, por favor", "pronunciation": "oh-mee-zoo koo-dah-sai"},
        {"japanese": "辛くないでください", "romaji": "karakunai de kudasai", "spanish": "No picante, por favor", "pronunciation": "kah-rah-koo-nai deh koo-dah-sai"},
        {"japanese": "おすすめは何ですか？", "romaji": "osusume wa nan desu ka?", "spanish": "¿Qué me recomienda?", "pronunciation": "oh-soo-soo-meh wah nahn des kah"},
        {"japanese": "このメニューをください", "romaji": "kono menyuu wo kudasai", "spanish": "Este menú, por favor", "pronunciation": "koh-noh men-yoo oh koo-dah-sai"},
        {"japanese": "ビールをください", "romaji": "biiru wo kudasai", "spanish": "Una cerveza, por favor", "pronunciation": "bee-roo oh koo-dah-sai"},
        {"japanese": "日本酒をください", "romaji": "nihonshu wo kudasai", "spanish": "Sake, por favor", "pronunciation": "nee-hohn-shoo oh koo-dah-sai"},
        {"japanese": "お箸をください", "romaji": "ohashi wo kudasai", "spanish": "Palillos, por favor", "pronunciation": "oh-hah-shee oh koo-dah-sai"},
        {"japanese": "スプーンをください", "romaji": "supuun wo kudasai", "spanish": "Una cuchara, por favor", "pronunciation": "skoo-ohn oh koo-dah-sai"},
        {"japanese": "おしぼりをください", "romaji": "oshibori wo kudasai", "spanish": "Toallita húmeda, por favor", "pronunciation": "oh-shee-boh-ree oh koo-dah-sai"},
        {"japanese": "温かいものをください", "romaji": "atatakai mono wo kudasai", "spanish": "Algo caliente, por favor", "pronunciation": "ah-tah-tah-kai mo-noh oh koo-dah-sai"},
        {"japanese": "冷たいものをください", "romaji": "tsumetai mono wo kudasai", "spanish": "Algo frío, por favor", "pronunciation": "tsoo-meh-tai mo-noh oh koo-dah-sai"},
        {"japanese": "持ち帰りできますか？", "romaji": "mochikaeri dekimasu ka?", "spanish": "¿Puedo llevarme la comida?", "pronunciation": "mo-chee-kai-ree deh-kee-mahs kah"},
    ],
    "transporte": [
        {"japanese": "駅はどこですか", "romaji": "eki wa doko desu ka", "spanish": "¿Dónde está la estación?", "pronunciation": "eh-kee wah doh-koh des kah"},
        {"japanese": "東京までお願いします", "romaji": "Tokyo made onegaishimasu", "spanish": "A Tokio, por favor", "pronunciation": "toh-kyoh mah-deh oh-neh-gai-shee-mahs"},
        {"japanese": "いくらですか", "romaji": "ikura desu ka", "spanish": "¿Cuánto cuesta?", "pronunciation": "ee-koo-rah des kah"},
        {"japanese": "タクシーを呼んでください", "romaji": "takushii wo yonde kudasai", "spanish": "Llame un taxi, por favor", "pronunciation": "tak-shee oh yohn-deh koo-dah-sai"},
        {"japanese": "トイレはどこですか", "romaji": "toire wa doko desu ka", "spanish": "¿Dónde está el baño?", "pronunciation": "toi-reh wah doh-koh des kah"},
        {"japanese": "右", "romaji": "migi", "spanish": "Derecha", "pronunciation": "mee-jee"},
        {"japanese": "左", "romaji": "hidari", "spanish": "Izquierda", "pronunciation": "hee-dah-ree"},
        {"japanese": "まっすぐ", "romaji": "massugu", "spanish": "Todo recto", "pronunciation": "mahs-soo-goo"},
        {"japanese": "バス停はどこですか", "romaji": "basutei wa doko desu ka", "spanish": "¿Dónde está la parada del bus?", "pronunciation": "bah-soo-teh wah doh-koh des kah"},
        {"japanese": "JR Passはありますか", "romaji": "JR Pass wa arimasu ka", "spanish": "¿Tienen JR Pass?", "pronunciation": "jay-ah ruh pass wah ah-ree-mahs kah"},
        {"japanese": "次の駅はどこですか", "romaji": "tsugi no eki wa doko desu ka", "spanish": "¿Dónde está la siguiente estación?", "pronunciation": "tsoo-gee noh eh-kee wah doh-koh des kah"},
        {"japanese": "どこで降りますか", "romaji": "doko de orimasu ka", "spanish": "¿Dónde bajo?", "pronunciation": "doh-koh deh oh-ree-mahs kah"},
        {"japanese": "空港までお願いします", "romaji": "kuukou made onegaishimasu", "spanish": "Al aeropuerto, por favor", "pronunciation": "koo-koh mah-deh oh-neh-gai-shee-mahs"},
        {"japanese": "この電車は__に行きますか", "romaji": "kono densha wa __ ni ikimasu ka", "spanish": "¿Este tren va a __?", "pronunciation": "koh-noh den-shah wah __ nee ee-kee-mahs kah"},
        {"japanese": "切符をください", "romaji": "kippu wo kudasai", "spanish": "Un billete, por favor", "pronunciation": "keep-poo oh koo-dah-sai"},
        {"japanese": "片道です", "romaji": "katamichi desu", "spanish": "Solo ida", "pronunciation": "kah-tah-mee-chee des"},
        {"japanese": "往復です", "romaji": "oufuku desu", "spanish": "Ida y vuelta", "pronunciation": "oh-foo-koo des"},
        {"japanese": "ここで止まってください", "romaji": "koko de tomatte kudasai", "spanish": "Pare aquí, por favor", "pronunciation": "koh-koh deh toh-mah-teh koo-dah-sai"},
        {"japanese": "地図を見せてください", "romaji": "chizu wo misete kudasai", "spanish": "Muéstreme el mapa, por favor", "pronunciation": "chee-zoo oh mee-seh-teh koo-dah-sai"},
        {"japanese": "どの線ですか", "romaji": "dono sen desu ka", "spanish": "¿Qué línea es?", "pronunciation": "doh-noh sen des kah"},
    ],
    "compras": [
        {"japanese": "これはいくらですか", "romaji": "kore wa ikura desu ka", "spanish": "¿Cuánto cuesta esto?", "pronunciation": "koh-reh wah ee-koo-rah des kah"},
        {"japanese": "カードで払えますか", "romaji": "kaado de haraemasu ka", "spanish": "¿Puedo pagar con tarjeta?", "pronunciation": "kah-doh deh hah-rah-eh-mahs kah"},
        {"japanese": "割引はありますか", "romaji": "waribiki wa arimasu ka", "spanish": "¿Hay descuento?", "pronunciation": "wah-ree-bee-kee wah ah-ree-mahs kah"},
        {"japanese": "免税できますか", "romaji": "menzei dekimasu ka", "spanish": "¿Puedo hacer tax-free?", "pronunciation": "mehn-zeh deh-kee-mahs kah"},
        {"japanese": "試着してもいいですか", "romaji": "shichaku shitemo ii desu ka", "spanish": "¿Puedo probármelo?", "pronunciation": "shee-chak shee-teh-moh ee des kah"},
        {"japanese": "もう少し安くなりますか", "romaji": "mou sukoshi yasuku narimasu ka", "spanish": "¿Se puede más barato?", "pronunciation": "moh soo-koh-shee yah-soo-koo nah-ree-mahs kah"},
        {"japanese": "包んでください", "romaji": "tsutsunde kudasai", "spanish": "Envuélvalo, por favor", "pronunciation": "tsoo-tsoon-deh koo-dah-sai"},
        {"japanese": "大きいサイズはありますか", "romaji": "ookii saizu wa arimasu ka", "spanish": "¿Tiene talla grande?", "pronunciation": "oh-kee sah-ee-zoo wah ah-ree-mahs kah"},
        {"japanese": "これをください", "romaji": "kore wo kudasai", "spanish": "Esto, por favor", "pronunciation": "koh-reh oh koo-dah-sai"},
        {"japanese": "もっと見せてください", "romaji": "motto misete kudasai", "spanish": "Muésteme más, por favor", "pronunciation": "moht-toh mee-seh-teh koo-dah-sai"},
        {"japanese": "色はありますか", "romaji": "iro wa arimasu ka", "spanish": "¿Tiene otros colores?", "pronunciation": "ee-roh wah ah-ree-mahs kah"},
        {"japanese": "クレジットカードは使えますか", "romaji": "kurejitto kaado wa tsukaemasu ka", "spanish": "¿Aceptan tarjeta de crédito?", "pronunciation": "koo-reh-jee-toh kah-doh wah tsoo-kai-mahs kah"},
        {"japanese": "現金だけですか", "romaji": "genkin dake desu ka", "spanish": "¿Solo efectivo?", "pronunciation": "gen-keen dah-keh des kah"},
        {"japanese": "税金は含まれていますか", "romaji": "zeikin wa fukumarete imasu ka", "spanish": "¿El impuesto está incluido?", "pronunciation": "zeh-keen wah foo-koo-mah-reh-teh ee-mahs kah"},
        {"japanese": "返品できますか", "romaji": "henpin dekimasu ka", "spanish": "¿Puedo devolverlo?", "pronunciation": "hen-peen deh-kee-mahs kah"},
        {"japanese": "レシートをください", "romaji": "reshiito wo kudasai", "spanish": "El recibo, por favor", "pronunciation": "reh-shee-toh oh koo-dah-sai"},
        {"japanese": "送料はいくらですか", "romaji": "souryou wa ikura desu ka", "spanish": "¿Cuánto cuesta el envío?", "pronunciation": "soh-ree-yoh wah ee-koo-rah des kah"},
        {"japanese": "袋をください", "romaji": "fukuro wo kudasai", "spanish": "Una bolsa, por favor", "pronunciation": "foo-koo-roh oh koo-dah-sai"},
        {"japanese": "お土産は何がいいですか", "romaji": "omiyage wa nani ga ii desu ka", "spanish": "¿Qué souvenirs me recomienda?", "pronunciation": "oh-mee-yah-geh wah nah-nee gai ee des kah"},
        {"japanese": "Tax-freeはどこですか", "romaji": "Tax-free wa doko desu ka", "spanish": "¿Dónde está el tax-free?", "pronunciation": "takhs-free wah doh-koh des kah"},
    ],
    "emergencias": [
        {"japanese": "助けてください", "romaji": "tasukete kudasai", "spanish": "Ayúdeme, por favor", "pronunciation": "tah-soo-keh-teh koo-dah-sai"},
        {"japanese": "警察を呼んでください", "romaji": "keisatsu wo yonde kudasai", "spanish": "Llame a la policía, por favor", "pronunciation": "keh-sah-tsoo oh yohn-deh koo-dah-sai"},
        {"japanese": "救急車を呼んでください", "romaji": "kyuukyuusha wo yonde kudasai", "spanish": "Llame a una ambulancia, por favor", "pronunciation": "kyoo-kyoo-shah oh yohn-deh koo-dah-sai"},
        {"japanese": "病院はどこですか", "romaji": "byouin wa doko desu ka", "spanish": "¿Dónde está el hospital?", "pronunciation": "byoh-een wah doh-koh des kah"},
        {"japanese": "水が欲しい", "romaji": "mizu ga hoshii", "spanish": "Necesito agua", "pronunciation": "mee-zoo gah hoh-shee"},
        {"japanese": "日本語が話せません", "romaji": "nihongo ga hanasemasen", "spanish": "No hablo japonés", "pronunciation": "nee-hohn-goh gah hah-nah-seh-mah-sen"},
        {"japanese": "英語が話せる人はいますか", "romaji": "eigo ga hanaseru hito wa imasu ka", "spanish": "¿Hay alguien que hable inglés?", "pronunciation": "eh-goh gah hah-nah-seh-roo hee-toh wah ee-mahs kah"},
        {"japanese": "パスポートをなくしました", "romaji": "pasupooto wo nakushimashita", "spanish": "He perdido el pasaporte", "pronunciation": "pahs-poh-toh oh nah-koo-shee-mah-shee-tah"},
        {"japanese": "薬が必要です", "romaji": "kusuri ga hitsuyou desu", "spanish": "Necesito medicinas", "pronunciation": "koo-soo-ree gah hee-tsoo-yoh des"},
        {"japanese": "大使館はどこですか", "romaji": "taishikan wa doko desu ka", "spanish": "¿Dónde está la embajada?", "pronunciation": "tai-shee-kahn wah doh-koh des kah"},
        {"japanese": "道に迷いました", "romaji": "michi ni mayoimashita", "spanish": "Estoy perdido/a", "pronunciation": "mee-chee nee mah-yoh-ee-mah-shee-tah"},
        {"japanese": "地震です！", "romaji": "jishin desu!", "spanish": "¡Es un terremoto!", "pronunciation": "jee-sheen des"},
        {"japanese": "火事です！", "romaji": "kaji desu!", "spanish": "¡Hay incendio!", "pronunciation": "kah-jee des"},
        {"japanese": "非常口はどこですか", "romaji": "hijou-guchi wa doko desu ka", "spanish": "¿Dónde está la salida de emergencia?", "pronunciation": "hee-joh-goo-chee wah doh-koh des kah"},
        {"japanese": "护照を失くしました", "romaji": "pasupooto wo ushinaimashita", "spanish": "Perdí mi pasaporte", "pronunciation": "pahs-poh-toh oh oo-shee-nai-mah-shee-tah"},
        {"japanese": "財布を盗まれました", "romaji": "saifu wo nusumaremashita", "spanish": "Me robaron la cartera", "pronunciation": "sai-foo oh noo-soo-mah-reh-mah-shee-tah"},
        {"japanese": "連絡先を教えてください", "romaji": "renrakusaki wo oshiete kudasai", "spanish": "Dígame su número de contacto", "pronunciation": "ren-rah-koo-sah-kee oh oh-shee-eh-teh koo-dah-sai"},
        {"japanese": "ここに座ってもいいですか", "romaji": "koko ni suwatte mo ii desu ka", "spanish": "¿Puedo sentarme aquí?", "pronunciation": "koh-koh nee soo-wah-teh moh ee des kah"},
        {"japanese": "寒いです", "romaji": "samui desu", "spanish": "Tengo frío", "pronunciation": "sah-moo-ee des"},
        {"japanese": "暑いです", "romaji": "atsui desu", "spanish": "Tengo calor", "pronunciation": "ah-tsoo-ee des"},
    ],
    "hotel": [
        {"japanese": "予約があります", "romaji": "yoyaku ga arimasu", "spanish": "Tengo una reserva", "pronunciation": "yoh-yah-koo gah ah-ree-mahs"},
        {"japanese": "チェックインお願いします", "romaji": "chekku-in onegaishimasu", "spanish": "Check-in, por favor", "pronunciation": "chek-ee-in oh-neh-gai-shee-mahs"},
        {"japanese": "部屋の鍵をください", "romaji": "heya no kagi wo kudasai", "spanish": "La llave de la habitación, por favor", "pronunciation": "heh-yah noh kah-gee oh koo-dah-sai"},
        {"japanese": "WiFiのパスワードは", "romaji": "WiFi no pasuwaado wa", "spanish": "¿Cuál es el password del WiFi?", "pronunciation": "wai-fai noh pahs-wah-doh wah"},
        {"japanese": "チェックアウトは何時ですか", "romaji": "chekkuauto wa nanji desu ka", "spanish": "¿A qué hora es el checkout?", "pronunciation": "chek-oo-ah-oo-toh wah nahn-jee des kah"},
        {"japanese": "もう一泊できますか", "romaji": "mou ippaku dekimasu ka", "spanish": "¿Puedo quedarme una noche más?", "pronunciation": "moh eep-pakoo deh-kee-mahs kah"},
        {"japanese": "タオルを追加でお願いします", "romaji": "taoru wo tsuika de onegaishimasu", "spanish": "Toallas extra, por favor", "pronunciation": "tah-oh-roo oh tsoo-ee-kah deh oh-neh-gai-shee-mahs"},
        {"japanese": "荷物を預けたいです", "romaji": "nimotsu wo azuketai desu", "spanish": "Quiero dejar el equipaje", "pronunciation": "nee-moh-tsoo oh ah-zoo-keh-tai des"},
        {"japanese": "朝ごはんは何時ですか", "romaji": "asagohan wa nanji desu ka", "spanish": "¿A qué hora es el desayuno?", "pronunciation": "ah-sah-goh-hahn wah nahn-jee des kah"},
        {"japanese": "コインランドリーはどこですか", "romaji": "koin randorii wa doko desu ka", "spanish": "¿Dónde está la lavandería?", "pronunciation": "koin ran-doh-ree wah doh-koh des kah"},
        {"japanese": "コピーをお願いできますか", "romaji": "kopii wo onegai dekimasu ka", "spanish": "¿Pueden hacer una copia?", "pronunciation": "koh-pee oh oh-neh-gai deh-kee-mahs kah"},
        {"japanese": "チェックアウト遅れます", "romaji": "chekkuauto okuremasu", "spanish": "Me retraso en el checkout", "pronunciation": "chek-oo-ah-oo-toh oh-koo-reh-mahs"},
        {"japanese": "冷蔵庫に何がありますか", "romaji": "reizouko ni nan ga arimasu ka", "spanish": "¿Qué hay en la nevera?", "pronunciation": "reh-zoh-koh nee nah-n gah ah-ree-mahs kah"},
        {"japanese": "プールはありますか", "romaji": "puuru wa arimasu ka", "spanish": "¿Tienen piscina?", "pronunciation": "poo-roo wah ah-ree-mahs kah"},
        {"japanese": "送迎バスはありますか", "romaji": "sougei basu wa arimasu ka", "spanish": "¿Tienen shuttle bus?", "pronunciation": "soh-geh bah-soo wah ah-ree-mahs kah"},
        {"japanese": "部屋を変えてもらえますか", "romaji": "heya wo kaete moraemasu ka", "spanish": "¿Pueden cambiarme de habitación?", "pronunciation": "heh-yah oh kah-eh-teh moh-rah-eh-mahs kah"},
        {"japanese": "静かな部屋をお願いします", "romaji": "shizuka na heya wo onegai shimasu", "spanish": "Quisiera una habitación tranquila", "pronunciation": "shee-zoo-kah nah heh-yah oh oh-neh-gai shee-mahs"},
        {"japanese": "スーツケースを預けてください", "romaji": "suutsukeesu wo azukete kudasai", "spanish": "Guárdeme la maleta, por favor", "pronunciation": "skoo-tsoo-kee-su oh ah-zoo-keh-teh koo-dah-sai"},
        {"japanese": "ドライヤーはありますか", "romaji": "doraiyaa wa arimasu ka", "spanish": "¿Tienen secador de pelo?", "pronunciation": "doh-rah-yah wah ah-ree-mahs kah"},
        {"japanese": "アラームを設定してください", "romaji": "araamu wo settei shite kudasai", "spanish": "Póngame una alarma, por favor", "pronunciation": "ah-rah-oo-moh oh seh-tay shee-teh koo-dah-sai"},
    ],
    "turismo": [
        {"japanese": "写真を撮ってもいいですか", "romaji": "shashin wo tottemo ii desu ka", "spanish": "¿Puedo tomar una foto?", "pronunciation": "shee-sheen oh toht-teh-moh ee des kah"},
        {"japanese": "ここは何ですか", "romaji": "koko wa nan desu ka", "spanish": "¿Qué es esto?", "pronunciation": "koh-koh wah nah-n des kah"},
        {"japanese": "入場料はいくらですか", "romaji": "nyuujouryou wa ikura desu ka", "spanish": "¿Cuánto cuesta la entrada?", "pronunciation": "nyoo-joh-ree-yoh wah ee-koo-rah des kah"},
        {"japanese": "何時に開きますか", "romaji": "nanji ni hirakimasu ka", "spanish": "¿A qué hora abren?", "pronunciation": "nahn-jee nee hee-rah-kee-mahs kah"},
        {"japanese": "何時に閉まりますか", "romaji": "nanji ni shimarimasu ka", "spanish": "¿A qué hora cierran?", "pronunciation": "nahn-jee nee shee-mah-ree-mahs kah"},
        {"japanese": "ガイドはいますか", "romaji": "gaido wa imasu ka", "spanish": "¿Hay guía?", "pronunciation": "gai-doh wah ee-mahs kah"},
        {"japanese": "トイレはどこですか", "romaji": "toire wa doko desu ka", "spanish": "¿Dónde está el baño?", "pronunciation": "toi-reh wah doh-koh des kah"},
        {"japanese": "お土産を買いたいです", "romaji": "omiyage wo kaitai desu", "spanish": "Quiero comprar souvenirs", "pronunciation": "oh-mee-yah-geh oh kai-tai des"},
        {"japanese": "おすすめの観光スポットは？", "romaji": "osusume no kankou supotto wa?", "spanish": "¿Qué lugares turísticos recomienda?", "pronunciation": "oh-soo-soo-meh noh kahn-koh sup-poh-toh wah"},
        {"japanese": "地図をもらえますか", "romaji": "chizu wo moraemasu ka", "spanish": "¿Me puede dar un mapa?", "pronunciation": "chee-zoo oh moh-rah-eh-mahs kah"},
        {"japanese": "ここで待っています", "romaji": "koko de matte imasu", "spanish": "Espero aquí", "pronunciation": "koh-koh deh mah-teh ee-mahs"},
        {"japanese": "團体ですか", "romaji": "dantai desu ka", "spanish": "¿Es un grupo organizado?", "pronunciation": "dahn-tai des kah"},
        {"japanese": "料金は別ですか", "romaji": "ryoukin wa betsu desu ka", "spanish": "¿El precio es aparte?", "pronunciation": "ree-yoh-keen wah beh-tsoo des kah"},
        {"japanese": "もう少しだけ見せてください", "romaji": "mou sukoshi dake misete kudasai", "spanish": "Muésteme un poco más, por favor", "pronunciation": "moh soo-koh-shee dah-keh mee-seh-teh koo-dah-sai"},
        {"japanese": "ここに坐ってもいいですか", "romaji": "koko ni suwatte mo ii desu ka", "spanish": "¿Puedo sentarme aquí?", "pronunciation": "koh-koh nee soo-wah-teh moh ee des kah"},
        {"japanese": "喫煙所はどこですか", "romaji": "kitsuenjo wa doko desu ka", "spanish": "¿Dónde está la zona de fumar?", "pronunciation": "keep-tsoo-en-joh wah doh-koh des kah"},
        {"japanese": "荷物を置いてもいいですか", "romaji": "nimotsu wo oite mo ii desu ka", "spanish": "¿Puedo dejar mis cosas aquí?", "pronunciation": "nee-moh-tsoo oh oh-ee-teh moh ee des kah"},
        {"japanese": "Wi-Fiはありますか", "romaji": "wai-fai wa arimasu ka", "spanish": "¿Hay WiFi?", "pronunciation": "wai-fai wah ah-ree-mahs kah"},
        {"japanese": "充電はできますか", "romaji": "juuden wa dekimasu ka", "spanish": "¿Puedo cargar el móvil?", "pronunciation": "joo-den wah deh-kee-mahs kah"},
        {"japanese": "おすすめは何ですか", "romaji": "osusume wa nan desu ka", "spanish": "¿Qué me recomienda?", "pronunciation": "oh-soo-soo-meh wah nahn des kah"},
    ],
}


def _flatten_phrases():
    all_phrases = []
    for cat_phrases in TRANSLATIONS.values():
        all_phrases.extend(cat_phrases)
    return all_phrases


ALL_PHRASES = _flatten_phrases()


@router.get("/translate")
async def translate(category: str = "básico"):
    """Traductor de frases japonesas por categoría"""
    cat_lower = category.lower()
    if cat_lower in TRANSLATIONS:
        return {"category": cat_lower, "phrases": TRANSLATIONS[cat_lower]}
    return {"categories": list(TRANSLATIONS.keys()), "message": f"Categoría '{category}' no encontrada. Usa una de: {', '.join(TRANSLATIONS.keys())}"}


@router.get("/categories")
async def get_categories():
    """Lista de categorías disponibles"""
    return {"categories": list(TRANSLATIONS.keys())}


@router.post("/translate")
async def translate_text(req: TranslateRequest):
    """Traduce texto bidireccionalmente: japonés↔español usando diccionario + MyMemory API"""
    text = req.text.strip()
    if not text:
        return {"translation": "", "source": "empty"}

    is_japanese = has_japanese(text)

    for phrase in ALL_PHRASES:
        jp = phrase["japanese"]
        if text.lower() == jp.lower() or text == jp:
            return {
                "translation": phrase["spanish"],
                "romaji": phrase.get("romaji", ""),
                "source": "dictionary"
            }

    for phrase in ALL_PHRASES:
        jp = phrase["japanese"]
        if text in jp or jp in text:
            return {
                "translation": phrase["spanish"],
                "romaji": phrase.get("romaji", ""),
                "source": "partial_match"
            }

    if is_japanese:
        sl, tl = "ja", "es"
    else:
        sl, tl = "es", "ja"

    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{sl}|{tl}",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("responseStatus") == 200:
                    translated = data["responseData"]["translatedText"]
                    if translated and translated.lower() != text.lower():
                        return {"translation": translated, "source": "mymemory"}
    except Exception:
        pass

    return {
        "translation": f"No se pudo traducir '{text}'. Prueba con una de las frases rápidas.",
        "source": "not_found"
    }


@router.get("/tts")
async def text_to_speech(text: str, lang: str = "ja"):
    """Genera audio de texto usando Google Translate TTS"""
    url = "https://translate.google.com/translate_tts"
    params = {"ie": "UTF-8", "q": text, "tl": lang, "client": "tw-ob"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, headers=headers, timeout=10.0, follow_redirects=True)
        if resp.status_code == 200:
            return StreamingResponse(
                iter([resp.content]),
                media_type="audio/mpeg",
                headers={"Content-Disposition": "inline; filename=tts.mp3"}
            )
        return {"error": "No se pudo generar el audio"}
