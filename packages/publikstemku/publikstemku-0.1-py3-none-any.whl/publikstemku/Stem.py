class Stemmer:
    def __init__(self):
        self.lemma = None
        self.suffix = None
        self.prefix = None
        self.nasal = None

    def cf(self, data):  # proses merubah seluruh huruf besar menjadi huruf kecil//
        return data.lower()

    def tokenizing(
        self, data_cf
    ):  # proses mengahpus simbol yang tida diperlukan dan merubah kalimat menjadi kata berdasarkan spasi'''
        allowedChar = "abcdefghijklmnopqrstuvwxyz0123456789âèḍ '-.,"
        temp = ""
        for char in data_cf:
            if char in allowedChar:
                if char == "." or char == ",":
                    temp += " " + char
                else:
                    temp += char
        return temp.split()

    def identifikasiCe(self, token):
        imbuhan = ["na", "da", "sa", "ra", "nga", "eng", "ma", "dha"]
        indeksTarget = []
        for i in range(len(token)):  # proses rule based kata ce'
            if token[i] == "cè'":
                indeksTarget.append(i + 1)

        for j in indeksTarget:  # identifikasi imbuhan pada kata setelah kata ce'''
            for kataImbuhan in imbuhan:
                if token[j].endswith(kataImbuhan):
                    if kataImbuhan == "dha":
                        token[j] = token[j].replace("ddha", "t")
                    else:
                        token[j] = token[j].replace(kataImbuhan, "")
                    break
        return token

    def identifikasiGhallu(self, token):  # proses identifikasi kata ghallu
        demonstratif = [
            "rèya",
            "jarèya",
            "arèya",
            "jariya",
            "jiya",
            "jajiya",
            "jeh",
            "rowa",
            "arowa",
            "juwa",
        ]
        se = ["sè"]
        indeksTarget = []
        for i in range(len(token)):
            if token[i] == "ghallu" and token[i - 2] in se:
                indeksTarget.append(i - 1)
            elif token[i] == "ghallu" and token[i - 2] in demonstratif:
                indeksTarget.append(i - 1)
            elif token[i] == "ghallu" and token[i - 1].startswith(
                "ta"
            ):  # contoh kata = tamera
                indeksTarget.append(i - 1)
                token[i - 1] = token[i - 1][2 : (len(token[i - 1]))]

        # indekstarget = rajah, kene'
        for j in indeksTarget:
            token[j], token[j + 1] = token[j + 1], token[j]

        return token

    def kataulang(self, kata):
        temp = kata.split("-")
        if (
            temp[0] == temp[1]
        ):  # Kata Ulang Sempurna. contoh kata: mogha-mogha, #revisi pengecekan kata ulang sempurna
            return {"kd": temp[1], "prefix": "", "suffix": ""}
        else:
            if temp[0].startswith("e"):
                if temp[0].startswith("e") and temp[1].endswith(
                    "aghi"
                ):  # Kata Ulang Dwi Lingga Berimbuhan e- dan -aghi.contoh kata: ekol-pokolaghi
                    return {
                        "kd": temp[1][: temp[1].index("aghi")],
                        "prefix": "di",
                        "suffix": "kan",
                    }
                else:
                    return {
                        "kd": temp[1],
                        "prefix": "di",
                        "suffix": "",
                    }  # Kata Ulang Dwi Lingga Berimbuhan e-. contoh kata: ero-soro
            elif temp[0].startswith(
                "a"
            ):  # Kata Ulang Dwi Lingga Tidak Berimbuhan a-. contoh kata: areng-sareng
                if temp[0].startswith("a") and temp[1].endswith(
                    "an"
                ):  # Kata Ulang Dwi Lingga Berimbuhan a- dan -an.contoh kata: aka'-berka'an
                    return {
                        "kd": temp[1][: temp[1].index("an")],
                        "prefix": "ber",
                        "suffix": "an",
                    }
                else:
                    return {"kd": temp[1], "prefix": "ber", "suffix": ""}
            elif temp[1].endswith(
                "na"
            ):  # Kata Ulang Dwi Lingga Berimbuhan -na. contoh kata: ca-kancana
                return {
                    "kd": temp[1][: temp[1].index("na")],
                    "prefix": "",
                    "suffix": "nya",
                }
            elif temp[1].endswith("an"):
                return {
                    "kd": temp[1][: temp[1].index("an")],
                    "prefix": "",
                    "suffix": "an",
                }  # Kata Ulang Dwi Lingga Berimbuhan -an. contoh kata: ca-kancaan
            elif temp[1].endswith("ân"):
                return {
                    "kd": temp[1][: temp[1].index("ân")],
                    "prefix": "",
                    "suffix": "an",
                }
            elif temp[1].endswith("a"):
                return {"kd": temp[1][: temp[1].index("a")], "prefix": "", "suffix": ""}
            elif temp[1].endswith(
                temp[0]
            ):  # Kata Ulang Dwi Lingga Tidak Berimbuhan. #contoh kata: ku-buku,
                return {"kd": temp[1], "prefix": "", "suffix": ""}

    def imbuhansisipan(self, kata):
        kata = kata.replace("ten", "t")
        self.prefix = "ten"
        return {
            "kd": kata,
            "prefix": "di",
        }  # contoh kata: tenolong-->tolong-->ditolong, tenompang-->tompang-ditumpang (sisipan 'en')

    def imbuhanawalan(self, kata):
        return {"kd": kata[1:], "prefix": "ter"}

    def imbuhanawalanpa(self, kata):
        self.suffix = "pa"
        return {"kd": kata[2 : kata.index("na")], "suffix": "annya"}

    def imbuhanawalanka(self, kata):
        if kata.startswith("ka") and kata.endswith("ânna"):
            self.prefix = "ka"
            self.suffix = "ânna"
            return {
                "kd": kata[2 : kata.index("ânna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif kata.startswith("ka") and kata.endswith("anna"):
            self.prefix = "ka"
            self.suffix = "anna"
            return {
                "kd": kata[2 : kata.index("anna")],
                "prefix": "ke",
                "suffix": "annya",
            }
        elif kata.startswith("ka") and kata.endswith("an"):
            self.prefix = "ka"
            self.suffix = "an"
            return {"kd": kata[2 : kata.index("an")], "prefix": "ke", "suffix": "an"}
        elif kata.startswith("ka") and kata.endswith("ân"):
            self.prefix = "ka"
            self.suffix = "ân"
            return {"kd": kata[2 : kata.index("ân")], "prefix": "ke", "suffix": "an"}

    def imbuhannasal(self, kata, kamus):
        if kata.startswith("nge"):
            kata = kata.replace("nge", "")
            self.nasal = "nge"
            return {"kd": kata, "prefix": "me", "suffix": ""}
        elif kata.startswith("ng"):
            temp = kata + ""
            temp = temp.replace("ng", "")
            self.nasal = "ng"
            if temp in kamus.keys():
                if temp.endswith("è"):
                    return {"kd": temp, "prefix": "me", "suffix": "i"}
                else:
                    return {"kd": temp, "prefix": "me", "suffix": ""}
            else:
                temp2 = kata + ""
                temp2 = kata.replace("ng", "gh")
                if temp2 in kamus.keys():
                    return {"kd": temp2, "prefix": "meng", "suffix": ""}
                else:
                    temp3 = kata + ""
                    temp3 = kata.replace("ng", "k")
                    if temp3 in kamus.keys():
                        return {"kd": temp3, "prefix": "meng", "suffix": ""}
        elif kata.startswith("ny"):
            temp = kata + ""
            temp = temp.replace("ny", "c")
            self.nasal = "ny"
            if temp in kamus.keys():
                return {"kd": temp, "prefix": "men", "suffix": ""}
            else:
                temp2 = kata + ""
                temp2 = kata.replace("ny", "j")  # nyajhal --> jajhal
                if temp2 in kamus.keys():
                    return {"kd": temp2, "prefix": "men", "suffix": ""}
                else:
                    temp3 = kata + ""
                    temp3 = kata.replace("ny", "s")  # nyabun --> sabun
                    if temp3 in kamus.keys():
                        return {"kd": temp3, "prefix": "meny", "suffix": ""}
                    # tambahan thoriq
                    else:
                        return {"kd": kata, "prefix": None, "suffix": None}
        elif kata.startswith("m"):
            temp = list(kata)
            temp[0] = "b"
            newkata = "".join(temp)
            self.nasal = "m"
            if newkata in kamus.keys():
                return {"kd": newkata, "prefix": "mem", "suffix": ""}
            else:
                temp[0] = "p"
                newkata = "".join(temp)
                return {"kd": newkata, "prefix": "mem", "suffix": ""}
        elif kata.startswith("n"):
            temp = list(kata)
            temp[0] = "t"
            newkata = "".join(temp)
            self.nasal = "n"
            if newkata in kamus.keys():
                return {"kd": newkata, "prefix": "men", "suffix": ""}
            # tambhan thoriq
            # else:
            #     return {"kd": kata, "prefix": "", "suffix": ""}
        else:
            return {"kd": kata, "prefix": None, "suffix": None}

    def imbuhan(self, kata, kamus):
        if kata.endswith("na"):
            self.suffix = "na"
            if kata.startswith("sa") and kata.endswith("na"):
                temp = kata + ""
                temp = temp[2:]
                temp = temp.replace("na", "")
                self.prefix = "sa"
                if temp in kamus.keys():
                    return {"kd": temp, "prefix": "se", "suffix": "nya"}
                else:
                    temp2 = kata + ""
                    temp2 = kata.replace("na", "")
                    if temp2 in kamus.keys():
                        return {"kd": temp2, "prefix": "", "suffix": "nya"}
            elif kata.endswith("ânna"):
                self.suffix = "ânna"
                return {
                    "kd": kata[: kata.index("ânna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            elif kata.endswith("anna"):
                self.suffix = "anna"
                return {
                    "kd": kata[: kata.index("anna")],
                    "prefix": "",
                    "suffix": "annya",
                }
            else:
                return {"kd": kata[: kata.index("na")], "prefix": "", "suffix": "nya"}
        elif kata.endswith("aghi"):
            self.suffix = "aghi"
            if kata.startswith("e") and kata.endswith("aghi"):
                self.prefix = "e"
                return {
                    "kd": kata[1 : kata.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif kata.startswith("è") and kata.endswith("aghi"):
                self.prefix = "è"
                return {
                    "kd": kata[1 : kata.index("aghi")],
                    "prefix": "di",
                    "suffix": "kan",
                }
            elif kata.startswith("a") and kata.endswith("aghi"):
                self.prefix = "a"
                return {
                    "kd": kata[1 : kata.index("aghi")],
                    "prefix": "meng",
                    "suffix": "kan",
                }
            else:
                return {"kd": kata[: kata.index("aghi")], "prefix": "", "suffix": "kan"}
        elif kata.startswith("ta"):
            self.prefix = "ta"
            return {"kd": kata[2:], "prefix": "ter", "suffix": ""}
        elif kata.startswith("ma"):
            self.prefix = "ma"
            return {"kd": kata[2:], "prefix": "memper", "suffix": ""}
        elif kata.startswith("ka"):
            self.prefix = "ka"
            if kata.startswith("ka") and kata.endswith("'"):
                return {"kd": kata[2:], "prefix": "ber", "suffix": ""}
            else:
                return {"kd": kata[2:], "prefix": "ter", "suffix": ""}
        elif kata.startswith("sa"):
            self.prefix = "sa"
            if kata.startswith("sa") and kata.endswith("sa"):
                return {
                    "kd": kata[2 : kata.index("sa")],
                    "prefix": "se",
                    "suffix": "nya",
                }
            else:
                return {"kd": kata[2:], "prefix": "se", "suffix": ""}
        elif kata.startswith("pa"):
            self.prefix = "pa"
            return {"kd": kata[2:], "prefix": "pe", "suffix": ""}
        elif kata.startswith("pe"):
            self.prefix = "pe"
            return {"kd": kata[2:], "prefix": "pe", "suffix": ""}
        elif kata.endswith("è"):
            self.suffix = "è"
            return {"kd": kata[: kata.index("è")], "prefix": "", "suffix": "kan"}
        elif kata.endswith("an"):
            if kata.startswith("a") and kata.endswith("an"):
                self.suffix = "an"
                self.prefix = "a"
                return {"kd": kata[1 : kata.index("an")], "prefix": "ber", "suffix": ""}
            elif kata.startswith("pa") and kata.endswith("an"):
                return {"kd": kata[2 : kata.index("an")], "prefix": "", "suffix": ""}
            elif kata.startswith("sa") and kata.endswith("an"):
                self.prefix = "sa"
                self.suffix = "an"
                return {
                    "kd": kata[2 : kata.index("an")],
                    "prefix": "se",
                    "suffix": "an",
                }
            else:
                return {"kd": kata[: kata.index("an")], "prefix": "", "suffix": "an"}
        elif kata.endswith("ân"):
            if kata.endswith("ân"):
                self.suffix = "ân"
                return {"kd": kata[: kata.index("ân")], "prefix": "", "suffix": "an"}
            elif kata.startswith("a") and kata.endswith("ân"):
                self.prefix = "a"
                return {"kd": kata[1 : kata.index("ân")], "prefix": "ber", "suffix": ""}
            # elif kata.startswith('ka') and kata.endswith("'ân"):
            # return {'kd':kata[2:kata.index("ân")],'prefix':'','suffix':'an'}
            elif kata.startswith("ka") and kata.endswith("ân"):
                self.prefix = "ka"
                self.suffix = "ân"
                return {
                    "kd": kata[2 : kata.index("ân")],
                    "prefix": "ke",
                    "suffix": "an",
                }
        elif kata.endswith("ra"):
            self.suffix = "ra"
            return {"kd": kata[: kata.index("ra")], "prefix": "", "suffix": "nya"}
        elif kata.endswith("sa"):
            self.suffix = "sa"
            return {"kd": kata[: kata.index("sa")], "prefix": "", "suffix": "nya"}
        elif kata.endswith("èpon"):
            self.suffix = "èpon"
            return {"kd": kata[: kata.index("èpon")], "prefix": "", "suffix": "nya"}
        elif kata.startswith("e"):
            if kata.startswith("epa"):
                self.prefix = "epa"
                return {"kd": kata[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "e"
                return {"kd": kata[1:], "prefix": "di", "suffix": ""}
        elif kata.startswith("è"):
            if kata.startswith("èpa"):
                self.prefix = "èpa"
                return {"kd": kata[3:], "prefix": "dipe", "suffix": ""}
            else:
                self.prefix = "è"
                return {"kd": kata[1:], "prefix": "di", "suffix": ""}
        elif kata.startswith("a"):
            self.prefix = "a"
            return {"kd": kata[1:], "prefix": "ber", "suffix": ""}

    def stemming(self, kalimat):
        import mysql.connector

        # import pandas as pd

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            # database="skripsi"
            database="madureseset",
        )

        kamus = {}
        mycursor = mydb.cursor()

        # mycursor.execute("SELECT * FROM kamus")
        mycursor.execute("SELECT * FROM lemmata")

        myresult = mycursor.fetchall()
        mycursor.close()
        for data in myresult:
            # kamus[data[1]] = [data[2]]
            kamus[data[1]] = [None]
        # print(kamus)
        kalimat = self.identifikasiGhallu(
            self.identifikasiCe(self.tokenizing(self.cf(kalimat)))
        )
        hasil = ""
        for kata in kalimat:
            if kata == ".":
                hasil = hasil[: len(hasil) - 1]
                hasil += ". "
            elif kata == ",":
                hasil = hasil[: len(hasil) - 1]
                hasil += ", "
            else:
                if kata == "ghallu":
                    hasil += "terlalu "
                else:
                    if "-" in kata:
                        temp = self.kataulang(kata)
                    #                     hasil += temp['prefix']+kamus[temp['kd']][0] + \
                    #                         "-"+kamus[temp['kd']][0]+temp['suffix']+" "
                    else:
                        if kata not in kamus.keys():
                            if kata.startswith("pa") and kata.endswith("na"):
                                temp = self.imbuhanawalanpa(kata)
                                self.lemma = temp["kd"]
                                # hasil += kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ka") and kata.endswith("ân"):
                                temp = self.imbuhanawalanka(kata)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ka") and kata.endswith("an"):
                                temp = self.imbuhanawalanka(kata)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ka") and kata.endswith("ânna"):
                                temp = self.imbuhanawalanka(kata)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ka") and kata.endswith("anna"):
                                temp = self.imbuhanawalanka(kata)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ten"):
                                temp = self.imbuhansisipan(kata)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("ny"):
                                temp = self.imbuhannasal(kata, kamus)
                                self.lemma = temp["kd"]
                                # if temp['prefix'] == 'meny':
                                #     hasil += temp['prefix']+kamus[temp['kd']][0][1:]+" "
                                # else:
                                #     hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("nge"):
                                temp = self.imbuhannasal(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ng"):
                                temp = self.imbuhannasal(kata, kamus)
                                self.lemma = temp["kd"]
                                # if temp['kd'].startswith('k'):
                                #     hasil += temp['prefix']+kamus[temp['kd']][0][1:]+temp['suffix']+" "
                                # else:
                                #     hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("na"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("aghi"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("ta"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("ma"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("ka"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("sa"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("pa"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("pe"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.endswith("è"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("an"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("ân"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("ra"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("sa"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.endswith("èpon"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("a"):
                                if kata == kalimat[-1]:
                                    temp = self.imbuhanawalan(kata)
                                    self.lemma = temp["kd"]
                                    # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                                else:
                                    temp = self.imbuhan(kata, kamus)
                                    self.lemma = temp["kd"]
                                    # hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                            elif kata.startswith("e"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("è"):
                                temp = self.imbuhan(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0]+temp['suffix']+" "
                            elif kata.startswith("m"):
                                temp = self.imbuhannasal(kata, kamus)
                                self.lemma = temp["kd"]
                                # if temp['kd'].startswith('b'):
                                #     hasil += temp['prefix']+kamus[temp['kd']][0]+" "
                                # else:
                                #     hasil += temp['prefix']+kamus[temp['kd']][0][1:]+" "
                            elif kata.startswith("n"):
                                temp = self.imbuhannasal(kata, kamus)
                                self.lemma = temp["kd"]
                                # hasil += temp['prefix']+kamus[temp['kd']][0][1:]+" "
                            else:
                                hasil += kata + " "
                                self.lemma = kata

                        else:
                            hasil += kamus[kata][0] + " "
                            self.lemma = kata

    #         if(kalimat.index(kata)==0):
    #             hasil = hasil.capitalize()

    #         indeks = len(hasil)-1
    #         while hasil[indeks] != "." and indeks >= 0:
    #             indeks -= 1
    #         if indeks > 0:
    #             text_temp = hasil[:indeks+2]
    #             last_word = hasil[indeks+2:len(hasil)].capitalize()

    #             hasil = text_temp + last_word
    # self.lemma = stem
    # return self.lemma


# stem = Stemmer()
# # # stem.stemming("alako")
# stem.stemming("kaadâ'anna")
# print(stem.lemma)
# print(stem.prefix)
# print(stem.suffix)
# print(stem.nasal)
# tes2 = stemming("Alè' toju' èadâ'")
# tes2 = stemming("alè' toju' èadâ'")
