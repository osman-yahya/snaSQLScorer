from tqdm import tqdm
import time
import tkinter as tk
from tkinter import filedialog
from backend import sqlSqorer

# ANSI renk kodları
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def exeute_main():
    first_score = 0
    second_score = 0
    report = ""
    first_code = ""
    second_code = ""

    print(f"\n\n{GREEN}SQLScorer'a hosgeldiniz.{RESET}\n")
    input(f"{YELLOW}devam etmek için ENTER'a basın.{RESET}")

    print(f"\n\n{GREEN}SQLScorer SQLite kullanmakadır. Mevcut dizinde bulunan örnek database.db kullanmak istemiyorsanız 'new' yazınız. Mevcut ile devam etmek için ENTER'a basınız :{RESET}\n")

    choice1 = input(f"{YELLOW}? ->{RESET}")
    choice2 = "database.db"
    cpuflag = False
    if choice1 == "new":
        print(f"\n\n{GREEN}Mevcut dizinde bulunan yeni istenilen Database'in adını giriniz. (SQLite){RESET}\n")
        choice2 = input(f"{YELLOW}? ->{RESET}")

    print(f"\n\n{RED}!- SQLScorer CPU testlerinde her zaman doğruyu yansıtmayabilir. CPU kullanımını puanlamaya dahil etmek istiyor musunuz? (y/n){RESET}\n")
    choice3 = input(f"{YELLOW}? ->{RESET}")
    if choice3 == "y":
        cpuflag = True



    print(f"\nLütfen sırasıyle karşılaştırılacak SQL dosyalarını seçin. Yalnızca sorgu dosyaları seçtiğinize emin olun.\n")
    input(f"{YELLOW}devam etmek için ENTER'a basın.{RESET}")

    root = tk.Tk()
    root.withdraw()  
    file1 = filedialog.askopenfilename(
        title="İlk SQL dosyası seçin",
        filetypes=[("SQL Dosyaları", "*.sql")]
        )
    if(not file1):
        print(f"\n\n{RED}Hiçbir dosya seçilmedi. Kod bitiriliyor.{RESET}\n")
        return
    
    file2 = filedialog.askopenfilename(
        title="İkinci SQL dosyasını seçin",
        filetypes=[("SQL Dosyaları", "*.sql")]
        )
    if(not file2):
        print(f"\n\n{RED}Hiçbir dosya seçilmedi. Kod bitiriliyor.{RESET}\n")
        return
    
    with open(file1,'r') as file:
        first_code = file.read()

    with open(file2,'r') as file:
        second_code = file.read()

    

    if(not first_code or not second_code):
        print(f"\n\n{RED}Boş dosyalar saptandı. Kod bitiriliyor.{RESET}\n")
        return
    
    try : 
        Q1 = sqlSqorer(first_code,choice2)
        Q2 = sqlSqorer(second_code,choice2)
    except Exception as e:
        print(f"\n{RED}Bir hata oluştu, kod bitiriliyor.{RESET}\nhata : {str(e)}")
        return
    
    print(f"\n\n{GREEN}Dosyalar başarıyla okundu! Karşılaştırmayı başlatabilirsiniz.{RESET}\n")
    input(f"{YELLOW}devam etmek için ENTER'a basın.{RESET}")

    total_steps = 6

    with tqdm(total=total_steps, desc=f"{GREEN}İşlemler{RESET}", unit="adım", ncols=100, leave=False) as pbar:

        pbar.set_postfix_str(f"{GREEN}Performanslar Test Ediliyor{RESET}")
        pbar.update(1)

        #* daha gerçekçi sonuçlar için iki kod da CPU'da sleep işleminden sonra çalıştırılıyor.
        time.sleep(3)

        #% ADIM 1 -
        try:

            res1 = Q1.evaluate_sql_performance()

            pbar.set_postfix_str(f"{GREEN}1.Performans Ölçümü Tamamlandı{RESET}")
            pbar.update(1)

            #* CPU kullanımını azaltmak için beklettik :
            time.sleep(5)

            res2 = Q2.evaluate_sql_performance()
            pbar.set_postfix_str(f"{GREEN}2.Performans Ölçümü Tamamlandı{RESET}")
            pbar.update(1)

            if res1["error"] and res2["error"]:
                raise Exception("Performans ölçümünde hata oluştu.")
            
            #! eğer CPU kullanımı isteniyorsa : 
            if(not cpuflag):
                print(f"{YELLOW}  *CPU kullanımı dikkate alınmıyor.{RESET}")
                #! bu durumda yalnızca zaman önemli olacak: (%50)
                total_time_passed = res1["time_passed"] + res2["time_passed"]
                first_score += 50*(res2["time_passed"]/total_time_passed)
                second_score += 50*(res1["time_passed"]/total_time_passed)

            #! cpu hesaba katılıyor :
            else:
                print(f"{YELLOW}  *CPU kullanımı dikkate alınıyor.{RESET}")
                total_cpu_usage = res1["cpu_usage"] + res2["cpu_usage"]
                first_score += 25*(res2["cpu_usage"]/total_cpu_usage)
                second_score += 25*(res1["cpu_usage"]/total_cpu_usage)

                #! Zaman kullanımı %25 etkileyecek :
                total_time_passed = res1["time_passed"] + res2["time_passed"]
                first_score += 25*(res2["time_passed"]/total_time_passed)
                second_score += 25*(res1["time_passed"]/total_time_passed)

            report = report + f"Performans Ölçümü -----\nAlınan Puanlar:\nKod 1 : {first_score}\nKod 2 : {second_score}\n\nCPU kullanımları :\nKod 1 : {res1["cpu_usage"]}\nKod 2 : {res2["cpu_usage"]}\n" + f"Geçen Zaman (ms) :\nKod 1 : {res1["time_passed"]}\nKod 2 : {res2["time_passed"]}\n"

        except Exception as e:
            print(f"\n{RED}Bir hata oluştu, kod bitiriliyor.{RESET}\nhata : {str(e)}")
            return
        
        pbar.set_postfix_str(f"{GREEN}Performans Ölçümleri Tamamlandı.{RESET}")
        pbar.update(1)

        print(0.2)

        #% ADIM 2 -
        try:
            res1 = Q1.evaluate_sql_query()
            res2 = Q2.evaluate_sql_query()
            report = report + f"""
Kalite Ölçümü -----
Alınan Puanlar : 
Kod 1 : {res1["point"]}
Kod 2 : {res2["point"]}

Kod 1:
SELECT kullanımı : {res1["selectcount"]} kez
'SELECT *' {"Kullanıldı" if res1["select_star"] else "Kullanılmadı"}
JOIN Kullanımı : {res1["joincount"]} kez
WHERE Kullanımı : {res1["wherecount"]} kez
Kod 2:
SELECT kullanımı : {res2["selectcount"]} kez
'SELECT *' {"Kullanıldı" if res2["select_star"] else "Kullanılmadı"}
JOIN Kullanımı : {res2["joincount"]} kez
WHERE Kullanımı : {res2["wherecount"]} kez
\n
            """
            first_score += res1["point"]
            second_score += res2["point"]
        except Exception as e: 
            print(f"\n{RED}Bir hata oluştu, kod bitiriliyor.{RESET}\nhata : {str(e)}")
            return
        
        pbar.set_postfix_str(f"{GREEN}Kalite Ölçümleri Tamamlandı.{RESET}")
        pbar.update(1)

        print(0.5)

        #% ADIM 3 -
        try:
            res1 = Q1.evaluate_sql_syntax()
            res2 = Q2.evaluate_sql_syntax()

            if res1["error"] or res2["error"] : 
                raise Exception("Syntax ölçümünde bir hata oluştu")
            
            first_score += res1["point"]
            second_score += res2["point"]

            report = report + f"""
Yazım Hataları -----
Alınan Puanlar : 
Kod 1 : {res1["point"]}
Kod 2 : {res2["point"]}

Sorunlar:
Kod 1 : {res1["issuecount"]} hata bulundu.
Kod 2 : {res2["issuecount"]} hata bulundu.
Kod 1 Hataları : 
{"\n".join(str(i) for i in res1["issues"])}
Kod 2 Hataları : 
{"\n".join(str(i) for i in res2["issues"])}
            """
        except Exception as e:
            print(f"\n{RED}Bir hata oluştu, kod bitiriliyor.{RESET}\nhata : {str(e)}")
            return


        pbar.set_postfix_str(f"{GREEN}Syntax Kontrolü Tamamlandı.{RESET}")
        pbar.update(1)

        print(1)

    print("\n\nSonuçlar :")
    if(first_score == second_score):
        print(f"{GREEN}Kodlar aynı puanı kazandılar - {RESET}Puan : {first_score}%")
        print(f"{YELLOW}Aynı dosya seçilmiş olabilir mi?{RESET}")
    
    elif(first_score > second_score):
        print(f"{GREEN}İlk seçilen kod daha iyi - {RESET}Puan : {first_score}%")
        print(f"{RED}İkinci seçilen kod daha kötü - {RESET}Puan : {second_score}%")

    else:
        print(f"{GREEN}İkinci seçilen kod daha iyi - {RESET}Puan : {second_score}%")
        print(f"{RED}İlk seçilen kod daha kötü - {RESET}Puan : {first_score}%")

    input(f"{YELLOW}devam etmek için ENTER'a basın.{RESET}")

    choice = input(f"{YELLOW}\nDetaylı raporu görüntülemek için 1, Dosyaya yazdırmak için 2, atlamak için 3 giriniz :\n ->{RESET}")
    
    match choice:
        case "1":
            print(report)
        case "2":
            with open("report.txt",'w') as file:
                file.write(report)
        case _:
            print(f"{RED}Raporlar atlandı!{RESET}")
    
    print(f"\n\n{GREEN}SQL Scorer tamamlandı.{RESET} by Osman Yahya Akıncı\n")
        

if __name__ == "__main__":
    exeute_main()