import time
import requests
from email_utils import generate_username, check_mail, delete_mail, domain

API = 'https://www.1secmail.com/api/v1/' #Обозначаем константу нашего API

def main():
  try:
    user_name = generate_username() 
    mail = f'{user_name}@{domain}' #Составляем почтовый адрес из имени + домена
    print(f'[@] Ваш почтовый адрес: {mail}') #Выводим результат
    
    mail_req = requests.get(f'{API}?login={mail.split('@')[0]}&domain={mail.split('@')[1]}') #Отправляем запрос к API и залогинимся
    
    while True:
      check_mail(mail=mail)
      time.sleep(5)
      
  except(KeyboardInterrupt): #Останавливаем программу
    delete_mail(mail=mail)
    print('Программа остановлена.')
    
if __name__ == '__main__':
  main()
