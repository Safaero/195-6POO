from tkinter import messagebox

class Verification :
    def veri(self, user, password):
        try: 
            if user == 'root' and password == 'root':
                return True
            else:
                return False        
        except Exception as e:
          print(f"Error en la verificación:{str(e)}")
          return False            