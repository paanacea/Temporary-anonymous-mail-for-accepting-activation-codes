import requests
import random
import string
import os

API = 'https://www.1secmail.com/api/v1/' #Обозначаем константу нашего API

#Создаем список возможных почтовых доменов
domain_list = ["1secmail.com",
  "1secmail.org",
  "1secmail.net",
  ]  

domain = random.choice(domain_list) #Выбираем рандомный домен

def generate_username(): #Функция генерации имени почты
  name = string.ascii_lowercase + string.digits #Рандомная генерация имени для почтового домена (используем латинские слова нижнего регистра + цифры)
  user_name = ''.join(random.choice(name) for i in range(10))
  
  return user_name

def check_mail(mail = ''): #Функция проверки входящих писем
  req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}' #Формируем ссылку к запросу API, по которому мы проверяем есть ли письма в ящике
  r = requests.get(req_link).json() #Отправляем запрос по ссылке и забираем ответ в json 
  length = len(r) #Возвращаем количество элементов в массиве с данными
  
  if length == 0:
    print('[INFO] На почте нет новых писем.(Проверка происходит каждые 5 секунд)')
  else: 
    id_list = [] #Создаем список для id
    
    for i in r:
      for k,v in i.items():
        if k == 'id':
          id_list.append(v)
        
    print(f'[+] У вас {length} входящих сообщений!')
    
    current_dir = os.getcwd()  #Получаем значение текущей директории
    final_dir = os.path.join(current_dir, 'all_mails')
    
    #Создаем директорию, если ее не существует
    if not os.path.exists(final_dir): 
      os.makedirs(final_dir)
      
    #Получаем информацию с писем
    for i in id_list:
      read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={i}'
      r = requests.get(read_msg).json() #Отправляем запрос и получаем json
      
      #Получем информацию по ключам
      sender = r.get('from')
      subject = r.get('subject')
      date = r.get('date')
      content = r.get('textBody')
      
      mail_file_path = os.path.join(final_dir, f'{i}.txt')#Сохраняем информацию в файл
      
      with open(mail_file_path, 'w', encoding='utf-8') as file:
        file.write(f'Sender/Отправитель: {sender}\nTO: {mail}\nSubject/Тема: {subject}\nDate/Дата: {date}\nContent/Содержимое: {content}')

		
def delete_mail(mail = ''): #Функция для удаления почты
  url = 'https://www.1secmail.com/mailbox' 
  
  data = {
		'action' : 'deleteMailbox',
  	'login' : mail.split('@')[0],
		'domain' : mail.split('@')[1]
	}
  
  r = requests.post(url, data=data) #Отправляем пост запрос
  print(f'[X] Почтовый адрес {mail} - удален!\n')