import timeit
import psutil
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlparse
import sqlfluff

class sqlSqorer:
    def __init__(self, code, dbname = "database.db"):
        try : 
            engine = create_engine(f'sqlite:///{dbname}', echo=False)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            self.query = code

        except Exception :
            raise

    def evaluate_sql_performance(self):
        #* initial conditions :
        
        cpu_before = psutil.cpu_percent(interval=None)
        start_time = timeit.default_timer()

        try:
            result = self.session.execute(text(self.query))
        except Exception as e:
            result = {
            "exception" : str(e),
            "error" : True,
            "cpu_usage" : 0,
            "time_passed" : 0
            }
            return result
        
        #* end conditions :
        end_time = timeit.default_timer()
        time_passed = (end_time - start_time) * 1000 #% miliseconds
        cpu_after = psutil.cpu_percent(interval=None)  

        #
        # --PUANLANDIRMA--
        # zaman ve kaynak kullanımı oldukça önemli, bu yüzden %50 lik puanı kapsayacak.
        # zamanda büyük bir fark bulunması, kodun verimliliğini gösterir.
        # bu yüzden puanlamada üstel bir azalış gösterilmeli.
        # ancak puan burada hesaplanmamalı, zaman diğer koda göre göreceli olmalı. 
        # bu yüzden main'de hesaplanacak.
        #

        self.session.close()
        
        result = {
            "exception" : "no exception",
            "error" : False,
            "cpu_usage" : cpu_after - cpu_before,
            "time_passed" : time_passed
        }
        return result



    def evaluate_sql_query(self):
        #* bu kısım sql sorgusunu parçalara ayırıyor:
        parsed = sqlparse.parse(self.query)
        #* burda joinleri tutacağımız array var:
        joinCount = 0
        whereCount = 0

        for stmt in parsed:
            #* stmt : her bir sql komutu (1-..; 2-..; 3-...; ...)
            for token in stmt.tokens:
                #* token ise bir sorgudaki anahtar kelimeleri temsil ediyor. bu for loop, where ve join kullanımlarını topluyor.

                if token.is_keyword and token.value.upper() in ['JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN']:
                    joinCount += 1

        #* SELECT * yerine column belirtmek daha efektif. eksi puan if true : 
        select_star = "SELECT *" in self.query.upper()

        #* TimeComplexity, select sayısı ile üstel artış gösterir. SELECT sayısını al :
        selectCount = self.query.upper().count("SELECT") 
        whereCount = self.query.upper().count("WHERE") 


        #
        # -- PUANLANDIRMA --
        # bir sql sorgusunun verimliliği önemli parametrelerden biri, bu 
        # yüzden %40 ı kapsayacak.
        # -
        # değerlendirme kriterleri : 
        #
        #   SELECT sayısı (int) - 0.6
        #   SELECT * kullanımı (bool) - 0.9
        #   WHERE sayısı (int) - 0.85
        #   JOIN sayısı (int)  - 0.5
        #   

        # select count can not be zero, otherwise query will disqualified.

        point = 40 * (0.9 if select_star else 1) * (pow(0.6,selectCount - 1)) * (pow(0.85,whereCount)) * (pow(0.5,joinCount))

        result = {
            "point" : point,
            "joincount" : joinCount,
            "wherecount" : whereCount,
            "select_star": select_star,
            "selectcount": selectCount,
        }

        return result
    
    def evaluate_sql_syntax(self):
        #
        # --PUANLANDIRMA--
        # yazım ve syntax kullanımı sistemsel açıdan diğer başlıklar 
        # kadar önem arz etmez.
        # bu kısımda göreceli bir değerlendirmeye ihtiyaç duyuyor.
        # bu yüzden main'de hesaplanacak.
        #.%10 etkileyecek

        # sql fluff sorgunun tüm syntaxını değerlendirir : 
        try:
            linting_result = sqlfluff.lint(self.query)
            issue_list = []
            issue_count = 0
            # sorgu sonuçlarını liste şeklinde döndürür : 
            if linting_result:
                for issue in linting_result:
                    issue_count += 1
                    issue_list.append(f"Satır {issue['start_line_no']}, Sütun {issue['start_line_pos']}: {issue['description']}")

            result = {
                "point" : 10 * pow(0.8,issue_count),
                "error" : False,
                "exception" : "no exception",
                "issuecount" : issue_count,
                "issues" : issue_list,
            }

            return result

        except Exception as e:
            result = {
                "point" : 0,
                "error" : True,
                "exception" : str(e),
                "issuecount" : 0,
                "issues" : [],
            }
            return result
        
    
""" *--------- small documentation ---------*
-evaluate sql performance :
        returns : 
            "exception" : "no exception",
            "error" : False,
            "cpu_usage" : cpu_after - cpu_before,
            "time_passed" : time_passed

-evaluate sql query : 
        returns : 
            "point" : point,
            "joincount" : joinCount,
            "wherecount" : whereCount,
            "select_star": select_star,
            "selectcount": selectCount,
        
-evaluate sql syntax : 
        returns : 
            "error" : False,
            "exception" : "no exception",
            "issuecount" : issue_count,
            "issues" : issue_list,
"""
    

if __name__ == "__main__":
    print("\nYanlış python dosyasını çalıştırmaktasınız. Lütfen 'main.py'ı çalıştırın.\n")