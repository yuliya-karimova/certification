import uvicorn
import requests
from pydantic import BaseModel
from fastapi import FastAPI 
from openai import OpenAI
from typing import Optional, List, Dict, Any
import json
import docx

API_KEY = 'sk-pRcWeebLkuOiIfDjIDuHxMjCCBscq3BdJoDKNvA6HBT3BlbkFJQtSEVxM4lqv2GrkNUao1E-0Ks4XmG33RVJEzBKSdUA'

class GPT_NAMES:
    GPT_3_5 = "gpt-3.5-turbo" # - 0.5$
    GPT_4 = "gpt-4" # - 10$
    GPT_4_OMNI = "gpt-4o" # - 5$
    GPT_4o_MINI = "gpt-4o-mini" # - cheap

class Message(BaseModel):
    role: str
    content: str
    
# Payload example
class Payload(BaseModel):
    model: Optional[str] = None
    messages: List[Message]
    
    
    
    

# Агентная система для анализа требований и сертификации

# Алгоритм работы системы:

# 1. Система анализирует бизнес-требования (use case), представленные в виде текста (например, в формате .docx).
#    Первый этап работы заключается в том, что текст use case проверяется на соответствие лучшим практикам написания:
#    структурированность, ясность, корректность формулировок.

# 2. После анализа структуры, система переходит ко второму этапу, в котором происходит поиск сертифицируемых объектов.
#    Ключевая задача системы — определить, какие компоненты или системы в сценарии использования подлежат сертификации
#    в соответствии с международными регламентами (например, регламентами ООН).

# 3. Система проводит тщательный анализ каждого сертифицируемого объекта, сопоставляя его с соответствующими регламентами.
#    Это включает проверку объектов, таких как тормозные системы, рулевые механизмы, системы звукового оповещения и т.д.
#    Все найденные объекты проверяются по каждому пункту регламентов для выявления соответствия.

# 4. Если система находит несоответствия между требованиями use case и регламентами, она фиксирует эти несоответствия и
#    выдает рекомендации по их устранению. При этом каждый объект проверяется индивидуально, чтобы гарантировать точность анализа.

# 5. После завершения работы всех агентов система формирует итоговый отчет, который содержит:
#    - Тип кейса (полностью соответствует регламентам, частично соответствует или не соответствует).
#    - Количество соблюденных и несоблюденных регламентов для каждого сертифицируемого объекта.
#    - Рекомендации по улучшению документации и исправлению ошибок, если таковые были найдены.

# 6. Система работает в автоматическом режиме и позволяет разработчикам быстро проверять соответствие требований международным регламентам,
#    что делает процесс сертификации более эффективным и снижает вероятность ошибок в документации.

    
    
    
regulations_files = {
    0: "data/AVAS.json",
    1: "data/braking.json",
    2: "data/wipe_and_wash.json",
    3: "data/audible.json",
    4: "data/electromagnetic.json",
    5: "data/safety_belt.json",
    6: "data/safety_glazing_materials.json",
    7: "data/seats.json",
    8: "data/speedometer_and_odometer.json",
    9: "data/steering_equipment_or_mechanism.json",
    10: "data/doors_parts.json",
    11: "data/heating_system.json"
}
 
    

    
    
    

    
# Функция `sent_to_ai` предназначена для отправки запроса в API OpenAI с помощью клиента OpenAI.
# Она принимает данные в формате словаря (payload), которые содержат параметры для выполнения запроса к модели GPT.
# Функция создает клиент, используя API-ключ, и отправляет запрос с переданными параметрами в API OpenAI.
# В результате выполнения запроса функция получает ответ от модели и возвращает его текстовое содержание.
    
def sent_to_ai(payload: Payload):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(**payload)
    
    return response.choices[0].message.content








# Первый агент: Анализ use case и рекомендации по улучшению.
# 
# Данная функция `analyze_use_case_from_message` отвечает за выполнение задачи первого агента.
# Первый агент занимается проверкой правильности составления use case и выявлением его недостатков на основе
# заданных стандартов и рекомендаций по написанию сценариев использования.
# 
# Цель работы первого агента — провести анализ структуры и содержания use case, определить, 
# насколько он соответствует лучшим практикам, и предложить конкретные улучшения.
# 
# Аргументы:
# - case_description (str): текстовое описание use case, которое будет анализироваться.
# - requirements (str): список требований и стандартов, с которыми будет сопоставлен use case для анализа.
# 
# Этапы выполнения:
# 1. Формируется полный запрос (full_prompt) для передачи в GPT. Этот запрос включает в себя описание use case 
#    и требования, на которые нужно опираться при анализе. Агент запрашивает краткий и четкий список недостатков
#    и предложений по улучшению.
# 2. Формируется список сообщений (messages), которые будут отправлены в GPT. Сообщения включают текст запроса.
# 3. Создается payload — это набор параметров для выполнения запроса. В него входит модель (GPT-4o Mini) и контекст сообщений.
# 4. С помощью функции `sent_to_ai` запрос отправляется в API GPT, и возвращается анализ, включающий выявленные проблемы
#    и рекомендации по их исправлению.
# 
# Результат работы первого агента — краткий и точный список предложений по улучшению use case и выявленных недостатков,
# который возвращается в ответе от GPT.

def analyze_use_case_from_message(case_description: str, requirements: str):
    # Формируем полный запрос
    full_prompt = (
        f"Проанализируй следующий Use Case на соответствие стандартам и выяви основные недостатки. "
        f"Укажи, что можно улучшить, и как это сделать. Ответ должен быть кратким и конкретным, "
        f"с перечислением недостатков и конкретными рекомендациями по каждому пункту.\n\n"
        f"Вот кейс:\n{case_description}\n\n"
        f"Требования для анализа:\n{requirements}\n\n"
        f"Убедись, что все обязательные элементы присутствуют и соответствуют стандартам. "
        f"Дай краткий список недостатков и рекомендации по каждому пункту. "
        f"Укажи конкретные улучшения, которые можно внести в описание кейса, чтобы оно соответствовало лучшим практикам.\n\n"
        f"Ответ должен быть лаконичным, но содержательным."
    )

    # Создаем payload для GPT
    messages = [Message(role="user", content=full_prompt)]
    payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

    # Отправляем запрос в GPT и получаем ответ
    response = sent_to_ai(payload.dict())

    return response

requirements = """
What is Use Case?
Abbreviations and terms
Term    Description
Actor   Human or System Entity participating in a use-case
Goal    Use-case summary describing the desired outcome
HMI     Human-machine Interface
HMI Team    Team developing in-vehicle HMI
OC Team     Operational Concept team
SA Team     System Architecture team
TBD         to be defined

References:
1. Use-Case Best Practices: https://www.cybermedian.com/the-nut-and-bolts-of-use-case-writing-best-practices-and-common-mistakes/
2. How to Write Good Use Case Names - 7 tips: https://tynerblain.com/blog/2007/01/22/how-to-write-good-use-case-names/
3. Alistair Cockburn. Writing Effective Use Cases: https://www-public.imtbs-tsp.eu/~gibson/Teaching/Teaching-ReadingMaterial/Cockburn00.pdf
4. OC UC. Lessons Learnt: https://evkama.sharepoint.com/:p:/r/sites/KamaEngineeringTeam/_layouts/15/Doc.aspx?sourcedoc=%7B86457B1A-FAD6-441F-B777-3ABA7F957A29%7D&file=OC%20Lessons%20Learnt.pptx&action=edit&mobileredirect=true

UC Template:
- Bold text: section title, should not be changed
- Text in the angle brackets: to be changed

Mandatory sections:
- Title (Mandatory): "<Title>"
- Goal (Maturity A, mandatory): <goal definition>
- Context (Maturity A, optional): <execution environment>
- Scope (Maturity A, optional): <design boundaries>
- Actors (Maturity A, mandatory): Human and System entities
- Preconditions (Maturity B, mandatory): List of required conditions
- Triggers (Maturity B, mandatory): Events to initiate the use case
- Main Scenario (Maturity C, mandatory): Describes the main path
- Post-conditions (Maturity B, optional): Expected outcome after execution
- Alternative Scenarios (Maturity C, optional): Branches for different scenarios
- Exceptions (Maturity C, optional): Cases for failure scenarios

UC Maturity Levels:
- Level A: Title, Goal, and Actors are mandatory, Context and Scope are optional
- Level B: Preconditions, Triggers are mandatory, Post-conditions and Requirements are optional
- Level C: Full Scenario, including main and alternative paths

Actors:
- Human: Driver, Fleet Manager, Owner, Passenger, Pedestrian, User
- System: ADAS, AVAS, Braking System, HUD, etc.
        
Use-Case Title (Mandatory):
- Naming should follow the format: "<Verb> <Noun> <Optional Purpose>"
Examples:
- Calculate Speed, Calculate Vehicle Speed from Braking system
"""












# Второй агент: Идентификация сертифицируемых объектов и проверка по регламентам.
#
# Данная функция `analyze_regulation_from_message` отвечает за выполнение задачи второго агента.
# Второй агент анализирует сценарий использования (use case) для определения, подлежат ли упомянутые элементы сертификации
# в соответствии с международными регламентами ООН (ECE). 
# Если объекты из use case попадают под действие регламентов, агент определяет, под какой именно регламент они попадают.
# 
# Цель работы второго агента — это выделение сертифицируемых объектов из use case и их проверка на соответствие регламентам,
# таким как электромагнитная совместимость (EMC), рулевое управление, тормозные системы и т.д.
#
# Аргументы:
# - case_description (str): текстовое описание use case, содержащее объекты и системы, которые будут анализироваться.
# - regulations (str): список регламентов ООН (ECE), с которыми будут сверяться объекты из use case.
#
# Этапы выполнения:
# 1. Формируется полный запрос (full_prompt), который содержит описание use case и список регламентов для проверки.
#    Агент задает четкий вопрос: попадает ли элемент из кейса под сертификацию, и если да, то под какой регламент.
#    Запрос включает набор конкретных регламентов для проверки, таких как регламент №10 (EMC) и другие регламенты для разных систем.
# 2. Формируется список сообщений (messages), где запрос будет передан в виде пользовательского сообщения.
# 3. Создается payload — это набор параметров для выполнения запроса. В него входит модель (GPT-4o Mini) и контекст сообщений.
# 4. Используется функция `sent_to_ai`, чтобы отправить запрос в API GPT, и возвращается анализ, указывающий,
#    под какие регламенты подпадают элементы из use case или же подтверждающий, что они не подлежат сертификации.
# 
# Результат работы второго агента — список сертифицируемых объектов и указание, под какие регламенты они попадают.
# Это позволяет определить, какие элементы use case должны соответствовать стандартам сертификации.

def analyze_regulation_from_message(case_description: str, regulations: str):
    # Формируем полный запрос
    full_prompt = (
        f"Проанализируй следующий Use Case или описание системы на предмет того, "
        f"регламентируется ли упомянутый элемент в соответствии с регламентами ООН (ECE) для сертификации автомобилей. "
        f"Если элемент подлежит сертификации, укажи под какой регламент он попадает. Если не подлежит сертификации, также укажи это.\n\n"
        f"Вот описание кейса:\n{case_description}\n\n"
        f"Регламенты для проверки:\n{regulations}\n\n"
        f"Используй следующие регламенты для оценки:\n"
        f"- EMC (Электромагнитная совместимость): Сертифицируется в соответствии с Регламентом ООН №10. \n"
        f"- Steering mechanism (Рулевое управление): Регулируется Регламентом ООН №79. \n"
        f"- Braking (Тормозная система): Подлежит сертификации по Регламенту ООН №13 и №13-H. \n"
        f"- Safety belt (Ремни безопасности): Регулируется Регламентом ООН №16. \n"
        f"- Seats (Сиденья): Регламентируется Регламентом ООН №17. \n"
        f"- Audible warning devices (Звуковые сигналы): Регламентируется Регламентом ООН №28. \n"
        f"- Speedometer and odometer (Спидометр и одометр): Регламентируется Регламентом ООН №39. \n"
        f"- Steering equipment (Оборудование рулевого управления): Регулируется Регламентом ООН №79. \n"
        f"- AVAS (Система звукового оповещения для гибридных и электрических автомобилей): Регламентируется Регламентом ООН №138. \n"
        f"- Wipe and wash (Системы стеклоочистки и омывания): Регулируется Регламентами ООН №43 и №45. \n\n"
        f"Не сертифицируются:\n"
        f"- Двери (Doors)\n"
        f"- Система отопления (Heating system)\n\n"
        f"Ответ должен быть конкретным и четко указывать, регулируется ли элемент, упомянутый в кейсе, и если да, то под каким регламентом."
    )

    # Создаем payload для GPT
    messages = [Message(role="user", content=full_prompt)]
    payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

    # Отправляем запрос в GPT и получаем ответ
    response = sent_to_ai(payload.dict())

    return response

regulations = """
- EMC (Электромагнитная совместимость): Регламент ООН №10
- Steering mechanism (Рулевое управление): Регламент ООН №79
- Braking (Тормозная система): Регламент ООН №13 и №13-H
- Safety belt (Ремни безопасности): Регламент ООН №16
- Seats (Сиденья): Регламент ООН №17
- Audible warning devices (Звуковые сигналы): Регламент ООН №28
- Speedometer and odometer (Спидометр и одометр): Регламент ООН №39
- Steering equipment (Оборудование рулевого управления): Регламент ООН №79
- AVAS (Система звукового оповещения): Регламент ООН №138
- Wipe and wash (Системы стеклоочистки и омывания): Регламент ООН №43 и №45
"""
















# Второй агент: Проверка на необходимость сертификации.
#
# Данная функция `check_certification` отвечает за выполнение задачи второго агента.
# Она проверяет, подлежит ли упомянутый в use case элемент сертификации в соответствии с регламентами ООН (ECE).
# Второй агент оценивает, нужно ли сертифицировать объект или систему, и возвращает однозначный ответ в формате True или False.
#
# Аргументы:
# - case_description (str): текстовое описание use case, которое содержит объекты и системы, требующие проверки на сертификацию.
#
# Этапы выполнения:
# 1. Формируется полный запрос (full_prompt), который включает описание use case и регламенты для проверки.
#    В запросе перечисляются конкретные регламенты, с которыми необходимо сверить объекты, такие как регламент №10 (EMC), 
#    регламент №79 (рулевое управление) и другие.
#    Вопрос четко сформулирован: регламентируется ли элемент, упомянутый в кейсе, в соответствии с указанными регламентами, 
#    и ожидается ответ только в формате 'True' или 'False'.
# 2. Формируется список сообщений (messages), которые будут отправлены в GPT для обработки запроса.
# 3. Создается payload — это набор параметров, включающий модель (GPT-4o Mini) и сообщения для запроса.
# 4. Используется функция `sent_to_ai`, которая отправляет запрос в API GPT и получает ответ. Функция возвращает
#    ответ в формате 'True' или 'False' в зависимости от того, требуется ли сертификация.
#
# Результат работы второго агента — это четкий ответ: True, если элемент подлежит сертификации, и False, если не подлежит.

def check_certification(case_description):
    try:
        full_prompt = (
            f"Проанализируй следующий Use Case или описание системы и ответь строго True или False: "
            f"регламентируется ли упомянутый элемент в соответствии с регламентами ООН (ECE) для сертификации автомобилей?\n\n"
            f"Вот описание кейса:\n{case_description}\n\n"
            f"Используй следующие регламенты для оценки:\n"
            f"- EMC (Электромагнитная совместимость): Сертифицируется в соответствии с Регламентом ООН №10. \n"
            f"- Steering mechanism (Рулевое управление): Регулируется Регламентом ООН №79. \n"
            f"- Braking (Тормозная система): Подлежит сертификации по Регламенту ООН №13 и №13-H. \n"
            f"- Safety belt (Ремни безопасности): Регулируется Регламентом ООН №16. \n"
            f"- Seats (Сиденья): Регламентируется Регламентом ООН №17. \n"
            f"- Audible warning devices (Звуковые сигналы): Регламентируется Регламентом ООН №28. \n"
            f"- Speedometer and odometer (Спидометр и одометр): Регламентируется Регламентом ООН №39. \n"
            f"- Steering equipment (Оборудование рулевого управления): Регулируется Регламентом ООН №79. \n"
            f"- AVAS (Система звукового оповещения для гибридных и электрических автомобилей): Регламентируется Регламентом ООН №138. \n"
            f"- Wipe and wash (Системы стеклоочистки и омывания): Регулируется Регламентами ООН №43 и №45. \n\n"
            f"Не сертифицируются:\n"
            f"- Двери (Doors)\n"
            f"- Система отопления (Heating system)\n\n"
            f"Ответь только 'True' или 'False', без лишних слов."
        )

        # Создаем payload для GPT
        messages = [Message(role="user", content=full_prompt)]
        payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)
        
        # Отправляем запрос в GPT и получаем ответ
        response = sent_to_ai(payload.dict())
        
        # Получение ответа
        return response.strip()

    except Exception as e:
        print(f"Ошибка при проверке сертификации: {e}")
        return None





# Второй агент: Определение применимых регламентов.
#
# Данная функция `determine_applicable_regulations` отвечает за выполнение задачи второго агента.
# Второй агент анализирует разделы "Scope" и "Triggers" в описании use case и определяет, какие из заранее указанных 
# международных регламентов ООН применимы к упомянутым элементам.
#
# Цель работы второго агента — это сопоставить объекты из use case с конкретными регламентами и вернуть список
# номеров регламентов, которые должны быть применены для сертификации упомянутых элементов.
#
# Аргументы:
# - case_description (str): текстовое описание use case, содержащее разделы "Scope" и "Triggers", которые должны быть проанализированы.
#
# Этапы выполнения:
# 1. Формируется полный запрос (full_prompt), в котором агент запрашивает анализ текста на наличие регламентируемых элементов 
#    и их сопоставление с перечисленными регламентами. В запросе указаны конкретные регламенты и номера, такие как:
#    - 0: AVAS (система звукового оповещения),
#    - 1: Braking (тормозная система),
#    - 4: Electromagnetic Compatibility (электромагнитная совместимость) и т.д.
#    Агент просит вернуть список номеров регламентов, которые применяются к элементам use case.
# 2. Формируется список сообщений (messages), где запрос будет передан в виде пользовательского сообщения.
# 3. Создается payload — это набор параметров, включающий модель (GPT-4o Mini) и контекст сообщений.
# 4. Используется функция `sent_to_ai`, которая отправляет запрос в API GPT и получает ответ.
# 5. Ответ, полученный от GPT, представляет собой список номеров применимых регламентов. 
#    Этот список преобразуется с помощью `eval()` и возвращается как результат функции.
# 
# Результат работы второго агента — список номеров регламентов, которые должны применяться к упомянутым элементам в use case.
# Этот список помогает точно определить, какие объекты должны соответствовать международным требованиям для сертификации.

def determine_applicable_regulations(case_description: str) -> list:
    # Создаем промт для отправки в API
    full_prompt = f"""
    В тексте ниже есть разделы "Scope" и "Triggers". Проанализируй их и определи, какие из следующих регламентов применимы к упомянутым элементам:

    0 - AVAS ("Acoustic Vehicle Alerting System" ) 
    1 - Braking
    2 - Wipe and wash
    3 - Audible warning devices
    4 - Electromagnetic Compatibility
    5 - Safety belt
    6 - Safety Glazing Materials
    7 - Seats
    8 - Speedometer and odometer
    9 - Steering equipment или Steering mechanism
    10 - doors parts
    11 -  регламент с обязательной сертификацией по частям систем отопления

    Вот текст для анализа:
    {case_description}

    Твоя задача — определить, какие из перечисленных регламентов могут применяться, и вернуть строго список номеров этих регламентов без лишних слов. Пример ответа: [0, 3, 4].
    """

    # Создаем payload для GPT
    messages = [Message(role="user", content=full_prompt)]
    payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)
    
    # Отправляем запрос в GPT и получаем ответ
    response = sent_to_ai(payload.dict())

    # Получаем результат — список номеров
    applicable_regulations = eval(response)

    return applicable_regulations






# Третий агент: Поиск и анализ релевантных пунктов регламентов.
#
# Функция `find_relevant_regulations` предназначена для поиска и извлечения соответствующих пунктов регламентов,
# если сертификация объекта требуется. Она используется третьим агентом для анализа регламентов и их сопоставления
# с описанием use case.
#
# Цель функции — это нахождение всех релевантных пунктов регламентов, которые применимы к описанному объекту или системе
# в use case, и предоставление этих пунктов для дальнейшего анализа соответствия.
#
# Аргументы:
# - case_description (str): описание use case, которое нужно проанализировать.
# - json_path (str): путь к JSON-файлу, содержащему данные регламентов.
#
# Этапы выполнения:
# 1. **Чтение данных регламентов**: Функция открывает и читает JSON-файл, содержащий полный текст регламентов.
#    Данные файла загружаются в переменную `regulations_data`.
# 
# 2. **Разбиение на части (chunks)**: Данные могут быть слишком большими для одного запроса, поэтому они разбиваются
#    на части (chunks) размером 75 000 символов. Это значение можно регулировать:
#    - **Меньший размер chunk_size** (например, 50 000 или меньше) позволяет более тщательно анализировать данные,
#      так как GPT сможет проанализировать каждую часть более детально. Однако это увеличит общее количество запросов
#      и сделает процесс анализа более долгим.
#    - **Больший размер chunk_size** (например, 100 000 или больше) ускоряет процесс, так как количество запросов уменьшается.
#      Однако такой подход может сделать анализ менее тщательным, с возможными пропусками деталей в больших объёмах данных.
#    Таким образом, регулирование `chunk_size` позволяет находить баланс между тщательностью и скоростью анализа.
#
# 3. **Формирование запроса**: Для каждой части данных формируется запрос (full_prompt), который включает текст
#    описания use case и часть данных регламентов (chunk). Агенту ставится задача найти все релевантные пункты регламентов,
#    которые применимы к описанному объекту, и процитировать их полностью.
#
# 4. **Отправка запроса в GPT**: Запрос отправляется в API GPT с помощью функции `sent_to_ai`. 
#    Ответ от GPT содержит текст всех релевантных пунктов регламентов для текущей части данных.
#    Ответы для всех частей данных агрегируются в переменную `cumulative_relevant_regulations`.
#
# 5. **Возвращение результата**: После обработки всех частей данных функция возвращает полный текст релевантных
#    пунктов регламентов, которые были найдены по описанию use case.
#
# Обработка ошибок:
# - Если во время работы возникает ошибка, например, при чтении файла или отправке запроса, функция выводит сообщение об ошибке
#   и возвращает строку "Произошла ошибка при поиске релевантных пунктов".
#
# Результат: Функция возвращает полный текст всех релевантных пунктов регламентов, которые применимы к сертифицируемому объекту
# в use case. Эти данные необходимы для дальнейшего анализа соответствия объектов сертификации требованиям регламентов.

# Функция для поиска подходящих пунктов регламентов, если сертификация требуется
def find_relevant_regulations(case_description, json_path):
    try:
        # Чтение регламентов из JSON файла
        with open(json_path, 'r', encoding='utf-8') as file:
            regulations_data = json.load(file)
        
        # Преобразуем данные в строку и делим на чанки (части) для отправки
        regulations_text = json.dumps(regulations_data, indent=2)
        chunk_size = 75000
        chunks = [regulations_text[i:i+chunk_size] for i in range(0, len(regulations_text), chunk_size)]
        
        cumulative_relevant_regulations = ""
        
        for chunk in chunks:
            full_prompt = (
                f"На основе следующего Use Case найди все релевантные пункты регламентов:\n"
                f"{case_description}\n\n"
                f"Часть данных регламента:\n{chunk}\n\n"
                f"Ответом должны быть только номера и текст релевантных пунктов регламентов. ты должен процетировать пункт полностью от начала до конца ничего не упуская"
            )

            messages = [Message(role="user", content=full_prompt)]
            payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

            # Отправляем запрос в GPT и получаем ответ
            response = sent_to_ai(payload.dict())
            cumulative_relevant_regulations += response
        # Возвращаем результат анализа
        return cumulative_relevant_regulations

    except Exception as e:
        print(f"Ошибка при поиске релевантных пунктов регламентов: {e}")
        return "Произошла ошибка при поиске релевантных пунктов."



# Функция для создания детализированного промта.
# Она формирует текст запроса (prompt) для анализа use case на соответствие нормативным требованиям сертификации.
# 
# Аргументы:
# - case_description: описание use case.
# - relevant_regulations: список нормативных требований, которые могут применяться.
#
# В задаче описывается:
# 1. Поиск сертифицируемых объектов в кейсе.
# 2. Проверка соблюдения регламентов.
# 3. Классификация кейса по трем типам на основе соответствия регламентам.
# 
# Результат: Возвращает текст запроса, который будет отправлен для анализа в GPT.
def create_detailed_prompt(case_description, relevant_regulations):
    full_prompt = f"""
    Ты являешься экспертом по сертификации и проверке нормативных требований. Твоя задача — проанализировать предоставленный Use Case и определить, насколько он соответствует нормативным требованиям сертификации, а также выявить возможные недостатки и ограничения.
    
    Вот описание кейса:
    {case_description}
    
    Вот список нормативных требований, которые могут касаться этого кейса:
    {relevant_regulations}
    
    Твоя задача:
    
    1. Определить, упоминаются ли в кейсе сертифицируемые объекты.
    2. Если сертифицируемые объекты упоминаются, проверить, соблюдены ли все необходимые регламенты.
    3. Классифицировать соответствие кейса одному из типов:
        - **Тип 1**: В кейсе упоминаются сертифицируемые объекты, регламенты соблюдены. Отметь, какие конкретно регламенты затрагивает данный кейс на разработку.
        - **Тип 2**: В кейсе упоминаются сертифицируемые объекты, на которые накладываются ограничения по сертификации, но они не описаны в кейсе. Укажи, какие ограничения из регламентов нужно дополнительно описать в кейсе.
        - **Тип 3**: В кейсе упоминаются сертифицируемые объекты, требование на разработку противоречит (не соответствует) регламентам сертификации. Предложи корректировки, которые нужно внести.
    
    Приведи полный анализ по каждому типу с примерами.
    """
    return full_prompt




# Функция для создания финального промта.
# Она формирует запрос (prompt), который объединяет описание use case и финальный результат анализа.
# Цель: оценить соответствие кейса регламентам сертификации, определить сертифицируемые объекты и классифицировать кейс по типам (1, 2, 3).
#
# Аргументы:
# - case_description: описание use case.
# - final_result: результат предыдущего анализа кейса.
#
# Результат: Возвращает финальный текст запроса для проведения детализированного анализа.

def create_final_prompt(case_description, final_result):
    full_prompt = f"""
    Ты являешься экспертом по сертификации и проверке нормативных требований. Твоя задача — проанализировать предоставленный Use Case и определить, насколько он соответствует нормативным требованиям сертификации, а также выявить возможные недостатки и ограничения.
    
    Вот описание кейса:
    {case_description}
    
    Вот анализ этого кейса :
    {final_result}
    
    Твоя задача:
    
    1. Объеденить все, определить, упоминаются ли в кейсе сертифицируемые объекты.
    2. Если сертифицируемые объекты упоминаются, проверить, соблюдены ли все необходимые регламенты.
    3. Классифицировать соответствие кейса одному из типов:
        - **Тип 1**: В кейсе упоминаются сертифицируемые объекты, регламенты соблюдены. Отметь, какие конкретно регламенты затрагивает данный кейс на разработку.
        - **Тип 2**: В кейсе упоминаются сертифицируемые объекты, на которые накладываются ограничения по сертификации, но они не описаны в кейсе. Укажи, какие ограничения из регламентов нужно дополнительно описать в кейсе.
        - **Тип 3**: В кейсе упоминаются сертифицируемые объекты, требование на разработку противоречит (не соответствует) регламентам сертификации. Предложи корректировки, которые нужно внести.
    
    Вот притмеры ответов:
    
    Пример type 1.
    Исходя из регламента, можно понять несколько вещей, например, что изготовитель транспортного средства может установить альтернативные звуковые сигналы, которые могут выбираться водителем, хотя в use case описано обратное - 
    описания требования (use case) можно понять, что
    Описание бизнес-требования:
    Goal: Notify the surrounding people, cyclists and other road users of the Vehicle's reverse movement by external sound.
    Description:
    AVAS sound starts when moving in R starts (vehicle speed > 0).
    The driver is in the Vehicle, the Vehicle is in the R drive mode and reversing at any speed, an external soundtrack notifies surrounding road users about the movement of the Vehicle in reverse, so that an approaching Vehicle can be identified by ear. Only one sound is available to the driver. The function cannot be disabled.
    Preconditions:
    1) Vehicle is in working condition.
    2) Vehicle's AVAS system is working properly.
    3) Vehicle is in the R drive mode and is moving at any speed or standing still.
    4) There is no audio track selection, only one audio track is available.
    Main scenario:
    1) While driving the Vehicle in the R drive mode (vehicle speed > 0), it notifies the surrounding road users with an out_27.AVAS about reversing;
    2) When switching the drive mode from R to any other or the Vehicle speed 0 out_27.AVAS is disabled.
    Deactivation (Stopping, Cancelling)
    Driver stops pressing acceleration pedal and the vehicle's speed is equal 0
    Driver stops moving in reverse
    Сопоставление с регламентами сертификации:

    Результат:
    Кейс соответствует регламенту. При движении авто задним ходом звук AVAS может быть постоянным и не зависеть от скорости. Также при движении задним ходом AVAS не имеет верхнего порога по скорости 20 км/ч.
    
    Пример type 2. 
    Описание бизнес-требования:
    Goal: Driver to set a one-time PIN code via the vehicle's SWP for continued access and control of their vehicle in scenarios where the original key(mobile phone) is unavailable. 
    Trigger: The car has lost connection with the digital key
    Precondition:
    •	During the trip, the driver lost access to his phone (the phone battery ran out, broke, etc.).
    •	Access to the car was initially obtained using the key on the phone.
    •	Facial Recognition Driver Authentication not installed. 
    Main scenario:
    1.	The driver put car into park mode(in_2. SWP Android, in_9. PRND buttons (incl EPB function))
    2.	The car checks the connection with the phone (digital key)
    3.	out_2. SWP Android signals on the display that the key is missing and informs that it is necessary to set a one-time PIN code for further use of the car(change gears and continue driving).
    4.	The driver enters and confirms the one-time PIN code in_2. SWP Android display twice. 
    Postconditions:
    •	The driver sets a one time PIN code that can be used to gain access to the vehicle.
    •	If the driver has not entered the PIN code, the car is not blocked 
    •	The pin will be stored in the t-box

    Сопоставление с регламентами сертификации:
    GB 15740-202Х	UN reg.116
    4.9 Cars equipped with digital keys (including but not limited to Bluetooth keys, NFC keys, mobile phone applications, etc., but not applicable to biometric identification keys such as fingerprints and faces) shall meet the following requirements:
    a) The digital key shall be bound to the physical carrier;
    b) When the digital key communicates with the vehicle, it shall be authenticated and replay attacks shall be prevented;
    c) When the digital key communicates with the vehicle, the confidentiality and integrity of the communication data shall be guaranteed.	8.3.5.1.1. A key pad for inputting an individually selectable code having at least
    10,000 variants.
    8.5 Release state
    The power immobilizer state can be released by one of the following devices or a combination of them. Other devices with equivalent safety and working effect can also be used:
    a) The input codes of the electronic key should be independent and selectable, and the code should have at least 10,000 variations;
    b) The electric/electronic device (such as the remote control device) should have at least 50,000 variations and be programmed into the rolling code, and/or the minimum scanning time is 10 days (for example, for a device with at least 50,000 variations, there are a maximum of 5,000 variations per 24 hours);
    c) After the power immobilizer state is released by remote control, if the starting circuit is not operated, the power immobilizer should be restored to the set state within 300 seconds.	8.3.5.1.2. Electrical/electronic device, e.g. remote control, with at least 50,000 variants
    and shall incorporate rolling codes and/or have a minimum scan time of ten
    days, e.g. a maximum of 5,000 variants per 24 hours for 50,000 variants
    minimum

    Результат:
    При реализации функции «PIN to drive» необходимо учесть, что, согласно 116-м правилам, нужно выполнить требование - количество комбинаций паролей должно быть не мене 10 000. Например, длина более 4-х знаков / применяется буквенный алфавит / 16-ная система счисления. Это требуется обновлённым стандартом для китайского рынка GB 15740-202Х, аналогично 116 правилам.
    
    Пример type 3.
    Описание бизнес-требования:
    UC "Position Lights manual on/off modes"
    Precinditions
    - "Position lights" is in "off" mode
    - "Low beam lights"  is in "off" mode
    - "Hi beam lights"  is in "off" mode
    Main scenario
    1. Driver use SWP in_2 to turn Position Lights" to "on" mode
    Postconditions
    - "Position lights" is "on" mode
    - "Position lights" out_55 is active with indicator on RTOS out_1
    - "Position Lights" could be switched into "off" mode via SWP in_2 (deactivation described in alternative scenarios)
    Alternative scenario
    A. "Low beam light" is in "auto" or "on" mod
        A1. "Position Lights" couldn't be switched until "Low beam light" will be in "off" mode
    B. "Low beam light" is in the "off" mode
        B1. Driver turn "Position Lights" into "off" mode
        B2. "DRL" is active out_5
    Сопоставление с регламентами сертификации:
    
    Результат:
    Необходимо внести корректировку в кейс. В соответствии с п.6.8.9, tell-tale Position Lamps обязательно всегда отображать при включенных габаритах, даже, когда работает ближний свет.

    Сделай комплексный и красивый анализ. распиши все идеально. я отдам тебе все заработанные деньги )))

    """
    return full_prompt



# Функция для создания детализированного промта для объектов сертификации.
# Она формирует запрос для анализа конкретных объектов сертификации в use case на соответствие регламентам.
# Цель: проверить, правильно ли описаны сертифицируемые объекты, учтены ли все необходимые требования и выявить возможные недочёты.
#
# Аргументы:
# - case_description: описание use case.
# - relevant_regulations: список нормативных требований, применимых к кейсу.
# - certifiable_objects: список объектов сертификации, которые нужно проанализировать.
#
# Результат: Возвращает текст запроса для проведения детализированного анализа объектов сертификации.
def create_detailed_prompt_certifiable_objects(case_description, relevant_regulations, certifiable_objects):
    full_prompt = f"""
    Ты являешься экспертом по сертификации и проверке нормативных требований. Твоя задача — проанализировать предоставленный Use Case и определить, насколько он соответствует нормативным требованиям сертификации, а также выявить возможные недостатки и ограничения.
    
    Вот описание кейса:
    {case_description}
    
    Вот список нормативных требований, которые могут касаться этого кейса:
    {relevant_regulations}
    
    Твоя задача проанализировать объект сертификации и понять все ли правильно по нему описано все ли требования учтены:
    {certifiable_objects}

    Приведи полный анализ по каждому типу с примерами.
    """
    return full_prompt



# Функция для извлечения сертифицируемых объектов из use case.
# Она формирует запрос, который анализирует текст use case и ищет действия или процессы, подлежащие сертификации.
# Цель: вернуть список предложений, описывающих сертифицируемые объекты.
#
# Аргументы:
# - case_description (str): текст use case, который нужно проанализировать.
#
# Этапы выполнения:
# 1. Формирование запроса (prompt), который запрашивает выделение сертифицируемых объектов.
# 2. Отправка запроса в GPT и получение ответа.
# 3. Преобразование ответа в список объектов.
#
# Результат: Возвращает список сертифицируемых объектов, извлеченных из текста use case.

def extract_certifiable_objects(case_description: str) -> list:
    try:
        # Идеальный промт для извлечения сертифицируемых объектов
        full_prompt = f"""
        Проанализируй текст ниже и найди все предложения, описывающие действия или процессы, которые могут подлежать сертификации. 
        Верни эти предложения строго в виде списка, как в примере: ['First certifiable action.', 'Second certifiable action.'].
        
        Вот текст для анализа:
        {case_description}
        
        Ответом должен быть только список сертифицируемых объектов, без лишних слов, в формате: ['...'].
        """
        messages = [Message(role="user", content=full_prompt)]
        payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)
        
        # Отправляем запрос в GPT и получаем ответ
        response = sent_to_ai(payload.dict())
        # Отправляем запрос в GPT

        certifiable_objects = eval(response)
        return certifiable_objects

    except SyntaxError as e:
        print(f"Ошибка синтаксиса при попытке преобразовать ответ: {e}")
        return []
    except KeyError as e:
        print(f"Ключ не найден в ответе: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []







# Функция для анализа финального результата сертификации.
# Эта функция получает итоговый анализ кейса (final_final_result) и на его основе определяет:
# 1. Тип кейса (1, 2 или 3): соответствие регламентам, наличие ограничений или противоречий.
# 2. Количество соблюденных регламентов.
# 3. Количество несоблюденных регламентов.
# 
# Основной шаг — отправка запроса в GPT, который анализирует текст итогового результата
# и возвращает список: [тип кейса, количество соблюденных регламентов, количество несоблюденных регламентов].
# Если результат не является списком, или есть другая ошибка, возвращается значение по умолчанию [1, 1, 0].
#
# Аргументы:
# - final_final_result (str): текст итогового анализа, который нужно оценить.
#
# Этапы выполнения:
# 1. Формируется промт (full_prompt) с объяснением задачи для GPT.
#    GPT должен определить тип кейса, количество соблюденных и несоблюденных регламентов на основе анализа.
# 2. Запрос отправляется в GPT через функцию `sent_to_ai`.
# 3. Полученный результат проверяется: если это список из трех элементов (тип кейса, соблюденные и несоблюденные регламенты),
#    он возвращается. Если результат не является списком, выбрасывается исключение.
# 4. В случае ошибки (например, если формат ответа неверен), функция возвращает значение по умолчанию [1, 1, 0].
#

def analyze_final_result(final_final_result):
    full_prompt = f"""
    Ты эксперт по сертификации и проверке нормативных требований. 
    У тебя есть анализ итогового кейса по следующим типам:
    - **Тип 0**: Разрабатываемая система не относится к сертифицируемым. Проверка не требуется.
    - **Тип 1**: Упоминаются сертифицируемые объекты, регламенты соблюдены.
    - **Тип 2**: Упоминаются сертифицируемые объекты, на которые накладываются ограничения, но они не описаны в кейсе.
    - **Тип 3**: Упоминаются сертифицируемые объекты, но требования разработки противоречат регламентам.
    
    Вот текст анализа кейса:
    {final_final_result}
    
    Твоя задача:
    1. Определить тип кейса (0, 1, 2 или 3).
    2. Подсчитать количество регламентов, которые соблюдены.
    3. Подсчитать количество регламентов, которые не соблюдены.

    Ответ в формате: [тип кейса, количество соблюденных регламентов, количество несоблюденных регламентов].
    Ответ должен быть срого в формате списка. Пример: [1, 1, 0]
    """
    
    try:

        messages = [Message(role="user", content=full_prompt)]
        payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)
        
        # Отправляем запрос в GPT и получаем ответ
        result = sent_to_ai(payload.dict())
        
        # Проверяем, является ли результат списком
        if isinstance(result, list) and len(result) == 3:
            return result
        else:
            raise ValueError("Ожидался список из трех элементов.")
    
    except Exception as e:
        print(f"Ошибка: {e}")
        # Возвращаем [1, 1, 0] в случае ошибки
        return [1, 1, 0]





# Основная функция для обработки процесса сертификации.
# Эта функция включает в себя несколько шагов, которые последовательно проверяют, подлежит ли элемент сертификации,
# ищут соответствующие регламенты, анализируют их и предоставляют итоговый анализ соответствия кейса требованиям сертификации.
#
# Аргументы:
# - case_description (str): текстовое описание use case, которое нужно проанализировать.

def process_certification(case_description: str):
    # Шаг 1: Проверяем, подлежит ли элемент сертификации.
    # Вызываем функцию check_certification, которая анализирует, требуется ли сертификация для объектов в use case.
    # Ответ может быть "True", если объект подлежит сертификации, или "False", если нет.
    
    response = check_certification(case_description)
    
    print('response', response)
    
    if response == "True":
        print("Сертифицируется, теперь ищем подходящие пункты регламента...")

        # Шаг 2: Находим подходящие пункты регламентов.
        # Используем функцию determine_applicable_regulations для получения списка регламентов,
        # которые могут быть применимы к объекту в use case.
        
        applicable_regulations = determine_applicable_regulations(case_description)

        # Печатаем результат
        # print(applicable_regulations)

    
        cumulative_relevant_regulations = ""
        
        # Шаг 3: Проходим по каждому регламенту из списка применимых регламентов.
        # Для каждого найденного регламента:        
        for i in applicable_regulations:
            # Получаем путь к файлу для текущего регламента
            json_path = regulations_files[i]
            
            # Вызываем функцию для поиска релевантных пунктов регламента
            relevant_regulations = find_relevant_regulations(case_description, json_path)
            
            # Добавляем результат к суммарному тексту
            cumulative_relevant_regulations += relevant_regulations + "\n"  # Добавляем перенос строки для разделения
        
        # print(cumulative_relevant_regulations)
        
        # Шаг 4: Создаем детализированный промт для финального анализа.
        # Используем функцию create_detailed_prompt для формирования запроса, который отправится в GPT для
        # финальной проверки и анализа соответствия объектов кейса регламентам.
        
        detailed_prompt = create_detailed_prompt(case_description, cumulative_relevant_regulations)




        messages = [Message(role="user", content=detailed_prompt)]
        payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

        # Шаг 4: Отправляем запрос в GPT
        final_response = sent_to_ai(payload.dict())

        final_result = ""
        # Вывод финального результата
        final_result += final_response
        
        
        # Шаг 5: Извлечение сертифицируемых объектов из текста use case.
        # Используем функцию extract_certifiable_objects для нахождения всех объектов,
        # которые подлежат сертификации в данном use case.

        certifiable_objects = extract_certifiable_objects(case_description)
        
        # Шаг 6: Для каждого сертифицируемого объекта создаем детализированный промт и отправляем запрос в GPT.
        
        for j in certifiable_objects:
            detailed_prompt = create_detailed_prompt_certifiable_objects(case_description, relevant_regulations, j)
        
            messages = [Message(role="user", content=detailed_prompt)]
            payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

            # Шаг 4: Отправляем запрос в GPT
            final_response = sent_to_ai(payload.dict())
            
            # Вывод финального результата
            final_result += final_response

        
        # Шаг 7: Создаем финальный промт для окончательного анализа кейса.
        # Используем функцию create_final_prompt для создания финального запроса,
        # который будет отправлен в GPT для получения полного заключения по кейсу.

        final_prompt = create_final_prompt(case_description, final_result)

        messages = [Message(role="user", content=final_prompt)]
        payload = Payload(model=GPT_NAMES.GPT_4_OMNI, messages=messages)

        final_response = sent_to_ai(payload.dict())
        
        # Шаг 8: Анализируем финальный результат.
        # Используем функцию analyze_final_result для анализа ответа и получения информации
        # о типе кейса и количестве соблюденных/несоблюденных регламентов.
        
        itog = analyze_final_result(final_response)

        return final_response, itog
    elif response == "False":
        return '', [0, 0, 0]
    else:
        print("Некорректный ответ от API")





# Эти функции выполняют различные этапы проверки и анализа use case в контексте сертификации:
#
# 1. **check_use_case**: Выполняет анализ текста use case на соответствие стандартам и лучшим практикам.
#    Вызывает функцию analyze_use_case_from_message, передавая описание use case и требования для анализа.
#    Если возникает ошибка (например, неверные данные), она перехватывается и возвращается в виде сообщения об ошибке.
#
# 2. **check_regulation_objects**: Выполняет анализ объектов в use case на соответствие регламентам сертификации.
#    Эта функция определяет, какие объекты могут подлежать сертификации. В случае ошибки результатом будет сообщение об ошибке.
#
# 3. **check_regulations**: Проводит полный процесс сертификации, который включает проверку соответствия use case регламентам,
#    нахождение релевантных пунктов регламентов и детализированный анализ объектов сертификации. Если возникает ошибка в процессе,
#    она перехватывается и возвращается в ответе.
#
# Каждая из функций выполняет конкретный этап анализа или проверки, перехватывает ошибки и возвращает результат или сообщение об ошибке.


def check_use_case(case_description: str):           
    try:
        res = analyze_use_case_from_message(case_description, requirements)
    except Exception as e:
        res = {"response": f"error: {e}"}
    return res

def check_regulation_objects(case_description: str):           
    try:
        res = analyze_regulation_from_message(case_description, regulations)
    except Exception as e:
        res = {"response": f"error: {e}"}
    return res

def check_regulations(case_description: str):           
    try:
        res = process_certification(case_description)
    except Exception as e:
        res = {"response": f"error: {e}"}
    return res


